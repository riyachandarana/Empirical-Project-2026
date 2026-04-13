# Does AI reward the rich? Evidence from US labour markets

## Overview
This project examines whether US occupations with higher AI exposure show different patterns in wages and different employment levels using the AIOE occupation-level AI exposure index and BLS Occupational Employment and Wage Statistics

## Repository contents
- `blog.ipynb` or `blog.qmd`: final project write-up
- `src/`: cleaning, merging, modelling, and figure scripts
- `data/`: raw, interim, and processed data
- `output/`: generated figures and tables

## Data sources
Place the raw files in:
- `data/raw/aioe.csv`
- `data/raw/employment.csv`
- `data/raw/earnings.csv`
- `data/raw/labour_demand.csv`

## How to replicate
1. Install dependencies:
   `pip install -r requirements.txt`

2. Run the scripts in order:
   `python src/01_clean_aioe.py`
   `python src/02_clean_employment.py`
   `python src/03_clean_earnings.py`
   `python src/04_clean_labour_demand.py`
   `python src/05_build_crosswalk.py`
   `python src/06_merge_data.py`
   `python src/07_features.py`
   `python src/08_regression.py`
   `python src/09_ml.py`
   `python src/10_figures.py`

## Final output
Include the link to the rendered blog or web version here.
