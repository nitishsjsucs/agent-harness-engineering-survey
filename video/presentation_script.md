# Video script: The Harness Is Half the Agent

Word-for-word narration taken from the speaker notes in `slides/harness_short_story.pptx` (27 slides, 2,155 words). At 135 words per minute plus a short pause per slide, the talk runs about **17.8 minutes**, which clears the 15-minute minimum.

| Slide | Starts at | Length | Section cue |
|---|---|---|---|
| 1 | 0:00 | 37 s | `$ agent = model + harness` The Harness Is |
| 2 | 0:36 | 37 s | `$ why-this-matters` Same model, same tasks, 18 points apart |
| 3 | 1:14 | 42 s | `$ cat papers.txt` One primary survey on harness design, plus three companions: self-improvement, terminals,  |
| 4 | 1:56 | 38 s | `$ wc -l literature` This field is young: most of the reviewed work was released in 2026 alone. |
| 5 | 2:34 | 43 s | `$ git log --oneline agent-engineering` Each phase was adopted to fix what the previous one could not. All four coexist today. |
| 6 | 3:16 | 38 s | `$ agent = model + harness` A benchmark score belongs to the model-harness pair, not to the model alone. |
| 7 | 3:54 | 34 s | `$ man harness` The six parts are coupled: fixing one pushes risk into another. |
| 8 | 4:28 | 41 s | `$ match --task --harness` Match the harness to the oracle: tests → verify-and-repair loop; no tests → provenance and |
| 9 | 5:10 | 48 s | `$ leaderboard --same-model` Median harness spread 13.6 pts; one model-generation step 11-19 pts. Comparable levers. |
| 10 | 5:58 | 30 s | `$ diff top-entries baseline` Five techniques behind the top leaderboard entries |
| 11 | 6:28 | 41 s | `$ cost --per-trial` Better harnesses trade money for reliability; accuracy-only leaderboards hide the trade. |
| 12 | 7:09 | 39 s | `$ browse --with-harness` The web shows the biggest lifts, but systems differ in more than the harness: read as uppe |
| 13 | 7:48 | 33 s | `$ ssh terminal-agents-survey` A terminal agent is defined by its execution substrate, not its interface. |
| 14 | 8:21 | 44 s | `$ ablate --harness --model` Model tier changed results by at most 2.5 pts (not significant). Harness changed them by u |
| 15 | 9:04 | 32 s | `$ trace --process-signals` Each benchmark exposes a different weakness; agents verify near the end in only 24-37% of  |
| 16 | 9:36 | 39 s | `$ coverage --competences` Only one benchmark family explicitly scores governance: most reward the answer, not safe b |
| 17 | 10:15 | 38 s | `$ agent --rewrite-self` Keep noisy updates in the scaffold; consolidate into weights only once they are stable. |
| 18 | 10:53 | 39 s | `$ diff harness@v0 harness@vN` A frozen model with a self-edited harness went from 20% to 50% on SWE-bench. |
| 19 | 11:32 | 38 s | `$ memory --gc` 16 of 25 memory systems have no clear delete step, and 10 lack maintenance (consolidation, |
| 20 | 12:10 | 38 s | `$ agentops --lifecycle` Zero evaluated links from operations back to requirements or design: the feedback loop is  |
| 21 | 12:48 | 37 s | `$ evidence --real-world` Only 37 of 570 contributions carry evidence from real projects or production. |
| 22 | 13:25 | 49 s | `$ eval --metrics` The metrics that matter, merged from all four surveys |
| 23 | 14:14 | 37 s | `$ two-cents --leaderboards` Benchmark version and referee matter as much as the harness. One ranking is one measuremen |
| 24 | 14:51 | 58 s | `$ two-cents --critique` Where I think the story is weaker than it sounds |
| 25 | 15:49 | 43 s | `$ report-card --required` My proposal: no agent score without identity, budget, outcome with CI, process signals and |
| 26 | 16:32 | 36 s | `$ checklist --practitioner` If you are building an agent next week |
| 27 | 17:08 | 37 s | `$ exit 0` Strong models are becoming a commodity. |

---

## Slide 1 · 0:00  `$ agent = model + harness`

Hi everyone. My short story is about one idea that took over agent engineering in 2026: the harness. I read four surveys posted to arXiv between June and October, and I will walk you through their taxonomies, the key techniques, the leaderboard and ablation evidence, and the metrics they recommend. Then I will give my own two cents. Every chart here is in my GitHub repository, with the data and code to regenerate it.

## Slide 2 · 0:36  `$ why-this-matters`

Let me start with one number. On Terminal-Bench 2.0, Claude Opus 4.6 solves 58 percent of tasks inside Claude Code, and 76.4 percent inside a harness called Meta-Harness. Same model, same weights, same tasks: an 18-point gap. On paper, the only thing that changed is the code around the model, meaning what it sees, what it can do, what it remembers, when it stops, and how its work is checked. That code is the harness.

## Slide 3 · 1:14  `$ cat papers.txt`

Here are the four surveys. The primary one, by Guo and colleagues from City University of Hong Kong, the University of Sydney and TokenRhythm, gives the vocabulary for the whole talk. The second, from Schmidhuber's group, covers agents that improve their own harness. The third is a terminal-agents survey from Tongji that runs its own matched comparisons. The fourth, from Nanjing, NTU and Peking University, treats agents as software across their lifecycle, which is the AgentOps view. All four were posted within the last six months.

## Slide 4 · 1:56  `$ wc -l literature`

Why are these surveys appearing now? Look at the corpora two of them reviewed. In the terminal-agents survey, 112 of 186 works are from 2026, through August. In the software-engineering survey, 199 of 355 published papers are from 2026. Most of what we know about engineering agents is less than a year old, which is exactly when a good survey is most useful, and also when you should be careful about how settled any claim is.

## Slide 5 · 2:34  `$ git log --oneline agent-engineering`

The harness survey describes four overlapping phases. Prompt engineering optimizes the instruction: how to ask. Context engineering optimizes what the model sees and when, with retrieval and memory, but it is still feed-forward, so nothing notices when a run drifts. Harness engineering makes the whole runtime the design object and closes the loop with sandboxes, verifiers and retries. And the fourth phase trains some of that behaviour back into the model and updates model and harness together. These phases coexist today; most production agents combine all four.

## Slide 6 · 3:16  `$ agent = model + harness`

This is the central formalism: an agent is a model coupled with a harness, and the harness has six jobs. Observation decides what the model sees. Context decides what enters the window. The control loop decides who acts next and when to stop. Action decides what the agent may do. State decides what persists. Verification and governance check the work and enforce guard-rails. In the survey's words, agent performance is a property of the model-harness pairing.

## Slide 7 · 3:54  `$ man harness`

Each job has a trade-off. Observation trades richness against tractability, and many failures are legibility failures, where the information was missing, buried or stale. Context trades fidelity against manageability. Control trades adaptability against stability, and action trades flexibility against controllability. I like the last split: verification produces evidence, governance decides what to do with it. And because the parts are coupled, fixing one can push risk into another.

## Slide 8 · 4:28  `$ match --task --harness`

How do you choose a harness? The survey maps task properties to failure modes and responses. Long horizons cause state drift, so you add checkpoints and summaries. If tests exist, you build verify-and-repair loops; if success can only be judged later, you need provenance and review. Irreversible actions need sandboxes, gates and rollback. The survey says the jump from multi-step to long-horizon tasks is where harness design starts to dominate. Domains differ too: coding is verification-dominant, web agents are grounding-dominant, and research is synthesis-dominant.

## Slide 9 · 5:10  `$ leaderboard --same-model`

Now the evidence. On the left, the same model under different harnesses on Terminal-Bench 2.0. GPT-5.3 Codex spans 13.7 points, Opus 4.6 spans 18.4, Gemini 3.1 Pro spans 20.8. Across 20 models with at least three harnesses, the median spread is 13.6 points. But on the right, the survey is honest that it cuts both ways: inside a fixed harness, each newer model adds roughly 11 to 19 points, and two or three generations add about 30. The two levers are about the same size. Fourteen of those twenty models vary by at least ten points depending on the harness.

## Slide 10 · 5:58  `$ diff top-entries baseline`

What do the top entries do differently? Five patterns. Searched or generated harnesses, like Meta-Harness and SageAgent. Verification before declaring done, which agents left to themselves often skip. Minimal, legible tools: the 100-line mini-SWE-agent nearly matches the full OpenHands runtime. Fixed pipelines like Agentless when tests exist. And deliberately spending tokens on context, which is the next slide.

## Slide 11 · 6:28  `$ cost --per-trial`

This is the most under-discussed result in the harness survey. For Opus 4.6, Meta-Harness uses a median of 755 thousand input tokens per trial, against 79 thousand for Terminus 2, about nine and a half times as much. In exchange, accuracy goes up 13.5 points and timeouts drop from 18 to 8 percent. The same pattern holds for GPT-5.3 Codex with Mux. Better harnesses are not free. They buy reliability with context, and a leaderboard that shows only accuracy hides that trade completely.

## Slide 12 · 7:09  `$ browse --with-harness`

On the web the effect is even bigger, because a bare model is so weak at browsing. GPT-4o goes from 13 percent to almost 55 with WebOperator. An 8-billion-parameter Llama goes from under 6 percent to 48 with AgentSymbiotic. One caveat I want to be clear about: these systems differ in more than the harness. Some use tree search with many more environment interactions, some add training. So these are upper bounds on what the harness alone contributes.

## Slide 13 · 7:48  `$ ssh terminal-agents-survey`

Now the terminal-agents survey, which zooms into where most coding agents live. Its definition is about substrate, not interface: if running commands and changing persistent state is what drives progress, it is a terminal agent. It describes four layers on top of the model, and a seven-dimensional competence profile from command formulation to governance. These are responsibilities of the whole system, not abilities of the model.

## Slide 14 · 8:21  `$ ablate --harness --model`

This is the cleanest comparison in the four papers; the authors call it a bounded diagnostic. The authors ran DeepSeek-V4 Flash and the larger Pro under three harnesses on identical tasks, with paired statistical tests. Changing the model tier moved results by at most 2.5 points, and nothing was significant. Changing the harness moved them by up to 21 points on Claw-SWE-Bench Lite. But on SWE-bench Lite the biggest harness gap was only 7 points, and two harnesses swap places. How much the harness matters depends on the benchmark.

## Slide 15 · 9:04  `$ trace --process-signals`

The same survey ran one fixed agent across four benchmark families and logged process signals. Each benchmark exposes a different weakness: SetupBench stresses environment setup, LongCLI-Bench has the lowest success at about 24 percent, and BashArena shows the most state-tracking errors. And on three of the four, the agent verified its work near the end in only 24 to 37 percent of tasks.

## Slide 16 · 9:36  `$ coverage --competences`

This is the survey's coverage map: which of the seven competences each benchmark can even observe. Command formulation and feedback interpretation are well covered. Governance, meaning permissions, sandboxing and side effects, is explicitly scored only by the BashArena and ClawSafety family. Most benchmarks reward getting the right answer and do not penalize doing something dangerous along the way. The survey also cites an audit that found about 16 percent of tasks across five terminal benchmarks could be reward-hacked.

## Slide 17 · 10:15  `$ agent --rewrite-self`

If the harness matters this much, the next step is letting the agent improve its own harness. The Schmidhuber-group survey models an agent as weights plus a scaffold of prompts, memory, tools and control logic, and organizes methods by what gets updated and which signal drives it. Prompts can be optimized with scores, critiques, evolving populations or textual gradients, and whole scaffolds can be patched as code. Their advice: keep noisy updates in the fast, reversible scaffold.

## Slide 18 · 10:53  `$ diff harness@v0 harness@vN`

Here is the headline example, the Darwin Gödel Machine. It keeps the foundation model frozen and lets coding agents rewrite their own source code, validating every variant on coding benchmarks and keeping an open-ended archive of diverse agents. Per the original paper, SWE-bench went from 20 to 50 percent, and Polyglot from 14 to about 31. What it discovered were harness features: better code-editing tools, long-context window management, and peer-review steps. In other words, it automated harness engineering.

## Slide 19 · 11:32  `$ memory --gc`

The survey also tabulates 25 agent memory systems. Almost all of them write and read well, but 16 of the 25 have no clear delete step, and 10 lack ongoing maintenance, which is where forgetting lives. Memory that never forgets eventually lies to you. Their evaluation rules are worth adopting: report the whole improvement trajectory under a fixed budget, track regressions on solved tasks, and never use the same judge to drive updates and report results.

## Slide 20 · 12:10  `$ agentops --lifecycle`

The fourth survey asks what happens after the demo works. It maps 355 papers with publication evidence onto five lifecycle stages. Testing dominates with 215 papers, against 26 on requirements: we are much better at measuring agents than at specifying what they should and should not do. And the loop is broken: zero implemented or evaluated links from operations back to requirements or design. A few papers describe such a loop, but none builds and tests it.

## Slide 21 · 12:48  `$ evidence --real-world`

Evidence quality is the other finding. Only 37 of 570 contributions, about six and a half percent, come from real projects or production. Their motivating example is Anthropic's research agent, where the team could not diagnose bad answers until they added production tracing. The practices they collect are useful, like policy-aware success metrics and evaluation gates before a model migration. One industrial pilot raised 23 regression alerts in four months, and only 8 were genuine.

## Slide 22 · 13:25  `$ eval --metrics`

Pulling the surveys together, this is the metric set I want on any agent result. Success with a confidence interval. Pass at k next to pass hat k, because users care whether it succeeds every time. Cost per successful task, and where the budget goes. Process signals: does it verify, does it recover, how often does it run risky commands. Regressions on solved tasks. And policy-compliant completion: success only counts if it also followed the rules. The harness survey even proposes a value-aware objective that combines success with cost, latency, risk and reliability, though it never computes it for any system.

## Slide 23 · 14:14  `$ two-cents --leaderboards`

Now my two cents. I checked the live leaderboards on November 19. On the left, Opus 4.6 under nine harnesses, from 58 to 76 percent. On the right, harness rankings flip. On the 2.0 board, Claude Code trails Terminus 2; in the maintainers' re-run on corrected tasks, Claude Code wins. GPT-5.5 wins in Codex on tbench.ai, but loses badly in Codex on Vals AI's independent run. One ranking is one measurement, not a fact.

## Slide 24 · 14:51  `$ two-cents --critique`

Four more critiques. First, 'harness, not model' is half true: one model-generation step adds 11 to 19 points, about the same as the median harness spread. The model sets the ceiling; the harness decides how much you reach. Second, vendor CLIs ranking low is not a scandal: they are built for humans in the loop, while leaderboard harnesses are tuned to the benchmark. Third, cost is the missing axis: Codex spends about four times what Terminus 2 does for five more points. Fourth, governance and forgetting are blind spots. And a fair warning: all four are first versions with rough edges, such as mixed model versions in one table and single-family diagnostics, so check the primary source behind any number you cite.

## Slide 25 · 15:49  `$ report-card --required`

If I could add one convention to the field, it would be this report card. Every agent result should say which model and harness, with versions and reasoning effort. The budget: step limits, retries, tokens and dollars. The outcome with a confidence interval, cost per success, and regressions. A few process signals: verification, recovery, governance events. And provenance: who ran it, which benchmark version, and whether the traces are published. The identity, budget and provenance fields would explain many of the ranking flips I just showed you.

## Slide 26 · 16:32  `$ checklist --practitioner`

If I were building an agent next week: start minimal and add pieces only when a trace shows you need them. Match the harness to the oracle. Manage context deliberately and gate irreversible actions. Measure reliability, not just capability, and put cost per success next to accuracy. Feed production traces back into your specs. And if the agent improves itself, gate every change and never grade with the judge that guided it.

## Slide 27 · 17:08  `$ exit 0`

To wrap up: all four surveys agree that an agent is a system, and its behaviour comes from the model, the harness, the runtime and the evaluation together. My takeaway is that strong models are becoming a commodity, and the harness is where agents now differ. It deserves the rigour we gave to models: controlled comparisons, honest cost accounting, and full configurations. The data, code, article and slides are all on my GitHub. Thank you.
