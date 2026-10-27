"""Build the presentation script PDF: what to say for each slide, plus the code guide.

Run (from SupportSense/):  .venv/bin/python tools/build_script_pdf.py
Output: docs/presentation/SupportSense_Presentation_Script.pdf
"""
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (KeepTogether, PageBreak, Paragraph, SimpleDocTemplate,
                                Spacer, Table, TableStyle)

OUT = Path(__file__).resolve().parent.parent / "docs" / "presentation" / "SupportSense_Presentation_Script.pdf"

# Arial covers the arrows, minus signs and quotes used below
FONTS = "/System/Library/Fonts/Supplemental/"
pdfmetrics.registerFont(TTFont("Arial", FONTS + "Arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Bold", FONTS + "Arial Bold.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Italic", FONTS + "Arial Italic.ttf"))
pdfmetrics.registerFont(TTFont("Mono", FONTS + "Courier New.ttf"))
pdfmetrics.registerFontFamily("Arial", normal="Arial", bold="Arial-Bold", italic="Arial-Italic",
                              boldItalic="Arial-Bold")

NAVY, BLUE, ORANGE = colors.HexColor("#13203A"), colors.HexColor("#2350C8"), colors.HexColor("#B24E14")
GREY, LIGHT, PALE = colors.HexColor("#4A5568"), colors.HexColor("#EEF1F7"), colors.HexColor("#F6F7F3")

S = {
    "title": ParagraphStyle("title", fontName="Arial-Bold", fontSize=30, leading=36, textColor=NAVY, alignment=TA_CENTER),
    "subtitle": ParagraphStyle("subtitle", fontName="Arial", fontSize=14, leading=20, textColor=BLUE, alignment=TA_CENTER),
    "center": ParagraphStyle("center", fontName="Arial", fontSize=11, leading=16, textColor=NAVY, alignment=TA_CENTER),
    "part": ParagraphStyle("part", fontName="Arial-Bold", fontSize=18, leading=24, textColor=NAVY, spaceAfter=4),
    "partinfo": ParagraphStyle("partinfo", fontName="Arial", fontSize=10, leading=14, textColor=GREY, spaceAfter=10),
    "slidehead": ParagraphStyle("slidehead", fontName="Arial-Bold", fontSize=12, leading=15, textColor=colors.white),
    "slidemeta": ParagraphStyle("slidemeta", fontName="Arial", fontSize=10, leading=15, textColor=colors.HexColor("#D4DEFF"), alignment=2),
    "label": ParagraphStyle("label", fontName="Arial-Bold", fontSize=8, leading=11, textColor=BLUE),
    "screen": ParagraphStyle("screen", fontName="Arial-Italic", fontSize=9.5, leading=13, textColor=GREY),
    "say": ParagraphStyle("say", fontName="Arial", fontSize=11.5, leading=16.5, textColor=NAVY),
    "body": ParagraphStyle("body", fontName="Arial", fontSize=10.5, leading=15, textColor=NAVY, spaceAfter=6),
    "h2": ParagraphStyle("h2", fontName="Arial-Bold", fontSize=13, leading=18, textColor=BLUE, spaceBefore=10, spaceAfter=6),
    "cell": ParagraphStyle("cell", fontName="Arial", fontSize=9, leading=12, textColor=NAVY),
    "cellb": ParagraphStyle("cellb", fontName="Arial-Bold", fontSize=9, leading=12, textColor=colors.white),
    "mono": ParagraphStyle("mono", fontName="Mono", fontSize=8.5, leading=12, textColor=NAVY),
}

PAGE_W = A4[0] - 4 * cm


def slide_block(n, title, speaker, time, screen, say):
    """One slide: a navy header bar, what's on screen, and what to say."""
    head = Table([[Paragraph(f"Slide {n} · {title}", S["slidehead"]),
                   Paragraph(f"{speaker} · {time}", S["slidemeta"])]],
                 colWidths=[PAGE_W * 0.72, PAGE_W * 0.28])
    head.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), NAVY),
                              ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                              ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    body = [Paragraph("ON SCREEN", S["label"]), Paragraph(screen, S["screen"]), Spacer(1, 6),
            Paragraph("SAY", S["label"])]
    body += [Paragraph(p, S["say"]) for p in say]
    box = Table([[body]], colWidths=[PAGE_W])
    box.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), PALE),
                             ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                             ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 10)]))
    return KeepTogether([head, box, Spacer(1, 12)])


