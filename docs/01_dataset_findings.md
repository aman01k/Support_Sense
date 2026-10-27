# Step 1 — Dataset Selection

## Chosen: Bitext Customer Support Dataset
Source: Hugging Face `bitext/Bitext-customer-support-llm-chatbot-training-dataset`

| Column | Meaning | Used? |
|---|---|---|
| `instruction` | Customer's message | **Yes — input text** |
| `category` | Ticket type (11 classes) | **Yes — target label** |
| `intent` | Finer sub-type (27 classes) | No (optional extra) |
| `response` | Agent's reply | No |
| `flags` | Writing-style tags (typos, slang…) | No |

**Facts**
- 26,872 messages, **0 missing values**, 2,237 duplicate messages (to remove).
- Short messages: ~9 words on average.
- Categories: ACCOUNT 5986 · ORDER 3988 · REFUND 2992 · INVOICE 1999 · CONTACT 1999 · PAYMENT 1998 · FEEDBACK 1997 · DELIVERY 1994 · SHIPPING 1970 · SUBSCRIPTION 999 · CANCEL 950
- Contains placeholders like `{{Order Number}}` and deliberate typos ("rtying") — realistic noise.
- Quick TF-IDF + Logistic Regression test: **~99.7% accuracy**.

## Rejected: Tobi-Bueck/customer-support-tickets
Has `queue` (department) and `priority` labels, which looked attractive, but:
- Half the data is German.
- Labels are noisy: same baseline got only **52% (queue)** and **62% (priority)**.
- Example: *"Urgent Help Needed for Possible Data Breach"* is labelled **medium** priority.
→ Too hard to get a clean, explainable result.

## What this means for each feature
| Feature | Approach |
|---|---|
| Category | **ML model** trained on Bitext `category` |
| Urgency | **Keyword rules** (Bitext has no urgency labels) |
| Sentiment | **Pre-trained** analyser (Bitext has no sentiment labels) |

## Viva notes
- **Why Bitext?** Clean, balanced enough, no missing values, categories match real support teams.
- **Why is accuracy so high?** Bitext is generated from templates, so wording per category is very consistent. Real tickets would score lower — say this honestly; it shows understanding.
- **Why not train urgency/sentiment?** No reliable labels exist in our data; the noisy priority dataset proved that bad labels give bad models.
