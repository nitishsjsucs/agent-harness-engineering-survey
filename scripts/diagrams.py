"""Explanatory diagrams (taxonomies, architectures, loops), drawn with matplotlib.

Each diagram restates a survey's structure in my own layout and words; the
caption under each one names the section it summarises.
Run:  python scripts/diagrams.py
"""
from __future__ import annotations

import math
import textwrap

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch

import style as S

S.apply()


# ---------------------------------------------------------------------------
# drawing helpers
# ---------------------------------------------------------------------------
def canvas(w: float, h: float, xmax: float = 100, ymax: float | None = None):
    fig, ax = plt.subplots(figsize=(w, h))
    ymax = ymax if ymax is not None else xmax * h / w
    ax.set_xlim(0, xmax)
    ax.set_ylim(0, ymax)
    ax.axis("off")
    ax.set_aspect("equal")
    return fig, ax


def box(ax, x, y, w, h, fill="#ffffff", edge=None, lw=1.2, r=1.2, z=1):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                       facecolor=fill, edgecolor=edge or fill, linewidth=lw, zorder=z)
    ax.add_patch(p)
    return p


def text(ax, x, y, s, size=10, color=S.INK, weight="normal", ha="left", va="top", wrap=None,
         z=5, style="normal", ls=1.25):
    if wrap:
        s = "\n".join(textwrap.fill(par, wrap) for par in s.split("\n"))
    return ax.text(x, y, s, fontsize=size, color=color, fontweight=weight, ha=ha, va=va,
                   zorder=z, linespacing=ls, fontstyle=style)


def arrow(ax, x1, y1, x2, y2, color=S.INK_3, lw=1.6, style="-|>", ls="-", rad=0.0, z=2, ms=14):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=ms, color=color,
                        lw=lw, linestyle=ls, connectionstyle=f"arc3,rad={rad}", zorder=z)
    ax.add_patch(a)
    return a


def chip(ax, x, y, s, colour, size=8.6):
    """Small monospace tag, the deck's visual motif."""
    t = ax.text(x, y, s, fontsize=size, family="monospace", color=colour, ha="left", va="center",
                zorder=6, bbox=dict(boxstyle="round,pad=0.28,rounding_size=0.5",
                                    fc=S.TINT.get(colour, S.NEUTRAL_FILL), ec="none"))
    return t


# ---------------------------------------------------------------------------
# D1. Agent = Model + Harness (hero image)
# ---------------------------------------------------------------------------
COMPONENTS = [
    ("Observation", "what the model gets to see", ["output shaping", "filtering", "screenshots/DOM"], S.BLUE),
    ("Context", "what enters the window, when", ["compaction", "retrieval", "skills on demand"], S.VIOLET),
    ("Control loop", "who acts next, when to stop", ["plan-act-verify", "sub-agents", "routing"], S.ORANGE),
    ("Action", "what the agent may do", ["tool schemas", "MCP", "shell / code"], S.AQUA),
    ("State", "what persists across steps", ["checkpoints", "memory", "artifacts / diffs"], S.YELLOW),
    ("Verification\n& governance", "checks and guard-rails", ["tests / judges", "sandbox, approval", "rollback, budgets"], S.RED),
]


