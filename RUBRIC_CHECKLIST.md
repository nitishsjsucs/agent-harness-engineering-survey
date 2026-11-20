# Rubric checklist: Short Story assignment (individual)

Every line of the assignment brief, mapped to the artifact that satisfies it. ✅ = done in this repo. ⏳ = a step only the student can do (publishing under their own accounts), with exact instructions.

| # | Requirement from the brief | How it is met | Status |
|---|---|---|---|
| 1 | Individual assignment | Single-author repo, article and talk | ✅ |
| 2 | Topic approved in the class spreadsheet | Topic: *LLM agent harness engineering: agents, tool use, evaluation and AgentOps* | ⏳ confirm it matches your approved row |
| 3 | Survey papers from the **last 3 to 6 months** | arXiv v1 dates 14 Jun, 14 Jul, 20 Aug and 3 Oct 2026, all within six months of 19 Nov 2026 ([`papers/README.md`](papers/README.md)) | ✅ |
| 4 | From **good authors** | Groups led by Yunhe Wang, Chang Xu and Kai Han; Jürgen Schmidhuber (IDSIA/KAUST); Heng Tao Shen and Jingkuan Song; Zhi Jin and Yang Liu | ✅ |
| 5 | **Interesting gen-AI topic** (AI engineering, agents, prompting, reasoning, memory, tool use, risk/safety, LLMOps, evaluation, on-device…) | Covers agents, tool use, memory, self-improvement, evaluation/benchmarks, safety/governance and LLMOps/AgentOps | ✅ |
| 6 | **Summarise the main taxonomy** (various approaches) | Article Parts 1, 2, 4, 5, 6; slides 5–8, 13, 17, 20; README "taxonomy at a glance" with a Mermaid diagram | ✅ |
| 7 | **Explain important techniques that appear on the leaderboards** | Article Part 3 "techniques behind the top entries" (searched harnesses, ACI, verification, pipelines, managed context); slide 10; README table | ✅ |
| 8 | Encourage **LLMOps / LLM development** angle (evaluation, ops) | SE-for-agents survey (testing, guardrails, tracing, regression); metrics table; harness report card | ✅ |
| 9 | Clues list (awesome-generative-ai-guide) and **latest arXiv surveys** | Surveys found by searching arXiv for May–Nov 2026 surveys on agents, evaluation, memory and LLMOps | ✅ |
| 10 | **GitHub directory, public**, with a **proper README** | This repo; README with badges, contents, figures, layout, reproduction steps | ✅ |
| 11 | Add the **GitHub link to the spreadsheet** | — | ⏳ paste `https://github.com/nitishsjsucs/agent-harness-engineering-survey` into your row |
| 12 | Turn the paper into a **nice article written from scratch** (no copy-paste, paraphrase and summarise) | [`article/medium_article.md`](article/medium_article.md): original prose; one short attributed quote; all figures drawn from the data | ✅ |
| 13 | **Add more survey content together** | Primary survey plus three companion surveys plus a live leaderboard snapshot | ✅ |
| 14 | Focus on **gist, architecture, ablation studies and metrics** rather than math | Architecture: harness anatomy, terminal stack. Ablation: matched harness-vs-model experiment. Metrics: Part 7 table | ✅ |
| 15 | **As many pictures and visualisations as possible** | 20 original figures (11 data charts, 9 diagrams) | ✅ |
| 16 | **Your own two cents** on the papers | Article "My two cents" (6 points), slides 23–25, report-card proposal | ✅ |
| 17 | Article a **few pages long** | ~4,300 words, about 18 minutes of reading | ✅ |
| 18 | **Publish on Medium** | Paste [`article/medium_article.html`](article/medium_article.html) into the Medium editor (see below) | ⏳ [Medium link][medium] |
| 19 | **Slide deck** explaining the short story | [`slides/harness_short_story.pptx`](slides/harness_short_story.pptx), 27 slides with speaker notes | ✅ |
| 20 | **Presentation on SlideShare** | Upload [`slides/harness_short_story.pdf`](slides/harness_short_story.pdf) | ⏳ [SlideShare link][slideshare] |
| 21 | Submit the **Medium and SlideShare links** | Run `tools/update_links.py` and paste the links into Canvas | ⏳ |
| 22 | **Record a 10–15 min video with slides** and **upload it to the GitHub directory** | Script ready ([`video/presentation_script.md`](video/presentation_script.md)); compress with `tools/compress_video.sh` and commit to `video/` | ⏳ |
| 23 | **YouTube video no less than 15 minutes** | Script times at ~16–17.5 min | ⏳ [YouTube link][youtube] |
| 24 | Submit the **GitHub directory link with all details in a nice README** | This repo | ✅ |

> Note on video length: the brief says "10–15 minute video" in one place and "no less than 15 min" in another. The script is written to run **just over 15 minutes** (about 16 min at a brisk 150 words per minute, about 17.5 min at 135), which satisfies both.

## The publishing steps

1. **Medium.** Open [`article/medium_article.html`](article/medium_article.html) in a browser, press Cmd+A then Cmd+C, and paste into a new Medium story. Images load from this public repo, so push the repo first. Check that every image appears, set the title and subtitle, add 5 tags (e.g. *AI Agents, LLM, Machine Learning, MLOps, Generative AI*), and publish. Medium's **Import a story** (Profile → Stories → Import) with the GitHub file URL is a fallback.
2. **SlideShare.** Upload `slides/harness_short_story.pdf` with the title *The Harness Is Half the Agent* and a description with the four arXiv IDs.
3. **Video.** Follow [`video/README.md`](video/README.md): record over the slides reading the script, compress, commit the MP4 to `video/`, and upload to YouTube (public or unlisted).
4. **Fill the links**, then commit and push:

   ```bash
   python3 tools/update_links.py --medium <url> --slideshare <url> --youtube <url>
   ```

5. **Spreadsheet and Canvas.** Add the GitHub URL to the class spreadsheet, and submit the GitHub, Medium, SlideShare and YouTube links.

[medium]: article/medium_article.md
[slideshare]: slides/harness_short_story.pdf
[youtube]: video/README.md
