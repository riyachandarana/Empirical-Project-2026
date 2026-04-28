from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from config import FEATURES, FIGURES, TABLES

PRIMARY = "#4A9BAF"
SECONDARY = "#7BB5A0"
ACCENT = "#D4957A"

def style_plot():
    plt.rcParams.update({
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.facecolor": "white",
        "figure.facecolor": "white",
        "axes.grid": True,
        "grid.alpha": 0.3,
    })

def save_plot(path):
    plt.tight_layout()
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()

def main():
    style_plot()
    df = pd.read_csv(FEATURES)

    plt.figure(figsize=(8, 5))
    plt.hist(df["ai_exposure"].dropna(), bins=20, color=PRIMARY, edgecolor="white")
    plt.title("Distribution of AI Exposure Across Occupations", fontsize=13, fontweight="bold")
    plt.xlabel("AI Exposure", fontsize=11)
    plt.ylabel("Count", fontsize=11)
    save_plot(FIGURES / "01_ai_exposure_distribution.png")

    top10 = df.sort_values("ai_exposure", ascending=False).head(10)
    plt.figure(figsize=(10, 6))
    plt.barh(top10["occupation_name"], top10["ai_exposure"], color=SECONDARY, edgecolor="white")
    plt.title("Top 10 Most AI-Exposed Occupations", fontsize=13, fontweight="bold")
    plt.xlabel("AI Exposure", fontsize=11)
    plt.gca().invert_yaxis()
    save_plot(FIGURES / "02_top10_ai_exposed.png")

    plt.figure(figsize=(8, 5))
    plt.scatter(df["ai_exposure"], df["weekly_pay"], color=PRIMARY, alpha=0.5, edgecolors="white", linewidths=0.3)
    z = np.polyfit(df["ai_exposure"].dropna(), df["weekly_pay"].dropna(), 1)
    p = np.poly1d(z)
    x_line = np.linspace(df["ai_exposure"].min(), df["ai_exposure"].max(), 100)
    plt.plot(x_line, p(x_line), color=ACCENT, linewidth=2, label="Trend")
    plt.legend()
    plt.title("AI Exposure and Weekly Pay", fontsize=13, fontweight="bold")
    plt.xlabel("AI Exposure", fontsize=11)
    plt.ylabel("Weekly Pay (USD)", fontsize=11)
    save_plot(FIGURES / "03_exposure_vs_pay.png")

    plt.figure(figsize=(8, 5))
    plt.scatter(df["ai_exposure"], df["employment_growth"], color=SECONDARY, alpha=0.5, edgecolors="white", linewidths=0.3)
    plt.title("AI Exposure and Employment Growth", fontsize=13, fontweight="bold")
    plt.xlabel("AI Exposure", fontsize=11)
    plt.ylabel("Employment Growth", fontsize=11)
    save_plot(FIGURES / "04_exposure_vs_employment_growth.png")

    plt.figure(figsize=(8, 5))
    plt.scatter(df["ai_exposure"], df["advert_intensity"], color=ACCENT, alpha=0.5, edgecolors="white", linewidths=0.3)
    plt.title("AI Exposure and Job Advert Intensity", fontsize=13, fontweight="bold")
    plt.xlabel("AI Exposure", fontsize=11)
    plt.ylabel("Advert Intensity", fontsize=11)
    save_plot(FIGURES / "05_exposure_vs_advert_intensity.png")

    fi = pd.read_csv(TABLES / "ml_feature_importance.csv")
    colors = [PRIMARY, SECONDARY, ACCENT, "#6B9E8F", "#C4825A"]
    plt.figure(figsize=(8, 5))
    plt.barh(fi["feature_label"], fi["importance"], color=colors[:len(fi)], edgecolor="white")
    plt.title("Random Forest Feature Importance", fontsize=13, fontweight="bold")
    plt.xlabel("Importance", fontsize=11)
    plt.gca().invert_yaxis()
    save_plot(FIGURES / "06_ml_feature_importance.png")

    print(f"Saved figures to {FIGURES}")

if __name__ == "__main__":
    main()
