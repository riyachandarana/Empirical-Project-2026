import pandas as pd

df = pd.read_excel("data/raw/education.xlsx")

print(df.columns)  # run once to see names

# CHANGE THESE if needed based on what prints
df = df.rename(columns={
    "SOC Code": "occupation_code",
    "Typical education needed for entry": "education_required"
})

df = df[["occupation_code", "education_required"]]

# Fix codes like 15-1252.00 → 15-1252
df["occupation_code"] = df["occupation_code"].astype(str).str[:7]

df.to_csv("data/interim/education_clean.csv", index=False)

print("Done")
