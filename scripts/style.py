"""Shared look-and-feel for every figure in this repo.

One palette, one font stack, one set of mark rules, so the article, README and
slide deck read as a single system. Categorical colours come from a palette
validated for colour-vision deficiency (adjacent-pair CVD delta-E >= 8), and
are always assigned in this fixed order, never cycled.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import font_manager

ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "figures"
DATA_DIR = ROOT / "data"

# ---- colour tokens ---------------------------------------------------------
SURFACE = "#ffffff"
INK = "#0b0b0b"          # primary text
INK_2 = "#52514e"        # secondary text
INK_3 = "#8a8985"        # muted text / captions
GRID = "#e6e5e1"         # hairline grid
RULE = "#c9c8c3"         # axis rule

# categorical slots, fixed order (identity, never rank)
BLUE, ORANGE, AQUA, YELLOW, MAGENTA, GREEN, VIOLET, RED = (
    "#2a78d6", "#eb6834", "#1baf7a", "#eda100",
    "#e87ba4", "#008300", "#6250d6", "#e34948",
)
SERIES = [BLUE, ORANGE, AQUA, YELLOW, MAGENTA, GREEN, VIOLET, RED]

# single-hue sequential ramp (blue), light -> dark
SEQ_BLUE = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#2a78d6",
            "#1c5cab", "#184f95", "#0d366b"]

# tints used as quiet card fills in diagrams
TINT = {
    BLUE: "#eaf2fc", ORANGE: "#fdefe9", AQUA: "#e7f7f1", YELLOW: "#fdf5e1",
    MAGENTA: "#fcf0f5", GREEN: "#e5f3e5", VIOLET: "#efedfb", RED: "#fcecec",
}
NEUTRAL_FILL = "#f4f4f2"
DE_EMPHASIS = "#c9c8c3"   # grey for "the rest" when one bar is highlighted


def _pick_font() -> str:
    available = {f.name for f in font_manager.fontManager.ttflist}
    for name in ("Arial", "Helvetica", "DejaVu Sans"):
        if name in available:
            return name
    return "DejaVu Sans"


FONT = _pick_font()


def apply() -> None:
    """Install the house style into matplotlib's rcParams."""
    mpl.rcParams.update({
        "font.family": FONT,
        "font.size": 11,
        "figure.facecolor": SURFACE,
        "axes.facecolor": SURFACE,
        "savefig.facecolor": SURFACE,
        "axes.edgecolor": RULE,
        "axes.linewidth": 0.8,
        "axes.labelcolor": INK_2,
        "axes.titlecolor": INK,
        "axes.titlesize": 15,
        "axes.titleweight": "bold",
        "axes.titlelocation": "left",
        "axes.titlepad": 14,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "axes.axisbelow": True,
        "grid.color": GRID,
        "grid.linewidth": 0.8,
        "grid.linestyle": "-",
        "xtick.color": INK_2,
        "ytick.color": INK_2,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.frameon": False,
        "legend.fontsize": 10,
        "lines.linewidth": 2,
        "figure.dpi": 110,
        "savefig.dpi": 220,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.25,
    })


def subtitle(ax, text: str) -> None:
    """A one-line grey subtitle under the bold left-aligned title."""
    ax.text(0, 1.015, text, transform=ax.transAxes, ha="left", va="bottom",
            fontsize=10.5, color=INK_2)


def source(fig, text: str) -> None:
    """Source line in the bottom-left corner of the figure."""
    fig.text(0.01, -0.02, text, ha="left", va="top", fontsize=8.5, color=INK_3)


def save(fig, name: str, sub: str = "charts") -> Path:
    out = FIG_DIR / sub / f"{name}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out)
    plt.close(fig)
    print(f"wrote {out.relative_to(ROOT)}")
    return out


SEQ_ORANGE = ["#fde3d8", "#fac6b1", "#f5a585", "#f08a62", "#eb6834", "#c9521f", "#a3401a"]


def header(fig, title: str, sub: str | None = None) -> None:
    """Figure-level, left-aligned bold title plus optional grey subtitle.

    Placed above the axes area so it never collides with panel titles; the
    tight bounding box at save time pulls it into the image.
    """
    fig.text(0.01, 1.075 if sub else 1.03, title, ha="left", va="bottom",
             fontsize=15, fontweight="bold", color=INK)
    if sub:
        fig.text(0.01, 1.02, sub, ha="left", va="bottom", fontsize=10.5, color=INK_2)
