"""
Build a strain x metabolic-feature matrix (gene essentiality profile) and
test whether it separates resistant vs. susceptible strains, using PCA for
exploration and a Random Forest classifier evaluated with leave-one-species-
out cross-validation (to avoid the classifier simply re-learning species
identity rather than a genuine cross-species metabolic signature of
resistance). Addresses RQ3.

Usage:
    python 04_comparative_stats_ml.py \\
        --essentiality_csv results/essentiality_amr_overlay.csv \\
        --metadata_csv data/metadata/phenotypes.csv
"""
import argparse

import pandas as pd
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import LeaveOneGroupOut, cross_val_score
from sklearn.preprocessing import StandardScaler


def build_feature_matrix(essentiality_csv):
    df = pd.read_csv(essentiality_csv)
    pivot = df.pivot_table(
        index="sample_id", columns="gene", values="essential", aggfunc="max", fill_value=False
    )
    return pivot.astype(int)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--essentiality_csv", required=True)
    parser.add_argument(
        "--metadata_csv",
        required=True,
        help="CSV with columns: sample_id,species,resistance_phenotype",
    )
    args = parser.parse_args()

    features = build_feature_matrix(args.essentiality_csv)
    meta = pd.read_csv(args.metadata_csv).set_index("sample_id")
    data = features.join(meta, how="inner")

    if data.empty:
        raise SystemExit("No overlapping sample_ids between essentiality matrix and metadata.")

    y = (data["resistance_phenotype"].str.lower() == "resistant").astype(int)
    groups = data["species"]
    X = data.drop(columns=["resistance_phenotype", "species"])

    scaled = StandardScaler().fit_transform(X)
    pca_model = PCA(n_components=2).fit(scaled)
    print("PCA explained variance ratio:", pca_model.explained_variance_ratio_)

    clf = RandomForestClassifier(n_estimators=500, random_state=42, class_weight="balanced")
    logo = LeaveOneGroupOut()
    if groups.nunique() < 2:
        print("Only one species present - skipping leave-one-species-out CV; "
              "report requires >=2 species for a fair cross-species test.")
        return

    scores = cross_val_score(clf, X, y, groups=groups, cv=logo, scoring="roc_auc")
    print(f"Leave-one-species-out ROC-AUC: {scores.mean():.3f} +/- {scores.std():.3f}")


if __name__ == "__main__":
    main()
