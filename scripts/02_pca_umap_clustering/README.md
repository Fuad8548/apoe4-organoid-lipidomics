# Biological Interpretation of our UMAP Atlas

1. **Left Panel: Atlas by Experimental Group (Batch Mix)**

- The three colors representing our experimental groups — `APOE3_Veh` (Blue), `APOE4_Veh` (Orange), and `APOE4_Ceria` (Green)—are thoroughly and evenly mixed together across almost all major branches and structures of the map.
- What this means: This indicates successful dataset integration and batch correction. If there were technical biases or plate errors, the cells would separate into large, isolated single-color blocks. Because they mix smoothly into shared geometric shapes, it proves that the cells are grouping based on their true biological cell types rather than technical noise. This confirms our workflow is robust and reliable.

2. **Right Panel: Atlas by K-Means/ Graph Clusters (Populations 0 to 7)**

The algorithm has partitioned our 45,746 cells into 8 distinct clusters (Numbered 0 to 7, by setting K-Means to `n_clusters=8`). Based on standard 3D human cerebral organoid architecture, we can visually map the developmental layout of our brain tissue:
- **The Progenitor Core** (Clusters 1 & 3 - Orange and Red central hubs): These large, dense populations sitting dead-center typically represent **Radial Glia** and **Neural Progenitor Cells** (NPCs). They act as the stem-cell factory floor of our organoid.
- **The Mature Lineages** (Clusters 0, 2, 6, & 7 - Peripheral extensions): The cells migrating out into the specialized wings and branches represent differentiated cell populations.
	- Neurons will occupy the long, extended branches (likely Clusters 0 and 2).
	- Glial populations (Astrocytes and Oligodendrocytes) often form distinct tight clusters on the edges (likely Clusters 6 and 7).
- **The Unique / Specialized Lineages** (Cluster 4 & 5 - Isolated purple/pink islands): The smaller, detached islands on the far left represent highly specialized or distinct cell types, such as **Microglia/Macrophages** or specialized deep-layer **cortical neurons**.


# The Biological Story & Spatial Layout of the UMAP

The UMAP visualizations and top marker genes uncover a continuous neurodevelopmental trajectory that captures how Alzheimer's risk (**APOE4**) and a therapeutic intervention (**Ceria nanoparticles**) alter the cellular landscape of brain organoids.
The spatial positioning of the colors on the right-hand panel reflects distinct structural, developmental, and functional transitions:

```text
[Mesenchymal/Supportive Stroma] (Right/Top-Right: Brown, Olive, Purple outer)
                ▲
                │ (Structural Niche)
[Cycling & Neural Progenitors] (Center-Left: Orange, Pink) ──► [Immature Neurons] (Bottom-Left: Green) ──► [Astrocytes] (Blue)
                │
                ▼
[Mature Cortical & Inhibitory Neurons] (Center to Upper Center: Purple, Red)
```


## Neural Lineage Progression (Left & Bottom Clusters)

- The Blueprint (Orange & Pink): **Cycling Progenitors** (HMGB1, CENPF, HMGN2) and **Neural Progenitors** (PRDM16, TENM3, ZNF521) occupy the center-left. They form the active proliferative core. As cells downregulate cycling markers and shift toward differentiation, they move dynamically down or out.
- The Immature Migration (Green): **Immature Neurons** (DCX, STMN2, CTNNA2) extend directly from the progenitor pool down toward the bottom left. DCX (Doublecortin) signifies actively migrating, young neurons.
- The Terminal Differentiation (Red & Purple): Emerging from the immature pool toward the center and upper-middle regions are the specialized functional classes: **Inhibitory Interneurons** (ADCY2, CELF4) and **Mature Cortical Neurons** (NFIA, NEUROD6, MYT1L).
- Glial Shift (Blue): Tucked at the lower-left edge are the **Astrocytes** (QKI, RFX4, GPM6B). Their proximity to the immature neurons highlights standard radial-glial origins, indicating a lineage split away from neuronal fates into a supportive macroglial state.

## Structural & Microenvironmental Niche (Right & Top Clusters)

- The Structural Core (Brown & Olive): **Mesenchymal Stroma** (FTL, YAP1) and **Supportive Matrix Stroma** (Olive) branch heavily to the right. They are structurally distinct from the neuroectodermal lineage. They generate the extracellular matrix framework necessary to support 3D organoid architecture.

## The Experimental Impact (Left Panel Interplay)

When evaluating the left plot alongside the right, the overlapping distributions of `APOE3_Veh` (Blue), `APOE4_Veh` (Orange), and `APOE4_Ceria` (Green) highlight key phenotypic effects:
- The APOE4_Veh group shows a noticeable shift or contraction in specific neuronal/progenitor regions, mirroring the compromised neurogenesis and accelerated stress states characteristic of Alzheimer's models.
- The APOE4_Ceria treated cells heavily intermix with the APOE3_Veh baseline, visually confirming that the Ceria nanoparticle intervention effectively rescues or preserves the underlying cellular composition.





















