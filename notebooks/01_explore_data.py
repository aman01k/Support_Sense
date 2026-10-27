"""Step 1: Download and explore the Bitext customer support dataset.

Run:  .venv/bin/python notebooks/01_explore_data.py
"""
from pathlib import Path

import pandas as pd
from datasets import load_dataset

RAW = Path(__file__).resolve().parent.parent / "data" / "raw" / "bitext.csv"

# 1. Download once and cache as CSV
if not RAW.exists():
    RAW.parent.mkdir(parents=True, exist_ok=True)
    ds = load_dataset("bitext/Bitext-customer-support-llm-chatbot-training-dataset", split="train")
    ds.to_pandas().to_csv(RAW, index=False)

df = pd.read_csv(RAW)

# 2. Shape and columns
print("Shape:", df.shape)
print("Columns:", list(df.columns))

# 3. Data quality
print("\nMissing values:\n", df.isna().sum())
print("\nDuplicate messages:", df.duplicated("instruction").sum())

# 4. Label distribution (our target = 'category')
print("\nCategory counts:\n", df["category"].value_counts())
print("\nNumber of intents:", df["intent"].nunique())

# 5. Message length (in words)
print("\nWords per message:\n", df["instruction"].str.split().str.len().describe())

# 6. A few examples
print("\nSamples:\n", df.sample(8, random_state=1)[["instruction", "category"]].to_string())