def hero() -> None:
    fig, ax = canvas(12, 7.2, 120)
    cx, cy = 60, 30.5
    ax.add_patch(Circle((cx, cy), 30.5, facecolor="#f7f7f5", edgecolor="none", zorder=0))
    ax.add_patch(Circle((cx, cy), 10.5, facecolor=S.INK, edgecolor="none", zorder=3))
    text(ax, cx, cy + 2.4, "Foundation\nmodel", 13, "white", "bold", ha="center", va="center", ls=1.1)
    text(ax, cx, cy - 4.2, "reasons, proposes", 8.5, "#cfcfca", ha="center", va="center")
    for i, (name, desc, techs, col) in enumerate(COMPONENTS):
        ang = math.radians(90 - i * 60)
        bx, by = cx + 34 * math.cos(ang), cy + 22.5 * math.sin(ang)
        w, h = 27, 12.6
        ax.plot([cx, bx], [cy, by], color=col, lw=1.8, alpha=0.55, zorder=2, solid_capstyle="round")
        box(ax, bx - w / 2, by - h / 2, w, h, fill="white", edge=col, lw=1.8, r=1.6, z=4)
        title = name.replace("\n", " ")
        text(ax, bx - w / 2 + 1.4, by + h / 2 - 1.2, title, 11 if len(title) < 16 else 10.2, col, "bold", z=6)
        text(ax, bx - w / 2 + 1.4, by + h / 2 - 3.9, desc, 8.6, S.INK_2, z=6)
        text(ax, bx - w / 2 + 1.4, by + h / 2 - 6.6, "  ·  ".join(techs[:2]) + "\n" + techs[2], 8.2,
             S.INK, z=6, ls=1.35)
    text(ax, 3, 71.5, "Agent  =  Model  +  Harness", 22, S.INK, "bold")
    text(ax, 3, 66.6, "The harness is every piece of runtime code around the model. Six jobs, one loop.",
         11, S.INK_2)
    text(ax, 3, 0.5, "Synthesised from Guo et al. 2026 (arXiv 2606.20683), Sec. 2.4 and 5",
         8, S.INK_3, ha="left", va="bottom")
    S.save(fig, "agent_model_plus_harness", "diagrams")


# ---------------------------------------------------------------------------
# D2. Four paradigms of agent engineering
# ---------------------------------------------------------------------------
def paradigms() -> None:
    fig, ax = canvas(13, 6.6, 130)
    phases = [
        ("1", "Prompt\nengineering", "the instruction", "How do I ask?",
         "CoT, few-shot, ReAct, self-consistency", "Cannot add knowledge or recover over long runs", S.SEQ_BLUE[2]),
        ("2", "Workflows &\ncontext engineering", "the context window", "What should the model see, and when?",
         "RAG, MemGPT, context compression, tool specs", "Feed-forward: no way to notice drift or check work", S.SEQ_BLUE[3]),
        ("3", "Harness\nengineering", "the whole runtime", "How do we keep the run on track?",
         "SWE-agent ACI, sandboxes, verifier loops, sub-agents, Meta-Harness", "Hand-built; tuned per benchmark and model", S.SEQ_BLUE[5]),
        ("4", "Agent-native training\n& co-evolution", "model + harness + update rule", "What should be learned, and by which part?",
         "Agentic RL (WebRL, DeepSeek-R1), Darwin Gödel Machine, AHE", "Overfitting, wrong failure attribution, unsafe self-edits", S.SEQ_BLUE[7]),
    ]
    x0, w, gap = 3, 29.5, 2.3
    rows = [("Optimises", 2), ("Core question", 3), ("Typical tools", 4), ("Breaks when", 5)]
    for i, (num, name, unit, q, ex, lim, col) in enumerate(phases):
        x = x0 + i * (w + gap)
        box(ax, x, 45, w, 12.5, fill=col, r=1.6)
        text(ax, x + 1.6, 55.8, f"Phase {num}", 9, "white" if i else S.INK, "bold")
        text(ax, x + 1.6, 52.9, name, 13, "white" if i else S.INK, "bold", ls=1.1)
        box(ax, x, 3, w, 40.5, fill="#f7f7f5", r=1.6)
        for (label, content), y in zip([("OPTIMISES", unit), ("CORE QUESTION", q), ("TYPICAL TOOLS", ex),
                                        ("BREAKS WHEN", lim)], [41.5, 33.5, 24.0, 13.0]):
            text(ax, x + 1.6, y, label, 7.8, S.INK_3, "bold")
            text(ax, x + 1.6, y - 2.4, content, 9.6, S.INK, wrap=31)
        if i < 3:
            arrow(ax, x + w + 0.2, 51.25, x + w + gap - 0.2, 51.25, color=S.INK_2, lw=2, ms=16)
    text(ax, 3, 66.5, "Four phases of agent engineering: where the effort lives", 17, S.INK, "bold")
    text(ax, 3, 62.6, "The phases overlap and coexist today; each one was adopted to fix what the previous one could not.",
         10.5, S.INK_2)
    text(ax, 127, 0.8, "Summarised from Guo et al. 2026 (arXiv 2606.20683), Sec. 1.2 and 4", 8, S.INK_3,
         ha="right", va="bottom")
    S.save(fig, "four_paradigms", "diagrams")


