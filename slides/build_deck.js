// Builds slides/harness_short_story.pptx from the figures in ../figures.
// Run from the repo root:  NODE_PATH=slides/node_modules node slides/build_deck.js
// (optional) APPLY_THEME=/path/to/apply_theme.js also writes the colour theme into the file
// Presenter name can be overridden:  PRESENTER="Your Name" node slides/build_deck.js
const path = require("path");
const fs = require("fs");
const pptxgen = require("pptxgenjs");

const ROOT = path.resolve(__dirname, "..");
const SIZES = JSON.parse(fs.readFileSync(path.join(__dirname, "figure_sizes.json"), "utf8"));
const PRESENTER = process.env.PRESENTER || "nitishsjsucs";
const REPO = process.env.REPO_URL || "github.com/nitishsjsucs/agent-harness-engineering-survey";
const OUT = path.join(__dirname, "harness_short_story.pptx");

const THEME = {
  name: "Harness",
  headFontFace: "Arial",
  bodyFontFace: "Arial",
  colors: {
    dk1: "111827", lt1: "FFFFFF", dk2: "374151", lt2: "F4F4F2",
    accent1: "2A78D6", accent2: "EB6834", accent3: "1BAF7A", accent4: "EDA100",
    accent5: "6250D6", accent6: "E34948", hlink: "2A78D6", folHlink: "6250D6",
  },
};
const HEX = { ink: "111827", ink2: "4B5563", ink3: "8A8985", surface2: "F4F4F2", blue: "2A78D6", orange: "EB6834",
  aqua: "1BAF7A", yellow: "EDA100", violet: "6250D6", red: "E34948", green: "008300" };
const TINT = { blue: "EAF2FC", orange: "FDEFE9", aqua: "E7F7F1", yellow: "FDF5E1", violet: "EFEDFB", red: "FCECEC", green: "E5F3E5" };

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
pres.title = "The Harness Is Half the Agent";
pres.subject = "Short story: four 2026 surveys on LLM agent harness engineering";
pres.author = PRESENTER;
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
const C = pres.SchemeColor;
const W = 13.333, H = 7.5;

// Speaker notes: slides/speaker_notes.json holds the final, timed narration (one entry per slide, in
// order) and overrides the first-draft notes written inline below. Edit the JSON to change what you say.
const NOTES = JSON.parse(fs.readFileSync(path.join(__dirname, "speaker_notes.json"), "utf8"));
{
  const addSlide = pres.addSlide.bind(pres);
  let count = 0;
  pres.addSlide = (opts) => {
    const slide = addSlide(opts);
    const idx = count++;
    const addNotes = slide.addNotes.bind(slide);
    slide.addNotes = (draft) => addNotes(NOTES[idx] || draft);
    return slide;
  };
}

// ---------------------------------------------------------------- layouts
pres.defineSlideMaster({
  title: "DARK",
  background: { color: HEX.ink },
  objects: [],
  slideNumber: { x: 12.3, y: 7.0, w: 0.6, h: 0.3, color: "9CA3AF", fontSize: 10, align: "right" },
});
pres.defineSlideMaster({
  title: "FIGURE",
  background: { color: "FFFFFF" },
  objects: [
    { placeholder: { options: { name: "kicker", type: "body", x: 0.5, y: 0.28, w: 9, h: 0.4, fontSize: 12,
      fontFace: "Courier New", color: C.accent1, bold: true, margin: 0 }, text: "" } },
  ],
  slideNumber: { x: 12.3, y: 7.0, w: 0.6, h: 0.3, color: "9CA3AF", fontSize: 10, align: "right" },
});
pres.defineSlideMaster({
  title: "TITLE_ONLY",
  background: { color: "FFFFFF" },
  objects: [
    { placeholder: { options: { name: "kicker", type: "body", x: 0.5, y: 0.28, w: 9, h: 0.4, fontSize: 12,
      fontFace: "Courier New", color: C.accent1, bold: true, margin: 0 }, text: "" } },
    { placeholder: { options: { name: "title", type: "title", x: 0.5, y: 0.7, w: 12.3, h: 0.9, fontSize: 32,
      bold: true, color: C.text1, margin: 0, valign: "top", align: "left" }, text: "" } },
  ],
  slideNumber: { x: 12.3, y: 7.0, w: 0.6, h: 0.3, color: "9CA3AF", fontSize: 10, align: "right" },
});

// ---------------------------------------------------------------- helpers
function fitImage(slide, rel, box) {
  const [pw, ph] = SIZES[rel];
  const r = pw / ph;
  let w = box.w, h = w / r;
  if (h > box.h) { h = box.h; w = h * r; }
  const x = box.x + (box.w - w) / 2, y = box.y + (box.h - h) / 2;
  slide.addImage({ path: path.join(ROOT, rel), x, y, w, h, altText: path.basename(rel, ".png").replace(/_/g, " ") });
  return { x, y, w, h };
}

