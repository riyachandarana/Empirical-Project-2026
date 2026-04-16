import pandas as pd
from config import EMPLOYMENT_RAW, EMPLOYMENT_CLEAN

def main():
    df = pd.read_excel(EMPLOYMENT_RAW, sheet_name="All May 2023 data")

    # Keep only national U.S. occupation rows
    df = df[(df["AREA"] == 99) & (df["AREA_TITLE"] == "U.S.")].copy()

    df = df.rename(columns={
        "OCC_CODE": "occupation_code",
        "OCC_TITLE": "occupation_name",
        "TOT_EMP": "employment"
    })

    df = df[["occupation_code", "occupation_name", "employment"]].copy()

    df["occupation_code"] = df["occupation_code"].astype(str).str.strip()
    df["occupation_name"] = df["occupation_name"].astype(str).str.strip()
    df["employment"] = pd.to_numeric(df["employment"], errors="coerce")

    df = df[df["occupation_code"].str.contains("-", na=False)]
    df["year"] = 2023

    df = df.dropna(subset=["occupation_code", "occupation_name", "employment"])
    df = df.drop_duplicates(subset=["occupation_code"])

    df.to_csv(EMPLOYMENT_CLEAN, index=False)

    print(df.head())
    print("Saved employment clean data")

if __name__ == "__main__":
    main()