# ---------------------------------------------------------------------------
# D3. Harness anatomy: six responsibilities with their trade-offs
# ---------------------------------------------------------------------------
def anatomy() -> None:
    fig, ax = canvas(13, 7.0, 130)
    details = {
        "Observation": ("Turns raw signals (terminal output, diffs, DOM, screenshots, logs) into something the model can use.",
                        "Many failures are legibility failures: the needed state is missing, buried, or stale.",
                        "richness  vs  tractability"),
        "Context": ("Selects, compresses, orders and refreshes what is in the window: instructions, memory, tool docs, results.",
                    "The real split is monolithic vs managed context, not short vs long prompts.",
                    "fidelity  vs  manageability"),
        "Control loop": ("Schedules observe-reason-act steps, retries, delegation to sub-agents, model routing, stopping.",
                         "ReAct, plan-execute-verify, hierarchical and multi-agent loops are all options here.",
                         "adaptability  vs  stability"),
        "Action": ("Maps model output to real operations: function calls, MCP tools, shell, browser, sub-agent calls.",
                   "Granularity, schemas, routing and permissions are the four design knobs.",
                   "flexibility  vs  controllability"),
        "State": ("Keeps plans, checkpoints, logs, diffs, memory records and files across steps and sessions.",
                  "Failure modes: wrong state kept, right state lost, stale state treated as current.",
                  "completeness  vs  usability"),
        "Verification\n& governance": ("Tests, assertions, verifier models and judges produce evidence; gates, sandboxes, budgets, rollback act on it.",
                                       "Verification creates evidence; governance decides what to do with it.",
                                       "autonomy  vs  robustness"),
    }
    w, h = 40.5, 25.5
    for i, (name, _, _, col) in enumerate(COMPONENTS):
        r, c = divmod(i, 3)
        x, y = 3 + c * (w + 2.3), 32 - r * (h + 2.5)
        box(ax, x, y, w, h, fill=S.TINT[col], r=1.6)
        what, insight, trade = details[name]
        text(ax, x + 1.8, y + h - 1.6, name.replace("\n", " "), 13, col, "bold")
        text(ax, x + 1.8, y + h - 5.0, what, 9.6, S.INK, wrap=47)
        text(ax, x + 1.8, y + h - 13.8, insight, 9.2, S.INK_2, wrap=50, style="italic")
        text(ax, x + 1.8, y + 2.6, "trade-off:", 8.6, S.INK_3, "bold", va="center")
        chip(ax, x + 11.5, y + 2.6, trade, col, 8.8)
    text(ax, 3, 66, "Anatomy of a harness: six coupled responsibilities", 17, S.INK, "bold")
    text(ax, 3, 62.6, "Improving one part shifts risk to another: stronger compression can weaken verification; "
                      "richer actions raise governance pressure.", 10.2, S.INK_2)
    text(ax, 127, 0.6, "Summarised from Guo et al. 2026 (arXiv 2606.20683), Sec. 5.1-5.7", 8, S.INK_3,
         ha="right", va="bottom")
    S.save(fig, "harness_anatomy", "diagrams")


