"""SupportSense engine: runs all three features on one ticket.

    text ──► category model (ML) ──► category + confidence
         ──► VADER                ──► sentiment
         ──► urgency rules        ──► urgency + reason
"""
from src.predict import predict_category
from src.sentiment import analyze_sentiment
from src.urgency import detect_urgency

MIN_WORDS = 2


def analyze_ticket(text: str) -> dict:
    """Analyse one support message. Raises ValueError for empty/too-short input."""
    text = (text or "").strip()
    if len(text.split()) < MIN_WORDS:
        raise ValueError(f"Please enter at least {MIN_WORDS} words.")

    category = predict_category(text)
    sentiment = analyze_sentiment(text)
    urgency = detect_urgency(text, sentiment["score"])

    return {
        "text": text,
        "category": category["category"],
        "confidence": round(category["confidence"], 3),
        "needs_review": category["needs_review"],
        "sentiment": sentiment["sentiment"],
        "sentiment_score": round(sentiment["score"], 3),
        "urgency": urgency["urgency"],
        "urgency_reason": urgency["reason"],
    }
