"""RICE prioritization: rank product ideas by Reach x Impact x Confidence / Effort.

Reads data/features.csv, scores each idea, writes a ranked table and a chart.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent


def main():
    df = pd.read_csv(ROOT / "data" / "features.csv")
    # Reach: customers affected per quarter. Impact: 0.25 minimal .. 3 massive.
    # Confidence: 0-1. Effort: person-months.
    df["rice_score"] = (df["reach"] * df["impact"] * df["confidence"] / df["effort"]).round(0)
    df = df.sort_values("rice_score", ascending=False).reset_index(drop=True)
    df.index += 1
    df.index.name = "rank"
    df.to_csv(ROOT / "outputs" / "ranked_features.csv")
    print(df[["feature", "reach", "impact", "confidence", "effort", "rice_score"]].to_string(), "\n")

    fig, ax = plt.subplots(figsize=(9, 5))
    d = df.iloc[::-1]
    ax.barh(d["feature"], d["rice_score"], color="#2f6f9f")
    ax.set_title("Feature ideas ranked by RICE score")
    ax.set_xlabel("RICE score (higher = do sooner)")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(ROOT / "outputs" / "rice_ranking.png", dpi=150)


if __name__ == "__main__":
    main()
