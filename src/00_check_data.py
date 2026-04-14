import pandas as pd
from pathlib import Path

data_path = Path("data/raw")

files = [
    "aioe.xlsx",
    "employment.csv",
    "employment.xlsx",
    "earnings.xlsx",
    "labour_demand.xlsx",
    "vacancies_bonus.csv",
]

def try_read(file_path):
    if file_path.suffix.lower() == ".csv":
        for enc in ["utf-8", "latin1", "cp1252", "utf-8-sig"]:
            try:
                df = pd.read_csv(file_path, encoding=enc)
                return df, f"csv with encoding={enc}"
            except Exception:
                pass
        raise RuntimeError("Could not read CSV with common encodings")

    if file_path.suffix.lower() in [".xlsx", ".xls"]:
        xls = pd.ExcelFile(file_path)
        return xls, "excel workbook"

    raise RuntimeError("Unsupported file type")

print("Running data check...")

for file in files:
    file_path = data_path / file

    if not file_path.exists():
        continue

    print("\n==========================")
    print(f"FILE: {file}")
    print("==========================")

    try:
        obj, method = try_read(file_path)
        print(f"\nRead method: {method}")

        if isinstance(obj, pd.ExcelFile):
            print("\nSheet names:")
            print(obj.sheet_names)
            first_sheet = obj.sheet_names[0]
            df = pd.read_excel(file_path, sheet_name=first_sheet)
            print(f"\nPreview of first sheet: {first_sheet}")
            print(df.head())
            print("\nColumns:")
            print(df.columns.tolist())
            print("\nShape:")
            print(df.shape)
        else:
            df = obj
            print("\nColumns:")
            print(df.columns.tolist())
            print("\nFirst 5 rows:")
            print(df.head())
            print("\nShape:")
            print(df.shape)

    except Exception as e:
        print(f"Could not read file: {e}")
