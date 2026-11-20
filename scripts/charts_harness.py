"""Charts for the primary survey (harness design) and the self-improvement survey.

Run:  python scripts/charts_harness.py
"""
from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import style as S

S.apply()
D = S.DATA_DIR
MODEL_COLOURS = {"GPT-5.3 Codex": S.BLUE, "Claude Opus 4.6": S.ORANGE,
                 "Gemini 3.1 Pro": S.AQUA, "GPT-5": S.VIOLET}


# ---------------------------------------------------------------------------
# 1. Harness axis vs model axis on Terminal-Bench 2.0
# ---------------------------------------------------------------------------
def harness_and_model_axes() -> None:
    same_model = pd.read_csv(D / "harness_tb2_same_model.csv")
    same_harness = pd.read_csv(D / "harness_tb2_same_harness.csv")
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 5.2), gridspec_kw={"width_ratios": [1.35, 1]})

    order = ["GPT-5", "Claude Opus 4.6", "Gemini 3.1 Pro", "GPT-5.3 Codex"]
    for i, model in enumerate(order):
        rows = same_model[same_model.model == model].sort_values("score")
        c = MODEL_COLOURS[model]
        a1.plot([rows.score.min(), rows.score.max()], [i, i], color=c, lw=2.2, alpha=0.35,
                solid_capstyle="round")
        a1.scatter(rows.score, [i] * len(rows), s=64, color=c, zorder=3, edgecolor="white", lw=1.5)
        lo, hi = rows.iloc[0], rows.iloc[-1]
        a1.text(lo.score - 1.0, i + 0.26, lo.harness, ha="right", fontsize=9, color=S.INK_2)
        a1.text(hi.score + 1.0, i + 0.26, hi.harness, ha="left", fontsize=9, color=S.INK_2)
        a1.text(101, i, f"+{hi.score - lo.score:.1f} pts", ha="right", va="center",
                fontsize=10.5, fontweight="bold", color=S.INK)
    a1.set_yticks(range(len(order)), order)
    a1.set_ylim(-0.6, len(order) - 0.3)
    a1.set_xlim(25, 101)
    a1.grid(axis="y", visible=False)
    a1.set_xlabel("Terminal-Bench 2.0 accuracy (%)")
    a1.set_title("Same model, different harness", fontsize=12.5)

    for harness, colour in [("Terminus 2", S.INK_2), ("Codex CLI", S.BLUE)]:
        rows = same_harness[same_harness.harness == harness].sort_values("generation_order")
        a2.plot(rows.generation_order, rows.score, color=colour, lw=2, marker="o", ms=7,
                markeredgecolor="white", markeredgewidth=1.5)
        for _, r in rows.iterrows():
            a2.text(r.generation_order, r.score + 2.4, f"{r.model}\n{r.score:.1f}%", ha="center",
                    fontsize=8.6, color=S.INK_2, linespacing=1.1)
        last = rows.iloc[-1]
        a2.text(3.18, last.score, harness, va="center", fontsize=10.5, fontweight="bold", color=colour)
    a2.set_xlim(0.6, 3.9)
    a2.set_ylim(25, 95)
    a2.set_xticks([1, 2, 3], ["older model", "newer", "newest"])
    a2.grid(axis="x", visible=False)
    a2.set_ylabel("Terminal-Bench 2.0 accuracy (%)")
    a2.set_title("Same harness, newer model", fontsize=12.5)

    S.header(fig, "Comparable levers: a harness swap moves a model 14-21 pts; one model step adds 11-19",
             "Public Terminal-Bench 2.0 results compiled in the harness survey (5 trials per task, official leaderboard)")
    fig.tight_layout()
    S.source(fig, "Data: Guo et al., \"From Question Answering to Task Completion\" (arXiv 2606.20683), "
                  "Table 8 and Sec. 7.3. Observational leaderboard data, not a controlled ablation.")
    S.save(fig, "harness_vs_model_tb2")


# ---------------------------------------------------------------------------
# 2. What does a better harness cost? Tokens vs accuracy vs timeouts
# ---------------------------------------------------------------------------
LABEL_OFFSETS = {
    ("GPT-5.3 Codex", "Terminus 2"): (-10, 26, "right"),
    ("GPT-5.3 Codex", "Mux"): (-10, 26, "right"),
    ("Gemini 3.1 Pro", "Terminus-KIRA"): (10, -6, "left"),
}


