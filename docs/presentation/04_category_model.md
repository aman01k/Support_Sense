# Part 4 — Category model and results (≈ 3 minutes)

**Goal:** the examiner understands how TF-IDF and Logistic Regression work, how well the model performs, where it fails, and how we handle uncertainty.
**Speaker:** Aman presents all five slides; change this if you split it differently.
Slides 15–19 of the SupportSense Viva Presentation deck; the same text is in the speaker notes.

All numbers on these slides come from our trained model.

---

## Slide 15 — TF-IDF: turning words into numbers · ~40 s
**Show:** IDF of "the" vs "refund"; one real message with its TF-IDF weights; words the model has never seen.

**Say:**
> A model can't read text; it needs numbers. We use **TF-IDF**: term frequency times inverse document frequency.
>
> **IDF** rewards rare, informative words. "The" appears in many messages, so its IDF is low, 2.4. "Refund" appears in few, so it's high, 4.9.
>
> Here's a real message: *"I want my money back for the broken headphones."* TF-IDF gives each word and **word pair** a weight; "money back" counts as one feature. In total the vocabulary has **4,823 features**.
>
> Notice that "broken" and "headphones" get no weight. They never appeared in training, so they're simply ignored.

---

## Slide 16 — Logistic Regression: from numbers to a category · ~40 s
**Show:** probability bars for the same message (REFUND 90.9%), and the top words the model learned per category.

**Say:**
> Logistic Regression learns a **weight for every feature in every category**: 11 categories times 4,823 features. For a new message, it adds up those weights for each category and turns the scores into **probabilities** that sum to 100%.
>
> For our message, it says **REFUND with 90.9%**. Everything else is below 3%.
>
> We can also see what it learned. The strongest words for REFUND are refund, reimbursement and money; for CONTACT, agent, person and speak. These make sense, so the model learned real signals, not noise.

---

## Slide 17 — Results · ~35 s
**Show:** 99.6% accuracy, 0.997 macro F1, 17 errors out of 4,756, and the comparison with Linear SVM.

**Say:**
> We tested on the **4,756 messages** the model never saw. Accuracy is **99.6%** and macro F1 is **0.997**. Only **17 mistakes**, and every category has precision and recall of at least 0.987.
>
> We also tried a **Linear SVM**. It scored slightly higher, 99.8%, about 10 more correct messages. But SVM doesn't give probabilities, and we need them for the confidence check. So we kept Logistic Regression.

---

## Slide 18 — Where it goes wrong · ~35 s
**Show:** the confusion matrix and four of the real mistakes.

**Say:**
> This is the confusion matrix. Rows are the true category, columns are the prediction. Almost everything is on the diagonal, which means correct.
>
> The few mistakes are mostly **heavy typos**: "paymdnt", "invooce", or words stuck together like "requestreimbursements". The model has never seen those spellings, so it guesses.
>
> And honestly, 99.6% is high because Bitext is template-generated. On real tickets it would be lower.

---

## Slide 19 — Knowing when it's unsure · ~35 s
**Show:** the 50% confidence rule, "I was charged twice" at 23%, and accuracy on confident vs flagged tickets.

**Say:**
> That's why we added a **confidence check**. If the model's top probability is below **50%**, the ticket is marked **"Needs manual review"**.
>
> For example, *"I was charged twice"* gets only 23%, because "charged" and "twice" barely appear in the training data.
>
> On the test set, 74 tickets were flagged. On confident tickets the model is **99.9%** correct, and on flagged ones only **82.4%**. So the flag separates reliable predictions from risky ones, and a human checks the risky ones.

---

## Likely questions on this part
| Question | Answer |
|---|---|
| What is TF-IDF? | TF × log(N / DF): high for words frequent in this message but rare overall. |
| Why word pairs (`ngram_range=(1,2)`)? | They capture phrases and negation, e.g. "money back", "not working". |
| Why Logistic Regression over SVM? | Nearly the same accuracy (0.2% less), but it gives probabilities, which the confidence check needs. |
| Why not BERT? | We already have 99.6% with a model that trains in seconds and is explainable. BERT would make sense for messier real data. |
| What does `class_weight="balanced"` do? | Mistakes on small classes like CANCEL cost more, so the model doesn't ignore them. |
| How is the model saved? | TF-IDF and Logistic Regression are one scikit-learn Pipeline, saved with joblib as `category_model.joblib`. The Pipeline also guarantees TF-IDF is fitted on training data only. |
| Is 99.6% suspicious? | We removed duplicates and fitted TF-IDF on training data only, so it's not leakage. The data is very consistent because it's template-generated. |
| Why is the threshold 50%? | Below 50%, the model thinks another category is at least as likely. It's simple to explain, and it flags only 1.6% of tickets. |