function takeaway(slide, txt, color = HEX.blue) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.5, y: 6.55, w: 11.6, h: 0.62, rectRadius: 0.08,
    fill: { color: TINT[Object.keys(HEX).find((k) => HEX[k] === color)] || "F4F4F2" }, line: { color: "FFFFFF", width: 0 },
    objectName: "takeaway-bg" });
  slide.addText([{ text: "Takeaway  ", options: { bold: true, color } }, { text: txt, options: { color: HEX.ink } }],
    { x: 0.7, y: 6.55, w: 11.3, h: 0.62, fontSize: 15, valign: "middle", margin: 0, isTextBox: true, objectName: "takeaway" });
}

function figureSlide(section, kicker, rel, take, notes, color) {
  const s = pres.addSlide({ masterName: "FIGURE", sectionTitle: section });
  s.addText(kicker, { placeholder: "kicker" });
  fitImage(s, rel, { x: 0.5, y: 0.75, w: 12.33, h: take ? 5.7 : 6.3 });
  if (take) takeaway(s, take, color);
  s.addNotes(notes);
  return s;
}

function card(slide, x, y, w, h, title, body, color, opts = {}) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.1, fill: { color: TINT[color] },
    line: { color: "FFFFFF", width: 0 }, objectName: `card-${title}` });
  slide.addText(title, { x: x + 0.22, y: y + 0.16, w: w - 0.44, h: 0.5, fontSize: opts.titleSize || 17, bold: true,
    color: HEX[color], margin: 0, valign: "top", isTextBox: true });
  const top = opts.bodyTop || 0.7;
  slide.addText(body, { x: x + 0.22, y: y + top, w: w - 0.44, h: h - top - 0.15, fontSize: opts.bodySize || 14,
    color: HEX.ink, margin: 0, valign: "top", isTextBox: true, paraSpaceAfter: 4 });
}

// ---------------------------------------------------------------- slides
// 1. Title
pres.addSection({ title: "Opening" });
{
  const s = pres.addSlide({ masterName: "DARK", sectionTitle: "Opening" });
  s.addText("SHORT STORY  ·  GENERATIVE AI SURVEY", { x: 0.7, y: 0.8, w: 10, h: 0.4, fontFace: "Courier New",
    fontSize: 13, bold: true, color: "93C5FD", margin: 0, isTextBox: true });
  s.addText("The Harness Is\nHalf the Agent", { x: 0.7, y: 1.4, w: 8.2, h: 2.4, fontSize: 54, bold: true,
    color: "FFFFFF", margin: 0, valign: "top", isTextBox: true });
  s.addText("What four 2026 surveys say about building LLM agents that actually finish the job, and what the leaderboards really show",
    { x: 0.7, y: 3.95, w: 7.6, h: 1.1, fontSize: 18, color: "D1D5DB", margin: 0, valign: "top", isTextBox: true });
  s.addText([{ text: PRESENTER, options: { bold: true, color: "FFFFFF", breakLine: true } },
    { text: "November 2026  ·  " + REPO, options: { color: "9CA3AF" } }],
  { x: 0.7, y: 5.9, w: 8.5, h: 0.8, fontSize: 14, margin: 0, isTextBox: true });
  const jobs = ["observation", "context", "control loop", "action", "state", "verify & govern"];
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 8.9, y: 1.45, w: 3.9, h: 4.1, rectRadius: 0.12, fill: { color: "1F2937" },
    line: { color: "374151", width: 1 } });
  s.addText([{ text: "$ agent = model + harness", options: { color: "93C5FD", bold: true, breakLine: true } },
    { text: " ", options: { breakLine: true } },
    ...jobs.map((j, i) => ({ text: `  harness.${String(i + 1)}  ${j}`, options: { color: "E5E7EB", breakLine: i < jobs.length - 1 } }))],
  { x: 9.15, y: 1.7, w: 3.5, h: 3.6, fontFace: "Courier New", fontSize: 13, margin: 0, valign: "top", isTextBox: true,
    paraSpaceAfter: 6 });
  s.addNotes(`Hi everyone. My short story is about one idea that took over agent engineering in 2026: the harness. ` +
    `I read four survey papers posted to arXiv between June and October 2026, and I will walk you through their taxonomies, the key techniques, ` +
    `the leaderboard and ablation evidence, the metrics they recommend, and then my own two cents on where the story is weaker than it sounds. ` +
    `Everything you see, including every chart, is in my GitHub repository, with the data and the code to regenerate it.`);
}

