"""
Load draft GEMs produced by CarveMe, run basic sanity checks, and report the
predicted growth rate on the gap-filling medium.

Usage:
    python 01_load_and_qc_models.py --models_dir results/gems --out results/qc_summary.csv

Note: this is a fast structural/growth check, not a substitute for a full
`memote` quality report, which is recommended before drawing biological
conclusions from any of these models.
"""
import argparse
import glob
import os

import cobra
import pandas as pd


def qc_model(path):
    model = cobra.io.read_sbml_model(path)
    solution = model.optimize()
    return {
        "model": os.path.basename(path),
        "n_reactions": len(model.reactions),
        "n_metabolites": len(model.metabolites),
        "n_genes": len(model.genes),
        "growth_rate": solution.objective_value,
        "status": solution.status,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--models_dir", required=True, help="Directory containing *_draft.xml GEMs")
    parser.add_argument("--out", default="qc_summary.csv")
    args = parser.parse_args()

    rows = []
    model_paths = sorted(glob.glob(os.path.join(args.models_dir, "**", "*.xml"), recursive=True))
    if not model_paths:
        raise SystemExit(f"No .xml models found under {args.models_dir}")

    for path in model_paths:
        try:
            rows.append(qc_model(path))
        except Exception as exc:  # keep going even if one model fails to load/solve
            rows.append({"model": os.path.basename(path), "status": f"ERROR: {exc}"})

    df = pd.DataFrame(rows)
    df.to_csv(args.out, index=False)
    print(df.to_string(index=False))


if __name__ == "__main__":
    main()
