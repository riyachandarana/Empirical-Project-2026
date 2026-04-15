# Does AI exposure reward high-skill work? Evidence from US labour markets

## Research Question 
To what extent is occupation level AI exposure associated with wages in the US labour market, after accounting for skill differences and what does this imply about whether AI complements or subsitutes labour?

## Overview

Recent advances in AI are expected to reshape labour markets, but their impacts may differ across occupations depending on task content. This project examines whether occupations with higher exposure to AI exhibit different wage levels, employment patters and labour demand. 

Using occupation level measures of AI exposure combined with US labour market data with analysis focuses on cross sectional relationships between exposure and economic outcomes. Importantly AI exposure reflects the susceptibility of occupational takss to current AI capabilities rather than realised adoption. 

The empirical approach is descriptive and associative rathaer than causal but aims to provide evidence on whether Ai is more likely to complement high skill labour or subsitute it.

---

## Research outcome focus

1. Wages - tests whether AI exposure is associated with higher returns to labour consistent with skill biased or task biased technological change
2. Employment - examines whether AI exposed occupations are relatively larger or smaller providing evidence on potential displacement effects
3. Labour demand - captures whether AI exposed occupations exhibit stronger hiring demand which may indicate complementarity rather than subsitution

## Working Hypothesis 

Occupations with higher AI exposure are expected to exhibit higher wages reflecting a concentration of AI exposed tasks in cognitive and high skill roles. however the relationship with employment and labour demand is ambigious, as AI may both augment productivity and displace routine labour depending on task composition 

## Key Findings 
- AI exposure is strongly positively associated with wages  
- A one-unit increase in AI exposure is associated with increases wages approximately by ~22%  
- AI exposure has only a weak relationship with employment  

These findings are consistent with AI acting as a complement to high skill labour potentially reinforcing existing wage inequality across ocupation 

## Methodology
The analysis is conducted at the occupation level using cross-sectional regression models. The baseline specification is:

log(wage)_i = β₀ + β₁ AI_exposure_i + ε_i

where AI exposure is measured using occupation-level indices and wages are measured as median annual earnings.

To account for confounding factors, extended specifications include controls for occupation characteristics such as:
	•	education requirements
	•	occupational group fixed effects
	•	employment size

All results are interpreted as associations rather than causal effects

---
## Website Link 



## Data Sources

### 1. AI Exposure (AIOE Dataset)
- Source: AI Occupation Exposure dataset
- Used: Appendix A (occupation-level scores)
- Variable:
  - `ai_exposure`: degree to which occupations are exposed to AI

### 2. Labour Market Data (BLS OEWS)
- Source: US Bureau of Labor Statistics
- Variables:
  - `OCC_CODE` → occupation code
  - `OCC_TITLE` → occupation name
  - `TOT_EMP` → employment
  - `A_MEDIAN` → median annual wage

### Matching

Datasets are merged using **SOC occupation codes**, ensuring consistency across sources.

---

## Project Structure
