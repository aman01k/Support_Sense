# Part 1 — Introduction (≈ 2.5 minutes)

**Goal:** by the end, the examiner knows what SupportSense is, why it's needed, and what it outputs.
**Split:** Aman presents slides 1–3, Shashwat presents slides 4–6.
Slides: SupportSense Viva Presentation (the claude.ai deck); the same text is in each slide's speaker notes.

---

## Slide 1 — Title · Aman · ~15 s
**Show:** SupportSense title, subtitle, both names with enrollment numbers.

**Say:**
> Good morning. I'm Aman, enrollment number 230065, and this is my teammate Shashwat, 230127. Our NLP project is **SupportSense**, an AI-powered customer support ticket intelligence system.

---

## Slide 2 — The problem · Aman · ~35 s
**Show:** three pain points on the left; an inbox on the right where a hacked-account ticket sits 4th in line behind simple questions.

**Say:**
> Companies receive hundreds or thousands of support messages every day, through email, websites and feedback forms. Today, a person has to read each one, decide what it's about, and pass it to the right team.
>
> That has three problems. It's **slow**: nobody replies until someone has sorted the ticket. It's **inconsistent**: two agents can file the same message differently. And most importantly, **urgent issues get buried**. Look at this inbox: tickets are handled in arrival order, so a customer whose account was hacked waits behind three simple questions.

---

## Slide 3 — Our solution · Aman · ~25 s
**Show:** blue statement slide: SupportSense reads every ticket and answers three questions.

**Say:**
> SupportSense fixes this. It reads every ticket the moment it arrives and tells the support team three things: **what** the ticket is about, **how the customer feels**, and **how urgent** it is.
>
> One thing to be clear about: this is **not a chatbot**. It doesn't reply to customers. It's a triage tool that helps the support team decide what to handle first.
>
> Shashwat will show you what that looks like.

---

## Slide 4 — Example · Shashwat · ~30 s
**Show:** one real message going in, three real outputs coming out.

**Say:**
> Here's a real output from our system. The customer writes: *"My account was hacked and someone changed my email."*
>
> SupportSense says:
> - **Category: Account**, and the model is 90% confident.
> - **Sentiment: Negative.**
> - **Urgency: High**, and it tells us why: it found the security word "hacked".
>
> So instead of waiting 4th in line, this ticket goes straight to the top of the Account team's queue.

---

## Slide 5 — Three features · Shashwat · ~35 s
**Show:** three cards (category, sentiment, urgency) with the technique behind each, and the dashboard bar underneath.

**Say:**
> Each answer comes from a different technique, chosen to fit the data we had.
>
> **Category** is our main machine learning model. It uses TF-IDF to turn text into numbers and Logistic Regression to classify it into 11 categories like Refund, Payment and Account. It was trained on about 19,000 labelled messages.
>
> **Sentiment** uses VADER, a pre-trained sentiment analyser, because our dataset has no sentiment labels to train on.
>
> **Urgency** uses business rules: keywords such as "hacked", "charged twice" or "urgent", combined with the sentiment score. Every urgency comes with a reason.
>
> Everything is shown in a Streamlit dashboard, with the most urgent tickets first.

---

## Slide 6 — What we'll cover · Shashwat · ~15 s
**Show:** six numbered topics.

**Say:**
> In the rest of the presentation we'll cover the dataset, how we prepared the text, the category model and its results, sentiment and urgency, a live demo, and finally the limitations and what we'd improve.

---

## Tips
- **Handover line:** Aman ends slide 3 with "Shashwat will show you what that looks like." Practise it so the switch is smooth.
- **Don't read the slides aloud.** The slides show the picture; you tell the story.
- **If interrupted with "Is it a chatbot?"** No: it classifies and prioritises tickets for the support team, it doesn't talk to customers.
- **The numbers on slide 4 are real.** They come from running `analyze_ticket()` on that exact message: ACCOUNT 0.903, Negative −0.40, High (security: hacked).
