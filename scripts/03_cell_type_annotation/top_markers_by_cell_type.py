import os
import scanpy as sc
import pandas as pd

# 1. Load the processed master atlas object
print("Loading master organoid atlas...")
adata = sc.read_h5ad("results/scanpy_objects/processed_organoids_atlas.h5ad")

# 2. Re-verify the 23 Leiden communities and calculate marker genes
print("Calculating cluster marker genes...")
sc.pp.neighbors(adata)
sc.tl.leiden(adata)
sc.tl.rank_genes_groups(adata, groupby='leiden', method='wilcoxon')

# 3. Extract the top 10 marker genes into a raw dataframe
result = adata.uns['rank_genes_groups']
groups = result['names'].dtype.names
top_markers_raw = pd.DataFrame({
    group: result['names'][group][:10] for group in groups
})

# 4. Define the Biological Mapping Dictionary
cell_type_dictionary = {
    "0": "Immature Neurons", "1": "Immature Neurons", "2": "Immature Neurons", "3": "Immature Neurons",
    "4": "Neural Progenitors", "5": "Neural Progenitors", 
    "6": "Mesenchymal Stroma", "7": "Mesenchymal Stroma", "8": "Mesenchymal Stroma", "9": "Mesenchymal Stroma",
    "10": "Immature Neurons", "11": "Immature Neurons", "12": "Immature Neurons",
    "13": "Astrocytes",
    "14": "Immature Neurons",
    "15": "Mature Cortical Neurons",
    "16": "Cycling Progenitors",
    "17": "Inhibitory Interneurons", "18": "Inhibitory Interneurons",
    "19": "Mesenchymal Stroma",
    "20": "Neural Progenitors",
    "21": "Mesenchymal Stroma", "22": "Mesenchymal Stroma"
}

# 5. Method A: Simply Rename the 23 Columns for Full Granularity
# This keeps all 23 columns but alters headers to "Astrocytes (13)", "Neural Progenitors (5)", etc.
verbose_columns = {num: f"{name} ({num})" for num, name in cell_type_dictionary.items()}
top_markers_labeled = top_markers_raw.rename(columns=verbose_columns)

# Sort columns alphabetically by cell type name so duplicates sit next to each other
top_markers_labeled = top_markers_labeled.reindex(sorted(top_markers_labeled.columns), axis=1)
top_markers_labeled.to_csv("results/cluster_top_markers_by_cell_type_detailed.csv", index=False)

# 6. Method B: Compute Clean, Unified Cell-Type Marker Profiles (Recommended)
# This merges duplicates into a highly polished table with exactly 7 distinct columns
print("Recalculating unified markers directly on cell types...")
adata.obs['cell_types'] = adata.obs['leiden'].astype(str).map(cell_type_dictionary)
adata.obs['cell_types'] = adata.obs['cell_types'].astype('category')

sc.tl.rank_genes_groups(adata, groupby='cell_types', method='wilcoxon')
result_unified = adata.uns['rank_genes_groups']
groups_unified = result_unified['names'].dtype.names

top_markers_unified = pd.DataFrame({
    group: result_unified['names'][group][:10] for group in groups_unified
})

# Save the polished, unified table
os.makedirs("results", exist_ok=True)
top_markers_unified.to_csv("results/final_cell_type_markers_profile.csv", index=False)

print("\n--- Top 5 Signature Markers Per Cleaned Cell Type ---")
print(top_markers_unified.head(5))
print("\n🏆 Tables exported successfully to the results directory!")
