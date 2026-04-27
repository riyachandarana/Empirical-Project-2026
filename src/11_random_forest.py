from __future__ import annotations
import sys
sys.path.insert(0, 'src')
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
from config import FEATURES, TABLES

print("Script started")
df = pd.read_csv(FEATURES)
print(f"Loaded data: {df.shape}")
feature_cols = ["ai_exposure","skill","log_employment","advert_intensity","ai_skill_interaction"]
model_df = df[feature_cols + ["log_pay"]].dropna().copy()
print(f"Model data: {model_df.shape}")
X = model_df[feature_cols]
y = model_df["log_pay"]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
rf = RandomForestRegressor(n_estimators=200, max_depth=4, min_samples_leaf=10, random_state=42, n_jobs=-1)
rf.fit(X_scaled, y)
print("Model fitted")
cv_scores = cross_val_score(rf, X_scaled, y, cv=5, scoring="r2")
print(f"CV R2: {cv_scores.mean():.3f}")
label_map = {"ai_exposure":"AI Exposure","skill":"Education Level","log_employment":"Log Employment","advert_intensity":"Job Advert Intensity","ai_skill_interaction":"AI x Skill Interaction"}
importance_df = pd.DataFrame({"feature": feature_cols, "importance": rf.feature_importances_})
importance_df["feature_label"] = importance_df["feature"].map(label_map)
importance_df = importance_df.sort_values("importance", ascending=False)
out_path = TABLES / "ml_feature_importance.csv"
importance_df.to_csv(out_path, index=False)
print(f"Saved to {out_path}")
cv_df = pd.DataFrame({"fold": range(1,6), "r_squared": cv_scores})
cv_df.to_csv(TABLES / "ml_cv_results.csv", index=False)
print("Done")
