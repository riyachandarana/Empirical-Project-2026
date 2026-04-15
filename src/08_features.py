from __future__ import annotations

import numpy as np
import pandas as pd

from config import MERGED, FEATURES
from utils import save_csv, zscore


def main() -> None:
    df = pd.read_csv(MERGED)

    # identify dynamic employment columns
    emp_cols = [c for c in df.columns if c.startswith("employment_")]
    if len(emp_cols) < 2:
        raise ValueError("Need at least two employment columns to compute growth.")

    emp_cols_sorted = sorted(emp_cols)
    emp_base_col = emp_cols_sorted[0]
    emp_latest_col = emp_cols_sorted[-1]

    df["employment_growth"] = (
        (df[emp_latest_col] - df[emp_base_col]) / df[emp_base_col]
    )

    df["log_pay"] = np.log(df["weekly_pay"])
    df["advert_intensity"] = df["adverts"] / df[emp_latest_col]

    df["ai_exposure_z"] = zscore(df["ai_exposure"])
    df["pay_z"] = zscore(df["weekly_pay"])
    df["employment_growth_z"] = zscore(df["employment_growth"])
    df["advert_intensity_z"] = zscore(df["advert_intensity"])

    df["exposure_quantile"] = pd.qcut(
        df["ai_exposure"],
        q=4,
        labels=["Low", "Lower-middle", "Upper-middle", "High"],
        duplicates="drop",
    )

    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna(
        subset=[
            "occupation_code",
            "occupation_name",
            "ai_exposure",
            "weekly_pay",
            "log_pay",
            "employment_growth",
            "advert_intensity",
        ]
    )

    save_csv(df, FEATURES)
    print(f"Saved final analysis dataset with {len(df):,} rows to {FEATURES}")


if __name__ == "__main__":
    main()
