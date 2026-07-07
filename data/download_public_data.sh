#!/usr/bin/env bash
# Skeleton for pulling ESKAPE reference-quality genomes from NCBI.
# Requires the NCBI 'datasets' CLI:
#   https://www.ncbi.nlm.nih.gov/datasets/docs/v2/download-and-install/
#
# For AMR phenotype (MIC/S-I-R) metadata paired with genomes, use BV-BRC
# (https://www.bv-brc.org/) directly - its phenotype data isn't part of the
# NCBI assembly record and is best queried through its web UI or API.

set -euo pipefail

SPECIES=(
  "Enterococcus faecium"
  "Staphylococcus aureus"
  "Klebsiella pneumoniae"
  "Acinetobacter baumannii"
  "Pseudomonas aeruginosa"
  "Enterobacter cloacae"
)

OUTDIR="$(dirname "$0")/public/genomes"
mkdir -p "$OUTDIR"

for sp in "${SPECIES[@]}"; do
  echo "Fetching reference-quality assemblies for: $sp"
  slug="$(echo "$sp" | tr ' ' '_')"
  datasets download genome taxon "$sp" \
    --reference \
    --include genome,protein,gff3 \
    --filename "$OUTDIR/${slug}.zip"
done

echo "Done. Unzip each archive under $OUTDIR before use."
echo "For AMR phenotype metadata, query BV-BRC (https://www.bv-brc.org/) and merge on sample_id."
