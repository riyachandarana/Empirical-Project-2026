import pandas as pd
from config import LABOUR_DEMAND_RAW, LABOUR_DEMAND_CLEAN

def main():
    df = pd.read_excel(LABOUR_DEMAND_RAW, sheet_name="Table 1.10", header=1)

    print(df.columns)

    df = df.rename(columns={
        "2024 National Employment Matrix title": "occupation_name",
        "2024 National Employment Matrix code": "occupation_code",
        "Occupational openings, 2024–34 annual average": "adverts"
    })

    df = df[["occupation_code", "occupation_name", "adverts"]].copy()

    df["occupation_code"] = df["occupation_code"].astype(str).str.strip()
    df["occupation_name"] = df["occupation_name"].astype(str).str.strip()
    df["adverts"] = pd.to_numeric(df["adverts"], errors="coerce")

    # Keep occupation-style codes only
    df = df[df["occupation_code"].str.contains("-", na=False)]

    # Assign a reference year for the openings measure
    df["year"] = 2024

    df = df.dropna(subset=["occupation_code", "occupation_name", "adverts"])

    df.to_csv(LABOUR_DEMAND_CLEAN, index=False)

    print(df.head())
    print("Saved labour demand clean data")

if __name__ == "__main__":
    main()
