import pandas as pd

def clean(x):
    x = str(x).lower()
    x = x.replace(",", "")
    x = x.replace(" and ", " ")
    x = x.replace("-", " ")
    x = x.replace("(", "").replace(")", "")
    return x.strip()

aioe = pd.read_csv("data/interim/aioe_clean.csv")
emp = pd.read_csv("data/interim/employment_clean.csv")
earn = pd.read_csv("data/interim/earnings_clean.csv")

aioe["occ_clean"] = aioe["occupation_title_us"].apply(clean)
emp["occ_clean"] = emp["occupation_name"].apply(clean)
earn["occ_clean"] = earn["occupation_name"].apply(clean)

aioe.to_csv("data/interim/aioe_clean.csv", index=False)
emp.to_csv("data/interim/employment_clean.csv", index=False)
earn.to_csv("data/interim/earnings_clean.csv", index=False)

print("Done")
