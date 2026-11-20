# Data behind every figure

Every number plotted in this repository is in one of these CSV files, and each file says where its numbers came from. Survey values were copied from the arXiv text and checked against the rendered PDF tables. Live leaderboard values are a snapshot taken on **19 November 2026**.

| File | Contents | Source | Used by |
|---|---|---|---|
| `surveys.csv` | The four surveys: arXiv ID, title, authors, date, pages | arXiv abstract pages | survey timeline |
| `harness_tb2_same_model.csv` | Terminal-Bench 2.0 score, tokens, runtime and timeouts for one model under several harnesses | arXiv 2606.20683, Table 8 and Sec. 7.3 | `harness_vs_model_tb2`, `harness_cost_tradeoff` |
| `harness_tb2_same_harness.csv` | The same harness with successive model generations | arXiv 2606.20683, Sec. 7.3 | `harness_vs_model_tb2` |
| `harness_swebench_verified.csv` | SWE-bench Verified resolved rate by model and harness | arXiv 2606.20683, Table 7 | article text |
| `harness_webarena.csv` | WebArena bare model vs harness low/high | arXiv 2606.20683, Table 9 | `webarena_harness_lift` |
| `terminal_matched_runs.csv` | Matched DeepSeek-V4 Flash/Pro × 3 harnesses × 2 benchmarks (resolved counts) | arXiv 2608.20485, Tables 5 and 11 | `terminal_harness_vs_model` |
| `terminal_benchmark_profile.csv` | Outcome and process indicators P1–P7 on four benchmarks | arXiv 2608.20485, Table 4 | `terminal_benchmark_profile` |
| `terminal_observability.csv` | Which competence each benchmark can observe (E/T/I/–) | arXiv 2608.20485, Table 3 | `terminal_observability` |
| `se_lifecycle_stages.csv` | Papers and contributions per lifecycle stage, with evidence levels | arXiv 2611.23260, Sec. 3.5, stage syntheses, Table 12 | `se_lifecycle_evidence`, lifecycle diagram |
| `corpus_by_year.csv` | Papers per release year in two survey corpora | arXiv 2608.20485 Table 6; arXiv 2611.23260 Sec. 3.5 | `corpus_growth` |
| `memory_crud_coverage.csv` | How 25 memory systems implement create/read/update/delete | arXiv 2607.13104, Table 4 (counted from the rendered table) | `memory_crud_coverage` |
| `self_improvement_dgm.csv` | Darwin Gödel Machine before/after | arXiv 2505.22954 (abstract), reviewed in arXiv 2607.13104 Sec. 6.4 | `dgm_self_improvement` |
| `live_tb2_opus46_harnesses.csv` | Claude Opus 4.6 under nine harnesses on the TB 2.0 board, with the 95% CI shown on the board | tbench.ai, accessed 19 Nov 2026 | `leaderboard_reality_check` |
| `live_harness_ranking_flips.csv` | Vendor harness vs Terminus 2 across board versions and evaluators | tbench.ai boards and TB 2.1 post; vals.ai TB 2.1 page | `leaderboard_reality_check` |

## Things computed here, not reported by the papers

- **Wilson 95% confidence intervals** in `terminal_harness_vs_model` come from the paired resolved counts in Table 11 of arXiv 2608.20485.
- **Ratios** quoted in the text, such as "about 9.5 times the input tokens" (755.0K ÷ 79.4K), are my arithmetic on reported values.
- The **"harness gap" and "model-tier gap"** labels are maximum minus minimum over the reported cells. They match the paper's own statements (21.25 and 2.50 points).

## Caveats

- Leaderboard comparisons are **observational**. Submissions can differ in prompts, budgets, reasoning effort and versions, and the surveys say so too.
- The terminal survey's ablation uses **one model family, one run per task**, and an LLM judge from the same family for some process indicators.
- In arXiv 2606.20683 Table 7, some row labels group **different model versions** (for example "Claude Opus 4 / 4.5"). `harness_swebench_verified.csv` keeps only the rows whose model is clear from the text.
