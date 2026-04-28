from __future__ import annotations

import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

from config import FEATURES, TABLES


def run_model(df: pd.DataFrame, y_col: str, x_cols: list[str], model_name: str) -> pd.DataFrame:
    """
    Estimates an OLS regression of y_col on x_cols using heteroskedasticity-
    robust standard errors (HC1). Returns a tidy DataFrame of coefficients,
    standard errors, p-values, R-squared, and sample size.
    """
    # Drop rows with missing values in any variable used in the model
    model_df = df[x_cols + [y_col]].dropna().copy()

    # Add constant (intercept) to the feature matrix
    X = sm.add_constant(model_df[x_cols])
    y = model_df[y_col]

    # Fit OLS with HC1 robust standard errors to account for heteroskedasticity
    model = sm.OLS(y, X).fit(cov_type="HC1")

    # Return results as a tidy DataFrame for easy concatenation later
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
    """
    Estimates a median (q=0.5) quantile regression of y_col on x_cols.
    Used as a robustness check — median regression is less sensitive to
    outliers and skewness in the wage distribution than OLS.
    """
    model_df = df[x_cols + [y_col]].dropna().copy()

    # Build formula string required by statsmodels quantreg
    formula = y_col + " ~ " + " + ".join(x_cols)
    model = smf.quantreg(formula, model_df).fit(q=0.5)

    return pd.DataFrame(
        {
            "term": model.params.index,
            "coef": model.params.values,
            "std_err": model.bse.values,
            "p_value": model.pvalues.values,
            "r_squared": None,  # Quantile regression does not produce R-squared
            "n": int(model.nobs),
            "outcome": y_col,
            "model": model_name + "_median",
        }
    )


def main() -> None:
    # Load the final analysis dataset produced by 09_features.py
    df = pd.read_csv(FEATURES)

    # Define regression specifications:
    # baseline: AI exposure only (raw association)
    # with_skill: adds education-based skill control (tests whether AI effect survives)
    # with_interaction: adds AI x skill interaction (tests whether AI effect varies by skill)
    specs = [
        ("baseline", ["ai_exposure"]),
        ("with_skill", ["ai_exposure", "skill"]),
        ("with_interaction", ["ai_exposure", "skill", "ai_skill_interaction"]),
    ]

    # Three outcome variables: log wages, log employment, and advert intensity (labour demand proxy)
    outcomes = ["log_pay", "log_employment", "advert_intensity"]

    # Robustness check: trim top 5% of weekly pay to test sensitivity to high earners
    wage_cutoff = df["weekly_pay"].quantile(0.95)
    df_trimmed = df[df["weekly_pay"] <= wage_cutoff].copy()

    results = []

    # Run all specifications on the full sample
    for outcome in outcomes:
        for model_name, x_cols in specs:
            results.append(run_model(df, outcome, x_cols, model_name + "_full"))

    # Run all specifications on the trimmed sample (robustness check)
    for outcome in outcomes:
        for model_name, x_cols in specs:
            results.append(run_model(df_trimmed, outcome, x_cols, model_name + "_trimmed"))

    # Run median regression on wages only as a further robustness check
    for model_name, x_cols in specs:
        results.append(run_quantile(df, "log_pay", x_cols, model_name))

    # Combine all results into a single tidy DataFrame
    out = pd.concat(results, ignore_index=True)

    # Save to output/tables for use in the blog notebook
    out_path = TABLES / "regression_results.csv"
    out.to_csv(out_path, index=False)
    print(f"Saved regression results to {out_path}")


if __name__ == "__main__":
    main()
