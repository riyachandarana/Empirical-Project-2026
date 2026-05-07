import pandas as pd
from difflib import get_close_matches

# Merge scraped BLS outlook data with main analysis dataset
# using fuzzy name matching to align occupation names

df = pd.read_csv("data/processed/final_analysis_data.csv")
scraped = pd.read_csv("data/raw/bls_outlook_scraped.csv")

scraped_names = scraped["occupation_name_bls"].str.lower().tolist()

results = []
for _, row in df.iterrows():
    name = row["occupation_name"].lower()
    matches = get_close_matches(name, scraped_names, n=1, cutoff=0.6)
    if matches:
        matched = matches[0]
        outlook = scraped[
            scraped["occupation_name_bls"].str.lower() == matched
        ]["bls_outlook"].values[0]
        results.append({
            "occupation_name": row["occupation_name"],
            "bls_outlook": outlook
        })
    else:
        results.append({
            "occupation_name": row["occupation_name"],
            "bls_outlook": None
        })

outlook_df = pd.DataFrame(results)

# Merge back into main dataset
df_merged = df.merge(outlook_df, on="occupation_name", how="left")

# Save
df_merged.to_csv("data/processed/final_analysis_data_with_outlook.csv",
                 index=False)

print(f"Merged dataset saved.")
print(f"Matched: {df_merged['bls_outlook'].notna().sum()} of {len(df_merged)}")
print(df_merged["bls_outlook"].value_counts())
