import pandas as pd
import numpy as np
import networkx as nx
import matplotlib
matplotlib.use('Agg') # Non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.spatial import cKDTree
import geopandas as gpd
from shapely.geometry import Point, LineString
import os
import glob
import warnings

# Suppress warnings
warnings.filterwarnings('ignore')

# Configuration
OUTPUT_DIR = 'paper_analysis_output/network_analysis'
os.makedirs(OUTPUT_DIR, exist_ok=True)
plt.style.use('seaborn-v0_8-whitegrid')

print("="*80)
print("STARTING GRAPH-BASED SUPPLY CHAIN ANALYSIS")
print("="*80)

# 1. LOAD DATA
print("\n[1/5] Loading Supply Chain Data...")
list_of_files = glob.glob('supply_chain_spatial_fast/supply_chain_facilities_*.csv')
latest_file = max(list_of_files, key=os.path.getctime)
df = pd.read_csv(latest_file)

# Filter columns and drop invalid coords
df = df[['name', 'latitude', 'longitude', 'facility_type', 'search_location']].dropna(subset=['latitude', 'longitude'])
print(f"   Loaded {len(df)} facilities.")

# 2. BUILD NETWORK (DIGITAL TWIN)
print("\n[2/5] Building Supply Chain Network (Digital Twin)...")

G = nx.DiGraph() # Directed Graph

# Add Nodes
for idx, row in df.iterrows():
    G.add_node(idx, pos=(row['longitude'], row['latitude']), 
               type=row['facility_type'], 
               location=row['search_location'],
               name=row['name'])

# Separate by type for connection logic
producers = df[df['facility_type'] == 'production']
distributors = df[df['facility_type'] == 'distribution']
retailers = df[df['facility_type'] == 'retail']

# Helper to add edges based on distance
def add_spatial_edges(source_df, target_df, graph, radius_km=20, max_neighbors=3):
    if source_df.empty or target_df.empty:
        return 0
    
    source_coords = source_df[['latitude', 'longitude']].values
    target_coords = target_df[['latitude', 'longitude']].values
    
    # Use KDTree for fast nearest neighbor search
    # Note: KDTree uses Euclidean distance, so we approximate degrees to km
    # 1 degree lat approx 111 km. So radius_deg = radius_km / 111
    radius_deg = radius_km / 111.0
    
    tree = cKDTree(target_coords)
    distances, indices = tree.query(source_coords, k=max_neighbors, distance_upper_bound=radius_deg)
    
    edge_count = 0
    for i, (dists, idxs) in enumerate(zip(distances, indices)):
        source_node = source_df.index[i]
        
        # Handle single neighbor case (k=1 returns scalar) or multiple
        if max_neighbors == 1:
            dists = [dists]
            idxs = [idxs]
            
        for d, target_idx_tree in zip(dists, idxs):
            if d == float('inf'): continue # No neighbor found within radius
            
            target_node = target_df.index[target_idx_tree]
            
            # Add edge: Source -> Target
            # Weight = Distance (inverse weight for centrality usually, but here we just store it)
            graph.add_edge(source_node, target_node, weight=d*111) # dist in km
            edge_count += 1
            
    return edge_count

# Rule 1: Production -> Distribution (Radius 30km, max 5 distributors)
# Produsen mengirim barang ke pengepul/pasar induk terdekat
n_edges_p2d = add_spatial_edges(producers, distributors, G, radius_km=30, max_neighbors=5)

# Rule 2: Distribution -> Retail (Radius 15km, max 10 retailers)
# Distributor menyuplai ritel di sekitarnya
n_edges_d2r = add_spatial_edges(distributors, retailers, G, radius_km=15, max_neighbors=10)

# Rule 3: Distribution -> Distribution (Inter-hub connection, Radius 50km)
# Pasar induk saling bertukar barang
n_edges_d2d = add_spatial_edges(distributors, distributors, G, radius_km=50, max_neighbors=3)

print(f"   Network Stats:")
print(f"   - Nodes: {G.number_of_nodes()}")
print(f"   - Edges: {G.number_of_edges()} (P->D: {n_edges_p2d}, D->R: {n_edges_d2r}, D->D: {n_edges_d2d})")

# 3. CALCULATE RESILIENCE METRICS
print("\n[3/5] Calculating Resilience Metrics...")

# Degree Centrality (Hubness) - Who has the most connections?
degree_dict = dict(G.degree())
in_degree_dict = dict(G.in_degree())
out_degree_dict = dict(G.out_degree())

# Betweenness Centrality (Bottleneck) - Who is on the most shortest paths?
# We use a subset/k for speed because calculating exact betweenness for 17k nodes is slow
print("   - Calculating Betweenness (Approximation)...")
betweenness_dict = nx.betweenness_centrality(G, k=500, normalized=True, seed=42)

# Assign metrics to dataframe
df['degree'] = df.index.map(degree_dict)
df['in_degree'] = df.index.map(in_degree_dict)
df['out_degree'] = df.index.map(out_degree_dict)
df['betweenness'] = df.index.map(betweenness_dict)

# Identify Critical Hubs (High Betweenness + High Degree)
# Score = Normalized Degree + Normalized Betweenness
df['criticality_score'] = (df['degree'] / df['degree'].max()) + (df['betweenness'] / df['betweenness'].max())
critical_hubs = df.sort_values('criticality_score', ascending=False).head(20)

print("   Top 5 Critical Hubs (Potential Single Points of Failure):")
print(critical_hubs[['name', 'facility_type', 'search_location', 'criticality_score']].head(5))
critical_hubs.to_csv(f"{OUTPUT_DIR}/top_critical_hubs.csv")

# 4. VISUALIZATION
print("\n[4/5] Generating Network Visualizations...")

