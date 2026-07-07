# MetAMR-ESKAPE

**Genome-scale metabolic modeling of antimicrobial resistance in ESKAPE pathogens**

## Overview

Antimicrobial resistance (AMR) is one of the leading threats to global public health,
and countering it will require both novel antibacterial agents and alternative
approaches to understanding how resistance arises and persists. Genetic determinants
of resistance (resistance genes, point mutations, mobile elements) are extensively
catalogued, but the contribution of **bacterial metabolism** to the emergence,
persistence, and evolution of AMR remains poorly understood — metabolic state shapes
drug uptake and efflux, redox balance, target expression, and the physiological
tolerance that often precedes true genetic resistance.

**MetAMR-ESKAPE** reconstructs genome-scale metabolic models (GEMs) for the ESKAPE
pathogens — *Enterococcus faecium*, *Staphylococcus aureus*, *Klebsiella pneumoniae*,
*Acinetobacter baumannii*, *Pseudomonas aeruginosa*, and *Enterobacter* spp. — and
integrates them with resistome annotation and, where available, transcriptomic/
metabolomic data, to test whether metabolic network structure and flux capacity
predict or explain AMR phenotypes.

## Research questions

- **RQ1** — Do metabolic subsystems (central carbon metabolism, respiration/redox,
  amino acid biosynthesis) show altered flux capacity or gene essentiality in
  resistant vs. susceptible strains of the same species?
- **RQ2** — Is there a detectable metabolic fitness cost of resistance (reduced
  growth-associated flux, increased fragility of essential genes) in resistant
  strain models?
- **RQ3** — Do shared metabolic dependencies across ESKAPE species explain patterns
  of collateral sensitivity or cross-resistance?
- **RQ4** — When condition-specific omics data are available, do context-specific
  GEMs (transcriptome/metabolome-constrained) reveal condition-dependent metabolic
  vulnerabilities exploitable as adjuvant antibacterial targets?

## Repository structure

```
MetAMR-ESKAPE/
├── main.nf                     # Nextflow DSL2 entry point
├── nextflow.config              # profiles: standard / docker / tesla_server
├── modules/                     # one process per Nextflow module
│   ├── qc.nf
│   ├── assembly.nf
│   ├── annotation.nf
│   ├── amr_detection.nf
│   └── gem_reconstruction.nf
├── workflows/
│   └── eskape_gem_pipeline.nf
├── bin/                          # helper scripts called from Nextflow processes
├── analysis/scripts/             # COBRApy / stats analysis, run after the pipeline
│   ├── 01_load_and_qc_models.py
│   ├── 02_fba_fva.py
│   ├── 03_gene_essentiality_amr_overlay.py
│   └── 04_comparative_stats_ml.py
├── data/
│   ├── raw/                      # your own reads/assemblies (gitignored)
│   ├── public/                   # downloaded public genomes (gitignored)
│   └── metadata/                 # samplesheet.csv, phenotypes.csv
├── models/                       # draft + curated GEMs (SBML)
├── results/                      # pipeline outputs (gitignored)
├── docs/
│   └── methods.md                # detailed methods write-up 
├── environment.yml
├── Dockerfile
├── CITATION.cff
├── LICENSE
└── .gitignore
```

## Workflow overview

1. **Genome preparation** — QC (`fastp`) → assembly (`Unicycler`, skip if genomes are
   already assembled) → annotation (`Bakta`).
2. **Resistome annotation** — `AMRFinderPlus` (cross-checked against CARD where
   relevant) → gene-level resistance calls mapped onto model gene identifiers.
3. **Draft GEM reconstruction** — `CarveMe` (BiGG-based, fast and consistent across
   many strains), gap-filled on defined media (M9, LB).
4. **Model curation & QC** — structural sanity checks, growth-rate check on the
   gap-filling medium (`analysis/scripts/01_load_and_qc_models.py`); `memote` reports
   recommended before any model is used for biological conclusions.
5. **Simulation & analysis** (COBRApy) — FBA, flux variability analysis (FVA),
   single-gene essentiality, and an AMR-gene overlay to test RQ1/RQ2.
6. **Context-specific integration** (optional, needs RNA-seq/metabolomics) — GIMME/
   iMAT-style integration via `troppo`, to address RQ4.
7. **Comparative & statistical analysis** — cross-strain feature matrix (essentiality
   / flux ranges) → PCA, and a leave-one-species-out classifier to test whether a
   metabolic signature separates resistant from susceptible strains without simply
   re-learning species identity.

## Data sources

- **Your own isolates**: place raw reads or assemblies under `data/raw/<sample_id>/`
  and reference them in `data/metadata/samplesheet.csv`. Not tracked in git.
- **Public genomes + phenotypes**:
  - [BV-BRC](https://www.bv-brc.org/) (formerly PATRIC) — genome/AMR-phenotype pairs,
    searchable by species and drug; the most direct way to add resistant/susceptible
    contrast within each ESKAPE species.
  - [NCBI Pathogen Detection](https://www.ncbi.nlm.nih.gov/pathogens/) — isolates with
    AMR phenotype metadata and SNP clustering.
  - [NCBI RefSeq/GenBank assemblies](https://www.ncbi.nlm.nih.gov/datasets/genome/) —
    reference-quality genomes per species.
  - [CARD](https://card.mcmaster.ca/) — curated resistance gene sequences/ontology,
    used to cross-validate AMRFinderPlus calls.
- See `data/README.md` for the metadata schema and a genome-download helper script.

## Installation

```bash
conda env create -f environment.yml
conda activate metamr-eskape
```

or build the Docker image:

```bash
docker build -t metamr-eskape:latest .
```

## Usage

```bash
nextflow run main.nf \
  --samplesheet data/metadata/samplesheet.csv \
  --outdir results \
  -profile docker     

python analysis/scripts/01_load_and_qc_models.py --models_dir results/gems --out results/qc_summary.csv
python analysis/scripts/02_fba_fva.py --models_dir results/gems --out results/fva_results.csv
python analysis/scripts/03_gene_essentiality_amr_overlay.py --models_dir results/gems --amr_dir results/amr --out results/essentiality_amr_overlay.csv
python analysis/scripts/04_comparative_stats_ml.py --essentiality_csv results/essentiality_amr_overlay.csv --metadata_csv data/metadata/phenotypes.csv
```

## Citation

See `CITATION.cff`.

## License

MIT (see `LICENSE`) for code. Public genomic data retains the license of its
original source (BV-BRC / NCBI / CARD).

## Contact

Dorra Rjaibi — PhD researcher
