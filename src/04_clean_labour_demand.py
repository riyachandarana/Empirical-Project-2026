from __future__ import annotations

import pandas as pd

from config import LABOUR_DEMAND_RAW, LABOUR_DEMAND_CLEAN
from utils import read_table, snake_case_columns, save_csv, clean_text, safe_numeric

"""
Expected cleaned output:
- occupation_code
- occupation_name
- year
- adverts
"""


def main() -> None:
    df = read_table(LABOUR_DEMAND_RAW)
    df = snake_case_columns(df)

    print("Labour demand raw columns:", list(df.columns))

    rename_map = {
        "soc_code": "occupation_code",
        "occupation": "occupation_name",
        "occupation_title": "occupation_name",
        "job_adverts": "adverts",
        "advert_count": "adverts",
        "vacancies": "adverts",
        "value": "adverts",
    }
    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

    required = ["occupation_code", "occupation_name", "year", "adverts"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise KeyError(f"Labour demand file needs columns like {required}. Missing: {missing}")

    df = df[required].copy()
    df["occupation_code"] = df["occupation_code"].astype(str).str.strip()
    df["occupation_name"] = clean_text(df["occupation_name"])
    df["year"] = safe_numeric(df["year"]).astype("Int64")
    df["adverts"] = safe_numeric(df["adverts"])

    df = df.dropna(subset=["occupation_code", "occupation_name", "year", "adverts"])
    df = df[df["adverts"] >= 0]

    df = (
        df.groupby(["occupation_code", "occupation_name", "year"], as_index=False)["adverts"]
        .sum()
    )

    save_csv(df, LABOUR_DEMAND_CLEAN)
    print(f"Saved {len(df):,} rows to {LABOUR_DEMAND_CLEAN}")


if __name__ == "__main__":
    main()
