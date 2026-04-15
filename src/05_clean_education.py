import pandas as pd

df = pd.read_excel(
    "data/raw/education.xlsx",
    sheet_name="Table 5.4",
    header=1
)

print(df.columns)

df = df.rename(columns={
    "2024 National Employment Matrix title": "occupation_name",
    "2024 National Employment Matrix code": "occupation_code",
    "Typical education needed for entry": "education_required"
})

df = df[["occupation_code", "occupation_name", "education_required"]].copy()

df["occupation_code"] = df["occupation_code"].astype(str).str.strip()

df = df.dropna(subset=["occupation_code", "education_required"])

df.to_csv("data/interim/education_clean.csv", index=False)

print(df.head())
print("Done")
