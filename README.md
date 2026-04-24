# Does AI exposure reward high-skill work? 
### Evidence from US labour markets

## Research Question 
To what extent is occupation-level AI exposure associated with wages in the US labour market, after accounting for skill differences? What does this imply about whether AI complements or substitutes labour?

## Overview

Recent advances in AI are expected to reshape labour markets, but their impacts may differ across occupations depending on task content. This project examines whether occupations with higher exposure to AI exhibit different wage levels, employment patterns and labour demand. 

The analysis combines an occupation-level AI exposure index with US labour market data from the Bureau of Labor Statistics and education requirements from the National Employment Matrix. The empirical approach is cross-sectional and focuses on identifying associations rather than causal effects.

Importantly, AI exposure reflects the susceptibility of occupational tasks to current AI capabilities rather than realised adoption. The goal is to assess whether AI is more closely associated with high-skill complementarity or labour substitution.

---

## Research outcome focus

- Wages:Tests Whether AI exposure is associated with higher returns to labour consistent with skill-biased or task-biased technological change
- Employment: Examines whether AI-exposed occupations are relatively larger or smaller providing evidence on potential displacement effects
- Labour demand: Captures whether AI-exposed occupations exhibit stronger hiring demand which may indicate complementarity rather than substitution

## Working Hypothesis 

Occupations with higher AI exposure are expected to exhibit higher wages reflecting a concentration of AI exposed tasks in cognitive and high-skill roles. The relationship with employment and labour demand is ambiguous, as AI may both augment productivity and displace routine labour depending on task composition 

## Key Findings

- In raw comparisons, occupations with higher AI exposure tend to have higher wages.
- Once occupational skill is controlled for, the wage effect becomes much smaller and often statistically insignificant.
- AI exposure remains positively associated with employment levels across occupations.
- There is no robust relationship between AI exposure and labour demand once controls are included.

These results suggest that AI is concentrated in already high-skill, high-paying occupations rather than independently raising wage returns.

## Methodology
The analysis is conducted at the occupation level using cross-sectional regression models. The baseline specification is:

log(wage)_i = β₀ + β₁ AI_exposure_i + ε_i

where AI exposure is measured using occupation-level indices and wages are measured as median annual earnings.

To account for confounding factors, extended specifications include controls for occupation characteristics such as:
	- education requirements
	- occupational group fixed effects
	- employment size

All results are interpreted as associations rather than causal effects

---

## Data Sources

1. AI Exposure (AIOE Dataset)

Source: AI Occupation Exposure dataset
Variable:
ai_exposure: degree to which occupations are exposed to AI

2. Labour Market Data (BLS OEWS)

Source: US Bureau of Labor Statistics
Variables:
- OCC_CODE: occupation code
- OCC_TITLE: occupation name
- TOT_EMP: employment
- A_MEDIAN: median annual wage

3. Labour Demand (Employment Projections)

Source: BLS National Employment Matrix
Variable:
- occupational openings as a proxy for labour demand

4. Education (Skill Proxy)

Source: BLS education requirements
Variable:
- education_required converted into an ordinal skill measure

### Data Matching

All datasets are harmonised using SOC occupation codes to ensure consistency across sources. 

### Pipeline

The project follows a structured pipeline:

1. Clean each source dataset
2. Build and apply the occupation crosswalk
3. Merge datasets into a unified occupation-level file
4. Construct derived variables such as log pay, employment, and advert intensity
5. Run regression analysis
6. Produce figures and final outputs

---
## Project Structure

- `data/raw/` raw source files
- `data/interim/` cleaned intermediate files
- `data/processed/` merged and final datasets
- `output/tables/` regression outputs
- `src/` cleaning, merging, feature construction, and modelling scripts
- `blog.ipynb` notebook used to generate the website
- `index.html` rendered website for GitHub Pages

## How to Replicate
## Data Setup

Raw data files are not included due to size and licensing constraints.

To replicate the analysis, download:

- AI Occupation Exposure dataset (AIOE)
- BLS OEWS employment and earnings data (May 2023)
- BLS National Employment Matrix (labour demand and education)

Place all files in:

data/raw/

File names must match those used in the scripts (e.g. aioe.xlsx, employment.xlsx).

### Run the data pipeline

Run the following scripts in order:

python src/01_clean_aioe.py
python src/02_clean_employment.py
python src/03_clean_earnings.py
python src/04_clean_labour_demand.py
python src/05_clean_education.py
python src/05_build_crosswalk.py
python src/07_merge_data.py
python src/08_features.py
python src/09_regression.py

Then generate the website:

jupyter nbconvert --to html --execute blog.ipynb --output index

## Website Link
https://riyachandarana.github.io/Empirical-Project-2026/

### Notes 
The analysis is cross-sectional and doesn't identify causal effects. AI exposure reflects task susceptibility rather than realised adoption, and labour demand is measured using projected openings rather than real time hiring data.