// 2. Hook
{
  const s = pres.addSlide({ masterName: "TITLE_ONLY", sectionTitle: "Opening" });
  s.addText("$ why-this-matters", { placeholder: "kicker" });
  s.addText("Same model, same tasks, 18 points apart", { placeholder: "title" });
  const stat = (x, num, label, sub, color) => {
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 1.9, w: 5.6, h: 3.4, rectRadius: 0.12, fill: { color: TINT[color] },
      line: { color: "FFFFFF", width: 0 } });
    s.addText(num, { x: x + 0.35, y: 2.1, w: 5, h: 1.6, fontSize: 80, bold: true, color: HEX[color], margin: 0, isTextBox: true });
    s.addText(label, { x: x + 0.35, y: 3.75, w: 5, h: 0.5, fontSize: 20, bold: true, color: HEX.ink, margin: 0, isTextBox: true });
    s.addText(sub, { x: x + 0.35, y: 4.3, w: 5, h: 0.8, fontSize: 14, color: HEX.ink2, margin: 0, isTextBox: true });
  };
  stat(0.5, "58.0%", "Claude Opus 4.6 in Claude Code", "Terminal-Bench 2.0 accuracy", "orange");
  stat(6.73, "76.4%", "Claude Opus 4.6 in Meta-Harness", "same benchmark, same model weights", "blue");
  s.addText("The only thing that changed is the code wrapped around the model. That code is the harness.",
    { x: 0.5, y: 5.6, w: 12.3, h: 0.6, fontSize: 18, color: HEX.ink, margin: 0, isTextBox: true });
  s.addText("Source: Guo et al. 2026 (arXiv 2606.20683) Sec. 7.3; tbench.ai Terminal-Bench 2.0 leaderboard, accessed 19 Nov 2026",
    { x: 0.5, y: 6.75, w: 11.5, h: 0.35, fontSize: 10, color: HEX.ink3, margin: 0, isTextBox: true });
  s.addNotes(`Let me start with one number. On Terminal-Bench 2.0, Claude Opus 4.6 solves 58 percent of tasks when it runs inside Claude Code, ` +
    `and 76.4 percent when it runs inside a harness called Meta-Harness. Same model, same weights, same tasks. An 18-point gap. ` +
    `The only thing that changed is the code around the model: what it sees, what tools it can call, what it remembers, when it stops, and how its work is checked. ` +
    `That code is what people now call the harness, and it is the subject of this talk.`);
}

// 3. Surveys
figureSlide("Opening", "$ cat papers.txt", "figures/diagrams/surveys_at_a_glance.png",
  "One primary survey on harness design, plus three companions: self-improvement, terminals, AgentOps.",
  `Here are the four surveys. The primary one is "From Question Answering to Task Completion", by Guo and colleagues from City University of Hong Kong and the University of Sydney, posted in June. ` +
  `It gives the vocabulary for the whole talk. The second, from Schmidhuber's group at KAUST and IDSIA, is about agents that improve their own harness. ` +
  `The third is a 52-page survey on terminal agents from Tongji University, which also runs its own controlled experiments. ` +
  `The fourth, from Nanjing University, NTU and Peking University, treats agents as software and covers the full lifecycle, which is the AgentOps view. ` +
  `All four are within six months of today, and together they go from design, to self-improvement, to a deep case study, to shipping.`);

// 4. Corpus growth
figureSlide("Opening", "$ wc -l literature", "figures/charts/corpus_growth.png",
  "This field is young: most of the reviewed work was released in 2026 alone.",
  `Why are these surveys appearing now? Look at the corpora two of them reviewed. In the terminal-agents survey, 112 of 186 works are from 2026, through August. ` +
  `In the software-engineering survey, 199 of 355 published papers are from 2026. Most of what we know about engineering agents is less than a year old, ` +
  `which is exactly when a good survey is most useful, and also when you should be careful about how settled any claim is.`);

// 5. Paradigms
pres.addSection({ title: "Taxonomy" });
figureSlide("Taxonomy", "$ git log --oneline agent-engineering", "figures/diagrams/four_paradigms.png",
  "Each phase was adopted to fix what the previous one could not. All four coexist today.",
  `The harness survey describes four overlapping phases. Prompt engineering optimizes the instruction; it is about how to ask, but it cannot add knowledge or recover from mistakes. ` +
  `Workflows and context engineering optimize what the model sees and when, with retrieval, memory and compression, but they are still feed-forward: nothing notices when the run drifts. ` +
  `Harness engineering makes the whole runtime the design object, with sandboxes, verifier loops, retries and sub-agents that close the loop. ` +
  `And the fourth phase, agent-native training and co-evolution, pushes some of that behaviour back into the model weights through agentic reinforcement learning, and updates model and harness together.`);

// 6. Hero
figureSlide("Taxonomy", "$ agent = model + harness", "figures/diagrams/agent_model_plus_harness.png",
  "A benchmark score belongs to the model-harness pair, not to the model alone.",
  `This is the central formalism. An agent is a model coupled with a harness, and the harness has six jobs. ` +
  `Observation decides what the model gets to see. Context decides what enters the window and when. The control loop decides who acts next and when to stop. ` +
  `Action decides what the agent is allowed to do. State decides what persists across steps. And verification and governance check the work and enforce guard-rails. ` +
  `The survey's key sentence is that agent performance is a property of the model-harness pairing.`, HEX.blue);

