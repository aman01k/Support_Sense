# If they ask to see the code

**Rule:** start from `src/analyzer.py`. It’s 33 lines and shows the whole system: one message goes in, three features run, one result comes out. Every other file is one of the three branches.

---

## Before the viva
- Open the `SupportSense` folder in your editor (e.g. VS Code) and zoom in (Cmd +) so the code is readable on a projector.
- Pre-open these tabs, in this order:
  1. `src/analyzer.py`
  2. `src/preprocessing.py`
  3. `notebooks/03_train_model.py`
  4. `src/predict.py`
  5. `src/urgency.py`
  6. `src/sentiment.py`
  7. `streamlit_app.py`
- To jump to a line: **Ctrl+G** in VS Code, then type the line number.
- Don't scroll through whole files. Jump to the lines below and explain only those.

---

## The 3-minute code tour (if they say "walk us through the code")

| # | File : lines | What to point at | What to say |
|---|---|---|---|
| 1 | [src/analyzer.py:14-33](../../src/analyzer.py) | `analyze_ticket()` | "This is the heart of the system. It checks the input, then calls our three features: `predict_category`, `analyze_sentiment` and `detect_urgency`, and returns one result." |
| 2 | [src/preprocessing.py:9-18](../../src/preprocessing.py) | the three `re.sub` lines | "Our cleaning: lowercase, remove `{{placeholders}}`, remove numbers, collapse spaces. No stop-word removal, so 'not' survives. The same function is used in training and in the app." |
| 3 | [notebooks/03_train_model.py:45-59](../../notebooks/03_train_model.py) | `TfidfVectorizer(...)`, `Pipeline([...])`, `model.fit` | "TF-IDF with word pairs and `min_df=2`, then Logistic Regression with balanced class weights. Both are in one Pipeline, so `fit` learns TF-IDF from training data only, with no leakage." |
| 4 | [notebooks/03_train_model.py:126](../../notebooks/03_train_model.py) | `joblib.dump(...)` | "The trained Pipeline is saved as one file, which the app loads." |
| 5 | [src/predict.py:13, 25-35](../../src/predict.py) | `CONFIDENCE_THRESHOLD = 0.5`, `predict_proba` | "In the app we clean the text, get probabilities, take the highest, and flag the ticket for review if it's below 50%." |
| 6 | [src/urgency.py:41-65](../../src/urgency.py) | the `# Rule 1` … `# Rule 5` comments | "Urgency is five rules in order. The first match returns, always with a reason." |
| 7 | [src/sentiment.py:15-28](../../src/sentiment.py) | the two thresholds | "VADER gives a compound score; we turn it into a label with these thresholds. Positive needs 0.5 because polite words push scores up." |
| 8 | [streamlit_app.py:70-85](../../streamlit_app.py) | the form, `analyze_ticket(text)`, `save_tickets` | "The dashboard: when you click Analyze, it calls the same `analyze_ticket` and saves the result to a CSV file." |

---

## If they ask a specific question

| They ask… | Open | Show |
|---|---|---|
| "Where do you preprocess the text?" | `src/preprocessing.py` | lines 9-18 |
| "Show me how you removed duplicates / split the data" | `notebooks/02_prepare_data.py` | line 39 (`drop_duplicates`), lines 43-45 (`train_test_split` with `stratify` and `random_state=42`) |
| "Where is TF-IDF?" / "What parameters?" | `notebooks/03_train_model.py` | lines 45-51 |
| "Where is the model trained?" | `notebooks/03_train_model.py` | lines 53-59 |
| "How did you evaluate it?" | `notebooks/03_train_model.py` | line 66 (`classification_report`), plus the image `reports/confusion_matrix.png` |
| "How did you compare with SVM?" | `notebooks/03_train_model.py` | line 71 |
| "How does the confidence check work?" | `src/predict.py` | lines 13 and 25-35 |
| "Show the urgency keywords" | `src/urgency.py` | lines 10-29 (`HIGH_KEYWORDS`, `MEDIUM_KEYWORDS`) |
| "How is urgency decided?" | `src/urgency.py` | lines 41-65 |
| "How is sentiment done?" | `src/sentiment.py` | lines 15-28 |
| "How does the app handle empty input?" | `src/analyzer.py` | lines 11-17 (`MIN_WORDS`, `ValueError`) |
| "Where are tickets stored?" | `src/storage.py` | lines 16-35, and the file `data/tickets.csv` |
| "Show the dashboard code" | `streamlit_app.py` | lines 70-85 (input form), line 117 onward (dashboard) |
| "How do you know it doesn't crash?" | `notebooks/05_final_tests.py` | the `cases` list; run it live (below) |

---

## Proof in the terminal (if they want to see it run)
From the `SupportSense` folder:

**Analyze any message they suggest:**
```bash
.venv/bin/python -c "from src.analyzer import analyze_ticket; print(analyze_ticket('My account was hacked'))"
```

**Re-run the model evaluation** (about 10 seconds):
```bash
.venv/bin/python notebooks/03_train_model.py
```

**Re-run the edge-case tests:**
```bash
.venv/bin/python notebooks/05_final_tests.py
```

---

## Tips
- **Show, don't read.** Point at a line and say what it does in one sentence.
- **Know who wrote what.** If Shashwat built the dashboard, he should explain `streamlit_app.py`.
- **If you don't know a line:** say what the block does as a whole, e.g. "this part builds the table display", rather than guessing.