# ---------------------------------------------------------------------------
# D4. Task property -> failure pressure -> harness response
# ---------------------------------------------------------------------------
def task_to_harness() -> None:
    fig, ax = canvas(12.8, 6.4, 128)
    rows = [
        ("Long horizon", "State drift", "Checkpoints, summaries, artifacts", "Context, State, Control"),
        ("Partial observability", "Indirect state", "Structured observations, grounding", "Observation, Context, Action"),
        ("Strong oracle (tests exist)", "Checkable outcomes", "Verifier loops, repair cycles", "Verification, Control"),
        ("Weak or delayed oracle", "Uncertain success", "Provenance, review, approval", "Verification, Context, State"),
        ("Irreversible actions", "Persistent side effects", "Sandbox, gates, rollback", "Verification, Action"),
        ("High autonomy / low latency", "Little human correction", "Logging, budgets, controllers", "Verification, Control, Observation"),
    ]
    cols = [(3, 27, "IF THE TASK HAS...", S.INK), (34, 24, "IT FAILS BY...", S.RED),
            (62, 33, "SO THE HARNESS ADDS...", S.BLUE), (99, 25, "STRESSING", S.INK_2)]
    for x, w, label, col in cols:
        text(ax, x, 51.5, label, 8.6, S.INK_3, "bold")
    for i, row in enumerate(rows):
        y = 44 - i * 7.4
        for j, ((x, w, _, col), val) in enumerate(zip(cols, row)):
            fill = "#f7f7f5" if j != 2 else S.TINT[S.BLUE]
            box(ax, x, y - 2.9, w, 5.8, fill=fill, r=1.0)
            text(ax, x + 1.2, y, val, 9.6 if j < 3 else 8.8, col if j else S.INK,
                 "bold" if j in (0, 2) else "normal", va="center")
            if j < 3:
                arrow(ax, x + w + 0.3, y, cols[j + 1][0] - 0.3, y, color=S.RULE, lw=1.4, ms=10)
    text(ax, 3, 61, "Pick the harness from the task, not from the leaderboard", 17, S.INK, "bold")
    text(ax, 3, 57.6, "Verifier strength decides where configuration effort should go; "
                      "irreversibility and autonomy make guard-rails central.", 10.2, S.INK_2)
    text(ax, 124, 0.5, "Restyled from Guo et al. 2026 (arXiv 2606.20683), Table 5", 8, S.INK_3,
         ha="right", va="bottom")
    S.save(fig, "task_to_harness", "diagrams")


# ---------------------------------------------------------------------------
# D5. Terminal agents: four layers and seven competences
# ---------------------------------------------------------------------------
def terminal_stack() -> None:
    fig, ax = canvas(12.5, 6.6, 125)
    layers = [
        ("Harness & context", "packages history, formats prompts, manages the window", "Meta-Harness, AutoHarness", S.VIOLET, [4]),
        ("Control, verification, recovery, governance", "tests, rollback, approvals, role-split review", "STRATUS, AgentClick", S.RED, [5, 6, 7]),
        ("Runtime & workspace", "files, processes, packages, containers that persist", "OpenHands, DockSmith", S.YELLOW, [3, 4]),
        ("Interface & observation", "action units and feedback formats", "SWE-agent ACI, TACO", S.BLUE, [1, 2]),
    ]
    comps = ["1  Command & action formulation", "2  Feedback & artifact interpretation",
             "3  Runtime & environment management", "4  State, task & context tracking",
             "5  Progress verification", "6  Recovery & adaptation", "7  Governance & side-effect control"]
    for i, (name, desc, ex, col, dims) in enumerate(layers):
        y = 43.4 - i * 10.4
        box(ax, 3, y, 66, 9.4, fill=S.TINT[col], r=1.2)
        text(ax, 5, y + 8.2, name, 11.5, col, "bold")
        text(ax, 5, y + 5.2, desc, 9.3, S.INK)
        chip(ax, 5, y + 1.8, ex, col, 8.2)
        text(ax, 67.5, y + 4.7, "→ " + ", ".join(str(d) for d in dims), 10, S.INK_2, "bold", ha="right", va="center")
    box(ax, 3, 2.2, 66, 4.6, fill=S.INK, r=1.2)
    text(ax, 36, 4.5, "Model: issues commands, reads output, decides", 10.5, "white", "bold", ha="center", va="center")
    box(ax, 74, 2.2, 48, 50.6, fill="#f7f7f5", r=1.4)
    text(ax, 76, 50.8, "Seven-dimensional competence profile", 11.5, S.INK, "bold")
    text(ax, 76, 47.8, "System-level responsibilities, spread across the layers", 8.8, S.INK_2)
    for j, c in enumerate(comps):
        yy = 42.5 - j * 5.6
        box(ax, 76, yy - 2.2, 44, 4.4, fill="white", r=0.9)
        text(ax, 77.5, yy, c, 9.6, S.INK, va="center")
    text(ax, 3, 62.0, "Inside a terminal agent", 17, S.INK, "bold")
    text(ax, 3, 58.6, "Behaviour comes from model + interface + harness + runtime + environment together, "
                      "which is why attributing a score to one part is so hard.", 10.2, S.INK_2)
    text(ax, 122, 0.2, "Summarised from Bin et al. 2026 (arXiv 2608.20485), Sec. 2.3 and 3.2", 8, S.INK_3,
         ha="right", va="bottom")
    S.save(fig, "terminal_agent_stack", "diagrams")