// 7. Anatomy
figureSlide("Taxonomy", "$ man harness", "figures/diagrams/harness_anatomy.png",
  "The six parts are coupled: fixing one pushes risk into another.",
  `Each of the six responsibilities comes with a trade-off. Observation trades richness against tractability; a lot of failures are legibility failures, where the information was missing, buried or stale. ` +
  `Context trades fidelity against manageability; the real distinction is monolithic versus managed context. Control trades adaptability against stability. ` +
  `Action trades flexibility against controllability. State trades completeness against usability. And verification versus governance is a nice split: verification produces evidence, governance decides what to do with it. ` +
  `Because these are coupled, aggressive compression can starve the verifier, and a richer action space raises the bar for permissions and rollback.`);

// 8. Task to harness
figureSlide("Taxonomy", "$ match --task --harness", "figures/diagrams/task_to_harness.png",
  "Match the harness to the oracle: tests → verify-and-repair loop; no tests → provenance and review.",
  `How do you choose a harness? The survey maps task properties to failure pressures and to harness responses. ` +
  `Long horizons cause state drift, so you add checkpoints and summaries. Partial observability needs structured observations. ` +
  `If there is a strong oracle, like unit tests, you build verifier loops; if the oracle is weak or delayed, you need provenance and human review. ` +
  `Irreversible actions need sandboxes, gates and rollback. The survey also defines four complexity levels, and says the jump from multi-step to long-horizon tasks is where harness design starts to dominate. ` +
  `Domains differ too: coding is verification-dominant, web agents are grounding-dominant, research is synthesis-dominant.`);

// 9. Harness vs model
pres.addSection({ title: "Evidence" });
figureSlide("Evidence", "$ leaderboard --same-model", "figures/charts/harness_vs_model_tb2.png",
  "Harness spread: median 13.6 pts across 20 models. Model upgrade in a fixed harness: about 30 pts.",
  `Now the evidence. The harness survey treats public leaderboards as observational data. On the left, the same model under different harnesses on Terminal-Bench 2.0. ` +
  `GPT-5.3 Codex spans 13.7 points, Claude Opus 4.6 spans 18.4, Gemini 3.1 Pro spans 20.8. Across 20 models with at least three harnesses, the median spread is 13.6 points, and 14 of the 20 vary by at least 10. ` +
  `But on the right, the survey is honest that it cuts both ways: inside a fixed harness, a newer model adds about 30 points. ` +
  `So both levers are big. I will come back to this in my two cents.`);

// 10. Techniques
{
  const s = pres.addSlide({ masterName: "TITLE_ONLY", sectionTitle: "Evidence" });
  s.addText("$ diff top-entries baseline", { placeholder: "kicker" });
  s.addText("Five techniques behind the top leaderboard entries", { placeholder: "title" });
  const items = [
    ["Searched harnesses", "Meta-Harness searches prompts, tools and policies; SageAgent generates its own scaffold. Powerful, but can overfit the benchmark.", "violet"],
    ["Verify before 'done'", "Terminus-KIRA builds completion checks into the loop. Unforced agents verify near the end in only 24-37% of tasks.", "red"],
    ["Minimal, legible tools", "SWE-agent's agent-computer interface; the ~100-line mini-SWE-agent nearly matches OpenHands (76.8 vs 77.6).", "blue"],
    ["Pipelines for strong oracles", "Agentless and PatchPilot: localize, repair, validate. Cheaper, reproducible, strong on checkable tasks.", "aqua"],
    ["Spend context on purpose", "Top harnesses read far more: Meta-Harness uses ~9.5x Terminus 2's input tokens, and times out less.", "orange"],
  ];
  const w = 2.33, gap = 0.16;
  items.forEach(([t, b, c], i) => card(s, 0.5 + i * (w + gap), 1.85, w, 4.35, t, b, c, { titleSize: 17, bodySize: 15.5, bodyTop: 1.05 }));
  s.addText("Sources: Guo et al. 2026 (Tables 7, 8, 10); Bin et al. 2026 (Table 4)", { x: 0.5, y: 6.6, w: 11, h: 0.35,
    fontSize: 10, color: HEX.ink3, margin: 0, isTextBox: true });
  s.addNotes(`What do the top entries actually do differently? Five patterns. First, searched or generated harnesses: Meta-Harness treats the harness as a search space and optimizes it, and SageAgent writes its own scaffold. ` +
    `Second, verification before declaring done. Terminus-KIRA centres its design on completion checks, and the terminal survey found that, left alone, an agent runs a verification step near the end in only a quarter to a third of tasks. ` +
    `Third, minimal and legible tools: SWE-agent's agent-computer interface, and the 100-line mini-SWE-agent which nearly matches the full OpenHands runtime. ` +
    `Fourth, fixed pipelines like Agentless when tests exist. And fifth, deliberately spending tokens on context, which is the next slide.`);
}

// 11. Cost
figureSlide("Evidence", "$ cost --per-trial", "figures/charts/harness_cost_tradeoff.png",
  "Better harnesses trade money for reliability; accuracy-only leaderboards hide the trade.",
  `This is the most under-discussed result in the harness survey. For Opus 4.6, Meta-Harness uses a median of 755 thousand input tokens per trial, against 79 thousand for Terminus 2, about nine and a half times as much. ` +
  `In exchange, accuracy goes up 13.5 points and timeouts drop from 18 to 8 percent. The same pattern holds for GPT-5.3 Codex with Mux. ` +
  `Better harnesses are not free. They buy reliability with context, and a leaderboard that shows only accuracy hides that trade completely.`, HEX.orange);

