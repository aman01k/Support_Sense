"""Draw the SupportSense architecture diagram for the report.

Run:  .venv/bin/python notebooks/06_architecture_diagram.py
Output: reports/architecture.png
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Patch  # noqa: E402

OUT = Path(__file__).resolve().parent.parent / "reports" / "architecture.png"

COLORS = {
    "data": "#e8eaed",      # data / storage / UI
    "ml": "#cfe2ff",        # trained ML model
    "pre": "#d3f2dc",       # pre-trained
    "rule": "#ffe3c2",      # business rules
    "out": "#ffffff",       # outputs
}

fig, ax = plt.subplots(figsize=(17, 9))
ax.set_xlim(0, 17)
ax.set_ylim(0, 9)
ax.axis("off")


def box(x, y, w, h, text, kind="data", bold=False):
    """Draw a box with its LEFT edge at x and vertical CENTER at y."""
    ax.add_patch(FancyBboxPatch((x, y - h / 2), w, h, boxstyle="round,pad=0.02,rounding_size=0.12",
                                fc=COLORS[kind], ec="#444", lw=1.2))
    ax.text(x + w / 2, y, text, ha="center", va="center", fontsize=10.5,
            fontweight="bold" if bold else "normal", wrap=True)


def arrow(x1, y1, x2, y2, label=None, dx=0.08, dy=0.0):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=16,
                                 lw=1.4, color="#333"))
    if label:
        ax.text((x1 + x2) / 2 + dx, (y1 + y2) / 2 + dy, label, fontsize=9, color="#555",
                ha="left", va="center", style="italic")


# ---------- Panels ----------
ax.add_patch(FancyBboxPatch((0.2, 6.85), 16.6, 1.85, boxstyle="round,pad=0.02",
                            fc="#f7f7f9", ec="#bbb", lw=1, ls="--"))
ax.text(0.4, 8.5, "TRAINING  (offline, run once)", fontsize=11, fontweight="bold", color="#555")
ax.add_patch(FancyBboxPatch((0.2, 0.35), 16.6, 6.2, boxstyle="round,pad=0.02",
                            fc="#fbfbfc", ec="#bbb", lw=1, ls="--"))
ax.text(0.4, 6.3, "PREDICTION  (live, for every new ticket)", fontsize=11, fontweight="bold", color="#555")

# ---------- Training row ----------
ty, tw, th = 7.65, 2.6, 0.95
train_steps = [
    ("Bitext dataset\n26,872 messages, 11 categories", "data"),
    ("Clean text +\nremove duplicates\n(23,776 left)", "data"),
    ("Stratified 80/20 split\ntrain 19,020 / test 4,756", "data"),
    ("Train TF-IDF +\nLogistic Regression\naccuracy 99.6%", "ml"),
    ("category_model.joblib\n(saved model)", "ml"),
]
xs = [0.4, 3.7, 7.0, 10.3, 13.6]
for (text, kind), x in zip(train_steps, xs):
    box(x, ty, tw, th, text, kind)
for x in xs[:-1]:
    arrow(x + tw, ty, x + tw + 0.7, ty)

# ---------- Prediction ----------
r1, r2, r3, bh = 5.3, 3.9, 2.4, 0.95

box(0.4, r2, 2.2, 1.2, "Customer\nsupport message", "out", bold=True)

# Branch 1: category (ML)
box(3.3, r1, 2.2, bh, "clean_text()\nlowercase, remove\nplaceholders/numbers", "data")
box(6.0, r1, 2.2, bh, "TF-IDF\nwords → numbers\n(4,823 features)", "ml")
box(8.7, r1, 2.2, bh, "Logistic\nRegression", "ml")
box(11.6, r1, 2.5, bh, "CATEGORY + confidence\n(<50% → needs review)", "out", bold=True)
arrow(5.5, r1, 6.0, r1)
arrow(8.2, r1, 8.7, r1)
arrow(10.9, r1, 11.6, r1)

# Branch 2: sentiment (pre-trained)
box(3.3, r2, 2.2, bh, "VADER\n(pre-trained lexicon\n+ rules)", "pre")
box(11.6, r2, 2.5, bh, "SENTIMENT\nPositive / Neutral / Negative", "out", bold=True)
arrow(5.5, r2, 11.6, r2, label="compound score → label", dx=-1.0, dy=0.2)

# Branch 3: urgency (rules)
box(3.3, r3, 7.6, 1.15,
    "Urgency rules (checked in order)\n"
    "1. security / money / legal / 'urgent' keywords → High    2. score ≤ −0.7 → High\n"
    "3. problem words → Medium    4. negative tone → Medium    5. otherwise → Low", "rule")
box(11.6, r3, 2.5, bh, "URGENCY + reason\nHigh / Medium / Low", "out", bold=True)
arrow(10.9, r3, 11.6, r3)
arrow(4.4, r2 - bh / 2, 4.4, r3 + 0.575, label="sentiment score")

# Message → three branches
for y in (r1, r2, r3):
    arrow(2.6, r2, 3.3, y)

# Saved model is loaded by the prediction branch
arrow(14.9, ty - th / 2, 9.8, r1 + bh / 2, label="loaded at start-up", dx=0.3, dy=-0.3)

# Storage + dashboard
box(14.6, 4.6, 2.0, 0.95, "data/tickets.csv\n(saved tickets)", "data")
box(14.6, 2.9, 2.0, 1.15, "Streamlit\ndashboard\nKPIs · charts · table", "data", bold=True)
for y in (r1, r2, r3):
    arrow(14.1, y, 14.6, 4.6)
arrow(15.6, 4.6 - 0.475, 15.6, 2.9 + 0.575)

# Legend
ax.legend(handles=[
    Patch(fc=COLORS["ml"], ec="#444", label="Trained ML model"),
    Patch(fc=COLORS["pre"], ec="#444", label="Pre-trained model"),
    Patch(fc=COLORS["rule"], ec="#444", label="Business rules"),
    Patch(fc=COLORS["data"], ec="#444", label="Data / storage / UI"),
], loc="lower left", bbox_to_anchor=(0.02, 0.05), ncol=4, frameon=False, fontsize=10)

ax.set_title("SupportSense — System Architecture", fontsize=16, fontweight="bold", pad=10)
plt.tight_layout()
plt.savefig(OUT, dpi=150, bbox_inches="tight")
print("Saved", OUT)