def table(rows, widths, mono_cols=()):
    """A simple table with a navy header row. rows[0] is the header."""
    data = [[Paragraph(c, S["cellb"]) for c in rows[0]]]
    for r in rows[1:]:
        data.append([Paragraph(c, S["mono"] if i in mono_cols else S["cell"]) for i, c in enumerate(r)])
    t = Table(data, colWidths=[PAGE_W * w for w in widths], repeatRows=1)
    style = [("BACKGROUND", (0, 0), (-1, 0), NAVY), ("VALIGN", (0, 0), (-1, -1), "TOP"),
             ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#C9CFD9")),
             ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
             ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]
    style += [("BACKGROUND", (0, i), (-1, i), LIGHT) for i in range(2, len(data), 2)]
    t.setStyle(TableStyle(style))
    return t


def part(title, info):
    return [Paragraph(title, S["part"]), Paragraph(info, S["partinfo"])]


# ---------------------------------------------------------------- content
story = []

# Cover
story += [Spacer(1, 4 * cm), Paragraph("SupportSense", S["title"]), Spacer(1, 6),
          Paragraph("Presentation Script", S["subtitle"]), Spacer(1, 1.2 * cm),
          Paragraph("What to say for each slide, and which code to show if asked", S["center"]),
          Spacer(1, 1.5 * cm),
          Paragraph("<b>Aman</b> · 230065 &nbsp;&nbsp;&nbsp; <b>Shashwat</b> · 230127", S["center"]),
          Paragraph("Natural Language Processing", S["center"]), Spacer(1, 2 * cm)]
story.append(table([
    ["Part", "Slides", "Speaker", "Time"],
    ["1. Introduction", "1–6", "Aman → Shashwat", "2.5 min"],
    ["2. Dataset", "7–10", "Aman", "2.5 min"],
    ["3. Preparing the text", "11–14", "Shashwat", "2.5 min"],
    ["4. Category model", "15–19", "Aman", "3 min"],
    ["5. Sentiment and urgency", "20–23", "Shashwat", "2.5 min"],
    ["6. Live demo", "24 + app", "Aman", "3 min"],
    ["7. Limitations and conclusion", "25–28", "Shashwat", "2.5 min"],
    ["<b>Total</b>", "", "", "<b>≈ 18.5 min</b>"],
], [0.45, 0.17, 0.23, 0.15]))
story += [Spacer(1, 12), Paragraph(
    "<b>How to use this:</b> don’t read it word for word. Learn the main points of each slide and say "
    "them in your own words. Point at the screen while you talk.", S["body"]), PageBreak()]

