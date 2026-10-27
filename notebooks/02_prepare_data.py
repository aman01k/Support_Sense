"""Step 2: Clean the data and split it into training and testing sets.

Run:  .venv/bin/python notebooks/02_prepare_data.py
Output: data/processed/train.csv and data/processed/test.csv
"""
import sys
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))
from src.preprocessing import clean_text  # noqa: E402

RAW = ROOT / "data" / "raw" / "bitext.csv"
OUT = ROOT / "data" / "processed"
OUT.mkdir(parents=True, exist_ok=True)

# 1. Load and keep only the columns we need
df = pd.read_csv(RAW)[["instruction", "category"]]
df = df.rename(columns={"instruction": "text"})
print("Loaded:", len(df))

# 2. Clean the text
df["clean_text"] = df["text"].apply(clean_text)

# 3. Remove empty messages (can happen after removing placeholders)
df = df[df["clean_text"].str.len() > 0]
print("After removing empty:", len(df))

# 4. Remove messages that appear with MORE THAN ONE category (conflicting labels)
labels_per_text = df.groupby("clean_text")["category"].nunique()
conflicting = labels_per_text[labels_per_text > 1].index
df = df[~df["clean_text"].isin(conflicting)]
print("Conflicting texts removed:", len(conflicting))

# 5. Remove duplicate messages so the same sentence can't be in both train and test
df = df.drop_duplicates(subset="clean_text")
print("After removing duplicates:", len(df))

# 6. Stratified 80/20 split: each category keeps the same proportion in train and test
train, test = train_test_split(
    df, test_size=0.2, stratify=df["category"], random_state=42
)
print(f"\nTrain: {len(train)}   Test: {len(test)}")

# 7. Check that the split kept the class proportions
check = pd.DataFrame({
    "train_%": train["category"].value_counts(normalize=True).mul(100).round(1),
    "test_%": test["category"].value_counts(normalize=True).mul(100).round(1),
})
print("\nCategory share in train vs test:\n", check)

# 8. Save
train.to_csv(OUT / "train.csv", index=False)
test.to_csv(OUT / "test.csv", index=False)
print("\nSaved to", OUT)

# Before/after examples for the report
print("\nCleaning examples:")
for _, row in df.sample(5, random_state=7).iterrows():
    print(f"  {row['text']!r}\n  -> {row['clean_text']!r}")
