import os
import scanpy as sc
import pandas as pd
import matplotlib.pyplot as plt

# 1. Loading our master processed atlas object
print("Loading master organoid atlas...")
adata = sc.read_h5ad("results/scanpy_objects/processed_organoids_atlas.h5ad")

# 2. Explicit Biological Mapping Dictionary
cell_type_dictionary = {
    "0": "Immature Neurons",
    "1": "Neural Progenitors",
    "2": "Mesenchymal Stroma",
    "3": "Mature Cortical Neurons",
    "4": "Cycling Progenitors",
    "5": "Inhibitory Interneurons",
    "6": "Astrocytes",
    "7": "Supportive Matrix Stroma"
}

# 4. Inject structural cell names into the metadata slot
print("Swapping cluster numbers with verified biological cell types...")
adata.obs['cell_types'] = adata.obs['kmeans_clusters'].astype(str).map(cell_type_dictionary)
adata.obs['cell_types'] = adata.obs['cell_types'].astype('category')


# 5. Setting the color palettes directly in the uns slot prevents Scanpy from parsing strings on subplots
adata.uns['batch_colors'] = sc.pl.palettes.default_20[:len(adata.obs['batch'].cat.categories)]
adata.uns['cell_types_colors'] = sc.pl.palettes.default_20[:len(adata.obs['cell_types'].cat.categories)]

# 6. Build the Clean Side-by-Side Canvas
print("Generating publication-ready high-contrast dual UMAP...")

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Panel A (Left): Experimental Cohorts
sc.pl.umap(
    adata, 
    color='batch', 
    ax=axes[0], 
    show=False, 
    title="Atlas by Experimental Group",
    frameon=True
)

# Panel B (Right): Biological Cell Types
sc.pl.umap(
    adata, 
    color='cell_types', 
    ax=axes[1], 
    show=False, 
    title="Atlas by Identified Cell Types",
    frameon=True
)

plt.tight_layout()

# Save at high-fidelity 300 DPI resolution
output_file = "results/plots/final_cell_type_clean_atlas.png"
plt.savefig(output_file, dpi=300, bbox_inches='tight')
plt.close()

# 7. Save object back to disk to permanently store the annotation layers
adata.write("results/scanpy_objects/processed_organoids_atlas.h5ad")
print(f"🏆 Milestone Complete! Crisp cell-type atlas saved to: {output_file}")
