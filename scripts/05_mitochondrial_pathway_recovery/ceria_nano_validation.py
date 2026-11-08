import os
import scanpy as sc
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Load your master processed atlas object
adata = sc.read_h5ad("results/scanpy_objects/processed_organoids_atlas.h5ad")

# 2. Isolate the Astrocyte population (Cluster 6 in your native K-Means data)
print("Isolating Cluster 6 Astrocytes for oxidative stress evaluation...")
# FIX: Changed 'louvain' to 'kmeans_clusters'
astrocytes = adata[adata.obs['kmeans_clusters'] == '6'].copy()

# Enforce clean categories on 'batch' to avoid hidden category KeyErrors
astrocytes.obs['batch'] = astrocytes.obs['batch'].astype(str).astype('category')

# ==============================================================================
# 3. STATISTICAL PAIRWISE SCORING (The Visual Map Evidence)
# ==============================================================================
# Comparison A: Target Pathological State (APOE4 Vehicle vs APOE3 Vehicle)
print("Computing baseline APOE4 oxidative injury markers...")
sc.tl.rank_genes_groups(astrocytes, groupby='batch', reference='APOE3_Veh', method='wilcoxon', key_added='disease_effect')
# FIX: Using group=None to get all structural comparisons safely without indexing breaks
df_disease = sc.get.rank_genes_groups_df(astrocytes, group=None, key='disease_effect')

# Comparison B: Therapeutic Reversal State (APOE4 Vehicle vs APOE4 Ceria)
print("Computing Ceria nanoparticle recovery signatures...")
sc.tl.rank_genes_groups(astrocytes, groupby='batch', reference='APOE4_Veh', method='wilcoxon', key_added='treatment_effect')
df_treatment = sc.get.rank_genes_groups_df(astrocytes, group=None, key='treatment_effect')

# ==============================================================================
# 4. TARGET EXPRESSION PROFILING
# ==============================================================================
# Define core mitochondrial stress protection and ROS scavenging targets
stress_genes = ['SOD2', 'CAT', 'PINK1', 'PRDX1', 'GPX1', 'ATF4']

print("\n=== EVIDENCE MATRIX: MITOCHONDRIAL PATHWAY RECOVERY ===")
print(f"{'Gene':<8} | {'APOE4 Pathfold (vs E3)':<22} | {'Ceria Shift (vs E4_Veh)':<22}")
print("-" * 65)

for gene in stress_genes:
    # Extract disease effect parameters safely
    dis_row = df_disease[df_disease['names'] == gene]
    dis_lfc = dis_row['logfoldchanges'].values[0] if not dis_row.empty else 0.0
    dis_p = dis_row['pvals_adj'].values[0] if not dis_row.empty else 1.0
    
    # Extract treatment effect parameters safely
    tx_row = df_treatment[df_treatment['names'] == gene]
    tx_lfc = tx_row['logfoldchanges'].values[0] if not tx_row.empty else 0.0
    tx_p = tx_row['pvals_adj'].values[0] if not tx_row.empty else 1.0
    
    print(f"{gene:<8} | LFC: {dis_lfc:>6.3f} (p: {dis_p:.3e}) | LFC: {tx_lfc:>6.3f} (p: {tx_p:.3e})")

# ==============================================================================
# 5. EXPORT VISUAL PROOF (Expression Distribution Matrix)
# ==============================================================================
# Generate a violin plot tracking the structural restoration of mitochondrial genes
os.makedirs("results", exist_ok=True)
sc.pl.violin(
    astrocytes, 
    keys=['SOD2', 'PINK1'], 
    groupby='batch', 
    rotation=0,
    show=False,
    save="_mitochondrial_recovery_proof.png"
)
print("\nValidation chart exported to your results/scanpy_plots/ directory!")
