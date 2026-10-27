"""Text cleaning shared by training and the Streamlit app.

The SAME function must be used at training time and prediction time,
otherwise the model sees differently formatted text in the app.
"""
import re


def clean_text(text: str) -> str:
    """Light cleaning only. We do NOT remove stop words or negations,
    because words like "not" and "can't" change the meaning of a ticket."""
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"\{\{.*?\}\}", " ", text)   # placeholders like {{Order Number}}
    text = re.sub(r"[#]?\d+", " ", text)       # numbers like #12588
    text = re.sub(r"\s+", " ", text).strip()   # extra spaces
    return text
