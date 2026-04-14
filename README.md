# How AI Exposure Relates to Wages, Employment, and Labour Demand in the US Labour Market

## Research Question 
How is AI exposure associated with wages, employment, and labour demand across occupations in the US labour market?

## Overview

Some occupations appear more exposed to AI than others. But does that exposure line up with better pay, fewer workers, or stronger labour demand? By combining occupation-level measures of AI exposure with labour market data, this project examines how AI exposure is related to wages, employment, and job demand in the US.

Some occupations appear more exposed to AI than others. But does that exposure line up with better pay, fewer workers, or stronger labour demand? By combining occupation-level measures of AI exposure with labour market data, this project examines how AI exposure is related to wages, employment, and job demand in the US.

AI is often discussed as a major force reshaping work, but its relationship with pay, employment, and labour demand may differ sharply across occupations.

---

## Research outcome focus

1. Wages - tells us whether highly AI-exposed occupations tend to be better paid
2. Employment - tells us whether highly AI-exposed occupations are concentrated in larger or smaller occupations
3. Labour demand - this tells us whether highly AI-exposed occupations appear in stronger or weaker hiring demand.

## Working Hypothesis 

Occupations with higher AI exposure are likely to have higher wages on average, because many AI-exposed roles involve cognitive and professional tasks, but the relationship with employment and labour demand may be more mixed


---

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
