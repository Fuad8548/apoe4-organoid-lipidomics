import os
import scanpy as sc
import pandas as pd

# 1. Load the processed master atlas object
adata = sc.read_h5ad("results/scanpy_objects/processed_organoids_atlas.h5ad")

# 2. Extract and Isolate the Astrocyte population (Cluster 6 in your K-Means Plot)
print("Isolating Astrocyte cluster cells using native K-Means metadata...")
astrocytes = adata[adata.obs['kmeans_clusters'] == '6'].copy()

# 3. Track Genotype comparisons inside the subset
astrocytes.obs['compare_group'] = astrocytes.obs['batch'].astype(str)

# Filter out the Ceria treated group for this baseline pathology check
astrocytes = astrocytes[astrocytes.obs['compare_group'].isin(['APOE3_Veh', 'APOE4_Veh'])].copy()
astrocytes.obs['compare_group'] = astrocytes.obs['compare_group'].astype('category')

# 4. Execute Differential Gene Expression (DGE)
print("Calculating genotype-specific transcriptomic shifts in lipids...")
sc.tl.rank_genes_groups(
    astrocytes, 
    groupby='compare_group', 
    reference='APOE3_Veh', 
    method='wilcoxon',
    key_added='apoe4_vs_apoe3_dge'
)

# 5. Extract results cleanly into a structured dataframe
print("Extracting DGE matrices securely...")
dge_results = sc.get.rank_genes_groups_df(astrocytes, group=None, key='apoe4_vs_apoe3_dge')

# 6. Save the complete differential expression profile
os.makedirs("results", exist_ok=True)
dge_results.to_csv("results/astrocyte_apoe4_lipid_dge.csv", index=False)
print("DGE complete! Results saved to results/astrocyte_apoe4_lipid_dge.csv")

# ==============================================================================
# 7. METABOLIC LENS: Filter for key lipid/cholesterol genes to check status
# ==============================================================================
lipid_genes = ['APOE', 'ABCA1', 'ABCG1', 'LDLR', 'SREBF2', 'HMGCR', 'CLU', 'APOD']

print("\n--- Status of Core Lipid/Cholesterol Pathological Genes ---")
target_dge = dge_results[dge_results['names'].isin(lipid_genes)]

# Clear print target (no 'group' index slicing column)
if not target_dge.empty:
    print(target_dge[['names', 'logfoldchanges', 'pvals_adj']])
else:
    print("Warning: Target lipid genes were not caught in the filtering threshold. Top 5 DGE genes:")
    print(dge_results.head(5))
