# Milestone 2 Documentation: Quality Control, Filtering, and Normalization

This folder details the rigorous preprocessing and quality control (QC) pipeline executed on the raw single-cell HDF5 (.h5) matrices from dataset **GSE334035**. The primary purpose of this phase is to eliminate technical noise, cellular debris, and apoptotic artifacts before downstream dimensional reduction or lipid metabolic profiling. 


## What we have done with `scanpy`
1. Memory-Safe Ingestion: Instead of keeping three separate huge tables in your computer's RAM, Scanpy loaded the `.h5` files as highly efficient sparse matrices (storing only actual non-zero gene readouts) and merged them into a single object instantly.
2. Dynamic RAM Flushing (`del`): As soon as the main data matrix (`adata`) was created, we explicitly deleted the temporary variables from the memory, freeing up your RAM.
3. In-Place Processing (`inplace=True`): We performed the filtering and quality metrics calculations directly onto the existing data table. R creates entirely new copies of a dataset every time you filter it; Python modified the matrix directly, completely eliminating the lag.



## Output
```bash
Calculating mitochondrial QC markers...
Cells before filtering: 54198
Cells after filtering: 45746
Final sample profile:
 batch
APOE3_Veh      19279
APOE4_Veh      14478
APOE4_Ceria    11989
```

## Verdict: The Output is Highly Optimal

In single-cell transcriptomics, losing a small percentage of cells during preprocessing is completely normal.
- Our initial count was `54,198` cells.
- After applying the quality control filters, you have `45,746` cells remaining.
- This means **84.4%** of our cells survived, which is a fantastic yield rate. It indicates the original dataset was high-quality, and we have preserved plenty of biological data to map your lipid pathways.


## Biological Interpretation
- `APOE3_Veh` (19,279 cells): This is our **healthy control** baseline. Having nearly 20,000 cells here gives us an extremely deep baseline of how normal, healthy astrocytes and neurons handle lipid and cholesterol transport.
- `APOE4_Veh` (14,478 cells): This is our **Alzheimer's disease** baseline. With over 14,000 cells, we have massive statistical power to look at this group, compare it to the APOE3 group, and pinpoint exactly which lipid synthesis genes are failing.
- `APOE4_Ceria` (11,989 cells): This is our **treatment** group. Having roughly 12,000 healthy cells post-QC allows us to run a highly accurate statistical comparison to see if the Ceria nanoparticles successfully pushed the broken lipid pathways back toward the healthy APOE3 baseline.















