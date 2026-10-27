# Step 2 — Data Preparation & Train/Test Split

Script: `notebooks/02_prepare_data.py` · Cleaning function: `src/preprocessing.py`

## Pipeline
| Step | Rows after |
|---|---|
| Load `instruction` + `category` | 26,872 |
| Clean text | 26,872 |
| Remove empty messages | 26,872 |
| Remove conflicting labels (same text, different category) | 26,872 (none found) |
| Remove duplicates | **23,776** |
| Stratified 80/20 split | **Train 19,020 · Test 4,756** |

Output files: `data/processed/train.csv`, `data/processed/test.csv`
(columns: `text`, `category`, `clean_text`)

## What cleaning does
1. Lowercase: "Refund" and "refund" become the same word.
2. Remove placeholders like `{{Order Number}}`: they're template filler, not real words.
3. Remove numbers like `#12588`: order numbers carry no category meaning.
4. Collapse extra spaces.

Example: `"i have to find my invoice #12588 how todo it"` → `"i have to find my invoice how todo it"`

## What cleaning does NOT do (and why)
- **No stop-word removal:** it would delete "not", "can't", "no". *"I can pay"* and *"I can't pay"* mean opposite things.
- **No typo fixing:** real customers make typos; the model learns from them.
- **No stemming/lemmatization:** messages are short and TF-IDF with word pairs works well without it. Fewer steps, easier to explain.

## Viva notes
- **Why remove duplicates?** If the same sentence is in train and test, the model is tested on something it memorised. That inflates the score (a form of *data leakage*). 2,237 exact duplicates existed; cleaning merged a few more (3,096 removed in total).
- **Why stratified split?** Categories are imbalanced (ACCOUNT 21.5%, CANCEL 4%). Stratifying keeps the same proportions in train and test, so every category is fairly tested.
- **Why 80/20?** Standard choice: enough data to learn from, enough held back to test fairly.
- **Why `random_state=42`?** Makes the split reproducible: same split every run.
- **Why a shared `clean_text` function?** The app must clean new tickets exactly the way training data was cleaned, or predictions get worse.
- **Data leakage rule:** the TF-IDF vectorizer (Phase 3) will be fitted on **train only**, never on test.
