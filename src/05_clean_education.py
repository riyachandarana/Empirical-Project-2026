import pandas as pd
from config import EDUCATION_RAW, EDUCATION_CLEAN

def main():
    # Read education requirements from BLS National Employment Matrix
    df = pd.read_excel(
        EDUCATION_RAW,
        sheet_name="Table 5.4",
        header=1
    )

    print(df.columns)

    # Rename columns to consistent snake_case format used across all datasets
    df = df.rename(columns={
        "2024 National Employment Matrix title": "occupation_name",
        "2024 National Employment Matrix code": "occupation_code",
        "Typical education needed for entry": "education_required"
    })

    # Keep only columns needed for analysis
    df = df[["occupation_code", "occupation_name", "education_required"]].copy()

    # Strip whitespace to prevent merge failures caused by invisible characters
    df["occupation_code"] = df["occupation_code"].astype(str).str.strip()

    # Drop rows missing occupation code or education requirements
    df = df.dropna(subset=["occupation_code", "education_required"])

    df.to_csv(EDUCATION_CLEAN, index=False)

    print(df.head())
    print("Done")

if __name__ == "__main__":
    main()