# ---------------------------------------------------------------------------
# D6. Self-improvement: what gets updated, by which signal
# ---------------------------------------------------------------------------
def self_improvement_map() -> None:
    fig, ax = canvas(13, 6.7, 130)
    cols = [
        ("Model weights  θ", "SFT / RL on self-made data", "self-generated demos, self-judging, environment reward",
         "Self-Instruct, Constitutional AI, TTRL, WebRL, Absolute Zero", S.INK_2),
        ("Prompts  p", "rewrite system instructions", "scores, critiques, populations, textual gradients",
         "OPRO, Reflexion, Promptbreeder, GEPA, TextGrad", S.BLUE),
        ("Memory  m", "create / read / update / delete records", "retrieval misses, task feedback, capacity",
         "Mem0, A-MEM, ExpeL, ReasoningBank, ACE", S.VIOLET),
        ("Tools  T", "route, refine, or write new tools", "error traces, verifier checks, failures",
         "Voyager, SkillWeaver, DRAFT, Alita, TOOLMAKER", S.AQUA),
        ("Whole scaffold  Σ", "patch the agent's own code", "benchmarks and unit tests gate each patch",
         "ADAS, Gödel Agent, Darwin Gödel Machine, AlphaEvolve", S.GREEN),
    ]
    w, gap = 24.2, 1.4
    for i, (name, how, sig, ex, col) in enumerate(cols):
        x = 3 + i * (w + gap)
        box(ax, x, 40, w, 9, fill=col, r=1.4)
        text(ax, x + w / 2, 44.5, name, 11.5, "white", "bold", ha="center", va="center")
        box(ax, x, 6, w, 32.5, fill=S.TINT.get(col, "#f2f2f0"), r=1.4)
        y = 36.6
        for label, val in [("WHAT CHANGES", how), ("DRIVEN BY", sig), ("EXAMPLES", ex)]:
            text(ax, x + 1.3, y, label, 7.6, S.INK_3, "bold")
            text(ax, x + 1.3, y - 2.2, val, 9.1, S.INK, wrap=27)
            y -= 4.6 + 2.9 * len(textwrap.wrap(val, 27))
    arrow(ax, 17, 2.6, 113, 2.6, color=S.INK_3, lw=1.6, style="<|-|>")
    text(ax, 3, 2.6, "slow, global,\nhard to undo", 8.4, S.INK_2, va="center", ha="left")
    text(ax, 127, 2.6, "fast, local,\neasy to roll back", 8.4, S.INK_2, va="center", ha="right")
    text(ax, 3, 63.5, "Harnesses that improve themselves: what gets updated, and by which signal", 16, S.INK, "bold")
    text(ax, 3, 60.1, "Agent = (weights θ, scaffold Σ). Self-improvement is any self-induced, lasting update to either part.",
         10.2, S.INK_2)
    text(ax, 3, 56.8, "The survey's advice: keep noisy updates in the scaffold; consolidate into weights only once they are stable.",
         10.2, S.INK_2)
    text(ax, 127, -2.0, "Summarised from Ren et al. 2026 (arXiv 2607.13104), Sec. 3-6", 8, S.INK_3,
         ha="right", va="bottom")
    S.save(fig, "self_improvement_map", "diagrams")