// 12. WebArena
figureSlide("Evidence", "$ browse --with-harness", "figures/charts/webarena_harness_lift.png",
  "The web shows the biggest lifts, but systems differ in more than the harness: read as upper bounds.",
  `On the web the effect is even bigger, because a bare model is so weak at browsing. GPT-4o goes from 13 percent to almost 55 with WebOperator. ` +
  `An 8-billion-parameter Llama goes from under 6 percent to 48 with AgentSymbiotic. ` +
  `One caveat I want to be clear about: these systems differ in more than the harness. Some use tree search with many more environment interactions, some add training. So these are upper bounds on what the harness alone contributes.`);

// 13. Terminal stack
pres.addSection({ title: "Terminal agents" });
figureSlide("Terminal agents", "$ ssh terminal-agents-survey", "figures/diagrams/terminal_agent_stack.png",
  "A terminal agent is defined by its execution substrate, not its interface.",
  `Now the terminal agents survey, which zooms into the environment most coding agents actually live in. ` +
  `Its definition is about substrate, not interface: if running commands, reading their output and changing persistent state is what drives progress, it is a terminal agent. ` +
  `It describes four layers on top of the model: interface and observation, runtime and workspace, control and verification, and harness and context. ` +
  `And it proposes a seven-dimensional competence profile, from command formulation to governance. These are responsibilities of the whole system, not abilities of the model.`);

// 14. Ablation
figureSlide("Terminal agents", "$ ablate --harness --model", "figures/charts/terminal_harness_vs_model.png",
  "Model tier changed results by at most 2.5 pts (not significant). Harness changed them by up to 21.25 pts.",
  `This is the cleanest experiment in the four papers. The authors ran DeepSeek-V4 Flash and the larger Pro under three harnesses, mini-SWE-agent, SWE-agent and OpenHands, on identical tasks with paired statistical tests. ` +
  `Changing the model tier barely mattered: at most 2.5 points, and nothing survived multiple-comparison correction. Changing the harness mattered a lot on Claw-SWE-Bench Lite, up to 21 points, and significant. ` +
  `But on SWE-bench Lite the biggest harness gap was only 7 points, and OpenHands and mini-SWE-agent swap places between the two benchmarks. ` +
  `So the harness matters, but how much depends on the benchmark you look at.`, HEX.blue);

// 15. Process profile, then observability (one chart per slide for readability)
figureSlide("Terminal agents", "$ trace --process-signals", "figures/charts/terminal_benchmark_profile.png",
  "Each benchmark exposes a different weakness; agents verify near the end in only 24-37% of tasks.",
  `The same survey also ran one fixed agent, mini-SWE-agent with DeepSeek-V4 Flash, across four benchmark families and logged process signals. ` +
  `Each benchmark exposes a different weakness. SetupBench stresses environment setup. LongCLI-Bench has the lowest success at about 24 percent and the hardest long-horizon demands. ` +
  `BashArena shows the most state-tracking errors and the most governance-relevant commands. ` +
  `And on three of the four benchmarks the agent ran a verification step near the end in only 24 to 37 percent of tasks. Left alone, agents often do not check their work.`, HEX.orange);
figureSlide("Terminal agents", "$ coverage --competences", "figures/charts/terminal_observability.png",
  "Only one benchmark family explicitly scores governance: most reward the answer, not safe behaviour.",
  `This is the survey's coverage map: which of the seven competences each benchmark can even observe. ` +
  `Command formulation and feedback interpretation are well covered. Governance, meaning permissions, sandboxing and side effects, is explicitly scored only by the BashArena and ClawSafety family. ` +
  `Most benchmarks reward getting the right answer and do not penalize doing something dangerous along the way. ` +
  `The survey also cites an audit that found about 16 percent of tasks across five terminal benchmarks could be reward-hacked.`, HEX.red);

// 16. Self-improvement map
pres.addSection({ title: "Self-improvement" });
figureSlide("Self-improvement", "$ agent --rewrite-self", "figures/diagrams/self_improvement_map.png",
  "Keep noisy updates in the scaffold; consolidate into weights only once they are stable.",
  `If the harness matters this much, the next step is to let the agent improve its own harness. The Schmidhuber-group survey formalizes it: an agent is weights plus a scaffold, and the scaffold is prompts, memory, tools and control logic. ` +
  `Self-improvement is any lasting update the agent makes to either part from a signal it produced. ` +
  `The taxonomy is what gets updated, and which signal drives it. Prompts are optimized with scores, critiques, evolving populations or textual gradients. Memory is create, read, update, delete. Tools can be routed, refined or written. ` +
  `And the whole scaffold can be patched as code. Their practical advice: keep noisy updates in the fast, reversible scaffold, and only consolidate into weights once they are stable.`, HEX.green);

