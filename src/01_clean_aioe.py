import pandas as pd
from config import AIOE_RAW, AIOE_CLEAN

def main():
    df = pd.read_excel(AIOE_RAW, sheet_name="Appendix A")

    df = df.rename(columns={
        "SOC Code": "occupation_code",
        "Occupation Title": "occupation_title",
        "AIOE": "ai_exposure"
    })

    df = df[["occupation_code", "occupation_title", "ai_exposure"]].copy()

    df["occupation_code"] = df["occupation_code"].astype(str).str.strip()
    df["occupation_title"] = df["occupation_title"].astype(str).str.strip()

    df = df.dropna(subset=["occupation_code", "occupation_title", "ai_exposure"])

    df.to_csv(AIOE_CLEAN, index=False)

    print(df.head())
    print("Saved AIOE clean data")

if __name__ == "__main__":
    main()