# ---------------------------------------------------------------------------
# D7. The agent software lifecycle and its missing feedback loop
# ---------------------------------------------------------------------------
def lifecycle_loop() -> None:
    fig, ax = canvas(12.5, 6.3, 125)
    stages = [("Requirements", 26, "needs, allowed actions, delegation", S.MAGENTA),
              ("Architecture\n& design", 127, "patterns, protocols, safety by design", S.VIOLET),
              ("Implementation\n& integration", 76, "tools, MCP, configs, caching", S.BLUE),
              ("Testing\n& assurance", 215, "benchmarks, oracles, red-teaming, judges", S.AQUA),
              ("Maintenance\n& evolution", 49, "monitoring, diagnosis, repair, versions", S.YELLOW)]
    w, gap, y = 21.5, 3, 30
    for i, (name, n, desc, col) in enumerate(stages):
        x = 3 + i * (w + gap)
        box(ax, x, y, w, 17, fill=S.TINT[col], r=1.5)
        text(ax, x + 1.4, y + 15.5, name, 11.5, col, "bold", ls=1.05)
        text(ax, x + 1.4, y + 8.6, f"{n}", 22, S.INK, "bold")
        text(ax, x + 1.4 + 2.2 * len(str(n)) + 1.2, y + 7.4, "papers", 9, S.INK_2)
        text(ax, x + 1.4, y + 3.6, desc, 8.4, S.INK_2, wrap=27)
        if i < 4:
            arrow(ax, x + w + 0.2, y + 8.5, x + w + gap - 0.2, y + 8.5, color=S.INK_2, lw=1.8, ms=14)
    arrow(ax, 3 + 4 * (w + gap) + w / 2, y - 0.6, 3 + w / 2, y - 0.6, color=S.RED, lw=2, ls=(0, (5, 4)),
          rad=-0.12, ms=16)
    text(ax, 62, 14.5, "Operations → requirements / design:  0 implemented or evaluated links",
         11, S.RED, "bold", ha="center", va="center")
    text(ax, 62, 11.0, "Production lessons almost never flow back upstream in the published literature.",
         9.4, S.INK_2, ha="center", va="center")
    text(ax, 3, 60, "Shipping an agent is a software lifecycle, and its feedback loop is broken", 16, S.INK, "bold")
    text(ax, 3, 56.6, "355 published papers mapped to five stages (a paper can cover several). "
                      "Only 37 of 570 contributions carry real-project or production evidence.", 10.2, S.INK_2)
    text(ax, 122, 0.2, "Data: Ge et al. 2026 (arXiv 2611.23260), Sec. 3.5 and Table 13 (D4)", 8, S.INK_3,
         ha="right", va="bottom")
    S.save(fig, "agent_lifecycle_loop", "diagrams")


# ---------------------------------------------------------------------------
# D8. The four surveys at a glance
# ---------------------------------------------------------------------------
def surveys_at_a_glance() -> None:
    fig, ax = canvas(13, 6.2, 130)
    papers = [
        ("14 Jun 2026", "Agent System & Harness Design", "Guo, Han, Xu, Wang et al.\nCityU HK · Sydney · TokenRhythm",
         "29 pp · 262 refs", "Model + harness lens; six harness jobs; four paradigms; leaderboard analysis", S.BLUE, "primary"),
        ("14 Jul 2026", "Self-Improvements in Modern Agentic Systems", "Ren, ..., Zhuge, Schmidhuber\nJilin · KAUST · IDSIA",
         "97 pp", "What a self-improving agent updates (weights, prompts, memory, tools, code) and from which signal", S.GREEN, "companion"),
        ("20 Aug 2026", "Terminal Agents", "Bin, ..., Song, Shen\nTongji · SJTU · PolyU",
         "52 pp · 186 works", "Seven terminal competences; own matched experiments on three harnesses", S.ORANGE, "companion"),
        ("3 Oct 2026", "Software Engineering for LLM-Based Agents", "Ge, ..., Liu, Jin\nNanjing · NTU · Peking",
         "79 pp · 355 papers", "Agents as software: requirements to maintenance, evidence quality, AgentOps gaps", S.VIOLET, "companion"),
    ]
    arrow(ax, 3, 40, 127, 40, color=S.RULE, lw=2, style="-")
    w, gap = 29.5, 2.3
    for i, (date, title, who, size, gist, col, role) in enumerate(papers):
        x = 3 + i * (w + gap)
        ax.add_patch(Circle((x + 3, 40), 1.1, facecolor=col, edgecolor="white", lw=2, zorder=4))
        text(ax, x + 1.6, 44.2, date, 10.5, S.INK, "bold", va="center")
        box(ax, x, 3, w, 33.5, fill=S.TINT[col], r=1.5)
        text(ax, x + 1.5, 34.7, role.upper(), 7.8, col, "bold")
        text(ax, x + 1.5, 31.8, title, 11.5, S.INK, "bold", wrap=25)
        text(ax, x + 1.5, 23.8, who, 8.6, S.INK_2, ls=1.3)
        chip(ax, x + 1.5, 17.7, size, col, 8.4)
        text(ax, x + 1.5, 14.2, gist, 9.0, S.INK, wrap=33)
    text(ax, 3, 60, "Four 2026 surveys, one question: where does agent performance come from?", 16, S.INK, "bold")
    text(ax, 3, 56.6, "All four were posted to arXiv between June and October 2026, within six months of this write-up.",
         10.2, S.INK_2)
    text(ax, 3, 52.8, "Read together, they trace the harness from design (Jun) to self-improvement (Jul), "
                      "to a deep case study (Aug), to shipping it (Oct).", 10.2, S.INK_2)
    S.save(fig, "surveys_at_a_glance", "diagrams")


