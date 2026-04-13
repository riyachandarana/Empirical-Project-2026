from pathlib import Path

# Project root
ROOT = Path(__file__).resolve().parents[1]

# Data folders
DATA_RAW = ROOT / "data" / "raw"
DATA_INTERIM = ROOT / "data" / "interim"
DATA_PROCESSED = ROOT / "data" / "processed"

# Output folders
OUTPUT = ROOT / "output"
FIGURES = OUTPUT / "figures"
TABLES = OUTPUT / "tables"

# Ensure directories exist
for folder in [DATA_RAW, DATA_INTERIM, DATA_PROCESSED, FIGURES, TABLES]:
    folder.mkdir(parents=True, exist_ok=True)

# Raw input files
AIOE_RAW = DATA_RAW / "aioe.csv"
EMPLOYMENT_RAW = DATA_RAW / "employment.csv"
EARNINGS_RAW = DATA_RAW / "earnings.csv"
LABOUR_DEMAND_RAW = DATA_RAW / "labour_demand.csv"

# Interim files
AIOE_CLEAN = DATA_INTERIM / "aioe_clean.csv"
EMPLOYMENT_CLEAN = DATA_INTERIM / "employment_clean.csv"
EARNINGS_CLEAN = DATA_INTERIM / "earnings_clean.csv"
LABOUR_DEMAND_CLEAN = DATA_INTERIM / "labour_demand_clean.csv"
CROSSWALK = DATA_INTERIM / "occupation_crosswalk.csv"
MERGED = DATA_PROCESSED / "merged_data.csv"
FEATURES = DATA_PROCESSED / "final_analysis_data.csv"
