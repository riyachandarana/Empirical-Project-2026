# Does AI Reward High-Skill Work? Evidence from US Labour Markets

## Overview

This project investigates whether artificial intelligence (AI) is reshaping labour market outcomes across occupations.

Specifically, it examines whether occupations with higher exposure to AI:
- earn higher wages
- employ more or fewer workers

The analysis combines an occupation-level AI exposure index with US labour market data to explore how AI is associated with wages and employment.

---

## Research Question

Does AI exposure increase wages and employment across occupations?

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
