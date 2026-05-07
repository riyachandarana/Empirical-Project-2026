#!/bin/bash
set -e

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running pipeline..."
python src/00_scrape_bls_outlook.py
python src/01b_merge_outlook.py
python src/01_clean_aioe.py
python src/02_clean_employment.py
python src/03_clean_earnings.py
python src/04_clean_labour_demand.py
python src/05_clean_education.py
python src/06_build_crosswalk.py
python src/07_standardise_names.py
python src/08_merge_data.py
python src/09_features.py
python src/10_regression.py
python src/11_random_forest.py
python src/12_figures.py

echo "Rendering blog..."
quarto render blog.qmd --to html
cp blog.html index.html

echo "Done. Open index.html to view the blog."