// 17. DGM, then memory
figureSlide("Self-improvement", "$ diff harness@v0 harness@vN", "figures/charts/dgm_self_improvement.png",
  "A frozen model with a self-edited harness went from 20% to 50% on SWE-bench.",
  `Here is the headline example, the Darwin Gödel Machine. It keeps the foundation model frozen and lets an archive of coding agents rewrite their own source code, keeping only changes that score better. ` +
  `Per the original paper, SWE-bench went from 20 to 50 percent, and Polyglot from 14 to about 31. ` +
  `What it discovered were harness features: better code-editing tools, long-context window management, and peer-review steps. In other words, it automated harness engineering.`, HEX.green);
figureSlide("Self-improvement", "$ memory --gc", "figures/charts/memory_crud_coverage.png",
  "16 of 25 memory systems have no real forgetting: memory that never forgets eventually lies to you.",
  `The survey also tabulates 25 agent memory systems by create, read, update and delete. Almost all of them write and read memory well. ` +
  `But 16 of the 25 have no real delete or forgetting mechanism, and 10 lack ongoing maintenance. For a long-running agent, memory that never forgets is memory that eventually lies to you. ` +
  `The survey's evaluation rules are worth adopting: report the whole improvement trajectory under a fixed budget, track regressions on tasks you could already solve, and never use the same judge to drive updates and to report results.`, HEX.blue);

// 18. Lifecycle loop, then evidence
pres.addSection({ title: "AgentOps" });
figureSlide("AgentOps", "$ agentops --lifecycle", "figures/diagrams/agent_lifecycle_loop.png",
  "Zero evaluated links from operations back to requirements or design: the feedback loop is broken.",
  `The fourth survey asks what happens after the demo works. If an agent is a product, how is it engineered across its life? The authors map 355 published papers onto five software lifecycle stages, from requirements to maintenance. ` +
  `Testing dominates with 215 papers, against only 26 on requirements: we are much better at measuring agents than at specifying what they should and should not do. ` +
  `And the feedback loop is broken. They found zero implemented or evaluated links from operations back to requirements or design. Production incidents get patched locally and never reach the spec.`, HEX.red);
figureSlide("AgentOps", "$ evidence --real-world", "figures/charts/se_lifecycle_evidence.png",
  "Only 37 of 570 contributions carry evidence from real projects or production.",
  `Evidence quality is the other finding. Of 570 coded contributions, only 37, about six and a half percent, come with evidence from real projects or production; the rest is lab and benchmark evidence. ` +
  `Their motivating example is Anthropic's multi-agent research system: the team could not tell whether bad answers came from queries, sources or tools until they added production tracing, and long-running agents forced rolling deploys with old and new versions side by side. ` +
  `The practices they collect are useful: policy-aware success metrics, pass at k reported next to all-pass at k, pre-action permission checks, formal trace monitors, and versioned prompts with evaluation gates before a model migration. One industrial pilot raised 23 regression alerts in four months: 8 genuine, 12 borderline, 3 false positives.`, HEX.violet);

// 19. Metrics
{
  const s = pres.addSlide({ masterName: "TITLE_ONLY", sectionTitle: "AgentOps" });
  s.addText("$ eval --metrics", { placeholder: "kicker" });
  s.addText("The metrics that matter, merged from all four surveys", { placeholder: "title" });
  const hdr = { bold: true, color: "FFFFFF", fill: { color: HEX.ink }, fontSize: 15 };
  const rows = [
    [{ text: "Metric", options: hdr }, { text: "What it tells you", options: hdr }, { text: "Source", options: hdr }],
    ["Success rate with 95% CI", "Did it work, and how sure are we", "All four"],
    ["pass@k and pass^k (all-pass@k)", "Capability vs reliability", "SE survey; harness survey"],
    ["Cost per successful task", "Real economics, not cost per attempt", "Harness survey"],
    ["Median tokens, wall-clock, timeout rate", "Where the budget goes", "Harness survey, Table 8"],
    ["Final-window verification rate", "Does it check before saying 'done'", "Terminal survey (P5)"],
    ["Recovery rate after failure", "Can it get unstuck", "Terminal survey (P6)"],
    ["Governance trigger rate", "Risky commands, side effects", "Terminal survey (P7)"],
    ["Regression on solved tasks", "Did the update break something", "Self-improvement survey"],
    ["Policy-compliant completion", "Success that also obeyed the rules", "SE survey"],
  ];
  s.addTable(rows, { x: 0.5, y: 1.75, w: 12.3, colW: [4.3, 4.8, 3.2], fontSize: 15, color: HEX.ink,
    border: { type: "solid", pt: 0.5, color: "E5E7EB" }, rowH: 0.5, fill: { color: "FFFFFF" }, margin: 0.06 });
  s.addNotes(`Pulling the four surveys together, this is the metric set I would want on any agent result. Success with a confidence interval. ` +
    `pass at k and pass hat k together, because pass at k measures whether it can ever succeed, and pass hat k whether it succeeds every time, which is what a user cares about. ` +
    `Cost per successful task, not per attempt. Tokens, wall-clock and timeout rate. Then process signals from the terminal survey: does it verify before saying done, does it recover after a failure, how often does it run risky commands. ` +
    `Regression on previously solved tasks, from the self-improvement survey. And policy-compliant completion from the SE survey: success only counts if the agent also followed the rules.`);
}

