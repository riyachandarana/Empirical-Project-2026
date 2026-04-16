import pandas as pd
from config import EARNINGS_RAW, EARNINGS_CLEAN

def main():
    df = pd.read_excel(EARNINGS_RAW, sheet_name="All May 2023 data")

    # Keep only national U.S. occupation rows
    df = df[(df["AREA"] == 99) & (df["AREA_TITLE"] == "U.S.")].copy()

    df = df.rename(columns={
        "OCC_CODE": "occupation_code",
        "OCC_TITLE": "occupation_name",
        "A_MEDIAN": "weekly_pay"
    })

    df = df[["occupation_code", "occupation_name", "weekly_pay"]].copy()

    df["occupation_code"] = df["occupation_code"].astype(str).str.strip()
    df["occupation_name"] = df["occupation_name"].astype(str).str.strip()
    df["weekly_pay"] = pd.to_numeric(df["weekly_pay"], errors="coerce")

    df = df[df["occupation_code"].str.contains("-", na=False)]
    df["year"] = 2023

    df = df.dropna(subset=["occupation_code", "occupation_name", "weekly_pay"])
    df = df.drop_duplicates(subset=["occupation_code"])

    df.to_csv(EARNINGS_CLEAN, index=False)

    print(df.head())
    print("Saved earnings clean data")

if __name__ == "__main__":
    main()
