from __future__ import annotations

import numpy as np
import pandas as pd

from config import MERGED, FEATURES
from utils import save_csv, zscore


def main() -> None:
    df = pd.read_csv(MERGED)

    # Identify employment columns
    emp_cols = [c for c in df.columns if c.startswith("employment_")]
    if len(emp_cols) == 0:
        raise ValueError("No employment columns found.")

    emp_cols_sorted = sorted(emp_cols)
    emp_latest_col = emp_cols_sorted[-1]

    # Ensure valid values for transformations
    df = df[
        (df["weekly_pay"] > 0) &
        (df[emp_latest_col] > 0)
    ].copy()

    # If two employment years exist, compute growth
    if len(emp_cols_sorted) >= 2:
        emp_base_col = emp_cols_sorted[0]
        df = df[df[emp_base_col] > 0].copy()
        df["employment_growth"] = (
            (df[emp_latest_col] - df[emp_base_col]) / df[emp_base_col]
        )
    else:
        df["employment_growth"] = np.nan

    # Core derived variables
    df["log_pay"] = np.log(df["weekly_pay"])
    df["log_employment"] = np.log(df[emp_latest_col])
    df["advert_intensity"] = df["adverts"] / df[emp_latest_col]

    # Education to skill mapping
    education_map = {
        "No formal educational credential": 0,
        "High school diploma or equivalent": 1,
        "Some college, no degree": 2,
        "Postsecondary nondegree award": 2,
        "Associate's degree": 3,
        "Bachelor's degree": 4,
        "Master's degree": 5,
        "Doctoral or professional degree": 6,
    }

    df["skill"] = df["education_required"].map(education_map)

    # Optional interaction term
    df["ai_skill_interaction"] = df["ai_exposure"] * df["skill"]

    # Standardised variables
    df["ai_exposure_z"] = zscore(df["ai_exposure"])
    df["pay_z"] = zscore(df["weekly_pay"])
    df["employment_z"] = zscore(df[emp_latest_col])
    df["advert_intensity_z"] = zscore(df["advert_intensity"])

    # Exposure groups for descriptive analysis
    df["exposure_quantile"] = pd.qcut(
        df["ai_exposure"],
        q=4,
        labels=["Low", "Lower-middle", "Upper-middle", "High"],
        duplicates="drop",
    )

    df = df.replace([np.inf, -np.inf], np.nan)

    required_cols = [
        "occupation_code",
        "occupation_name",
        "ai_exposure",
        "weekly_pay",
        "log_pay",
        "log_employment",
        "advert_intensity",
        "skill",
    ]

    df = df.dropna(subset=required_cols)

    save_csv(df, FEATURES)
    print(f"Saved final analysis dataset with {len(df):,} rows to {FEATURES}")


if __name__ == "__main__":
    main()
