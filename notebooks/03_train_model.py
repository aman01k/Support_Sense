"""Step 3: Train the category classifier (TF-IDF + Logistic Regression) and evaluate it.

Run:  .venv/bin/python notebooks/03_train_model.py
Output: models/category_model.joblib, reports/confusion_matrix.png, reports/metrics.txt
"""
import sys
from pathlib import Path

import joblib
import matplotlib
import pandas as pd

matplotlib.use("Agg")  # save plots to file without opening a window
import matplotlib.pyplot as plt  # noqa: E402
from sklearn.feature_extraction.text import TfidfVectorizer  # noqa: E402
from sklearn.linear_model import LogisticRegression  # noqa: E402
from sklearn.metrics import (  # noqa: E402
    ConfusionMatrixDisplay,
    accuracy_score,
    classification_report,
    f1_score,
)
from sklearn.pipeline import Pipeline  # noqa: E402
from sklearn.svm import LinearSVC  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))
from src.preprocessing import clean_text  # noqa: E402

DATA = ROOT / "data" / "processed"
MODELS = ROOT / "models"
REPORTS = ROOT / "reports"
MODELS.mkdir(exist_ok=True)
REPORTS.mkdir(exist_ok=True)

# 1. Load the train/test split from Phase 2
train = pd.read_csv(DATA / "train.csv")
test = pd.read_csv(DATA / "test.csv")
X_train, y_train = train["clean_text"], train["category"]
X_test, y_test = test["clean_text"], test["category"]


# 2. Build the model: TF-IDF turns text into numbers, Logistic Regression classifies them.
#    Using a Pipeline keeps both steps together, so the vectorizer is fitted on TRAIN only.
def make_tfidf():
    return TfidfVectorizer(
        ngram_range=(1, 2),   # single words + word pairs ("not working", "credit card")
        min_df=2,             # ignore words that appear in only one message
        sublinear_tf=True,    # dampen words repeated many times in one message
    )


model = Pipeline([
    ("tfidf", make_tfidf()),
    ("clf", LogisticRegression(max_iter=1000, class_weight="balanced")),
])

# 3. Train
model.fit(X_train, y_train)
print("Vocabulary size:", len(model.named_steps["tfidf"].vocabulary_))

# 4. Evaluate on the unseen test set
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
macro_f1 = f1_score(y_test, y_pred, average="macro")
report = classification_report(y_test, y_pred, digits=3)
print(f"\nAccuracy: {acc:.3f}   Macro F1: {macro_f1:.3f}\n")
print(report)

# 5. Compare against a Linear SVM (same features, different classifier)
svm = Pipeline([("tfidf", make_tfidf()), ("clf", LinearSVC(class_weight="balanced"))])
svm.fit(X_train, y_train)
svm_pred = svm.predict(X_test)
svm_acc = accuracy_score(y_test, svm_pred)
svm_f1 = f1_score(y_test, svm_pred, average="macro")
print("Model comparison:")
print(f"  Logistic Regression  acc={acc:.3f}  macroF1={macro_f1:.3f}")
print(f"  Linear SVM           acc={svm_acc:.3f}  macroF1={svm_f1:.3f}")

# 6. Confusion matrix
fig, ax = plt.subplots(figsize=(10, 8))
ConfusionMatrixDisplay.from_predictions(
    y_test, y_pred, ax=ax, cmap="Blues", xticks_rotation=45, colorbar=False
)
ax.set_title("SupportSense — Category Confusion Matrix (test set)")
plt.tight_layout()
plt.savefig(REPORTS / "confusion_matrix.png", dpi=150)
print("\nSaved confusion matrix to reports/confusion_matrix.png")

# 7. Top words per category: what the model learned (useful to explain in the viva)
vocab = model.named_steps["tfidf"].get_feature_names_out()
clf = model.named_steps["clf"]
print("\nTop 6 words per category:")
for i, label in enumerate(clf.classes_):
    top = clf.coef_[i].argsort()[-6:][::-1]
    print(f"  {label:<13} {', '.join(vocab[top])}")

# 8. Show the mistakes
errors = test[y_test != y_pred].assign(predicted=y_pred[y_test != y_pred])
print(f"\nMisclassified: {len(errors)} of {len(test)}")
print(errors[["text", "category", "predicted"]].head(10).to_string(index=False))

# 9. Try brand-new messages the model has never seen
samples = [
    "I've been charged twice for my subscription!",
    "I can't log into my account",
    "where is my package? it was supposed to arrive yesterday",
    "I want my money back for the broken headphones",
    "how do I talk to a real person?",
]
print("\nNew messages (prediction, confidence):")
for s in samples:
    probs = model.predict_proba([clean_text(s)])[0]
    print(f"  {model.classes_[probs.argmax()]:<13} {probs.max():.2f}  <- {s}")

# 10. Confidence check: how many test tickets would be sent for manual review?
THRESHOLD = 0.5
test_conf = model.predict_proba(X_test).max(axis=1)
low = test_conf < THRESHOLD
print(f"\nTest tickets below {THRESHOLD} confidence: {low.sum()} of {len(test)}")
print(f"Accuracy on confident tickets: {accuracy_score(y_test[~low], y_pred[~low]):.3f}")
if low.any():
    print(f"Accuracy on low-confidence tickets: {accuracy_score(y_test[low], y_pred[low]):.3f}")

# 11. Save the model (TF-IDF + classifier together) and the metrics
joblib.dump(model, MODELS / "category_model.joblib")
(REPORTS / "metrics.txt").write_text(
    f"Accuracy: {acc:.3f}\nMacro F1: {macro_f1:.3f}\n\n{report}\n"
    f"Linear SVM: acc={svm_acc:.3f} macroF1={svm_f1:.3f}\n"
)
print("\nSaved model to models/category_model.joblib")
