"""Charts built from numbers reported inside the surveys themselves.

Every value is read from a CSV in data/, and each CSV names the table it was
copied from. Run:  python scripts/charts_papers.py
"""
from __future__ import annotations

import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

import style as S

S.apply()
D = S.DATA_DIR


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """95% Wilson score interval for a binomial proportion, in percent."""
    p = k / n
    den = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / den
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return 100 * (centre - half), 100 * (centre + half)


# ---------------------------------------------------------------------------
# 1. Same model, three harnesses (Terminal Agents survey, Table 5 / Table 11)
# ---------------------------------------------------------------------------
def harness_vs_model() -> None:
    df = pd.read_csv(D / "terminal_matched_runs.csv")
    systems = ["mini-SWE-agent", "OpenHands", "SWE-agent"]
    models = {"DeepSeek-V4-Flash": S.BLUE, "DeepSeek-V4-Pro": S.ORANGE}
    benches = ["Claw-SWE-Bench Lite", "SWE-bench Lite"]

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.6), sharex=True)
    for ax, bench in zip(axes, benches):
        sub = df[df.benchmark == bench].copy()
        n = int(sub.n_tasks.iloc[0])
        for i, system in enumerate(systems):
            rows = sub[sub.system == system]
            for j, (model, colour) in enumerate(models.items()):
                r = rows[rows.model == model].iloc[0]
                lo, hi = wilson(int(r.resolved), n)
                y = i + (0.14 if j == 0 else -0.14)
                ax.plot([lo, hi], [y, y], color=colour, lw=1.4, alpha=0.45,
                        solid_capstyle="round")
                ax.scatter(r.resolved_pct, y, s=70, color=colour, zorder=3,
                           edgecolor="white", linewidth=1.5,
                           label=model if (i == 0 and bench == benches[0]) else None)
        ax.set_yticks(range(len(systems)), systems)
        ax.set_ylim(-0.6, len(systems) - 0.4)
        ax.set_xlim(35, 90)
        ax.grid(axis="y", visible=False)
        ax.set_xlabel("Resolved tasks (%)  ·  dot = score, line = 95% Wilson CI")
        ax.set_title(f"{bench}  (n = {n})", fontsize=12.5)
        # spreads computed from integer counts so they match the paper exactly
        harness = sub.groupby("model").resolved.agg(lambda s: s.max() - s.min()).max() * 100 / n
        model_tier = sub.groupby("system").resolved.agg(lambda s: s.max() - s.min()).max() * 100 / n
        ax.text(0.0, -0.34, f"Harness gap: up to {harness:.2f} pts     Model-tier gap: at most {model_tier:.2f} pts",
                transform=ax.transAxes, fontsize=10.5, color=S.INK, fontweight="bold")
    fig.legend(*axes[0].get_legend_handles_labels(), loc="upper left", bbox_to_anchor=(0.01, 0.975),
               ncol=2, handletextpad=0.3, columnspacing=1.4, fontsize=10)
    S.header(fig, "Swapping the harness moved scores far more than upgrading the model")
    fig.tight_layout(rect=(0, 0, 1, 0.9))
    S.source(fig, "Data: Bin et al., \"Terminal Agents\" survey (arXiv 2608.20485), Tables 5 and 11. "
                  "One run per task; CIs computed here from the paired counts.")
    S.save(fig, "terminal_harness_vs_model")