def cost_of_harness() -> None:
    df = pd.read_csv(D / "harness_tb2_same_model.csv").dropna(subset=["input_k"])
    fig, ax = plt.subplots(figsize=(11, 5))
    for model, rows in df.groupby("model"):
        rows = rows.sort_values("input_k")
        c = MODEL_COLOURS[model]
        ax.plot(rows.input_k, rows.score, color=c, lw=1.6, alpha=0.5)
        ax.scatter(rows.input_k, rows.score, s=40 + rows.timeout_pct * 9, color=c, alpha=0.9,
                   edgecolor="white", lw=1.5, zorder=3, label=model)
        for _, r in rows.iterrows():
            dx, dy, ha = LABEL_OFFSETS.get((model, r.harness), (9, -4, "left"))
            ax.annotate(f"{r.harness}\n{r.timeout_pct:.1f}% timeouts", (r.input_k, r.score),
                        textcoords="offset points", xytext=(dx, dy), fontsize=8.6, color=S.INK_2,
                        va="top", ha=ha)
    ax.set_xscale("log")
    ax.set_xticks([50, 100, 200, 400, 800], ["50K", "100K", "200K", "400K", "800K"])
    ax.minorticks_off()
    ax.set_xlim(40, 1300)
    ax.set_ylim(60, 78.5)
    ax.set_xlabel("Median input tokens per trial (log scale)")
    ax.set_ylabel("Terminal-Bench 2.0 accuracy (%)")
    ax.legend(loc="lower right", title="Bubble size = timeout rate", title_fontsize=9.5)
    S.header(fig, "Better harnesses buy accuracy with context: up to ~10x the input tokens",
             "Same model, different harness. The extra tokens often come with fewer timeouts, not more")
    S.source(fig, "Data: arXiv 2606.20683, Table 8 (median per-trial tokens, timeout rate; 445 trials per row). "
                  "Rows without token data omitted.")
    S.save(fig, "harness_cost_tradeoff")


# ---------------------------------------------------------------------------
# 3. WebArena: how much a browser harness adds to a bare model
# ---------------------------------------------------------------------------
def webarena_lift() -> None:
    df = pd.read_csv(D / "harness_webarena.csv").sort_values("harness_high")
    fig, ax = plt.subplots(figsize=(11, 4.8))
    y = np.arange(len(df))
    ax.hlines(y, df.model_only, df.harness_high, color=S.SEQ_BLUE[2], lw=3, alpha=0.7)
    ax.scatter(df.model_only, y, s=60, color=S.DE_EMPHASIS, zorder=3, edgecolor="white", lw=1.5,
               label="Model only (no harness)")
    ax.scatter(df.harness_high, y, s=70, color=S.BLUE, zorder=3, edgecolor="white", lw=1.5,
               label="Best reported harness")
    for yi, (_, r) in zip(y, df.iterrows()):
        name = "" if r.best_harness.startswith("(") else f"  ({r.best_harness})"
        ax.text(r.harness_high + 1.2, yi, f"+{r.harness_high - r.model_only:.1f} pts{name}",
                va="center", fontsize=9.5, color=S.INK_2)
    ax.set_yticks(y, df.backbone)
    ax.set_xlim(0, 80)
    ax.grid(axis="y", visible=False)
    ax.set_xlabel("WebArena task success (%)")
    ax.legend(loc="lower right")
    S.header(fig, "On the web, the harness can multiply a small model's success rate several times over",
             "Bare model vs the strongest harness reported for the same backbone")
    S.source(fig, "Data: arXiv 2606.20683, Table 9. Systems differ in more than the harness "
                  "(e.g. search budget, training), so read the lifts as upper bounds.")
    S.save(fig, "webarena_harness_lift")


# ---------------------------------------------------------------------------
# 4. A harness that rewrites itself: Darwin Gödel Machine
# ---------------------------------------------------------------------------
def dgm() -> None:
    df = pd.read_csv(D / "self_improvement_dgm.csv")
    fig, ax = plt.subplots(figsize=(8, 4.2))
    x = np.arange(len(df))
    w = 0.34
    ax.bar(x - w / 2, df.before_pct, w, color=S.DE_EMPHASIS, label="Initial coding agent")
    ax.bar(x + w / 2, df.after_pct, w, color=S.GREEN, label="After open-ended self-modification")
    for xi, b, a in zip(x, df.before_pct, df.after_pct):
        ax.text(xi - w / 2, b + 1, f"{b:.1f}%", ha="center", fontsize=10.5, color=S.INK_2)
        ax.text(xi + w / 2, a + 1, f"{a:.1f}%", ha="center", fontsize=10.5, color=S.INK, fontweight="bold")
    ax.set_xticks(x, df.benchmark)
    ax.set_ylim(0, 60)
    ax.grid(axis="x", visible=False)
    ax.set_ylabel("Solved (%)")
    ax.legend(loc="upper right")
    S.header(fig, "Same frozen model, self-edited harness: 2.5x on SWE-bench",
             "Darwin Gödel Machine rewrites its own agent code; each variant is benchmark-validated and kept in an open-ended archive")
    S.source(fig, "Data: Zhang et al., Darwin Gödel Machine (arXiv 2505.22954, abstract), a system reviewed "
                  "in the self-improvement survey (arXiv 2607.13104, Sec. 6.4).")
    S.save(fig, "dgm_self_improvement")


