# Data

## `data/raw/`

Your own raw sequencing reads (FASTQ) or assemblies (FASTA), one subfolder per
`sample_id`. Not tracked in git (see `.gitignore`) — keep on the Tesla server /
local storage and reference by path in `samplesheet.csv`.

## `data/public/`

Public ESKAPE genomes and phenotypes, used to add resistant/susceptible contrast
within each species without needing every comparison to come from your own
isolates.

Recommended sources:

- **[BV-BRC](https://www.bv-brc.org/)** (formerly PATRIC) — genome + curated AMR
  phenotype (MIC / clinical S-I-R) pairs, searchable by species and drug. This is
  the most direct source for resistant/susceptible genome pairs per ESKAPE species.
- **[NCBI Pathogen Detection](https://www.ncbi.nlm.nih.gov/pathogens/)** — isolates
  with AMR phenotype metadata and SNP clustering.
- **[NCBI Datasets (genome)](https://www.ncbi.nlm.nih.gov/datasets/genome/)** —
  reference-quality RefSeq/GenBank assemblies per species.
- **[CARD](https://card.mcmaster.ca/)** — curated resistance gene sequences and
  ontology, for cross-validating AMRFinderPlus calls.

See `download_public_data.sh` for a starting point using the NCBI `datasets` CLI.
BV-BRC genome+phenotype pairs are best pulled through its web interface or API,
since the phenotype/MIC metadata isn't part of the NCBI assembly record.

## `data/metadata/`

- `samplesheet.csv` — Nextflow pipeline input.
  Columns: `sample_id,species,reads_1,reads_2,assembly`
  (leave `reads_1`/`reads_2` empty if `--skip_assembly` and providing `assembly`
  directly, or vice versa).
- `phenotypes.csv` — used by `analysis/scripts/04_comparative_stats_ml.py`.
  Columns: `sample_id,species,resistance_phenotype,drug,mic_value`
