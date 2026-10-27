"""SupportSense dashboard.

Run:  .venv/bin/streamlit run streamlit_app.py
"""
from pathlib import Path

import pandas as pd
import streamlit as st

from src.analyzer import analyze_ticket
from src.storage import clear_tickets, load_tickets, save_tickets

st.set_page_config(page_title="SupportSense", page_icon=":material/support_agent:", layout="wide")

DATA = Path(__file__).resolve().parent / "data"
URGENCY_COLORS = {"High": "red", "Medium": "orange", "Low": "green"}
SENTIMENT_COLORS = {"Negative": "red", "Neutral": "gray", "Positive": "green"}
EXAMPLES = {
    "Double charge": "I've been charged twice for my subscription, and nobody has responded to my previous complaint!",
    "Login problem": "I can't log into my account, it keeps saying wrong password",
    "Hacked account": "My account was hacked and someone changed my email",
    "Late delivery": "My package hasn't arrived yet and it has been 10 days",
    "Question": "What payment methods do you accept?",
    "Praise": "Your support team was excellent, thanks for the quick help!",
}


@st.cache_data
def load_sample_pool() -> list[str]:
    """Messages used by the 'Add sample tickets' button."""
    manual = pd.read_csv(DATA / "eval" / "manual_samples.csv")["text"].tolist()
    bitext = pd.read_csv(DATA / "processed" / "test.csv")["text"].sample(200, random_state=1).tolist()
    return manual + bitext


def use_example():
    st.session_state.ticket_text = EXAMPLES[st.session_state.example]
    st.session_state.example = None


# ---------------- Sidebar ----------------
with st.sidebar:
    st.header("SupportSense")
    st.caption("AI-powered customer support ticket intelligence")

    st.subheader("Demo data")
    if st.button("Add 20 sample tickets", icon=":material/playlist_add:", width="stretch"):
        sample = pd.Series(load_sample_pool()).sample(20).tolist()
        save_tickets([analyze_ticket(t) for t in sample])
        st.toast("Added 20 sample tickets", icon=":material/check:")
    if st.button("Clear all tickets", icon=":material/delete:", width="stretch"):
        clear_tickets()
        st.session_state.pop("last_result", None)
        st.toast("All tickets cleared", icon=":material/check:")

    st.subheader("How it works")
    st.markdown(
        "1. **Category:** TF-IDF + Logistic Regression\n"
        "2. **Sentiment:** VADER (pre-trained)\n"
        "3. **Urgency:** keyword rules + sentiment\n\n"
        "Tickets below 50% category confidence are flagged for manual review."
    )

# ---------------- Analyse a ticket ----------------
st.title(":material/support_agent: SupportSense")
st.caption("Paste a customer message to predict its category, sentiment and urgency.")

st.pills("Try an example", list(EXAMPLES), key="example", on_change=use_example)

with st.form("analyze_form", clear_on_submit=False):
    text = st.text_area(
        "Customer message",
        key="ticket_text",
        height=110,
        placeholder="e.g. I was charged twice for my order and need a refund",
    )
    submitted = st.form_submit_button("Analyze ticket", type="primary", icon=":material/search:")

if submitted:
    try:
        result = analyze_ticket(text)
    except ValueError as err:
        st.warning(str(err), icon=":material/edit:")
    else:
        save_tickets([result])
        st.session_state.last_result = result

result = st.session_state.get("last_result")
if result:
    with st.container(border=True):
        st.markdown(f"**Result for:** _{result['text']}_")
        cat_col, urg_col, sent_col = st.columns(3)
        with cat_col:
            st.caption("Category")
            st.badge(result["category"], icon=":material/label:", color="blue")
            st.progress(result["confidence"], text=f"Confidence {result['confidence']:.0%}")
        with urg_col:
            st.caption("Urgency")
            st.badge(result["urgency"], icon=":material/priority_high:",
                     color=URGENCY_COLORS[result["urgency"]])
            st.caption(f"Reason: {result['urgency_reason']}")
        with sent_col:
            st.caption("Sentiment")
            st.badge(result["sentiment"], icon=":material/mood:",
                     color=SENTIMENT_COLORS[result["sentiment"]])
            st.caption(f"VADER score: {result['sentiment_score']:+.2f}")
        if result["needs_review"]:
            st.warning(
                "The model isn't confident about the category. "
                "A support agent should check this ticket.",
                title="Needs manual review",
                icon=":material/visibility:",
            )

# ---------------- Dashboard ----------------
st.header("Ticket dashboard")
tickets = load_tickets()

