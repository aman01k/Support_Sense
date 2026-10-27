"""Sentiment analysis with VADER, a pre-trained rule-based analyser.

VADER uses a dictionary of ~7,500 words, each scored from very negative to
very positive, plus rules for negation ("not good"), intensifiers ("extremely"),
CAPITALS and "!!!". It gives a 'compound' score from -1 (very negative)
to +1 (very positive). No training data needed.
"""
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

_analyzer = SentimentIntensityAnalyzer()

# Support messages are often polite ("please", "thanks") without being happy,
# which pushes VADER slightly positive. So we need a HIGHER bar for Positive
# than the usual 0.05, while any clear negativity counts as Negative.
POSITIVE_THRESHOLD = 0.5
NEGATIVE_THRESHOLD = -0.05


def analyze_sentiment(text: str) -> dict:
    """Return {'sentiment': Positive/Neutral/Negative, 'score': compound}."""
    score = _analyzer.polarity_scores(text or "")["compound"]
    if score >= POSITIVE_THRESHOLD:
        label = "Positive"
    elif score <= NEGATIVE_THRESHOLD:
        label = "Negative"
    else:
        label = "Neutral"
    return {"sentiment": label, "score": score}