# ---------------------------------------------------------------------------
# 2. Same agent, four benchmark families: process profile (Table 4)
# ---------------------------------------------------------------------------
def benchmark_profile() -> None:
    df = pd.read_csv(D / "terminal_benchmark_profile.csv").set_index("benchmark")
    cols = {
        "outcome": "Outcome\n(official)",
        "P2_helpful_feedback_use": "Uses feedback\nhelpfully",
        "P5_final_window_verification": "Verifies near\nthe end",
        "P6_successful_recovery": "Recovers after\na failure",
        "P3_env_cmd_nonzero_exit": "Env. command\nfails",
        "P4_state_tracking_error": "State-tracking\nerror",
        "P7_governance_review_trigger": "Governance\nreview trigger",
    }
    m = df[list(cols)].to_numpy()
    fig, ax = plt.subplots(figsize=(11, 3.9))
    blue = ListedColormap(S.SEQ_BLUE)
    orange = ListedColormap(S.SEQ_ORANGE)
    good = np.ma.masked_where(np.arange(m.shape[1])[None, :].repeat(m.shape[0], 0) >= 4, m)
    bad = np.ma.masked_where(np.arange(m.shape[1])[None, :].repeat(m.shape[0], 0) < 4, m)
    ax.imshow(good, cmap=blue, vmin=0, vmax=100, aspect="auto")
    ax.imshow(bad, cmap=orange, vmin=0, vmax=30, aspect="auto")
    for i in range(m.shape[0]):
        for j in range(m.shape[1]):
            v = m[i, j]
            dark = v >= 55 if j < 4 else v >= 18
            ax.text(j, i, f"{v:.1f}%", ha="center", va="center", fontsize=10.5,
                    color="white" if dark else S.INK)
    ax.set_xticks(range(len(cols)), cols.values(), fontsize=9.5)
    ax.set_yticks(range(len(df)), [f"{b}  ({t} tasks)" for b, t in zip(df.index, df.tasks)])
    ax.tick_params(length=0)
    ax.grid(False)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.axvline(0.5, color="white", lw=4)
    ax.axvline(3.5, color="white", lw=4)
    S.header(fig, "One agent, four benchmarks: each one exposes a different weakness",
             "mini-SWE-agent + DeepSeek-V4-Flash.  Blue columns: higher is better.  "
             "Orange columns: friction signals (lower is smoother).")
    S.source(fig, "Data: Bin et al. (arXiv 2608.20485), Table 4. Feedback, state and recovery "
                  "columns are LLM-judge assisted; LongCLI-Bench has only 21 tasks.")
    S.save(fig, "terminal_benchmark_profile")


# ---------------------------------------------------------------------------
# 3. What each benchmark can actually see (Table 3 observability matrix)
# ---------------------------------------------------------------------------
def observability() -> None:
    df = pd.read_csv(D / "terminal_observability.csv").set_index("benchmark")
    code = {"E": 3, "T": 2, "I": 1, "-": 0}
    m = df.apply(lambda col: col.map(code)).to_numpy(dtype=int)
    colours = ["#f4f4f2", S.SEQ_BLUE[1], S.SEQ_BLUE[3], S.SEQ_BLUE[6]]
    fig, ax = plt.subplots(figsize=(11, 5.6))
    ax.imshow(m, cmap=ListedColormap(colours), vmin=-0.5, vmax=3.5, aspect="auto")
    for i in range(m.shape[0]):
        for j in range(m.shape[1]):
            ax.text(j, i, df.iloc[i, j].replace("-", "–"), ha="center", va="center",
                    fontsize=10, color="white" if m[i, j] >= 2 else S.INK_2,
                    fontweight="bold" if m[i, j] == 3 else "normal")
    ax.set_xticks(range(df.shape[1]), [c.replace(" ", "\n") for c in df.columns], fontsize=9.5)
    ax.set_yticks(range(len(df)), df.index, fontsize=10)
    ax.tick_params(length=0)
    ax.xaxis.tick_top()
    ax.grid(False)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xticks(np.arange(-0.5, df.shape[1]), minor=True)
    ax.set_yticks(np.arange(-0.5, len(df)), minor=True)
    ax.grid(which="minor", color="white", linewidth=2)
    ax.tick_params(which="minor", length=0)
    handles = [Patch(facecolor=colours[3], label="E  explicitly scored"),
               Patch(facecolor=colours[2], label="T  visible in traces, unscored"),
               Patch(facecolor=colours[1], label="I  incidental"),
               Patch(facecolor=colours[0], edgecolor=S.RULE, label="–  not observable")]
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.45, -0.02), ncol=4,
              fontsize=9.5, handlelength=1.2)
    S.header(fig, "Governance is the blind spot: only one benchmark family scores it",
             "Which of the seven terminal competences each benchmark can observe (plus task freshness)")
    S.source(fig, "Data: Bin et al. (arXiv 2608.20485), Table 3. Coding is the authors' qualitative judgement.")
    S.save(fig, "terminal_observability")