if tickets.empty:
    st.info(
        "No tickets yet. Analyze a message above or click **Add 20 sample tickets** in the sidebar.",
        icon=":material/inbox:",
    )
    st.stop()

# KPI row
total = len(tickets)
with st.container(horizontal=True):
    st.metric("Total tickets", total, border=True)
    st.metric("High priority", int((tickets["urgency"] == "High").sum()), border=True)
    st.metric("Negative sentiment", f"{(tickets['sentiment'] == 'Negative').mean():.0%}", border=True)
    st.metric("Needs review", int(tickets["needs_review"].sum()), border=True)

# Charts
def count_by(column: str, order: list[str] | None = None) -> pd.DataFrame:
    counts = tickets[column].astype(str).value_counts()
    if order:
        counts = counts.reindex(order, fill_value=0)
    return counts.rename_axis(column).reset_index(name="tickets")


chart_cat, chart_urg, chart_sent = st.columns(3)
with chart_cat, st.container(border=True, height="stretch"):
    st.markdown("**Tickets by category**")
    st.bar_chart(count_by("category"), x="category", y="tickets", horizontal=True,
                 sort="-tickets", height=260, alt="Number of tickets in each category")
with chart_urg, st.container(border=True, height="stretch"):
    st.markdown("**Tickets by urgency**")
    st.bar_chart(count_by("urgency", ["High", "Medium", "Low"]), x="urgency", y="tickets",
                 horizontal=True, sort=False, color="#e5484d", height=260,
                 alt="Number of tickets per urgency level")
with chart_sent, st.container(border=True, height="stretch"):
    st.markdown("**Tickets by sentiment**")
    st.bar_chart(count_by("sentiment", ["Negative", "Neutral", "Positive"]), x="sentiment",
                 y="tickets", horizontal=True, sort=False, height=260,
                 alt="Number of tickets per sentiment")

# Filters
with st.container(border=True):
    st.markdown("**All tickets** (high urgency first)")
    with st.container(horizontal=True, gap="large"):
        urg_filter = st.pills("Urgency", ["High", "Medium", "Low"], selection_mode="multi")
        sent_filter = st.pills("Sentiment", ["Negative", "Neutral", "Positive"], selection_mode="multi")
    f1, f2 = st.columns(2, vertical_alignment="bottom")
    cat_filter = f1.multiselect("Category", sorted(tickets["category"].unique()), placeholder="All")
    search = f2.text_input("Search text", placeholder="e.g. refund")
    review_only = st.toggle("Only show tickets that need manual review")

    view = tickets
    if urg_filter:
        view = view[view["urgency"].isin(urg_filter)]
    if sent_filter:
        view = view[view["sentiment"].isin(sent_filter)]
    if cat_filter:
        view = view[view["category"].isin(cat_filter)]
    if search:
        view = view[view["text"].str.contains(search, case=False, regex=False)]
    if review_only:
        view = view[view["needs_review"]]

    # One-item lists so the dataframe can show colored badges
    display = view.assign(
        urgency=view["urgency"].astype(str).map(lambda u: [u]),
        sentiment=view["sentiment"].map(lambda s: [s]),
    )
    st.caption(f"Showing {len(view)} of {total} tickets")
    st.dataframe(
        display,
        hide_index=True,
        column_order=["ticket_id", "urgency", "category", "sentiment", "text",
                      "urgency_reason", "confidence", "needs_review", "created_at"],
        column_config={
            "ticket_id": st.column_config.NumberColumn("ID", width="small"),
            "urgency": st.column_config.MultiselectColumn(
                "Urgency", options=list(URGENCY_COLORS), color=["#e5484d", "#f5a524", "#30a46c"]),
            "category": st.column_config.TextColumn("Category"),
            "sentiment": st.column_config.MultiselectColumn(
                "Sentiment", options=list(SENTIMENT_COLORS), color=["#e5484d", "#8b8d98", "#30a46c"]),
            "text": st.column_config.TextColumn("Message", width="large"),
            "confidence": st.column_config.ProgressColumn(
                "Confidence", min_value=0, max_value=1, format="percent"),
            "needs_review": st.column_config.CheckboxColumn("Review?"),
            "urgency_reason": st.column_config.TextColumn("Why this urgency"),
            "created_at": st.column_config.DatetimeColumn("Received", format="MMM DD, HH:mm"),
        },
        alt="Analysed support tickets sorted by urgency",
    )
    st.download_button(
        "Download as CSV", view.to_csv(index=False), file_name="supportsense_tickets.csv",
        icon=":material/download:",
    )
