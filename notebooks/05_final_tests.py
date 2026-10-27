"""Step 6: End-to-end tests on unusual and tricky inputs.

Checks that the full system (category + sentiment + urgency) never crashes
and shows how it behaves on edge cases. Results go in the report.

Run:  .venv/bin/python notebooks/05_final_tests.py
"""
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))
from src.analyzer import analyze_ticket  # noqa: E402

pd.set_option("display.width", 220)
pd.set_option("display.max_colwidth", 55)

# 1. Inputs that must be REJECTED with a friendly message (not a crash)
print("1. Invalid inputs")
for text in ["", "   ", "hi", None]:
    try:
        analyze_ticket(text)
        print(f"  FAIL  {text!r} was accepted")
    except ValueError as err:
        print(f"  PASS  {text!r:8} -> rejected: {err}")

# 2. Edge cases: must not crash; we record what happens
cases = [
    ("Normal", "I want a refund for my broken headphones"),
    ("ALL CAPS + !!!", "MY ACCOUNT HAS BEEN HACKED!!! HELP"),
    ("Emoji", "Still no refund 😡😡 this is ridiculous"),
    ("Numbers only", "12345 67890"),
    ("Not English", "Quiero un reembolso de mi pedido"),
    ("Greeting only", "hello there"),
    ("HTML/code", "<script>alert(1)</script> where is my invoice"),
    ("Very long", "My order is late. " * 150),
    ("Typos", "i cnat acess my acount pls hlep"),
    ("Negation", "I was not charged twice, I just want to check my invoice"),
    ("Resolved issue", "Thanks, my issue is resolved now"),
    ("Sarcasm", "Great, another late delivery. Just perfect."),
    ("Calm but serious", "Someone else is using my account without my permission"),
    ("Mixed topics", "I need a refund and also want to change my shipping address"),
]

rows = []
for name, text in cases:
    try:
        r = analyze_ticket(text)
        rows.append({"case": name, "text": text[:55], "category": r["category"],
                     "conf": r["confidence"], "review": r["needs_review"],
                     "sentiment": r["sentiment"], "urgency": r["urgency"],
                     "reason": r["urgency_reason"][:30]})
    except Exception as err:  # any crash is a bug
        rows.append({"case": name, "text": text[:55], "category": f"CRASH: {err}"})

print("\n2. Edge cases")
results = pd.DataFrame(rows)
print(results.to_string(index=False))

crashes = results["category"].astype(str).str.startswith("CRASH").sum()
print(f"\nCrashes: {crashes} of {len(cases)}")
results.to_csv(ROOT / "reports" / "edge_case_results.csv", index=False)
print("Saved to reports/edge_case_results.csv")
