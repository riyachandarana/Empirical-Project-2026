import pandas as pd
from config import AIOE_RAW, AIOE_CLEAN

def main():
    # Read the AIOE dataset from the appendix sheet which contains occupation-level exposure scores
    df = pd.read_excel(AIOE_RAW, sheet_name="Appendix A")

    # Rename columns to consistent snake_case format used across all datasets
    df = df.rename(columns={
        "SOC Code": "occupation_code",
        "Occupation Title": "occupation_title",
        "AIOE": "ai_exposure"
    })

    # Keep only the three columns needed for analysis
    df = df[["occupation_code", "occupation_title", "ai_exposure"]].copy()

    # Strip whitespace from string columns to prevent merge failures caused by invisible characters
    df["occupation_code"] = df["occupation_code"].astype(str).str.strip()
    df["occupation_title"] = df["occupation_title"].astype(str).str.strip()

    # Drop rows missing key identifiers or exposure score 
    df = df.dropna(subset=["occupation_code", "occupation_title", "ai_exposure"])

    df.to_csv(AIOE_CLEAN, index=False)

    print(df.head())
    print("Saved AIOE clean data")

if __name__ == "__main__":
    main()
