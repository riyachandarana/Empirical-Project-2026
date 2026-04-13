from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd

from config import FEATURES, FIGURES, TABLES


def save_plot(path):
    plt.tight_layout()
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()


def main() -> None:
    df = pd.read_csv(FEATURES)

    # 1. Distribution of AI exposure
    plt.figure(figsize=(8, 5))
    plt.hist(df["ai_exposure"].dropna(), bins=20)
    plt.title("Distribution of AI Exposure Across Occupations")
    plt.xlabel("AI Exposure")
    plt.ylabel("Count")
    save_plot(FIGURES / "01_ai_exposure_distribution.png")

    # 2. Top 10 most exposed occupations
    top10 = df.sort_values("ai_exposure", ascending=False).head(10)
    plt.figure(figsize=(10, 6))
    plt.barh(top10["occupation_name"], top10["ai_exposure"])
    plt.title("Top 10 Most AI-Exposed Occupations")
    plt.xlabel("AI Exposure")
    plt.ylabel("Occupation")
    plt.gca().invert_yaxis()
    save_plot(FIGURES / "02_top10_ai_exposed.png")

    # 3. AI exposure vs pay
    plt.figure(figsize=(8, 5))
    plt.scatter(df["ai_exposure"], df["weekly_pay"])
    plt.title("AI Exposure and Weekly Pay")
    plt.xlabel("AI Exposure")
    plt.ylabel("Weekly Pay")
    save_plot(FIGURES / "03_exposure_vs_pay.png")

    # 4. AI exposure vs employment growth
    plt.figure(figsize=(8, 5))
    plt.scatter(df["ai_exposure"], df["employment_growth"])
    plt.title("AI Exposure and Employment Growth")
    plt.xlabel("AI Exposure")
    plt.ylabel("Employment Growth")
    save_plot(FIGURES / "04_exposure_vs_employment_growth.png")

    # 5. AI exposure vs advert intensity
    plt.figure(figsize=(8, 5))
    plt.scatter(df["ai_exposure"], df["advert_intensity"])
    plt.title("AI Exposure and Job Advert Intensity")
    plt.xlabel("AI Exposure")
    plt.ylabel("Advert Intensity")
    save_plot(FIGURES / "05_exposure_vs_advert_intensity.png")

    # 6. ML feature importance
    fi = pd.read_csv(TABLES / "ml_feature_importance.csv")
    plt.figure(figsize=(8, 5))
    plt.barh(fi["feature"], fi["importance"])
    plt.title("Random Forest Feature Importance")
    plt.xlabel("Importance")
    plt.ylabel("Feature")
    plt.gca().invert_yaxis()
    save_plot(FIGURES / "06_ml_feature_importance.png")

    print(f"Saved figures to {FIGURES}")


if __name__ == "__main__":
    main()
