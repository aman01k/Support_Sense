# Part 3 — Preparing the text (≈ 2.5 minutes)

**Goal:** the examiner sees that the data was prepared carefully, with each step justified, and that we avoided data leakage.
**Speaker:** Shashwat presents all four slides; change this if you split it differently.
Slides 11–14 of the SupportSense Viva Presentation deck; the same text is in the speaker notes.

---

## Slide 11 — Light cleaning, on purpose · ~35 s
**Show:** the four cleaning steps, and two real messages before and after.

**Say:**
> Before training, we clean the text, but only lightly. We do four things: convert to **lowercase**, remove **placeholders** like *{{Order Number}}*, remove **numbers** like order IDs, and remove **extra spaces**.
>
> For example, *"i have to find my invoice #12588"* becomes *"i have to find my invoice"*. An order number tells us nothing about the category.
>
> All of this is one Python function, `clean_text()`. The dashboard uses the **same function** on new tickets, so new messages are cleaned exactly like the training data.

---

## Slide 12 — What we deliberately keep · ~35 s
**Show:** "I can pay" vs "I can't pay", and three things we chose not to do.

**Say:**
> Just as important is what we **don't** remove.
>
> Many NLP tutorials remove stop words. But stop-word lists include words like "not" and "can't". *"I can pay"* and *"I can't pay"* mean opposite things, so removing them would destroy the meaning.
>
> We also don't fix typos, because real customers make them and the model learns from them. And we skip stemming: the messages are short, and TF-IDF with word pairs already works well.

---

## Slide 13 — Removing duplicates · ~40 s
**Show:** the row count at each step, from 26,872 to 23,776, and why duplicates cause leakage.

**Say:**
> Next we checked the data step by step. There were no empty messages and no message with two different labels. But there were **3,096 duplicates** after cleaning, so we removed them, leaving **23,776** messages.
>
> Why does this matter? If the same sentence is in both the training set and the test set, the model is tested on something it has already memorised. The score looks better than it really is. This is called **data leakage**.

---

## Slide 14 — Stratified 80/20 split · ~40 s
**Show:** the train/test bar (19,020 vs 4,756), category shares equal in both, and the two rules that prevent leakage.

**Say:**
> Finally, we split the data: **80% for training**, 19,020 messages, and **20% for testing**, 4,756 messages the model never sees during training.
>
> The split is **stratified**, so each category keeps the same share in both sets: ACCOUNT is 21.5% of both, CANCEL is 4% of both. We use a fixed random seed, 42, so anyone who runs our code gets exactly the same split.
>
> And one more rule against leakage: the TF-IDF vectorizer is fitted on the **training set only**. Next, we'll show how the model learns from this data.

---

## Likely questions on this part
| Question | Answer |
|---|---|
| Why 3,096 duplicates when the dataset had 2,237? | 2,237 were exact copies. Cleaning made a few more identical, e.g. two messages that differed only in an order number. |
| Why not lemmatize? | It adds a step and a dependency, and TF-IDF with word pairs already reached 99.6%. Nothing to gain. |
| What is data leakage? | When information from the test set reaches training, so the test score is unrealistically good. Duplicates across sets and fitting TF-IDF on all data are both examples. |
| Why `random_state=42`? | Any fixed number works; it makes the split reproducible. 42 is just a common convention. |
| Why stratify? | With imbalanced classes, a random split could leave very few CANCEL examples in the test set. Stratifying guarantees fair testing of every category. |
