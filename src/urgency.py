"""Rule-based urgency detection: High / Medium / Low.

Our dataset has no urgency labels, so instead of training a model we use
clear business rules. Every result comes with a reason, so a support agent
(or examiner) can see exactly why a ticket got its priority.
"""
import re

# HIGH: money lost, security risk, legal threat, or the customer says it's urgent.
HIGH_KEYWORDS = {
    "security": ["hacked", "hack", "fraud", "scam", "unauthorized", "unauthorised",
                 "stolen", "compromised", "suspicious", "phishing", "identity theft",
                 "without my permission", "without permission"],
    "money": ["charged twice", "double charged", "charged me twice", "double charge",
              "deducted twice", "money deducted", "money was deducted", "overcharged",
              "wrong amount"],
    "legal": ["lawyer", "legal action", "sue", "court", "consumer forum", "police"],
    "urgent": ["urgent", "urgently", "asap", "immediately", "emergency", "right now",
               "as soon as possible"],
}

# MEDIUM: something is broken or not working, but no money/security risk.
MEDIUM_KEYWORDS = [
    "not working", "doesn't work", "does not work", "isn't working", "stopped working",
    "can't", "cannot", "can not", "unable", "error", "failed", "fail", "broken",
    "damaged", "problem", "issue", "wrong", "missing", "lost", "delayed", "late",
    "not received", "never received", "never arrived", "hasn't arrived", "not arrived",
    "still waiting", "no response", "nobody has responded", "locked out",
]

# Very negative sentiment on its own also makes a ticket High priority.
# (-0.6 flagged mild messages like "I chose a wrong address by mistake" as High.)
VERY_NEGATIVE_SCORE = -0.7


def _find(text: str, phrases: list[str]) -> list[str]:
    """Return the phrases that appear in text as whole words."""
    return [p for p in phrases if re.search(r"\b" + re.escape(p) + r"\b", text)]


def detect_urgency(text: str, sentiment_score: float = 0.0) -> dict:
    """Return {'urgency': High/Medium/Low, 'reason': why}."""
    text = (text or "").lower().replace("’", "'")

    # Rule 1: any High keyword -> High
    for group, phrases in HIGH_KEYWORDS.items():
        hits = _find(text, phrases)
        if hits:
            return {"urgency": "High", "reason": f"{group}: {', '.join(hits)}"}

    # Rule 2: very angry customer -> High
    if sentiment_score <= VERY_NEGATIVE_SCORE:
        return {"urgency": "High", "reason": f"very negative sentiment ({sentiment_score:.2f})"}

    # Rule 3: something is broken -> Medium
    hits = _find(text, MEDIUM_KEYWORDS)
    if hits:
        return {"urgency": "Medium", "reason": f"problem: {', '.join(hits)}"}

    # Rule 4: negative tone but no specific problem -> Medium
    if sentiment_score < 0:
        return {"urgency": "Medium", "reason": f"negative sentiment ({sentiment_score:.2f})"}

    # Rule 5: everything else (questions, requests, feedback) -> Low
    return {"urgency": "Low", "reason": "general request"}
