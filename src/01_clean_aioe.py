from __future__ import annotations

import pandas as pd

from config import AIOE_RAW, AIOE_CLEAN
from utils import read_table, snake_case_columns, save_csv, clean_text

"""
Expected raw columns, or similar:
- occupation_title
- ai_exposure

Edit the rename_map below once you inspect your actual file.
"""


def main() -> None:
    df = read_table(AIOE_RAW)
    df = snake_case_columns(df)

    print("AIOE raw columns:", list(df.columns))

    rename_map = {
        # update these to match your actual raw file
        "occupation": "occupation_title",
        "job_title": "occupation_title",
        "title": "occupation_title",
        "aioe": "ai_exposure",
        "exposure": "ai_exposure",
        "ai_exposure_score": "ai_exposure",
    }
    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

    required = ["occupation_title", "ai_exposure"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise KeyError(f"AIOE file needs columns like {required}. Missing: {missing}")

    df = df[required].copy()
    df["occupation_title"] = clean_text(df["occupation_title"])
    df["ai_exposure"] = pd.to_numeric(df["ai_exposure"], errors="coerce")

    df = df.dropna(subset=["occupation_title", "ai_exposure"])
    df = df.drop_duplicates()

    save_csv(df, AIOE_CLEAN)
    print(f"Saved {len(df):,} rows to {AIOE_CLEAN}")


if __name__ == "__main__":
    main()
