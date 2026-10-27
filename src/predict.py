"""Load the trained category model and predict for a new ticket.
Used by the Streamlit app."""
from pathlib import Path

import joblib

from src.preprocessing import clean_text

MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "category_model.joblib"

# Below this confidence the ticket is flagged for a human to check.
# Words the model never saw in training (e.g. "charged twice") give ~20% confidence.
CONFIDENCE_THRESHOLD = 0.5

_model = None


def load_model():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model


def predict_category(text: str) -> dict:
    """Return {'category', 'confidence', 'needs_review'} for one message."""
    model = load_model()
    probs = model.predict_proba([clean_text(text)])[0]
    best = probs.argmax()
    confidence = float(probs[best])
    return {
        "category": model.classes_[best],
        "confidence": confidence,
        "needs_review": confidence < CONFIDENCE_THRESHOLD,
    }
