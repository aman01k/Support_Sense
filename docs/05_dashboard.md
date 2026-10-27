# Step 5 — Streamlit Dashboard

Run (from the `SupportSense` folder):
```
.venv/bin/streamlit run streamlit_app.py
```
Opens at http://localhost:8501

## Files
| File | Job |
|---|---|
| `streamlit_app.py` | The user interface |
| `src/analyzer.py` | `analyze_ticket(text)`: runs all three features on one message |
| `src/storage.py` | Saves/loads tickets in `data/tickets.csv` |
| `src/predict.py`, `src/sentiment.py`, `src/urgency.py` | The three features from Phases 3–4 |

## What the app does
1. **Analyze a ticket:** type a message (or click an example) → **Analyze ticket**. Shows:
   - Category + confidence bar
   - Urgency + the reason (e.g. `money: charged twice`)
   - Sentiment + VADER score
   - A **"Needs manual review"** warning if category confidence < 50%
2. **Every analysed ticket is saved** to `data/tickets.csv`.
3. **Dashboard:**
   - KPI cards: total tickets, High priority, % negative, needs review
   - Bar charts: tickets by category, urgency, sentiment
   - Ticket table sorted **High urgency first, then newest**, with coloured badges
   - Filters: urgency, sentiment, category, text search, "needs review only"
   - Download the filtered table as CSV
4. **Sidebar:** *Add 20 sample tickets* (for the demo) and *Clear all tickets*.

## Input handling
- Empty or one-word messages show a warning instead of crashing (`MIN_WORDS = 2` in `analyzer.py`).
- The model is loaded once and reused, not reloaded on every click.

## Architecture (for the report)
```
             ┌──────────────── streamlit_app.py ────────────────┐
 message ──► │ analyze_ticket()                                  │
             │   ├─ clean_text → TF-IDF → LogReg → category      │
             │   ├─ VADER                       → sentiment      │
             │   └─ keyword rules + sentiment   → urgency        │
             │ save_tickets() → data/tickets.csv                 │
             │ load_tickets() → KPIs, charts, filtered table     │
             └───────────────────────────────────────────────────┘
```

## Demo script for the viva (2 minutes)
1. Click **Clear all tickets**, then **Add 20 sample tickets**: the dashboard fills up.
2. Click the **Double charge** example → Analyze. Show: High urgency (reason `money: charged twice`), Negative, and the **Needs manual review** warning (27% confidence, because "charged twice" barely appears in training data). This shows the system knows when it's unsure.
3. Click **Hacked account** → High (`security: hacked`).
4. Click **Question** → Low, Neutral, PAYMENT with high confidence.
   - Know this one in advance: **Late delivery** is predicted ACCOUNT, which is wrong, but at 28% confidence it gets flagged for review. Bitext delivery messages are phrased like "how long does delivery take", not complaints.
5. In the table, filter **Urgency = High**: these are what an agent handles first.
6. Type an empty message → warning, no crash.

## Viva notes
- **Why Streamlit?** Pure Python, no HTML/JS, and it's quick to build a working UI for an ML model.
- **Why CSV instead of a database?** It's enough for a demo, needs zero setup, and you can open it in Excel. A real system would use SQLite or PostgreSQL.
- **Why sort High first?** The whole point of the project: agents should see urgent tickets before routine questions.