# ---------------------------------------------------------------------------
# 5. Agent memory: everyone writes and reads, few forget
# ---------------------------------------------------------------------------
def memory_crud() -> None:
    df = pd.read_csv(D / "memory_crud_coverage.csv").iloc[::-1]
    fig, ax = plt.subplots(figsize=(10.5, 4.2))
    y = np.arange(len(df))
    ax.barh(y, df.primary, color=S.BLUE, height=0.6, label="Primary mechanism")
    ax.barh(y, df.secondary, left=df.primary + 0.12, color=S.SEQ_BLUE[1], height=0.6,
            label="Secondary")
    ax.barh(y, df.absent_or_unclear, left=df.primary + df.secondary + 0.24, color="#f0efec",
            height=0.6, label="Absent or unclear")
    for yi, (_, r) in zip(y, df.iterrows()):
        ax.text(25.6, yi, f"{r.absent_or_unclear} of 25 lack it", va="center", fontsize=10,
                color=S.INK if r.absent_or_unclear >= 10 else S.INK_2,
                fontweight="bold" if r.absent_or_unclear >= 10 else "normal")
    ax.set_yticks(y, df.operation)
    ax.set_xlim(0, 31)
    ax.set_xticks([0, 5, 10, 15, 20, 25])
    ax.grid(axis="y", visible=False)
    ax.set_xlabel("Number of the 25 memory systems tabulated in the survey")
    ax.legend(loc="lower left", bbox_to_anchor=(0, 1.0), ncol=3, frameon=False)
    S.header(fig, "Agent memory writes and reads, but rarely deletes",
             "How strongly 25 published memory systems implement each memory operation", )
    S.source(fig, "Data: Ren et al., \"Self-Improvements in Modern Agentic Systems\" (arXiv 2607.13104), "
                  "Table 4, counted from the rendered table.")
    S.save(fig, "memory_crud_coverage")




# ---------------------------------------------------------------------------
# 6. Live leaderboard reality check (snapshot taken 2026-11-19)
# ---------------------------------------------------------------------------
def leaderboard_reality_check() -> None:
    board = pd.read_csv(D / "live_tb2_opus46_harnesses.csv").sort_values("score")
    flips = pd.read_csv(D / "live_harness_ranking_flips.csv")
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12.5, 5), gridspec_kw={"width_ratios": [1, 1.1]})

    y = np.arange(len(board))
    colours = [S.ORANGE if h == "Claude Code" else (S.INK_2 if h == "Terminus 2" else S.BLUE)
               for h in board.harness]
    a1.barh(y, board.score, color=colours, height=0.62)
    ci = board.ci95_halfwidth.fillna(0)
    a1.errorbar(board.score, y, xerr=ci, fmt="none", ecolor=S.INK, elinewidth=1, capsize=0, alpha=0.6)
    for yi, s in zip(y, board.score):
        a1.text(s + 3.2, yi, f"{s:.1f}", va="center", fontsize=9.5, color=S.INK_2)
    a1.set_yticks(y, board.harness)
    a1.set_xlim(0, 90)
    a1.grid(axis="y", visible=False)
    a1.set_xlabel("Accuracy (%), whisker = 95% CI as shown on the board")
    a1.set_title("Claude Opus 4.6 under nine harnesses (TB 2.0)", fontsize=12)

    yy = np.arange(len(flips))[::-1]
    for yi, (_, r) in zip(yy, flips.iterrows()):
        a2.plot([r.vendor_score, r.terminus2_score], [yi, yi], color=S.RULE, lw=2.5, zorder=1)
        a2.scatter(r.vendor_score, yi, s=80, color=S.ORANGE, zorder=3, edgecolor="white", lw=1.5,
                   label="Vendor's own harness (Claude Code / Codex)" if yi == yy[0] else None)
        a2.scatter(r.terminus2_score, yi, s=80, color=S.INK_2, zorder=3, edgecolor="white", lw=1.5,
                   label="Terminus 2 (neutral reference harness)" if yi == yy[0] else None)
        winner = "vendor wins" if r.vendor_score > r.terminus2_score else "Terminus 2 wins"
        a2.text(91, yi, f"{winner}\n{abs(r.vendor_score - r.terminus2_score):.1f} pts",
                va="center", ha="right", fontsize=9, color=S.INK, linespacing=1.15)
    a2.set_yticks(yy, flips.condition)
    a2.set_xlim(50, 92)
    a2.set_ylim(-0.7, len(flips) - 0.3)
    a2.grid(axis="y", visible=False)
    a2.set_xlabel("Terminal-Bench accuracy (%)")
    a2.legend(loc="upper center", bbox_to_anchor=(0.45, -0.17), ncol=1, fontsize=9.5)
    a2.set_title("Which harness wins depends on version and referee", fontsize=12)

    S.header(fig, "Leaderboard reality check: harness rankings are not stable facts",
             "Public Terminal-Bench boards and re-runs, snapshot taken 19 Nov 2026")
    fig.tight_layout()
    S.source(fig, "Sources: tbench.ai leaderboards (TB 2.0, TB 2.1), tbench.ai 'Terminal-Bench 2.1' post (May 2026), "
                  "vals.ai Terminal-Bench 2.1 page (updated 1 Oct 2026). Effort settings differ across rows.")
    S.save(fig, "leaderboard_reality_check")


if __name__ == "__main__":
    harness_and_model_axes()
    cost_of_harness()
    webarena_lift()
    dgm()
    memory_crud()
    leaderboard_reality_check()
