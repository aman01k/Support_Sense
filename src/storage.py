"""Very simple ticket storage: one CSV file, one row per analysed ticket."""
from datetime import datetime
from pathlib import Path

import pandas as pd

TICKETS_FILE = Path(__file__).resolve().parent.parent / "data" / "tickets.csv"

COLUMNS = [
    "ticket_id", "created_at", "text", "category", "confidence", "needs_review",
    "sentiment", "sentiment_score", "urgency", "urgency_reason",
]
URGENCY_ORDER = ["High", "Medium", "Low"]


def load_tickets() -> pd.DataFrame:
    if not TICKETS_FILE.exists():
        return pd.DataFrame(columns=COLUMNS)
    df = pd.read_csv(TICKETS_FILE, parse_dates=["created_at"])
    # Sort: High first, then newest first
    df["urgency"] = pd.Categorical(df["urgency"], categories=URGENCY_ORDER, ordered=True)
    return df.sort_values(["urgency", "created_at"], ascending=[True, False])


def save_tickets(results: list[dict]) -> None:
    """Append analysed tickets to the CSV file."""
    existing = load_tickets()
    next_id = int(existing["ticket_id"].max()) + 1 if len(existing) else 1
    now = datetime.now().replace(microsecond=0)
    rows = pd.DataFrame(results)
    rows.insert(0, "created_at", now)
    rows.insert(0, "ticket_id", range(next_id, next_id + len(rows)))
    rows = rows[COLUMNS]
    rows.to_csv(TICKETS_FILE, mode="a", header=not TICKETS_FILE.exists(), index=False)


def clear_tickets() -> None:
    TICKETS_FILE.unlink(missing_ok=True)
