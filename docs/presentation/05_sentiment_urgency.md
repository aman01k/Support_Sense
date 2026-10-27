# Part 5 — Sentiment and urgency (≈ 2.5 minutes)

**Goal:** the examiner understands how VADER scores tone, how the urgency rules work and why they combine keywords with tone, and how well both perform, honestly.
**Speaker:** Shashwat presents all four slides; change this if you split it differently.
Slides 20–23 of the SupportSense Viva Presentation deck; the same text is in the speaker notes.

Every score below was produced by our code on that exact sentence.

---

## Slide 20 — Sentiment with VADER · ~40 s
**Show:** "This is good" → "This is not good" → "This is NOT good!!!" with scores, and the score scale with our thresholds.

**Say:**
> For sentiment we use **VADER**, a pre-trained analyser. It has a dictionary of about 7,500 words, each scored from negative to positive, plus rules for how people write.
>
> Look at these three. *"This is good"* scores **+0.44**. Add "not" and it flips to **−0.34**: VADER handles **negation**. Write NOT in capitals with exclamation marks and it gets stronger, **−0.51**.
>
> VADER gives a score from −1 to +1. Below −0.05 we call it **Negative**, and above **0.5** Positive. We set the Positive bar higher than usual because support messages are polite: *"Please tell me how to update my address"* scores +0.32 just because of "please", but it isn't a happy customer.

---

## Slide 21 — Urgency: five rules, in order · ~35 s
**Show:** the five rules as a ladder, each with a real example.

**Say:**
> Our dataset has no urgency labels, so we use **business rules**, checked in order; the first match wins.
>
> One: security, money, legal or "urgent" keywords mean **High**, like *"hacked"* or *"charged twice"*. Two: a very angry tone, below −0.7, is also **High**. Three: problem words like *"can't"* or *"error"* mean **Medium**. Four: any negative tone is **Medium**. Five: everything else, like simple questions, is **Low**.
>
> Every result comes with a **reason**, so an agent can see exactly why a ticket got its priority.

---

## Slide 22 — Why keywords *and* tone · ~35 s
**Show:** two real tickets: a calm one that's urgent, and an angry one with no keyword.

**Say:**
> Why combine both? Because each alone misses something.
>
> *"I need access to my account urgently, my business depends on it"* sounds calm: sentiment score **0**. Tone alone would call it Low. But the keyword "urgently" makes it **High**.
>
> *"Absolutely terrible, I am furious and disgusted with your company"* has no keyword at all. But its tone is **−0.89**, so the tone rule makes it **High**.
>
> Together, they cover both kinds of urgent ticket.

---

## Slide 23 — How well it works, honestly · ~40 s
**Show:** 94% sentiment, 100% urgency, 100% High recall on 36 hand-labelled messages; the caveat; two known failures.

**Say:**
> We had no labels to test with, so we wrote and labelled **36 messages** ourselves. Sentiment was **94%** correct, and urgency **100%**. Most importantly, **High recall is 100%**: no urgent ticket was missed. For urgency, missing a real emergency is far worse than over-flagging a normal ticket.
>
> But we want to be honest: we wrote those messages alongside the rules, so these numbers are **optimistic**.
>
> And we know where it fails. *"I was not charged twice"* is still High, because the keyword rule ignores "not". And sarcasm, *"Great, another late delivery. Just perfect."*, is scored **positive**, +0.83.

---

## Likely questions on this part
| Question | Answer |
|---|---|
| Why not train a sentiment model? | No sentiment labels in our data. VADER needs no training and works well on short, informal text. |
| Why rules for urgency, not ML? | No reliable urgency labels: the one dataset with priorities had noisy labels (62% baseline). Rules need no data, are explainable, and a business can change them easily. |
| Which urgency metric matters most? | Recall for High: missing a fraud or double-charge ticket costs much more than flagging a normal one. |
| Did you tune the rules? | Yes, once: "I chose a wrong address by mistake" (−0.67) was marked High, so we moved the threshold from −0.6 to −0.7. |
| How would you improve urgency? | Collect the priorities agents actually assign, then train a real classifier. Also add negation handling to the keyword rules. |
| "This is good" is +0.44, so is it Neutral? | Yes, with our 0.5 threshold. That's the trade-off: we accept calling mild praise Neutral so that polite requests ("please…") aren't called Positive. Strong praise like "Your support team was excellent" (+0.75) is still Positive. |
| Why does VADER miss "overcharged"? | It's not in VADER's general-purpose dictionary. The urgency rule still catches it as a money keyword. |
