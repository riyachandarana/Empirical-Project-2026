import pandas as pd

aioe = pd.read_csv("data/interim/aioe_broad.csv")
emp = pd.read_csv("data/interim/employment_broad.csv")
earn = pd.read_csv("data/interim/earnings_broad.csv")

df = pd.merge(aioe, emp, on="broad_group", how="inner")
df = pd.merge(df, earn, on="broad_group", how="inner")

print("Merged shape:", df.shape)
print(df)

df.to_csv("data/processed/final_dataset.csv", index=False)
