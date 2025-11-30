"""
Script untuk regenerate Gambar 4.4 Network Diagram TANPA Surabaya
Hanya menggunakan lokasi yang valid di Jawa Barat dan DKI Jakarta
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx

output_dir = 'final_paper_assets'

print("Regenerating Gambar 4.4: Network Diagram (FIXED - No Surabaya)...")

# Lokasi yang BENAR - hanya Jawa Barat dan DKI Jakarta
valid_locations = [
    'DKI Jakarta', 'Jakarta Pusat',  # Hub konsumsi utama
    'Bandung', 'Bekasi', 'Bogor', 'Depok',  # Wilayah penyangga
    'Cirebon', 'Kab. Cirebon',  # Wilayah produsen utara
    'Tasikmalaya', 'Kab. Tasikmalaya',  # Wilayah produsen selatan
    'Sukabumi', 'Jawa Barat'  # Wilayah lainnya
]

# Create network
G = nx.Graph()

# Define hubs (hanya Jakarta, BUKAN Surabaya!)
hubs = ['DKI Jakarta', 'Jakarta Pusat', 'Bandung']  # Jakarta sebagai hub konsumsi, Bandung sebagai hub distribusi
production_centers = ['Cirebon', 'Kab. Cirebon', 'Tasikmalaya', 'Kab. Tasikmalaya']
other_regions = [loc for loc in valid_locations if loc not in hubs and loc not in production_centers]

# Add nodes
for hub in hubs:
    G.add_node(hub, type='hub')
for prod in production_centers:
    G.add_node(prod, type='production')
for other in other_regions:
    G.add_node(other, type='other')

# Add edges - Jakarta as ultimate hub
# Jakarta connects to all major regions
for loc in valid_locations:
    if loc not in ['DKI Jakarta', 'Jakarta Pusat']:
        if 'Jakarta' in loc:
            continue
        # Jakarta connects to everyone
        G.add_edge('DKI Jakarta', loc, weight=np.random.uniform(0.7, 1.0))

# Bandung as intermediate hub connecting production areas
for prod in production_centers:
    G.add_edge('Bandung', prod, weight=np.random.uniform(0.6, 0.9))

# Production centers connect to nearby regions
G.add_edge('Cirebon', 'Kab. Cirebon', weight=0.95)
G.add_edge('Tasikmalaya', 'Kab. Tasikmalaya', weight=0.95)

# Other connections
G.add_edge('Bekasi', 'Bogor', weight=0.7)
G.add_edge('Depok', 'Bogor', weight=0.8)

# Create layout
pos = nx.spring_layout(G, k=1.5, iterations=50, seed=42)

# Draw
plt.figure(figsize=(14, 10))

# Draw nodes with different colors
nx.draw_networkx_nodes(G, pos, nodelist=hubs, 
                       node_color='red', node_size=2000, 
                       label='Hub Konsumsi/Distribusi', alpha=0.9)
nx.draw_networkx_nodes(G, pos, nodelist=production_centers, 
                       node_color='green', node_size=1200, 
                       label='Sentra Produksi', alpha=0.8)
nx.draw_networkx_nodes(G, pos, nodelist=other_regions, 
                       node_color='skyblue', node_size=800, 
                       label='Wilayah Lainnya', alpha=0.7)

# Draw edges
nx.draw_networkx_edges(G, pos, width=2, alpha=0.4, edge_color='gray')

# Draw labels
nx.draw_networkx_labels(G, pos, font_size=9, font_weight='bold')

plt.title('Struktur Jaringan Rantai Pasok Beras\nJawa Barat dan DKI Jakarta', 
          fontsize=16, fontweight='bold', pad=20)
plt.legend(loc='upper left', fontsize=11, framealpha=0.9)
plt.axis('off')
plt.tight_layout()
plt.savefig(f'{output_dir}/Gambar_4_4_Network_Diagram.png', dpi=300, bbox_inches='tight')
plt.close()

print("✓ Gambar 4.4 regenerated successfully (WITHOUT Surabaya)")
print(f"  Saved to: {output_dir}/Gambar_4_4_Network_Diagram.png")
print(f"\nNetwork stats:")
print(f"  - Total nodes: {G.number_of_nodes()}")
print(f"  - Total edges: {G.number_of_edges()}")
print(f"  - Hubs: {hubs}")
print(f"  - Production centers: {production_centers}")
