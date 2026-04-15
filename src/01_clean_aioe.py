import pandas as pd
from config import AIOE_RAW, AIOE_CLEAN

def main():
    df = pd.read_excel(AIOE_RAW)

    print(df.columns)  # check structure

    # You may need to adjust column names after seeing output
    df = df.rename(columns={
        "occupation_title": "occupation_title",
        "ai_exposure": "ai_exposure"
    })

    # Keep only relevant columns
    df = df[["occupation_title", "ai_exposure"]].copy()

    df = df.dropna()

    df.to_csv(AIOE_CLEAN, index=False)

    print(df.head())
    print("Saved AIOE clean data")

if __name__ == "__main__":
    main()
