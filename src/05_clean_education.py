import pandas as pd

xlsx = pd.ExcelFile("data/raw/education.xlsx")

print("Sheet names:", xlsx.sheet_names)

for sheet in xlsx.sheet_names:
    print("\n---", sheet, "---")
    test = pd.read_excel(
        "data/raw/education.xlsx",
        sheet_name=sheet,
        nrows=10,
        header=None
    )
    print(test)
