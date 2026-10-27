"""Step 4: Test sentiment analysis (VADER) and rule-based urgency detection.

Bitext has no sentiment/urgency labels, so we check both features on a small
hand-labelled set: data/eval/manual_samples.csv (36 messages we labelled ourselves).

Run:  .venv/bin/python notebooks/04_sentiment_urgency.py
"""
import sys
from pathlib import Path

import pandas as pd
from sklearn.metrics import accuracy_score, classification_report

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))
from src.sentiment import analyze_sentiment  # noqa: E402
from src.urgency import detect_urgency  # noqa: E402

pd.set_option("display.width", 200)
pd.set_option("display.max_colwidth", 70)

# 1. Run both features on the hand-labelled messages
df = pd.read_csv(ROOT / "data" / "eval" / "manual_samples.csv")
sent = df["text"].apply(analyze_sentiment)
df["sentiment"] = sent.str["sentiment"]
df["score"] = sent.str["score"]
urg = [detect_urgency(t, s) for t, s in zip(df["text"], df["score"])]
df["urgency"] = [u["urgency"] for u in urg]
df["reason"] = [u["reason"] for u in urg]

# 2. Sentiment results
print(f"SENTIMENT accuracy: {accuracy_score(df.expected_sentiment, df.sentiment):.2f}")
print(classification_report(df.expected_sentiment, df.sentiment, zero_division=0))

# 3. Urgency results (High recall matters most: we must not miss urgent tickets)
print(f"URGENCY accuracy: {accuracy_score(df.expected_urgency, df.urgency):.2f}")
print(classification_report(df.expected_urgency, df.urgency, zero_division=0))
print(pd.crosstab(df.expected_urgency, df.urgency, rownames=["expected"], colnames=["predicted"]))

# 4. Mistakes
wrong = df[(df.sentiment != df.expected_sentiment) | (df.urgency != df.expected_urgency)]
print(f"\nMessages with a mistake: {len(wrong)} of {len(df)}")
print(wrong[["text", "expected_sentiment", "sentiment", "expected_urgency", "urgency", "reason"]]
      .to_string(index=False))

# 5. What the rules say about the whole Bitext test set (no labels, just the distribution)
test = pd.read_csv(ROOT / "data" / "processed" / "test.csv")
scores = test["text"].apply(lambda t: analyze_sentiment(t)["score"])
test["sentiment"] = test["text"].apply(lambda t: analyze_sentiment(t)["sentiment"])
test["urgency"] = [detect_urgency(t, s)["urgency"] for t, s in zip(test["text"], scores)]
print("\nBitext test set — sentiment share (%):")
print(test["sentiment"].value_counts(normalize=True).mul(100).round(1).to_string())
print("\nBitext test set — urgency share (%):")
print(test["urgency"].value_counts(normalize=True).mul(100).round(1).to_string())
