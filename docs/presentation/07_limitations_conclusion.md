# Part 7 — Limitations, future work and conclusion (≈ 2.5 minutes)

**Goal:** show the examiner that you understand your system's weaknesses, have a realistic plan to fix them, and can sum up the project in one line.
**Speaker:** Shashwat presents slides 25–27; both of you on slide 28.
Slides 25–28 of the SupportSense Viva Presentation deck; the same text is in the speaker notes.

---

## Slide 25 — Limitations · ~50 s
**Show:** six limitations, each with a real example.

**Say:**
> We want to be clear about what the system can't do.
>
> First, and biggest: **synthetic data**. Bitext is generated from templates, so 99.6% is higher than we'd get on real tickets. For example, *"My package hasn't arrived and it's been 10 days"* is predicted as Account, though with low confidence it's flagged.
>
> Second, **one category per ticket**: a message about a refund *and* a new address only gets one label.
>
> Third, our urgency and sentiment test set is **small and self-written**.
>
> Fourth, the **keyword rules are literal**: *"I was not charged twice"* still triggers High.
>
> Fifth, **VADER misses sarcasm** and support jargon like "overcharged".
>
> And sixth, it's **English only**.

---

## Slide 26 — What we'd do next · ~40 s
**Show:** next steps grouped into data, models and system.

**Say:**
> Each limitation points to a next step.
>
> On **data**: train and test on real company tickets, and collect the priorities that agents actually assign.
>
> On **models**: with those priorities we could train a real **urgency classifier** instead of rules. If real data is messier, we'd try a transformer like **DistilBERT**. We'd also allow **multiple categories** per ticket and add **negation handling** to the rules.
>
> On the **system**: replace the CSV with a proper database, route tickets automatically to the right team, and connect it to email.

---

## Slide 27 — Conclusion · ~35 s
**Show:** what we built, three headline numbers, and the one-line takeaway.

**Say:**
> To conclude: SupportSense reads a customer message and predicts its **category**, **sentiment** and **urgency**, then puts urgent tickets first.
>
> The category model reaches **99.6% accuracy**; on our test messages no urgent ticket was missed; and in 18 edge-case tests, it never crashed.
>
> Our main takeaway: a **simple, explainable** NLP pipeline can do the first triage of support tickets, and, just as important, it **knows when to ask a human**.

---

## Slide 28 — Thank you · both · ~5 s
**Show:** thank-you slide with both names.

**Say (Aman or Shashwat):**
> Thank you. We're happy to take your questions.

---

## Likely questions on this part
| Question | Answer |
|---|---|
| What's the single biggest weakness? | The synthetic training data. Real tickets are messier, so accuracy would drop. The confidence check reduces the risk, but real data is the real fix. |
| If you had one more month, what would you do? | Get real tickets with agent-assigned priorities, then retrain the category model and train an urgency classifier. |
| Why not fix negation in the rules now? | It's a known, documented trade-off; we kept the rules simple and explainable. A fix would check for "not" or "no" just before a keyword. |
| Would BERT solve everything? | No. It would help with context and sarcasm on messy data, but it still needs labelled data, especially for urgency. |
| Is this ready for a real company? | As a prototype, yes; for production it needs real training data, a database, and testing with real agents. |

---

## Timing for the whole presentation
| Part | Speaker | Time |
|---|---|---|
| 1. Introduction | Aman → Shashwat | 2.5 min |
| 2. Dataset | Aman | 2.5 min |
| 3. Preparing the text | Shashwat | 2.5 min |
| 4. Category model | Aman | 3 min |
| 5. Sentiment & urgency | Shashwat | 2.5 min |
| 6. Live demo | Aman | 3 min |
| 7. Limitations & conclusion | Shashwat | 2.5 min |
| **Total** | | **≈ 18.5 min** |

**If you have only about 12 minutes**, skip slides 8, 13, 16, 18 and 22 (mention duplicates in one sentence on slide 14) and shorten the demo to steps 1, 3 and 6.
