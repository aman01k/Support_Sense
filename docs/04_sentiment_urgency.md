# Step 4 — Sentiment Analysis & Urgency Detection

Script: `notebooks/04_sentiment_urgency.py` · Code: `src/sentiment.py`, `src/urgency.py`
Test set: `data/eval/manual_samples.csv` (36 hand-labelled messages)

## Why not train models for these?
Bitext has **no sentiment or urgency labels**. Without labels you can't train a supervised model. So:
- **Sentiment:** use a **pre-trained** analyser (VADER).
- **Urgency:** use **business rules** (keywords + sentiment).

## Sentiment: VADER
VADER (Valence Aware Dictionary and sEntiment Reasoner) is a pre-trained, rule-based analyser built for short, informal text.
- A dictionary of ~7,500 words scored for positivity or negativity ("excellent" +, "broken" −).
- Rules for **negation** ("not good" → negative), **intensifiers** ("extremely"), **CAPITALS** and **"!!!"**.
- Output: a **compound score** from −1 (very negative) to +1 (very positive).

| Compound score | Label |
|---|---|
| ≥ 0.5 | Positive |
| ≤ −0.05 | Negative |
| in between | Neutral |

**Why 0.5 for Positive, not the usual 0.05?** Support messages are polite. *"Please tell me how to update my address"* scores +0.32 just because of "please". That isn't a happy customer, so polite requests should stay Neutral.

## Urgency: rules (checked in this order)
| # | Rule | Result | Example |
|---|---|---|---|
| 1 | Security words: hacked, fraud, unauthorized, stolen… | **High** | "My account was hacked" |
| 1 | Money words: charged twice, overcharged, money deducted… | **High** | "I've been charged twice" |
| 1 | Legal words: lawyer, legal action, sue, police… | **High** | "I will take legal action" |
| 1 | Urgent words: urgent, asap, immediately, emergency… | **High** | "I need access urgently" |
| 2 | Very negative sentiment (≤ −0.7) | **High** | "Absolutely terrible, I am furious" |
| 3 | Problem words: not working, can't, error, broken, missing, delayed… | **Medium** | "I can't log into my account" |
| 4 | Any negative sentiment | **Medium** | "I'm disappointed with the quality" |
| 5 | Everything else | **Low** | "What payment methods do you accept?" |

Every result includes a **reason** (e.g. `money: charged twice`), so agents can see *why*.

**Key design point:** urgency does not depend only on tone. *"I need access to my account urgently"* sounds calm (Neutral) but is **High** because of the keyword. A hacked account is High even if politely written.

## Results on 36 hand-labelled messages
| Feature | Accuracy | Note |
|---|---|---|
| Sentiment | **94%** | Positive 4/4 correct |
| Urgency | **100%** | **High recall = 100%**: no urgent ticket was missed |

The 2 sentiment mistakes:
1. *"You overcharged me…"* → Neutral. VADER doesn't know "overcharged" is negative. Urgency is still High (money rule).
2. *"Please refund me immediately or I will report you"* → Neutral. "please" cancels out the threat. Urgency is still High.

**Threshold change (−0.6 → −0.7):** while testing the dashboard, *"I chose a wrong address by mistake"* (score −0.67) was marked High. It's a mild message, so we raised the bar to −0.7. Side effect: *"I am not happy with how my complaint was handled"* (−0.64) is now correctly Medium. The fix came from a Bitext message, not the hand-labelled set, but because we have now adjusted the rules, the 100% on these 36 messages is even more optimistic. Test on new messages.

**Distribution on the Bitext test set:** sentiment is 82% Neutral, 16% Negative, 2% Positive; urgency is 80% Low, 20% Medium, 0.1% High. That makes sense, because Bitext is mostly calm "how do I…" questions.

## Honest limitations (say these in the viva)
- **The 36-message test set is small, and we wrote it ourselves**, alongside the rules. Real accuracy will be lower. Ask your teammate to write 20 *new* messages without looking at the rules, and test those.
- **Keywords miss phrasing they don't list**, e.g. *"someone else is using my account"* has no security keyword.
- **VADER doesn't know support jargon** like "overcharged" or "chargeback".
- **Sarcasm** (*"Great, another late delivery"*) fools VADER.

## Viva notes
- **Rule-based vs ML?** Rules need no labelled data, are fully explainable, and are easy to change for business needs. ML needs thousands of labelled examples we don't have.
- **Why is High-recall the key metric?** Missing an urgent ticket (fraud, double charge) is far worse than wrongly flagging a normal one. Recall for High is 100%.
- **Why combine sentiment and keywords?** Tone alone misses calm-but-serious tickets; keywords alone miss furious customers with no keyword. Together they cover both.
- **Future improvement:** collect agent-assigned priorities over time and train a real urgency classifier.
