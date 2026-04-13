import pandas as pd
from pathlib import Path

data_path = Path("data/raw")

files = [
    "aioe.csv",
    "employment.csv",
    "earnings.csv",
    "labour_demand.csv",
    "vacancies.csv",  # optional
]

for file in files:
    file_path = data_path / file

    print("\n==========================")
    print(f"FILE: {file}")
    print("==========================")

    if not file_path.exists():
        print("File not found, skipping.")
        continue

    try:
        if file_path.suffix.lower() == ".csv":
            df = pd.read_csv(file_path)
        elif file_path.suffix.lower() in [".xlsx", ".xls"]:
            df = pd.read_excel(file_path)
        else:
            print("Unsupported file type, skipping.")
            continue

        print("\nColumns:")
        print(df.columns.tolist())

        print("\nFirst 5 rows:")
        print(df.head())

        print("\nShape:")
        print(df.shape)

    except Exception as e:
        print(f"Could not read file: {e}")