# Part 1
story += part("Part 1 · Introduction", "Goal: explain what SupportSense is, why it is needed, and what it does.")
story += [
    slide_block(1, "Title", "Aman", "15 s", "Project name and both of our names.", [
        "Good morning. I am Aman, 230065, and this is Shashwat, 230127.",
        "Our NLP project is <b>SupportSense</b>, a system that reads customer support tickets and sorts them automatically."]),
    slide_block(2, "Every ticket is read by hand", "Aman", "35 s",
                "Three problems on the left. An inbox on the right where a hacked account is 4th in line.", [
        "Companies get hundreds or thousands of support messages every day. Today, a person reads each one and decides where it goes.",
        "This has three problems. It is <b>slow</b>. It is <b>inconsistent</b>: two people may sort the same message differently. "
        "And <b>urgent problems get buried</b>. In this inbox, a hacked account is waiting behind three simple questions."]),
    slide_block(3, "Our solution", "Aman", "25 s", "Blue slide with three questions: what, how the customer feels, how urgent.", [
        "SupportSense reads every ticket as soon as it arrives and answers three questions: "
        "<b>What is it about? How does the customer feel? How urgent is it?</b>",
        "It is <b>not a chatbot</b>. It does not reply to customers. It helps the support team decide what to handle first.",
        "Shashwat will show you an example."]),
    slide_block(4, "One message in, three answers out", "Shashwat", "30 s",
                "One real message on the left, three results on the right.", [
        "Here is a real result from our system. The message is: <i>“My account was hacked and someone changed my email.”</i>",
        "Category: <b>Account</b>, 90% confident. Sentiment: <b>Negative</b>. Urgency: <b>High</b>, because it found the word “hacked”.",
        "So this ticket goes straight to the top of the queue."]),
    slide_block(5, "Three features, three techniques", "Shashwat", "35 s", "Three cards: category, sentiment, urgency.", [
        "Each answer uses a different method.",
        "<b>Category</b> is our machine learning model: TF-IDF plus Logistic Regression, trained on about 19,000 messages.",
        "<b>Sentiment</b> uses VADER, a ready-made model, because our data has no sentiment labels.",
        "<b>Urgency</b> uses simple rules: keywords like “hacked” or “charged twice”, plus the sentiment score.",
        "Everything is shown in a Streamlit dashboard, with the most urgent tickets first."]),
    slide_block(6, "What we’ll cover", "Shashwat", "15 s", "Six numbered topics.", [
        "Next we will cover the dataset, how we cleaned the text, the model and its results, sentiment and urgency, "
        "a live demo, and finally the limitations."]),
    PageBreak(),
]

# Part 2
story += part("Part 2 · Dataset", "Goal: which data we used, why, what it looks like, and how it shaped our design.")
story += [
    slide_block(7, "We compared two public datasets", "Aman", "40 s",
                "Table comparing Bitext and Tobi-Bueck, and the “data breach labelled medium” example.", [
        "We needed customer messages with correct labels. We compared two free datasets from Hugging Face.",
        "The <b>Tobi-Bueck</b> dataset has priority labels, but more than half of it is in German and the labels are messy. "
        "A quick test model got only <b>52%</b> and <b>62%</b>. For example, “Urgent help needed for possible data breach” is labelled <i>medium</i> priority.",
        "The <b>Bitext</b> dataset is in English, has no missing values, and the same test got <b>99.7%</b>. So we chose Bitext."]),
    slide_block(8, "What the data looks like", "Aman", "35 s", "Five real rows (message → category) and four key numbers.", [
        "Bitext has <b>26,872 messages</b>. We use two columns: the <b>message</b>, which is the input, and the <b>category</b>, which is what we predict.",
        "Messages are short, about 9 words. There are no missing values, but there are 2,237 duplicates, which we remove.",
        "The data has real-looking mistakes: typos like “rtying”, slang like “wanna”, and placeholders like {{Order Number}}."]),
    slide_block(9, "11 categories, not balanced", "Aman", "40 s", "Bar chart of the 11 categories; Account and Cancel highlighted.", [
        "There are 11 categories, but they are not the same size. Account has almost 6,000 messages; Cancel has only 950, about <b>six times fewer</b>.",
        "To handle this we did three things: a <b>stratified split</b>, <b>balanced class weights</b>, and we report <b>macro F1</b>, which treats every category equally.",
        "Note: in this data, Cancel means cancellation <i>fees</i>. Cancelling an order is in Order."]),
    slide_block(10, "The labels decided our design", "Aman", "35 s", "Dark slide: category is labelled, sentiment and urgency are not.", [
        "Bitext has category labels, but <b>no sentiment and no urgency labels</b>. Without labels we cannot train a model.",
        "So category uses a <b>trained model</b>, sentiment uses the ready-made <b>VADER</b>, and urgency uses <b>rules</b>.",
        "One honest point: Bitext is made from templates, so it is cleaner than real tickets. That is why our accuracy is so high."]),
    PageBreak(),
]

