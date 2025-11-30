import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Rectangle, Polygon, FancyArrowPatch

try:
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 18))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 28)
    ax.axis('off')

    # Colors
    c_input = '#E3F2FD'
    c_process = '#BBDEFB'
    c_decision = '#FFE082'
    c_output = '#C8E6C9'
    c_data = '#F8BBD0'

    def box(x, y, w, h, text, typ='process', fs=8):
        if typ == 'process':
            r = Rectangle((x, y), w, h, fc=c_process, ec='black', lw=1.5)
            ax.add_patch(r)
        elif typ == 'input':
            r = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05", fc=c_input, ec='black', lw=1.5)
            ax.add_patch(r)
        elif typ == 'output':
            r = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1", fc=c_output, ec='black', lw=2)
            ax.add_patch(r)
        elif typ == 'data':
            pts = [[x+0.2, y+h], [x+w, y+h], [x+w-0.2, y], [x, y]]
            p = Polygon(pts, fc=c_data, ec='black', lw=1.5)
            ax.add_patch(p)
        elif typ == 'decision':
            pts = [[x+w/2, y+h], [x+w, y+h/2], [x+w/2, y], [x, y+h/2]]
            p = Polygon(pts, fc=c_decision, ec='black', lw=1.5)
            ax.add_patch(p)
        
        ax.text(x+w/2, y+h/2, text, ha='center', va='center', fontsize=fs, weight='bold')

    def arrow(x1, y1, x2, y2):
        a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle='->', mutation_scale=15, lw=1.5, color='black')
        ax.add_patch(a)

    # START
    y = 27
    box(4, y, 2, 0.5, 'START', 'output', 9)
    arrow(5, y, 5, y-0.7)

    # TAHAP 1
    y -= 1.2
    ax.text(5, y, 'TAHAP 1: DATA PREPARATION', ha='center', fontsize=10, weight='bold',
            bbox=dict(boxstyle='round', fc='#1976D2', ec='black', alpha=0.2))

    y -= 0.8
    box(0.5, y, 1.5, 0.5, 'PIHPS\nHarga', 'data', 7)
    box(2.2, y, 1.5, 0.5, 'OpenMeteo\nIklim', 'data', 7)
    box(4, y, 1.5, 0.5, 'Trading\nBBM', 'data', 7)
    box(5.8, y, 1.5, 0.5, 'BPS\nPanen', 'data', 7)
    box(7.6, y, 1.5, 0.5, 'OSM\nFasilitas', 'data', 7)

    arrow(1.25, y, 3.5, y-0.6)
    arrow(2.95, y, 4, y-0.6)
    arrow(4.75, y, 4.5, y-0.6)
    arrow(6.55, y, 5.5, y-0.6)
    arrow(8.35, y, 6, y-0.6)

    y -= 1.2
    box(3, y, 4, 0.6, 'Integrasi Dataset', 'process')
    arrow(5, y, 5, y-0.6)

    y -= 1.2
    box(3, y, 4, 0.6, 'Agregasi Temporal\nHarian → Bulanan', 'process')
    arrow(5, y, 5, y-0.6)

    y -= 1.2
    box(3, y, 4, 0.6, 'Konstruksi Lag Variables', 'process')
    arrow(5, y, 5, y-0.6)

    y -= 1.2
    box(3, y, 4, 0.6, 'Balanced Panel\n12×58 = 696 obs', 'data')
    arrow(5, y, 5, y-0.6)

    # TAHAP 2
    y -= 1.5
    ax.text(5, y, 'TAHAP 2: ESDA', ha='center', fontsize=10, weight='bold',
            bbox=dict(boxstyle='round', fc='#1976D2', ec='black', alpha=0.2))

    y -= 0.8
    box(3, y, 4, 0.6, 'Konstruksi Spatial Weights', 'process')
    arrow(5, y, 5, y-0.6)

    y -= 1.2
    box(1, y, 2.3, 0.5, 'W_geo\nKNN', 'process', 7)
    box(3.8, y, 2.3, 0.5, 'W_econ\nGravity', 'process', 7)
    box(6.6, y, 2.3, 0.5, 'W_combined\nHybrid', 'process', 7)

    arrow(2.15, y, 4, y-0.6)
    arrow(5, y, 5, y-0.6)
    arrow(7.75, y, 6, y-0.6)

    y -= 1.2
    box(3, y, 4, 0.6, 'Row-Standardization', 'process')
    arrow(5, y, 5, y-0.6)

    y -= 1.2
    box(3, y, 4, 0.6, 'Global Moran\'s I', 'process')
    arrow(5, y, 5, y-0.6)

    y -= 1.2
    box(3, y, 4, 0.6, 'Local Moran\'s I (LISA)', 'process')
    arrow(5, y, 5, y-0.6)

    # TAHAP 3
    y -= 1.5
    ax.text(5, y, 'TAHAP 3: DIAGNOSTICS', ha='center', fontsize=10, weight='bold',
            bbox=dict(boxstyle='round', fc='#1976D2', ec='black', alpha=0.2))

    y -= 0.8
    box(1.5, y, 2, 0.5, 'ADF Test', 'process', 7)
    box(4, y, 2, 0.5, 'VIF', 'process', 7)
    box(6.5, y, 2, 0.5, 'Breusch-Pagan', 'process', 7)

    arrow(2.5, y, 4, y-0.6)
    arrow(5, y, 5, y-0.6)
    arrow(7.5, y, 6, y-0.6)

    y -= 1.2
    box(3, y, 4, 0.6, 'LM-Lag & LM-Error', 'process')
    arrow(5, y, 5, y-0.6)

    y -= 1.2
    box(3.5, y, 3, 0.7, 'Model Selection\nSDM?', 'decision')
    arrow(5, y, 5, y-0.8)

    y -= 1.4
    box(3, y, 4, 0.6, 'Hausman Test\nFE vs RE', 'process')
    arrow(5, y, 5, y-0.6)

    # TAHAP 4
    y -= 1.5
    ax.text(5, y, 'TAHAP 4: ESTIMATION', ha='center', fontsize=10, weight='bold',
            bbox=dict(boxstyle='round', fc='#1976D2', ec='black', alpha=0.2))

    y -= 0.8
    box(3, y, 4, 0.6, 'Estimasi SDM-FE\nML/GMM', 'process')
    arrow(5, y, 5, y-0.6)

    y -= 1.2
    box(3, y, 4, 0.6, 'Dekomposisi Efek\n(I-ρW)⁻¹(βI+Wθ)', 'process')
    arrow(5, y, 5, y-0.6)

    y -= 1.2
    box(1, y, 2.3, 0.5, 'Direct\nEffects', 'output', 7)
    box(3.8, y, 2.3, 0.5, 'Indirect\nEffects', 'output', 7)
    box(6.6, y, 2.3, 0.5, 'Total\nEffects', 'output', 7)

    arrow(2.15, y, 4, y-0.6)
    arrow(5, y, 5, y-0.6)
    arrow(7.75, y, 6, y-0.6)

    y -= 1.2
    box(3, y, 4, 0.6, 'Validasi Residual', 'process')
    arrow(5, y, 5, y-0.6)

    # TAHAP 5
    y -= 1.5
    ax.text(5, y, 'TAHAP 5: SIMULATION', ha='center', fontsize=10, weight='bold',
            bbox=dict(boxstyle='round', fc='#1976D2', ec='black', alpha=0.2))

    y -= 0.8
    box(1, y, 2.3, 0.5, 'BBM\n+15%', 'input', 7)
    box(3.8, y, 2.3, 0.5, 'Drought\n-200mm', 'input', 7)
    box(6.6, y, 2.3, 0.5, 'Heat\n+2°C', 'input', 7)

    arrow(2.15, y, 4, y-0.6)
    arrow(5, y, 5, y-0.6)
    arrow(7.75, y, 6, y-0.6)

    y -= 1.2
    box(3, y, 4, 0.6, 'Counterfactual Analysis\nΔP=(I-ρW)⁻¹×(β+Wθ)×ΔX', 'process', 7)
    arrow(5, y, 5, y-0.6)

    y -= 1.2
    box(3, y, 4, 0.6, 'Spatial Impact Map', 'output')
    arrow(5, y, 5, y-0.6)

    y -= 1.2
    box(3, y, 4, 0.6, 'Forecast Validation\nRolling Window', 'process')
    arrow(5, y, 5, y-0.6)

    y -= 1.2
    box(3, y, 4, 0.6, 'MAPE, RMSE, Accuracy', 'output')
    arrow(5, y, 5, y-0.6)

    # END
    y -= 1.2
    box(4, y, 2, 0.5, 'END', 'output', 9)

    # Legend
    leg = [
        mpatches.Patch(fc=c_input, ec='black', label='Input/Start/End'),
        mpatches.Patch(fc=c_process, ec='black', label='Process'),
        mpatches.Patch(fc=c_decision, ec='black', label='Decision'),
        mpatches.Patch(fc=c_output, ec='black', label='Output'),
        mpatches.Patch(fc=c_data, ec='black', label='Data')
    ]
    ax.legend(handles=leg, loc='lower center', ncol=5, fontsize=7, bbox_to_anchor=(0.5, -0.01))

    # Title
    fig.suptitle('Gambar 3.1: Flowchart Metodologi Penelitian\nSpatial Durbin Model - Analisis Harga Beras', 
                 fontsize=12, weight='bold')

    plt.tight_layout()
    output_path = 'd:/Arsip Kompetisi/YELP BI 2025/Gambar_3_1_Flowchart_Metodologi.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print("✅ Flowchart berhasil dibuat!")
    print(f"📁 Lokasi: {output_path}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
