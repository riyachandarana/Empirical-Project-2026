from __future__ import annotations

import pandas as pd
import statsmodels.api as sm

from config import FEATURES, TABLES


def run_model(df: pd.DataFrame, y_col: str, x_cols: list[str], model_name: str) -> pd.DataFrame:
    model_df = df[x_cols + [y_col]].dropna().copy()

    X = sm.add_constant(model_df[x_cols])
    y = model_df[y_col]

    model = sm.OLS(y, X).fit(cov_type="HC1")

    return pd.DataFrame(
        {
            "term": model.params.index,
            "coef": model.params.values,
            "std_err": model.bse.values,
            "p_value": model.pvalues.values,
            "r_squared": model.rsquared,
            "n": int(model.nobs),
            "outcome": y_col,
            "model": model_name,
        }
    )


def main() -> None:
    df = pd.read_csv(FEATURES)

    specs = [
        ("baseline", ["ai_exposure"]),
        ("with_skill", ["ai_exposure", "skill_proxy"]),
    ]

    outcomes = ["log_pay", "employment_growth", "advert_intensity"]

    results = []
    for outcome in outcomes:
        for model_name, x_cols in specs:
            results.append(run_model(df, outcome, x_cols, model_name))

    out = pd.concat(results, ignore_index=True)

    out_path = TABLES / "regression_results.csv"
    out.to_csv(out_path, index=False)
    print(f"Saved regression results to {out_path}")


if __name__ == "__main__":
    main()
