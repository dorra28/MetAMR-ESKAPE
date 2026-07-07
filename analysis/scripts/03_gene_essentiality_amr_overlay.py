"""
Single-gene deletion essentiality analysis per model, joined against
AMRFinderPlus resistance-gene calls.

This is the core script for RQ1/RQ2: are AMR-associated genes metabolically
essential, and do resistant strains show a shifted essential-gene profile
relative to susceptible strains of the same species?

Usage:
    python 03_gene_essentiality_amr_overlay.py \\
        --models_dir results/gems \\
        --amr_dir results/amr \\
        --out results/essentiality_amr_overlay.csv
"""
import argparse
import glob
import os

import cobra
import pandas as pd
from cobra.flux_analysis import single_gene_deletion


def essentiality(path, growth_cutoff=0.01):
    model = cobra.io.read_sbml_model(path)
    wt_growth = model.slim_optimize()
    result = single_gene_deletion(model)
    result["model"] = os.path.basename(path)
    result["gene"] = result.index.map(lambda ids: sorted(ids)[0] if ids else None)
    result["essential"] = result["growth"] < (growth_cutoff * wt_growth)
    return result.reset_index(drop=True)


def load_amr_calls(amr_dir):
    frames = []
    for path in glob.glob(os.path.join(amr_dir, "**", "*_amrfinder.tsv"), recursive=True):
        df = pd.read_csv(path, sep="\t")
        df["sample_id"] = os.path.basename(path).replace("_amrfinder.tsv", "")
        frames.append(df)
    if not frames:
        return pd.DataFrame(columns=["sample_id", "Gene symbol", "Element type", "Class", "Subclass"])
    return pd.concat(frames, ignore_index=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--models_dir", required=True)
    parser.add_argument("--amr_dir", required=True)
    parser.add_argument("--out", default="essentiality_amr_overlay.csv")
    parser.add_argument("--growth_cutoff", type=float, default=0.01)
    args = parser.parse_args()

    model_paths = sorted(glob.glob(os.path.join(args.models_dir, "**", "*.xml"), recursive=True))
    if not model_paths:
        raise SystemExit(f"No .xml models found under {args.models_dir}")

    essentiality_df = pd.concat(
        [essentiality(p, args.growth_cutoff) for p in model_paths], ignore_index=True
    )
    essentiality_df["sample_id"] = essentiality_df["model"].str.replace("_draft.xml", "", regex=False)

    amr_df = load_amr_calls(args.amr_dir)

    merged = essentiality_df.merge(
        amr_df[["sample_id", "Gene symbol", "Element type", "Class", "Subclass"]],
        left_on=["sample_id", "gene"],
        right_on=["sample_id", "Gene symbol"],
        how="left",
    )
    merged["is_amr_gene"] = merged["Gene symbol"].notna()
    merged.to_csv(args.out, index=False)

    summary = merged.groupby("is_amr_gene")["essential"].mean()
    print("Fraction of genes that are essential, split by AMR annotation:")
    print(summary.to_string())


if __name__ == "__main__":
    main()
