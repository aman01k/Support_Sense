# Step 3 — Category Model: TF-IDF + Logistic Regression

Script: `notebooks/03_train_model.py` · Prediction helper: `src/predict.py`
Outputs: `models/category_model.joblib`, `reports/confusion_matrix.png`, `reports/metrics.txt`

## How it works
```
clean text ──► TF-IDF (text → numbers) ──► Logistic Regression ──► category + confidence
```
- **TF-IDF** gives each word a score: high if it's frequent in this message but rare across all messages. "refund" scores high; "the" scores low.
  - `ngram_range=(1,2)`: uses single words *and* word pairs, so "payment methods" is one feature.
  - `min_df=2`: ignores words seen in only one message (usually typos).
  - Vocabulary: **4,823 features**.
- **Logistic Regression** learns a weight for every word per category, then turns the scores into probabilities (which add up to 100%).
  - `class_weight="balanced"`: gives small classes (CANCEL, 4%) as much importance as big ones (ACCOUNT, 21.5%).
- Both steps are wrapped in a **Pipeline**, so TF-IDF is fitted on the training set only (no data leakage) and saved as one file.

## Results (4,756 unseen test messages)
| Model | Accuracy | Macro F1 |
|---|---|---|
| **Logistic Regression (chosen)** | **0.996** | **0.997** |
| Linear SVM | 0.998 | 0.998 |

- Every category has precision and recall ≥ 0.987.
- Only **17 mistakes** out of 4,756. Most are heavy typos: "paymdnt", "invooce", "requestreimbursements", "contactingassistant".
- Confusion matrix: almost everything sits on the diagonal. The few errors involve ORDER, PAYMENT and ACCOUNT, which share words like "order", "account" and "help".

## Why Logistic Regression, not SVM?
The SVM scores 0.2% higher, but it gives no **probability**. Logistic Regression tells us *how sure* it is, which we use for the confidence check below. A 0.2% difference is about 10 messages out of 4,756, so it's not worth losing that.

## What the model learned (top words)
| Category | Strongest words |
|---|---|
| REFUND | refund, reimbursement, money, rebate |
| CONTACT | customer, agent, contact, person, speak |
| INVOICE | bill, invoice, invoices, download |
| SHIPPING | address, shipping address, delivery address |
| SUBSCRIPTION | newsletter, subscription, unsubscribe |

These make sense, which shows the model learned real signals, not noise.

## Limitation found → confidence check
*"I've been charged twice for my subscription!"* is predicted **ACCOUNT with only 21% confidence**. "charged" and "twice" appear only once in training, and in Bitext "SUBSCRIPTION" means the *newsletter*, not a paid plan.

**Fix:** if confidence < 50%, the ticket is marked **"Needs manual review"** instead of trusting the guess.
- Test set: 74 of 4,756 tickets fall below 50%.
- Accuracy on confident tickets: **99.9%**. On low-confidence tickets: **82.4%**, so flagging them is worthwhile.

## Viva notes
- **Why is accuracy 99.6%? Isn't that suspicious?** We removed duplicates and fitted TF-IDF on train only, so it's not leakage. Bitext messages are template-generated, so wording per category is very consistent. Real tickets would score lower; the confidence check is our safety net.
- **Accuracy vs F1:** accuracy can hide a weak small class. Macro F1 averages F1 over all 11 categories equally, so CANCEL counts as much as ACCOUNT.
- **Precision:** of tickets predicted as X, how many really were X.
- **Recall:** of real X tickets, how many we found.
- **Why not BERT?** It's slower, harder to explain, and we already have 99.6%. Nothing to gain on this data.