// 20. Two cents: reality check
pres.addSection({ title: "My two cents" });
figureSlide("My two cents", "$ two-cents --leaderboards", "figures/charts/leaderboard_reality_check.png",
  "Benchmark version and referee matter as much as the harness. One ranking is one measurement.",
  `Now my two cents. I checked the live leaderboards on November 19. On the left, Opus 4.6 under nine harnesses on Terminal-Bench 2.0, from 58 to 76 percent. ` +
  `On the right, the part that surprised me: harness rankings flip. On the 2.0 board, Claude Code trails Terminus 2 for Opus 4.6. In the benchmark team's own re-run on the corrected 2.1 tasks, Claude Code wins by 6 points. ` +
  `On the 2.1 board GPT-5.5 scores 83 in Codex and 78 in Terminus 2, but Vals AI's independent run of the same benchmark gives 57 in Codex and 76 in Terminus 2. ` +
  `And the Terminal-Bench maintainers had to publish an integrity policy this year after finding cheating and reward hacking. So I treat any single harness ranking as one measurement, not a fact about the harness.`, HEX.red);

// 21. Two cents cards
{
  const s = pres.addSlide({ masterName: "TITLE_ONLY", sectionTitle: "My two cents" });
  s.addText("$ two-cents --critique", { placeholder: "kicker" });
  s.addText("Where I think the story is weaker than it sounds", { placeholder: "title" });
  const cards = [
    ["'Harness, not model' is half true", "Model upgrades add ~30 pts in a fixed harness vs a 13.6-pt median harness spread. The model sets the ceiling; the harness decides how much of it you reach.", "blue"],
    ["Vendor CLIs at the bottom is not a scandal", "Product CLIs are built for humans in the loop; leaderboard harnesses are tuned, some literally searched, for the benchmark. No one has tested transfer yet.", "orange"],
    ["Cost is the missing axis", "Only 15.2% of Terminal-Bench trial records carry cost. On TB 2.1, Codex spends ~4x Terminus 2 ($2.1k vs $0.5k) for +5 pts.", "yellow"],
    ["Governance and forgetting are blind spots", "1 benchmark family scores governance; 16 of 25 memory systems cannot forget; 0 papers link operations back to requirements.", "red"],
  ];
  const w = 6.05, h = 2.2;
  cards.forEach(([t, b, c], i) => card(s, 0.5 + (i % 2) * (w + 0.2), 1.8 + Math.floor(i / 2) * (h + 0.2), w, h, t, b, c, { titleSize: 18, bodySize: 16 }));
  s.addText("Also check before citing: mixed model versions in one survey table; single-family, single-run diagnostics; published-only corpus in the SE survey.",
    { x: 0.5, y: 6.6, w: 12.2, h: 0.5, fontSize: 12, italic: true, color: HEX.ink2, margin: 0, isTextBox: true });
  s.addNotes(`Four more critiques. First, "it's the harness, not the model" is half true. The survey's own numbers show model upgrades adding about 30 points in a fixed harness, against a median harness spread of 13.6. The terminal survey's "model tier barely matters" compares two variants of one model family. My reading: the model sets the ceiling, the harness decides how much of it you reach. ` +
    `Second, vendor CLIs ranking low is not a scandal. Claude Code and Gemini CLI are built for interactive use with a human approving actions; leaderboard harnesses are tuned, and some literally searched, against the benchmark. ` +
    `Third, cost is the missing axis. Only 15 percent of trial records carry cost. On the 2.1 board, GPT-5.5 in Codex spends about four times what Terminus 2 does for five more points. ` +
    `Fourth, governance and forgetting are blind spots. The field optimizes for finishing tasks far more than for being safe to leave running. ` +
    `And all four are first versions with some rough edges, so check the primary source behind any number you cite.`);
}

// 22. Report card
figureSlide("My two cents", "$ report-card --required", "figures/diagrams/harness_report_card.png",
  "My proposal: no agent score without identity, budget, outcome with CI, process signals and provenance.",
  `If I could add one convention to the field, it would be this report card. Every agent result should say which model and harness, with versions and reasoning effort. ` +
  `The budget: step limits, retries, tokens and dollars. The outcome with a confidence interval, cost per success, and regressions. A few process signals: verification, recovery, governance events. ` +
  `And provenance: who ran it, which benchmark version, and whether the traces are published. The identity and budget fields alone would explain most of the ranking flips I just showed you.`, HEX.violet);

