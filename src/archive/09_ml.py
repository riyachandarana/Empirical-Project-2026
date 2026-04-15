from __future__ import annotations

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

from config import FEATURES, TABLES


def main() -> None:
    df = pd.read_csv(FEATURES)

    # For now, predict pay from exposure and demand-related variables
    feature_cols = ["ai_exposure", "employment_growth", "advert_intensity"]
    target_col = "log_pay"

    model_df = df[feature_cols + [target_col]].dropna().copy()

    X = model_df[feature_cols]
    y = model_df[target_col]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=300,
        max_depth=5,
        min_samples_leaf=2,
        random_state=42,
    )
    model.fit(X_train, y_train)

    preds = model.predict(X_test)

    metrics = pd.DataFrame(
        {
            "metric": ["rmse", "r_squared"],
            "value": [
                mean_squared_error(y_test, preds) ** 0.5,
                r2_score(y_test, preds),
            ],
        }
    )

    importances = pd.DataFrame(
        {
            "feature": feature_cols,
            "importance": model.feature_importances_,
        }
    ).sort_values("importance", ascending=False)

    metrics.to_csv(TABLES / "ml_metrics.csv", index=False)
    importances.to_csv(TABLES / "ml_feature_importance.csv", index=False)

    print(f"Saved ML outputs to {TABLES}")


if __name__ == "__main__":
    main()
