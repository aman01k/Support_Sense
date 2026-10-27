# Part 6 — Live demo (≈ 3 minutes)

**Goal:** show the examiner that the system really works end to end: a message goes in, three predictions come out, and the dashboard puts urgent tickets first.
**Speaker:** Aman drives the laptop and speaks; change this if you split it differently.
On screen: slide 24 ("Live demo") for a moment, then switch to the browser with the dashboard.

Every result below was checked by running the app. If you get a different number, someone has retrained the model.

---

## Before the viva (do this 10 minutes early)

1. Open a terminal in the `SupportSense` folder and start the app:
   ```bash
   .venv/bin/streamlit run streamlit_app.py
   ```
2. The dashboard opens at **http://localhost:8501**. Keep that tab ready next to the slides.
3. In the sidebar, click **Clear all tickets**, then **Add 20 sample tickets** once, so the dashboard isn't empty.
4. Zoom the browser to about **125%** (Cmd +) so the examiner can read it.
5. Close other tabs and silence notifications.
6. **Backup:** take 3 screenshots now (an analysed ticket, the dashboard, the filtered table) in case the laptop or app fails. The app runs fully offline; no internet is needed.

---

## The demo, step by step

### Step 1 — A clear urgent ticket · ~30 s
**Do:** click the example **Hacked account** → click **Analyze ticket**.
**Screen shows:** ACCOUNT · Confidence 90% · Urgency **High**, reason *security: hacked* · Sentiment **Negative**, VADER −0.40.

**Say:**
> Let me show you the system running. I'll pick a message: *"My account was hacked and someone changed my email"*, and click Analyze.
>
> In under a second: category **Account** with 90% confidence, urgency **High**, and here's the reason: it found the security word "hacked". Sentiment is negative. This is exactly the example from our introduction.

### Step 2 — A simple question · ~20 s
**Do:** click **Question** → **Analyze ticket**.
**Screen shows:** PAYMENT · 97% · Urgency **Low** · Sentiment **Neutral** (+0.38).

**Say:**
> Compare that with a simple question: *"What payment methods do you accept?"*. Payment, 97% confident, **Low** urgency, neutral. This one can wait.

### Step 3 — When the model isn't sure · ~35 s
**Do:** click **Double charge** → **Analyze ticket**.
**Screen shows:** FEEDBACK · Confidence **27%** · yellow **"Needs manual review"** box · Urgency **High**, reason *money: charged twice* · Negative.

**Say:**
> Now a harder one: *"I've been charged twice for my subscription, and nobody has responded to my previous complaint."*
>
> Urgency is correctly **High**: the rule caught "charged twice". But look at the category: only **27%** confident. The words "charged twice" barely appear in our training data, so the model is unsure. Instead of trusting a guess, the system shows **"Needs manual review"**. That's the confidence check we explained earlier, working live.

### Step 4 — Bad input · ~10 s
**Do:** click into the text box, delete everything (Cmd A, Delete) → **Analyze ticket**.
**Screen shows:** warning *"Please enter at least 2 words."*

**Say:**
> And if someone submits an empty message, it doesn't crash; it asks for proper input.

### Step 5 — The dashboard · ~40 s
**Do:** scroll down to **Ticket dashboard**. Point at the cards, then the charts.
**Screen shows:** total tickets, High priority, % negative, needs review; bar charts by category, urgency and sentiment.

**Say:**
> Every ticket we analyse is saved and appears here. At the top: total tickets, how many are High priority, the share of negative customers, and how many need review. Below that, tickets by category, urgency and sentiment, so a team lead can see at a glance where the problems are.

### Step 6 — Urgent first, and filters · ~40 s
**Do:** scroll to **All tickets**. Point out that High rows are at the top. Then click the **High** urgency filter. Then switch on **Only show tickets that need manual review**. Then turn both off and type `refund` in **Search text**.
**Screen shows:** the table sorted High → Medium → Low, with coloured labels, a "Why this urgency" column and a confidence bar; then the filtered results.

**Say:**
> This is the agent's queue. It's sorted with **High urgency first**, not by arrival time; that's the problem we set out to solve. Each row shows the category, sentiment, the reason for its urgency and the model's confidence.
>
> An agent can filter to only High tickets, or only the ones that need manual review, or search, for example for "refund". And the table can be downloaded as a CSV.
>
> That's the full system. Shashwat will now talk about its limitations and what we'd improve.

---

## Optional: let the examiner type a message
Only do this if you have time and feel confident. Results are honest but can be surprising.

**Say:** "Would you like to type a message yourself?"

If they ask for ideas, these are safe and were checked:

| Message | Result |
|---|---|
| I want a refund, the product arrived broken | REFUND (52%) · Negative · Medium (*problem: broken*) |
| Someone used my card without my permission | ACCOUNT (30%, flagged for review) · Neutral · **High** (*security*) |
| I can't log into my account, it keeps saying wrong password | ACCOUNT (98%) · Negative · Medium |

If a result looks wrong, say what it shows: *"The confidence is low, so it's flagged for review; that's the safety net."* or *"This is the synthetic-data limitation we'll discuss next."*

---

## Examples to avoid (or explain)
| Example button | What happens | If it comes up |
|---|---|---|
| Late delivery | ACCOUNT, 28%, flagged | "Wrong category but low confidence, so it's sent for review. Bitext's delivery messages are questions, not complaints." |
| Praise | FEEDBACK, 22%, flagged; Positive; Low | Fine to show for sentiment; just mention the flag. |

---

## If something goes wrong
| Problem | Fix |
|---|---|
| `streamlit: command not found` / `no such file` | You're in the wrong folder: `cd` into `SupportSense` first. |
| Port already in use | Add `--server.port 8502` to the command and open localhost:8502. |
| App crashes or laptop dies | Switch to the backup screenshots and narrate the same steps. |
| Table empty | Click **Add 20 sample tickets** in the sidebar. |