// 23. Checklist
{
  const s = pres.addSlide({ masterName: "TITLE_ONLY", sectionTitle: "My two cents" });
  s.addText("$ checklist --practitioner", { placeholder: "kicker" });
  s.addText("If you are building an agent next week", { placeholder: "title" });
  const left = ["Start minimal: a small, legible tool loop is the baseline to beat",
    "Match the harness to the oracle: tests → verify-and-repair loop",
    "Manage context: compact, fold finished sub-tasks, load skills on demand",
    "Gate irreversible actions: sandbox, approvals, rollback"];
  const right = ["Measure reliability: pass^k next to pass@k, repeated runs, CIs",
    "Put cost per successful task on the same chart as accuracy",
    "Trace everything and feed it back into specs, not just hotfixes",
    "Self-improving? Gate every change, never grade with the guiding judge"];
  const list = (arr, x, start) => s.addText(arr.map((t, i) => ({ text: `${start + i}.  ${t}`,
    options: { breakLine: i < arr.length - 1, paraSpaceAfter: 26 } })), { x, y: 2.05, w: 5.55, h: 4.2, fontSize: 20,
    color: HEX.ink, margin: 0, valign: "top", isTextBox: true });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.5, y: 1.75, w: 6.05, h: 4.6, rectRadius: 0.1, fill: { color: TINT.blue }, line: { color: "FFFFFF", width: 0 } });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 6.78, y: 1.75, w: 6.05, h: 4.6, rectRadius: 0.1, fill: { color: TINT.aqua }, line: { color: "FFFFFF", width: 0 } });
  list(left, 0.75, 1);
  list(right, 7.03, 5);
  s.addNotes(`To make this practical, here is what I would do if I were building an agent next week. Start minimal: a small, legible tool loop on a strong model is the baseline to beat. ` +
    `Match the harness to the oracle. Manage context deliberately. Gate irreversible actions with sandboxes, approvals and rollback. ` +
    `Measure reliability, not just capability. Put cost per successful task on the same chart as accuracy. Trace everything and feed production lessons back into your specs. ` +
    `And if you let the agent improve itself, gate every change with held-out tests, and never grade with the same judge that guided the change.`);
}

// 24. Close
{
  const s = pres.addSlide({ masterName: "DARK", sectionTitle: "My two cents" });
  s.addText("$ exit 0", { x: 0.7, y: 0.8, w: 6, h: 0.4, fontFace: "Courier New", fontSize: 13, bold: true, color: "93C5FD",
    margin: 0, isTextBox: true });
  s.addText("Strong models are becoming a commodity.\nThe harness is where agents now differ.", { x: 0.7, y: 1.4, w: 11.8, h: 1.8,
    fontSize: 36, bold: true, color: "FFFFFF", margin: 0, valign: "top", isTextBox: true });
  s.addText("It deserves the rigour we gave to models: controlled comparisons, honest cost accounting, and results reported with their full configuration.",
    { x: 0.7, y: 3.35, w: 11.5, h: 0.9, fontSize: 18, color: "D1D5DB", margin: 0, isTextBox: true });
  const refs = [
    "Guo et al., Agent System and Harness Design, arXiv 2606.20683 (Jun 2026)",
    "Ren et al., Self-Improvements in Modern Agentic Systems, arXiv 2607.13104 (Jul 2026)",
    "Bin et al., Terminal Agents, arXiv 2608.20485 (Aug 2026)",
    "Ge et al., Software Engineering for LLM-Based Agents, arXiv 2611.23260 (Oct 2026)",
    "Leaderboards: tbench.ai (TB 2.0 / 2.1), vals.ai, accessed 19 Nov 2026",
  ];
  s.addText(refs.map((t, i) => ({ text: t, options: { bullet: true, breakLine: i < refs.length - 1 } })),
    { x: 0.7, y: 4.45, w: 8.6, h: 2.1, fontSize: 13, color: "D1D5DB", margin: 0, valign: "top", paraSpaceAfter: 4, isTextBox: true });
  s.addText([{ text: "Data, code, article and slides", options: { bold: true, color: "FFFFFF", breakLine: true } },
    { text: REPO, options: { color: "93C5FD" } }], { x: 9.4, y: 4.45, w: 3.6, h: 1.4, fontSize: 13, margin: 0, isTextBox: true, valign: "top" });
  s.addNotes(`To wrap up. The four surveys agree on the main point: an LLM agent is a system, and its behaviour comes from the model, the harness, the runtime and the evaluation together. ` +
    `The harness survey gives the vocabulary, the terminal survey gives the cleanest experiment, the self-improvement survey shows where automation is heading, and the software engineering survey shows how much discipline is still missing. ` +
    `My takeaway: strong models are becoming a commodity, and the harness is where agents now differ. It deserves the same rigour we gave to models. ` +
    `All the data, code, the article and these slides are in my GitHub repository. Thank you.`);
}

(async () => {
  await pres.writeFile({ fileName: OUT });
  // Optional: write THEME's colours into the .pptx theme part (every colour is also set directly,
  // so the deck looks the same without this step).
  if (process.env.APPLY_THEME) {
    const { applyTheme } = require(process.env.APPLY_THEME);
    await applyTheme(OUT, THEME);
  }
  console.log("wrote", path.relative(ROOT, OUT));
})();