# Part 3
story += part("Part 3 · Preparing the text", "Goal: show that the data was prepared carefully and that we avoided data leakage.")
story += [
    slide_block(11, "Light cleaning, on purpose", "Shashwat", "35 s", "Four cleaning steps and two messages before and after.", [
        "Before training we clean the text, but only a little. Four steps: make it <b>lowercase</b>, remove <b>placeholders</b> "
        "like {{Order Number}}, remove <b>numbers</b> like #12588, and remove <b>extra spaces</b>.",
        "For example, “find my invoice #12588” becomes “find my invoice”.",
        "This is one function, <b>clean_text()</b>. The dashboard uses the same function for new tickets."]),
    slide_block(12, "What we deliberately keep", "Shashwat", "35 s", "“I can pay ≠ I can’t pay” and three things we chose not to do.", [
        "What we <b>don’t</b> remove is just as important.",
        "We keep <b>stop words</b>, because they include “not” and “can’t”. “I can pay” and “I can’t pay” mean opposite things. "
        "With stop words removed, both become just “pay”.",
        "We keep <b>typos</b> because real customers make them. And we skip <b>stemming</b> because short messages don’t need it."]),
    slide_block(13, "Removing duplicates prevents leakage", "Shashwat", "40 s", "Row counts from 26,872 down to 23,776, and why duplicates matter.", [
        "We checked the data step by step. No empty messages and no message with two labels. But there were <b>3,096 duplicates</b>, "
        "which we removed. That leaves <b>23,776</b> messages.",
        "Why? If the same sentence is in both training and testing, the model is tested on something it already memorised. "
        "The score looks better than it really is. This is called <b>data leakage</b>."]),
    slide_block(14, "A stratified 80/20 split", "Shashwat", "40 s", "Train/test bar, a table of category shares, and two rules.", [
        "We split the data: <b>80% for training</b>, 19,020 messages, and <b>20% for testing</b>, 4,756 messages the model never sees while learning.",
        "The split is <b>stratified</b>: each category has the same share in both parts. We fix the random seed at <b>42</b>, so the split is the same every time.",
        "And TF-IDF learns only from the training data, which is another rule against leakage."]),
    PageBreak(),
]

# Part 4
story += part("Part 4 · Category model and results", "Goal: how TF-IDF and Logistic Regression work, how well the model does, and how it handles doubt.")
story += [
    slide_block(15, "TF-IDF turns words into numbers", "Aman", "40 s", "IDF of “the” vs “refund”, and the word weights for one real message.", [
        "A model needs numbers, not words. <b>TF-IDF</b> gives each word a number. The number is high when a word is <b>rare</b> across all messages.",
        "“The” is everywhere, so it scores low: 2.4. “Refund” is rare, so it scores high: 4.9.",
        "We also use word pairs like “money back”. In total we have <b>4,823 features</b>. Words never seen in training, like “headphones”, get zero."]),
    slide_block(16, "Logistic Regression picks the category", "Aman", "40 s", "Probability bars (Refund 90.9%) and the top words per category.", [
        "<b>Logistic Regression</b> learns a weight for every word for every category. For a new message it adds up the weights "
        "and turns them into <b>probabilities</b> that add up to 100%.",
        "For our example it says <b>Refund, 90.9%</b>.",
        "We can also see what it learned: Refund is linked to “refund”, “reimbursement” and “money”. That makes sense."]),
    slide_block(17, "Results on 4,756 unseen messages", "Aman", "35 s", "99.6% accuracy, 0.997 macro F1, 17 mistakes; comparison with SVM.", [
        "We tested on 4,756 messages the model had never seen. <b>Accuracy is 99.6%</b>, macro F1 is 0.997, and there are only <b>17 mistakes</b>.",
        "We also tried a <b>Linear SVM</b>. It was slightly better, 99.8%, but it does not give probabilities. "
        "We need probabilities for our confidence check, so we kept Logistic Regression."]),
    slide_block(18, "Where it goes wrong", "Aman", "35 s", "Confusion matrix and four real mistakes.", [
        "This is the <b>confusion matrix</b>. Rows are the true category, columns are the prediction. "
        "Almost everything is on the diagonal, which means correct.",
        "Most mistakes are <b>heavy typos</b> like “paymdnt” or “invooce”.",
        "Honestly, the score is this high because the data is clean. Real tickets would score lower."]),
    slide_block(19, "Knowing when it’s unsure", "Aman", "35 s", "The 50% rule, the “charged twice” example, and 99.9% vs 82.4%.", [
        "So we added a safety check. If the model is <b>less than 50% sure</b>, the ticket is marked <b>“Needs manual review”</b>.",
        "For example, “I was charged twice” gets only 23%, because these words are rare in our data.",
        "In the test set, 74 tickets were flagged. Confident tickets are <b>99.9%</b> correct; flagged ones only <b>82.4%</b>. So the flag catches the risky ones."]),
    PageBreak(),
]

