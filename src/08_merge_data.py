from __future__ import annotations

import pandas as pd

from config import (
    AIOE_CLEAN,
    EMPLOYMENT_CLEAN,
    EARNINGS_CLEAN,
    LABOUR_DEMAND_CLEAN,
    MERGED,
)
from utils import save_csv


def main() -> None:
    aioe = pd.read_csv(AIOE_CLEAN)
    emp = pd.read_csv(EMPLOYMENT_CLEAN)
    earnings = pd.read_csv(EARNINGS_CLEAN)
    labour = pd.read_csv(LABOUR_DEMAND_CLEAN)
    education = pd.read_csv("data/interim/education_clean.csv")

    # AIOE is already cleaned to occupation-code level
    aioe_mapped = aioe[["occupation_code", "occupation_title", "ai_exposure"]].copy()

    aioe_mapped = aioe_mapped.dropna(subset=["occupation_code", "ai_exposure"])
    aioe_mapped = (
        aioe_mapped.groupby("occupation_code", as_index=False)["ai_exposure"]
        .mean()
    )

    aioe_mapped = aioe_mapped.dropna(subset=["occupation_code"])
    aioe_mapped = (
        aioe_mapped.groupby("occupation_code", as_index=False)["ai_exposure"]
        .mean()
    )

    # Keep latest year for pay and adverts
    latest_pay_year = earnings["year"].max()
    latest_ad_year = labour["year"].max()

    earnings_latest = earnings.loc[earnings["year"] == latest_pay_year].copy()
    labour_latest = labour.loc[labour["year"] == latest_ad_year].copy()

    # Employment baseline and latest
    baseline_year = emp["year"].min()
    latest_emp_year = emp["year"].max()

    emp_base = emp.loc[emp["year"] == baseline_year, ["occupation_code", "employment"]].rename(
        columns={"employment": f"employment_{baseline_year}"}
    )
    emp_latest = emp.loc[emp["year"] == latest_emp_year, ["occupation_code", "occupation_name", "employment"]].rename(
        columns={"employment": f"employment_{latest_emp_year}"}
    )

    merged = aioe_mapped.merge(emp_latest, on="occupation_code", how="inner")
    merged = merged.merge(emp_base, on="occupation_code", how="left")
    merged = merged.merge(
        earnings_latest[["occupation_code", "weekly_pay"]],
        on="occupation_code",
        how="left",
    )
    merged = merged.merge(
        labour_latest[["occupation_code", "adverts"]],
        on="occupation_code",
        how="left",
    )
    merged = merged.merge(
    education[["occupation_code", "education_required"]],
    on="occupation_code",
    how="left",
    )

    save_csv(merged, MERGED)
    print(f"Saved merged data with {len(merged):,} rows to {MERGED}")
    print(f"Employment baseline year: {baseline_year}")
    print(f"Employment latest year: {latest_emp_year}")
    print(f"Earnings latest year: {latest_pay_year}")
    print(f"Labour latest year: {latest_ad_year}")


if __name__ == "__main__":
    main()
