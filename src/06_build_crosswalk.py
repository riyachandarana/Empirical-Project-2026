from __future__ import annotations

import difflib
import pandas as pd

from config import AIOE_CLEAN, EMPLOYMENT_CLEAN, CROSSWALK
from utils import save_csv


def best_match(title: str, choices: list[str]) -> tuple[str, float]:
    matches = difflib.get_close_matches(title, choices, n=1, cutoff=0.0)
    if not matches:
        return "", 0.0
    match = matches[0]
    score = difflib.SequenceMatcher(None, title, match).ratio()
    return match, score


def main() -> None:
    aioe = pd.read_csv(AIOE_CLEAN)
    emp = pd.read_csv(EMPLOYMENT_CLEAN)

    uk_titles = sorted(emp["occupation_name"].dropna().unique().tolist())

    rows = []
    for title in aioe["occupation_title"].dropna().unique():
        match, score = best_match(title, uk_titles)

        matched_rows = emp.loc[emp["occupation_name"] == match, ["occupation_code", "occupation_name"]].drop_duplicates()

        if matched_rows.empty:
            rows.append(
                {
                    "aioe_occupation_title": title,
                    "matched_occupation_title": None,
                    "occupation_code": None,
                    "match_score": score,
                    "manual_review": True,
                }
            )
        else:
            for _, r in matched_rows.iterrows():
                rows.append(
                    {
                        "aioe_occupation_title": title,
                        "matched_occupation_title": r["occupation_name"],
                        "occupation_code": r["occupation_code"],
                        "match_score": score,
                        "manual_review": score < 0.75,
                    }
                )

    crosswalk = pd.DataFrame(rows).drop_duplicates()

    save_csv(crosswalk, CROSSWALK)
    print(f"Saved crosswalk with {len(crosswalk):,} rows to {CROSSWALK}")
    print("Review rows where manual_review == True before proceeding.")


if __name__ == "__main__":
    main()