# Part 5
story += part("Part 5 · Sentiment and urgency", "Goal: how VADER scores tone, how the urgency rules work, and how well they do, honestly.")
story += [
    slide_block(20, "Sentiment with VADER", "Shashwat", "40 s", "“This is good” → “not good” → “NOT good!!!” with scores, and the score scale.", [
        "For sentiment we use <b>VADER</b>. It is a ready-made tool with a list of about 7,500 scored words, plus rules for how people write.",
        "“This is good” scores +0.44. Add “not” and it becomes −0.34. Write NOT in capitals with “!!!” and it gets stronger: −0.51.",
        "Below −0.05 we call it <b>Negative</b>; above 0.5, <b>Positive</b>. We use 0.5 because polite words like “please” make normal requests look happy."]),
    slide_block(21, "Urgency: five rules, checked in order", "Shashwat", "35 s", "Five rules, each with a real example and result.", [
        "Urgency uses <b>five rules</b>, checked in order. The first rule that matches wins.",
        "One: security, money, legal or “urgent” words → <b>High</b>. Two: a very angry tone → <b>High</b>. "
        "Three: problem words like “can’t” or “error” → <b>Medium</b>. Four: any negative tone → <b>Medium</b>. Five: everything else → <b>Low</b>.",
        "Every result shows its <b>reason</b>."]),
    slide_block(22, "Why keywords and tone together", "Shashwat", "35 s", "A calm but urgent message, and an angry message with no keyword.", [
        "Why use both? Each one alone misses something.",
        "“I need access to my account urgently” sounds calm, but the word “urgently” makes it High.",
        "“Absolutely terrible, I am furious” has no keyword, but its very negative tone makes it High. Together, they catch both."]),
    slide_block(23, "How well it works, honestly", "Shashwat", "40 s", "94%, 100%, 100% High recall; the warning; two known failures.", [
        "We had no labels, so we wrote and labelled <b>36 test messages</b> ourselves. Sentiment was <b>94%</b> correct, urgency <b>100%</b>, "
        "and <b>no urgent ticket was missed</b>.",
        "But we wrote these messages ourselves, so the numbers are <b>optimistic</b>.",
        "We know where it fails: “I was not charged twice” is still High, and sarcasm like “Great, another late delivery” is scored positive."]),
    PageBreak(),
]

# Part 6
story += part("Part 6 · Live demo", "Goal: prove the system works end to end. Aman drives the laptop. Start the app before the viva.")
story.append(slide_block(24, "Let’s see it running", "Aman", "3 min", "Demo slide for a moment, then switch to the browser.", [
    "Now let’s see it running. We’ll analyse three tickets and then look at the dashboard."]))
story.append(table([
    ["Step", "Do this", "You will see", "Say"],
    ["1", "Click <b>Hacked account</b> → Analyze ticket", "Account 90% · High (security: hacked) · Negative",
     "The category is Account, urgency High, and here is the reason: the word “hacked”."],
    ["2", "Click <b>Question</b> → Analyze ticket", "Payment 97% · Low · Neutral", "A simple question gets Low urgency. It can wait."],
    ["3", "Click <b>Double charge</b> → Analyze ticket", "Feedback 27% · yellow “Needs manual review” · High (money: charged twice)",
     "Urgency is correctly High. But the model is only 27% sure of the category, so it asks a human to check."],
    ["4", "Empty the text box → Analyze ticket", "“Please enter at least 2 words.”", "Empty input doesn’t crash the app."],
    ["5", "Scroll down to <b>Ticket dashboard</b>", "Total, High priority, % negative, needs review; three charts",
     "Every ticket is saved here. A team lead sees the totals and charts at a glance."],
    ["6", "In <b>All tickets</b>: click the <b>High</b> filter, then the review toggle, then search “refund”",
     "Table with High tickets first, then filtered results",
     "The queue puts urgent tickets first. Agents can filter and search. That’s the full system. Shashwat will now talk about the limitations."],
], [0.07, 0.26, 0.29, 0.38]))
story += [Spacer(1, 10), Paragraph(
    "<b>Avoid:</b> the <i>Late delivery</i> example gets the wrong category (it is flagged for review). If it comes up, say: "
    "“Wrong category, but low confidence, so it’s sent to a human.”", S["body"]), PageBreak()]

