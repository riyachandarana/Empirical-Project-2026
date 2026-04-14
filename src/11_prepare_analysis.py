import pandas as pd
import numpy as np

df = pd.read_csv("data/processed/final_dataset.csv")

# Log transforms (important for economics)
df["log_wage"] = np.log(df["median_wage"])
df["log_employment"] = np.log(df["employment"])

print(df[["ai_exposure", "median_wage", "log_wage"]].head())
print(df.describe())

df.to_csv("data/processed/final_dataset.csv", index=False)