# ---------------------------------------------------------------------------
# D9. My synthesis: a report card every agent result should carry
# ---------------------------------------------------------------------------
def report_card() -> None:
    fig, ax = canvas(12.5, 6.3, 125)
    groups = [
        ("Identity", S.BLUE, ["Model + version + reasoning effort", "Harness name + version", "Tool privileges (what it may touch)"]),
        ("Budget", S.ORANGE, ["Step / turn limit and timeout", "Retries and attempts (pass@k vs pass^k)", "Tokens, $ and wall-clock per task"]),
        ("Outcome", S.AQUA, ["Success with 95% CI over repeated runs", "Cost per successful task", "Regression on previously solved tasks"]),
        ("Process", S.VIOLET, ["Verification actions before 'done'", "Recovery after failures", "Governance events (risky commands, approvals)"]),
        ("Provenance", S.GREEN, ["Who ran it (vendor, board, third party)", "Benchmark version + task freshness", "Replayable traces published"]),
    ]
    w, gap = 22.8, 1.4
    for i, (name, col, items) in enumerate(groups):
        x = 3 + i * (w + gap)
        box(ax, x, 6, w, 39, fill=S.TINT[col], r=1.5)
        text(ax, x + 1.4, 43.2, name.upper(), 10.5, col, "bold")
        for j, it in enumerate(items):
            yy = 37.2 - j * 10.4
            box(ax, x + 1.0, yy - 7.6, w - 2.0, 8.6, fill="white", r=1.0)
            ax.add_patch(FancyBboxPatch((x + 2.1, yy - 1.9), 1.5, 1.5, boxstyle="round,pad=0,rounding_size=0.3",
                                        fc="white", ec=col, lw=1.4, zorder=6))
            text(ax, x + 4.4, yy - 0.3, it, 9.1, S.INK, wrap=21, ls=1.2)
    text(ax, 3, 60.5, "My two cents: the harness report card", 17, S.INK, "bold")
    text(ax, 3, 57.1, "A score without these fields cannot be compared. Merged from the reporting checklists in all four surveys, "
                      "plus provenance, which none of them puts first.", 10.2, S.INK_2)
    text(ax, 3, 53.8, "Fields in the Identity, Budget and Provenance columns would explain many of the 'ranking flips' "
                      "on today's leaderboards.", 10.2, S.INK_2)
    text(ax, 122, 0.8, "Author's synthesis of arXiv 2606.20683 Sec. 7.6, 2607.13104 Sec. 8.1, 2608.20485 App. E, "
                       "2611.23260 Sec. 5.3", 8, S.INK_3, ha="right", va="bottom")
    S.save(fig, "harness_report_card", "diagrams")


if __name__ == "__main__":
    hero()
    paradigms()
    anatomy()
    task_to_harness()
    terminal_stack()
    self_improvement_map()
    lifecycle_loop()
    surveys_at_a_glance()
    report_card()