# ---------------------------------------------------------------------------
# 4. Lifecycle coverage vs real-world evidence (SE-for-agents survey)
# ---------------------------------------------------------------------------
def lifecycle_evidence() -> None:
    df = pd.read_csv(D / "se_lifecycle_stages.csv")
    order = ["Requirements Engineering", "Architecture & Design", "Implementation & Integration",
             "Testing & Assurance", "Maintenance & Evolution"]
    df = df.set_index("stage").loc[order][::-1]
    fig, ax = plt.subplots(figsize=(11, 4.2))
    y = np.arange(len(df))
    rest = df.contributions - df.e3_e4_contributions
    ax.barh(y, df.e3_e4_contributions, color=S.ORANGE, height=0.58,
            label="Evidence from real projects or production (E3/E4)")
    ax.barh(y, rest, left=df.e3_e4_contributions + 0.8, color=S.SEQ_BLUE[2], height=0.58,
            label="Lab / benchmark evidence or unevaluated")
    for yi, (tot, e) in enumerate(zip(df.contributions, df.e3_e4_contributions)):
        ax.text(tot + 4, yi, f"{tot} contributions  ·  {e} real-world ({100 * e / tot:.0f}%)",
                va="center", fontsize=10, color=S.INK_2)
    ax.set_yticks(y, df.index)
    ax.set_xlim(0, 360)
    ax.grid(axis="y", visible=False)
    ax.set_xlabel("Lifecycle contributions coded in the survey (570 across 355 papers)")
    ax.legend(loc="lower right", fontsize=9.5)
    S.header(fig, "Agent research piles up in testing; real-world evidence is a sliver everywhere",
             "Contributions per software-lifecycle stage, split by strength of evidence")
    S.source(fig, "Data: Ge et al., \"Software Engineering for LLM-Based Agents\" (arXiv 2611.23260), "
                  "stage syntheses and Table 12 (E2/E3/E4 = 464/14/23).")
    S.save(fig, "se_lifecycle_evidence")


# ---------------------------------------------------------------------------
# 5. The field's growth curve, as seen by two of the surveys' own corpora
# ---------------------------------------------------------------------------
def corpus_growth() -> None:
    df = pd.read_csv(D / "corpus_by_year.csv")
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.6), sharey=False)
    for ax, (name, colour) in zip(axes, [("Terminal Agents (2608.20485)", S.BLUE),
                                         ("SE for LLM Agents (2611.23260)", S.AQUA)]):
        sub = df[df.survey == name]
        x = np.arange(len(sub))
        bars = ax.bar(x, sub.papers, color=colour, width=0.6)
        ax.bar(x[-1], sub.papers.iloc[-1], color=colour, width=0.6, hatch="///",
               edgecolor="white", linewidth=0)
        for xi, v in zip(x, sub.papers):
            ax.text(xi, v + max(sub.papers) * 0.03, str(v), ha="center", fontsize=10.5,
                    color=S.INK)
        ax.set_xticks(x, sub.year)
        ax.grid(axis="x", visible=False)
        ax.set_ylim(0, max(sub.papers) * 1.18)
        ax.set_title(name.split(" (")[0] + " survey corpus", fontsize=12)
        ax.text(x[-1], -max(sub.papers) * 0.2, sub.note.iloc[-1], ha="center", fontsize=8.5,
                color=S.INK_3)
    S.header(fig, "Most of what we know about agent engineering is less than a year old",
             "Papers per release year in each survey's coded literature corpus")
    S.source(fig, "Papers per release year in each survey's coded corpus. Hatched bar = partial year. "
                  "Sources: arXiv 2608.20485 Table 6; arXiv 2611.23260 Sec. 3.5.")
    fig.tight_layout()
    S.save(fig, "corpus_growth")


if __name__ == "__main__":
    harness_vs_model()
    benchmark_profile()
    observability()
    lifecycle_evidence()
    corpus_growth()
