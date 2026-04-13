python 
from __future__ import annotations 
import re 
from pathlib import Path
from typing import Iterable 

import pandas as pd 

def snake_case_columns(df: pd.DataFrame) -> pd.DataFrame:
  df = df.copy()
  df.columns = [
    red.sub(r"[^a-z0-9]+", "-", c.strip().lower()).strip("_")
    for c in df.columns 
  ]
  return df 

def read_table(path: Path) -> pd.DataFrame: 
  suffix = path.suffix.lower()
  if suffix == ".csv":
    return pd.read_csv(path)
  if suffix in {".xlsx", ".xls"}:
    return pd.read_excel(path)
  raise ValueError(f"Unsupported file type: {path}")
  
      