# Load Background Map
try:
    provinces = gpd.read_file('GeoJSON/Indonesia_provinces.geojson')
    background = provinces[provinces['NAME_1'].isin(['Jawa Barat', 'DKI Jakarta', 'Banten'])]
except:
    background = None
    print("   Warning: Could not load background map")

# MAP 1: Network Topology & Critical Hubs
fig, ax = plt.subplots(figsize=(14, 10))
if background is not None:
    background.plot(ax=ax, color='#f8f9fa', edgecolor='#dee2e6')

# Draw Edges (Sampled for visual clarity if too many)
# We draw only edges connected to critical hubs to avoid "hairball" mess
critical_nodes = set(critical_hubs.index)
edges_to_draw = []
for u, v in G.edges():
    if u in critical_nodes or v in critical_nodes:
        edges_to_draw.append((u, v))

# If too few edges, draw more random ones
if len(edges_to_draw) < 1000:
    import random
    all_edges = list(G.edges())
    edges_to_draw.extend(random.sample(all_edges, min(len(all_edges), 2000)))

# Create LineStrings for edges
lines = []
for u, v in edges_to_draw:
    p1 = G.nodes[u]['pos']
    p2 = G.nodes[v]['pos']
    lines.append(LineString([p1, p2]))

edge_gdf = gpd.GeoDataFrame(geometry=lines)
edge_gdf.plot(ax=ax, color='gray', alpha=0.1, linewidth=0.5)

# Draw Nodes
# Retailers (Small, Green)
retail_gdf = gpd.GeoDataFrame(
    retailers, geometry=gpd.points_from_xy(retailers.longitude, retailers.latitude))
retail_gdf.plot(ax=ax, color='#2ecc71', markersize=5, alpha=0.3, label='Retail')

# Producers (Medium, Blue)
prod_gdf = gpd.GeoDataFrame(
    producers, geometry=gpd.points_from_xy(producers.longitude, producers.latitude))
prod_gdf.plot(ax=ax, color='#3498db', markersize=20, alpha=0.6, label='Producer')

# Distributors (Large, Orange)
dist_gdf = gpd.GeoDataFrame(
    distributors, geometry=gpd.points_from_xy(distributors.longitude, distributors.latitude))
dist_gdf.plot(ax=ax, color='#f39c12', markersize=50, alpha=0.7, label='Distributor')

# Critical Hubs (Huge, Red, Star)
crit_gdf = gpd.GeoDataFrame(
    critical_hubs, geometry=gpd.points_from_xy(critical_hubs.longitude, critical_hubs.latitude))
crit_gdf.plot(ax=ax, color='#e74c3c', markersize=300, marker='*', edgecolor='black', label='CRITICAL HUB')

# Label Critical Hubs
for x, y, label in zip(crit_gdf.geometry.x, crit_gdf.geometry.y, crit_gdf.name):
    ax.text(x, y+0.02, str(label)[:15], fontsize=8, ha='center', fontweight='bold')

plt.title('Map 1: Supply Chain Network Topology & Critical Hubs\n(Red Stars = Systemic Vulnerabilities)', fontsize=16)
plt.legend(loc='lower right')
plt.axis('off')
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/Map1_Network_Topology.png", dpi=300)
print("   Saved Map1_Network_Topology.png")

# MAP 2: Regional Resilience Index
# Calculate avg degree per region (City/Regency)
resilience_index = df.groupby('search_location')['degree'].mean().reset_index()
resilience_index.columns = ['Region', 'Connectivity_Index']
resilience_index = resilience_index.sort_values('Connectivity_Index', ascending=False)

# Plot Bar Chart for Resilience
plt.figure(figsize=(12, 6))
sns.barplot(data=resilience_index, x='Region', y='Connectivity_Index', palette='viridis')
plt.title('Figure 2: Regional Supply Chain Resilience Index\n(Higher Connectivity = More Alternative Routes = More Resilient)', fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.ylabel('Avg Network Degree (Connectivity)')
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/Fig2_Resilience_Index.png", dpi=300)
print("   Saved Fig2_Resilience_Index.png")

# 5. ATTACK SIMULATION (SCENARIO)
print("\n[5/5] Running Attack Simulation...")

# Scenario: Remove Top 5 Critical Hubs (e.g., Flood/Policy Ban)
# Measure impact on Network Connectivity (Giant Component Size)
original_size = len(max(nx.weakly_connected_components(G), key=len))
G_attacked = G.copy()
nodes_to_remove = critical_hubs.index[:5]
G_attacked.remove_nodes_from(nodes_to_remove)
attacked_size = len(max(nx.weakly_connected_components(G_attacked), key=len))

impact_pct = (original_size - attacked_size) / original_size * 100

print(f"   Attack Scenario: Removing Top 5 Hubs")
print(f"   - Original Connected Network Size: {original_size}")
print(f"   - Post-Attack Connected Network Size: {attacked_size}")
print(f"   - SYSTEMIC IMPACT: {impact_pct:.2f}% of the network disconnected!")

# Save Simulation Result
with open(f"{OUTPUT_DIR}/simulation_results.txt", "w") as f:
    f.write(f"ATTACK SIMULATION REPORT\n")
    f.write(f"========================\n")
    f.write(f"Scenario: Disruption of Top 5 Critical Hubs\n")
    f.write(f"Impact: {impact_pct:.2f}% of the supply chain network disconnected.\n")
    f.write(f"Interpretation: High dependency on these 5 hubs indicates low redundancy.\n")
    f.write(f"\nTargeted Hubs:\n")
    for i, row in critical_hubs.head(5).iterrows():
        f.write(f"- {row['name']} ({row['search_location']})\n")

print("\n" + "="*80)
print("NETWORK ANALYSIS COMPLETED")
print("="*80)
