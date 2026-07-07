"""
Run flux balance analysis (FBA) and flux variability analysis (FVA) on each
GEM, producing one long-format CSV across all models so flux ranges can be
compared between strains/species downstream.

Usage:
    python 02_fba_fva.py --models_dir results/gems --out results/fva_results.csv \
        --fraction_of_optimum 0.9
"""
import argparse
import glob
import os

import cobra
import pandas as pd
from cobra.flux_analysis import flux_variability_analysis


def analyze(path, fraction_of_optimum):
    model = cobra.io.read_sbml_model(path)
    model.optimize()
    fva = flux_variability_analysis(model, fraction_of_optimum=fraction_of_optimum)
    fva["model"] = os.path.basename(path)
    fva["reaction"] = fva.index
    fva["subsystem"] = [
        model.reactions.get_by_id(r).subsystem if r in model.reactions else None
        for r in fva.index
    ]
    return fva.reset_index(drop=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--models_dir", required=True)
    parser.add_argument("--out", default="fva_results.csv")
    parser.add_argument("--fraction_of_optimum", type=float, default=0.9)
    args = parser.parse_args()

    model_paths = sorted(glob.glob(os.path.join(args.models_dir, "**", "*.xml"), recursive=True))
    if not model_paths:
        raise SystemExit(f"No .xml models found under {args.models_dir}")

    frames = [analyze(p, args.fraction_of_optimum) for p in model_paths]
    result = pd.concat(frames, ignore_index=True)
    result.to_csv(args.out, index=False)
    print(f"Wrote {len(result)} rows across {len(model_paths)} models to {args.out}")


if __name__ == "__main__":
    main()