# Part 7
story += part("Part 7 · Limitations and conclusion", "Goal: show we know the weak points, have a plan, and can sum up in one line.")
story += [
    slide_block(25, "What it can’t do (yet)", "Shashwat", "50 s", "Six limitation cards, each with a real example.", [
        "Here is what our system can’t do yet.",
        "One, the biggest: the training data is <b>synthetic</b>, so real accuracy would be lower. Two: only <b>one category</b> per ticket. "
        "Three: our sentiment and urgency test set is <b>small and written by us</b>. Four: keyword rules don’t understand “<b>not</b>”. "
        "Five: VADER misses <b>sarcasm</b>. Six: <b>English only</b>."]),
    slide_block(26, "What we’d do next", "Shashwat", "40 s", "Three columns: data, models, system.", [
        "Each limitation points to a next step.",
        "<b>Data:</b> use real company tickets and the priorities agents give. "
        "<b>Models:</b> train a real urgency model, try DistilBERT if the data is messy, allow several categories, and handle “not”. "
        "<b>System:</b> use a database, send tickets to the right team automatically, and connect to email."]),
    slide_block(27, "Conclusion", "Shashwat", "35 s", "One-line takeaway and three numbers.", [
        "To sum up: SupportSense reads a message, predicts its category, sentiment and urgency, and puts urgent tickets first.",
        "<b>99.6%</b> category accuracy, <b>no urgent ticket missed</b> in our tests, and <b>zero crashes</b> in 18 edge-case tests.",
        "Our main point: simple, explainable NLP can sort support tickets, and it <b>knows when to ask a human</b>."]),
    slide_block(28, "Thank you", "Both", "5 s", "Thank-you slide with both names.", [
        "Thank you. We are happy to take your questions."]),
    PageBreak(),
]

# Appendix: code guide
story += part("Appendix · If they ask to see the code",
              "Open the SupportSense folder in your editor and zoom in. In VS Code, press Ctrl+G and type a line number to jump to it.")
story.append(Paragraph("<b>Start here:</b> <font name='Mono'>src/analyzer.py</font>. Its function <font name='Mono'>analyze_ticket()</font> "
                       "is the whole system in 20 lines: it checks the input, runs the three features, and returns one result.", S["body"]))
