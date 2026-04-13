from __future__ import annotations

import pandas as pd

from config import EARNINGS_RAW, EARNINGS_CLEAN
from utils import read_table, snake_case_columns, save_csv, clean_text, safe_numeric

"""
Expected cleaned output:
- occupation_code
- occupation_name
- year
- weekly_pay
"""


def main() -> None:
    df = read_table(EARNINGS_RAW)
    df = snake_case_columns(df)

    print("Earnings raw columns:", list(df.columns))

    rename_map = {
        "soc_code": "occupation_code",
        "occupation": "occupation_name",
        "occupation_title": "occupation_name",
        "median_weekly_pay": "weekly_pay",
        "gross_weekly_pay": "weekly_pay",
        "weekly_earnings": "weekly_pay",
        "value": "weekly_pay",
    }
    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

    required = ["occupation_code", "occupation_name", "year", "weekly_pay"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise KeyError(f"Earnings file needs columns like {required}. Missing: {missing}")

    df = df[required].copy()
    df["occupation_code"] = df["occupation_code"].astype(str).str.strip()
    df["occupation_name"] = clean_text(df["occupation_name"])
    df["year"] = safe_numeric(df["year"]).astype("Int64")
    df["weekly_pay"] = safe_numeric(df["weekly_pay"])

    df = df.dropna(subset=["occupation_code", "occupation_name", "year", "weekly_pay"])
    df = df[df["weekly_pay"] > 0]

    df = (
        df.groupby(["occupation_code", "occupation_name", "year"], as_index=False)["weekly_pay"]
        .mean()
    )

    save_csv(df, EARNINGS_CLEAN)
    print(f"Saved {len(df):,} rows to {EARNINGS_CLEAN}")


if __name__ == "__main__":
    main()
