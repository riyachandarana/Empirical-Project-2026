from __future__ import annotations

import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

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


def run_quantile(df: pd.DataFrame, y_col: str, x_cols: list[str], model_name: str) -> pd.DataFrame:
    model_df = df[x_cols + [y_col]].dropna().copy()
    formula = y_col + " ~ " + " + ".join(x_cols)
    model = smf.quantreg(formula, model_df).fit(q=0.5)

    return pd.DataFrame(
        {
            "term": model.params.index,
            "coef": model.params.values,
            "std_err": model.bse.values,
            "p_value": model.pvalues.values,
            "r_squared": None,
            "n": int(model.nobs),
            "outcome": y_col,
            "model": model_name + "_median",
        }
    )


def main() -> None:
    df = pd.read_csv(FEATURES)

    specs = [
        ("baseline", ["ai_exposure"]),
        ("with_skill", ["ai_exposure", "skill"]),
        ("with_interaction", ["ai_exposure", "skill", "ai_skill_interaction"]),
    ]

    outcomes = ["log_pay", "log_employment", "advert_intensity"]

    # Robustness: trim top 5% wages
    wage_cutoff = df["weekly_pay"].quantile(0.95)
    df_trimmed = df[df["weekly_pay"] <= wage_cutoff].copy()

    results = []

    # Full sample
    for outcome in outcomes:
        for model_name, x_cols in specs:
            results.append(run_model(df, outcome, x_cols, model_name + "_full"))

    # Trimmed sample
    for outcome in outcomes:
        for model_name, x_cols in specs:
            results.append(run_model(df_trimmed, outcome, x_cols, model_name + "_trimmed"))

    # Median regression (wages only)
    for model_name, x_cols in specs:
        results.append(run_quantile(df, "log_pay", x_cols, model_name))

    out = pd.concat(results, ignore_index=True)

    out_path = TABLES / "regression_results.csv"
    out.to_csv(out_path, index=False)
    print(f"Saved regression results to {out_path}")


if __name__ == "__main__":
    main()
