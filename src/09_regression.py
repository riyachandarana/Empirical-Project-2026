from __future__ import annotations

import pandas as pd
import statsmodels.api as sm

from config import FEATURES, TABLES


def run_model(df: pd.DataFrame, y_col: str) -> pd.DataFrame:
    X = df[["ai_exposure"]].copy()
    X = sm.add_constant(X)
    y = df[y_col]

    model = sm.OLS(y, X, missing="drop").fit(cov_type="HC1")

    result = pd.DataFrame(
        {
            "term": model.params.index,
            "coef": model.params.values,
            "std_err": model.bse.values,
            "p_value": model.pvalues.values,
            "r_squared": model.rsquared,
            "n": int(model.nobs),
            "outcome": y_col,
        }
    )
    return result


def main() -> None:
    df = pd.read_csv(FEATURES)

    outcomes = ["log_pay", "employment_growth", "advert_intensity"]
    results = [run_model(df, outcome) for outcome in outcomes]
    out = pd.concat(results, ignore_index=True)

    out_path = TABLES / "regression_results.csv"
    out.to_csv(out_path, index=False)
    print(f"Saved regression results to {out_path}")


if __name__ == "__main__":
    main()