story.append(Paragraph("Code tour: if they say “walk us through the code”", S["h2"]))
story.append(table([
    ["#", "Open (file : lines)", "Point at", "Say"],
    ["1", "src/analyzer.py : 14–33", "analyze_ticket()", "The heart of the system. It calls our three features and returns one result."],
    ["2", "src/preprocessing.py : 9–18", "the three re.sub lines", "Our cleaning: lowercase, remove placeholders, numbers and extra spaces. No stop-word removal."],
    ["3", "notebooks/03_train_model.py : 45–59", "TfidfVectorizer, Pipeline, model.fit", "TF-IDF with word pairs, then Logistic Regression. One Pipeline, so TF-IDF learns from training data only."],
    ["4", "notebooks/03_train_model.py : 126", "joblib.dump", "The trained model is saved as one file, which the app loads."],
    ["5", "src/predict.py : 13, 25–35", "CONFIDENCE_THRESHOLD, predict_proba", "Get probabilities, take the highest, flag for review if below 50%."],
    ["6", "src/urgency.py : 41–65", "# Rule 1 … # Rule 5", "Five rules in order. The first match wins, always with a reason."],
    ["7", "src/sentiment.py : 15–28", "the two thresholds", "VADER gives a score; these thresholds turn it into a label."],
    ["8", "streamlit_app.py : 70–85", "the form, analyze_ticket, save_tickets", "Clicking Analyze calls the same function and saves the ticket to a CSV file."],
], [0.05, 0.37, 0.24, 0.34], mono_cols=(1, 2)))
story.append(Paragraph("When asked a specific question", S["h2"]))
story.append(table([
    ["If they ask…", "Open", "Show"],
    ["Where do you clean the text?", "src/preprocessing.py", "lines 9–18"],
    ["How did you remove duplicates and split the data?", "notebooks/02_prepare_data.py", "line 39 (drop_duplicates); lines 43–45 (train_test_split, stratify, random_state=42)"],
    ["Where is TF-IDF? What settings?", "notebooks/03_train_model.py", "lines 45–51"],
    ["Where is the model trained?", "notebooks/03_train_model.py", "lines 53–59"],
    ["How did you evaluate it?", "notebooks/03_train_model.py", "line 66 (classification_report); image reports/confusion_matrix.png"],
    ["How did you compare with SVM?", "notebooks/03_train_model.py", "line 71"],
    ["How does the confidence check work?", "src/predict.py", "lines 13 and 25–35"],
    ["Show the urgency keywords", "src/urgency.py", "lines 10–29 (HIGH_KEYWORDS, MEDIUM_KEYWORDS)"],
    ["How is urgency decided?", "src/urgency.py", "lines 41–65"],
    ["How is sentiment done?", "src/sentiment.py", "lines 15–28"],
    ["What happens with empty input?", "src/analyzer.py", "lines 11–17 (MIN_WORDS, ValueError)"],
    ["Where are tickets stored?", "src/storage.py", "lines 16–35, and the file data/tickets.csv"],
    ["Show the dashboard code", "streamlit_app.py", "lines 70–85 (input form); line 117 onward (dashboard)"],
    ["How do you know it doesn’t crash?", "notebooks/05_final_tests.py", "the cases list; run it live"],
], [0.31, 0.35, 0.34], mono_cols=(1,)))
story.append(Paragraph("Run it live in the terminal (from the SupportSense folder)", S["h2"]))
story.append(table([
    ["To do this", "Type this"],
    ["Start the dashboard", ".venv/bin/streamlit run streamlit_app.py"],
    ["Analyse any message", ".venv/bin/python -c \"from src.analyzer import analyze_ticket; print(analyze_ticket('My account was hacked'))\""],
    ["Re-run training and evaluation (about 10 s)", ".venv/bin/python notebooks/03_train_model.py"],
    ["Re-run the edge-case tests", ".venv/bin/python notebooks/05_final_tests.py"],
], [0.32, 0.68], mono_cols=(1,)))
story.append(Paragraph("Numbers to remember", S["h2"]))
story.append(table([
    ["What", "Number"],
    ["Dataset", "Bitext, 26,872 messages, 11 categories"],
    ["After removing duplicates", "23,776 (3,096 removed)"],
    ["Train / test", "19,020 / 4,756 (80/20, stratified, seed 42)"],
    ["TF-IDF features", "4,823 (words + word pairs)"],
    ["Category accuracy / macro F1", "99.6% / 0.997 · 17 mistakes"],
    ["Flagged for review (below 50%)", "74 tickets (1.6%) · 99.9% vs 82.4% correct"],
    ["Sentiment / urgency (36 messages)", "94% / 100% · High recall 100%"],
    ["Edge-case tests", "0 crashes in 18"],
], [0.45, 0.55]))


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Arial", 8)
    canvas.setFillColor(GREY)
    if doc.page > 1:
        canvas.drawString(2 * cm, 1.2 * cm, "SupportSense · Presentation Script")
        canvas.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"Page {doc.page}")
    canvas.restoreState()


doc = SimpleDocTemplate(str(OUT), pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm,
                        topMargin=1.8 * cm, bottomMargin=1.8 * cm,
                        title="SupportSense Presentation Script", author="Aman, Shashwat")
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print("Saved", OUT)
