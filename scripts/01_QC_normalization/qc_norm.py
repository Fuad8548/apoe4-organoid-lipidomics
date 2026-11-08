import os
import anndata as ad
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scanpy as sc

# Set Scanpy configurations
sc.settings.verbosity = 3
sc.settings.set_figure_params(dpi=80, facecolor="white")

os.makedirs("results/scanpy_objects", exist_ok=True)
os.makedirs("results/qc_plots", exist_ok=True)

# ==============================================================================
# 1. LOAD ALL THREE H5 MATRICES
# ==============================================================================
print("Loading H5 matrices into Scanpy AnnData objects...")

# Group 1: APOE3 Control
adata_e3 = sc.read_10x_h5(
    "GSM9779490_E3_vehicle_filtered_feature_bc_matrix.h5"
)
adata_e3.obs["genotype"] = "APOE3"
adata_e3.obs["treatment"] = "Vehicle"
adata_e3.var_names_make_unique()

# Group 2: APOE4 Target Disease
adata_e4 = sc.read_10x_h5(
    "GSM9779491_E4_vehicle_filtered_feature_bc_matrix.h5"
)
adata_e4.obs["genotype"] = "APOE4"
adata_e4.obs["treatment"] = "Vehicle"
adata_e4.var_names_make_unique()

# Group 3: APOE4 Ceria Nanoparticle Treatment (Crucial Reversal Group)
adata_e4_tx = sc.read_10x_h5(
    "GSM9779492_E4_ceria_filtered_feature_bc_matrix.h5"
)
adata_e4_tx.obs["genotype"] = "APOE4"
adata_e4_tx.obs["treatment"] = "Ceria_Nanoparticle"
adata_e4_tx.var_names_make_unique()

# ==============================================================================
# 2. CONCATENATE ALL THREE COHORTS (Memory-Safe Structural Union)
# ==============================================================================
print("Merging all three cohorts into a unified AnnData matrix...")
adata = ad.concat(
    {
        "APOE3_Veh": adata_e3,
        "APOE4_Veh": adata_e4,
        "APOE4_Ceria": adata_e4_tx,
    },
    label="batch",
    index_unique="-",
)

# IMMEDIATELY delete temporary single objects to flush your RAM
del adata_e3, adata_e4, adata_e4_tx

# ==============================================================================
# 3. METABOLIC QUALITY CONTROL CALCULATION
# ==============================================================================
print("Calculating mitochondrial viability baselines...")
adata.var["mt"] = adata.var_names.str.startswith("MT-")

sc.pp.calculate_qc_metrics(
    adata, qc_vars=["mt"], percent_top=None, log1p=False, inplace=True
)

# ==============================================================================
# 4. MEMORY-SAFE IN-PLACE TRANSCIPTOMIC FILTERING
# ==============================================================================
print(f"Cell count BEFORE filtering: {adata.n_obs}")

sc.pp.filter_cells(adata, min_genes=500)
sc.pp.filter_cells(adata, max_genes=6000)
adata = adata[adata.obs["pct_counts_mt"] < 15.0, :].copy()

# Remove background genes not expressed anywhere
sc.pp.filter_genes(adata, min_cells=3)

print(f"Cell count AFTER filtering: {adata.n_obs}")
print("Sample distribution after filtering:\n", adata.obs["batch"].value_counts())

# ==============================================================================
# 5. SECURE COMPRESSED ARCHIVE SAVE (.h5ad)
# ==============================================================================
adata.write("results/scanpy_objects/clean_filtered_organoids.h5ad")
print("Milestone 2 completed via Python with all 3 experimental groups!")
