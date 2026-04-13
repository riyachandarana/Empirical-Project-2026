from __future__ import annotations

import pandas as pd

from config import EMPLOYMENT_RAW, EMPLOYMENT_CLEAN
from utils import read_table, snake_case_columns, save_csv, clean_text, safe_numeric

"""
Expected cleaned output:
- occupation_code
- occupation_name
- year
- employment
"""


def main() -> None:
    df = read_table(EMPLOYMENT_RAW)
    df = snake_case_columns(df)

    print("Employment raw columns:", list(df.columns))

    rename_map = {
        "soc_code": "occupation_code",
        "occupation": "occupation_name",
        "occupation_title": "occupation_name",
        "value": "employment",
        "employment_count": "employment",
    }
    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

    required = ["occupation_code", "occupation_name", "year", "employment"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise KeyError(f"Employment file needs columns like {required}. Missing: {missing}")

    df = df[required].copy()
    df["occupation_code"] = df["occupation_code"].astype(str).str.strip()
    df["occupation_name"] = clean_text(df["occupation_name"])
    df["year"] = safe_numeric(df["year"]).astype("Int64")
    df["employment"] = safe_numeric(df["employment"])

    df = df.dropna(subset=["occupation_code", "occupation_name", "year", "employment"])
    df = df[df["employment"] >= 0]

    # Optional aggregation in case file has duplicates
    df = (
        df.groupby(["occupation_code", "occupation_name", "year"], as_index=False)["employment"]
        .sum()
    )

    save_csv(df, EMPLOYMENT_CLEAN)
    print(f"Saved {len(df):,} rows to {EMPLOYMENT_CLEAN}")


if __name__ == "__main__":
    main()
