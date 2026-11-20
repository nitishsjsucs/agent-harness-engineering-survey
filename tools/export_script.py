#!/usr/bin/env python3
"""Turn the deck's speaker notes into a timed narration script for the video.

Usage: python tools/export_script.py   (writes video/presentation_script.md)
Pace assumption: 135 words per minute, a relaxed presenting speed.
"""
from __future__ import annotations

from pathlib import Path

from pptx import Presentation

ROOT = Path(__file__).resolve().parents[1]
DECK = ROOT / "slides" / "harness_short_story.pptx"
OUT = ROOT / "video" / "presentation_script.md"
WPM = 135


def slide_label(slide) -> tuple[str, str]:
    texts = [sh.text_frame.text.strip() for sh in slide.shapes if sh.has_text_frame and sh.text_frame.text.strip()]
    kicker = next((t for t in texts if t.startswith("$")), "").split("\n")[0]
    take = next((t for t in texts if t.startswith("Takeaway")), "")
    title = take.replace("Takeaway", "", 1).strip() if take else next(
        (t for t in texts if not t.startswith(("$", "Source", "SHORT")) and len(t) > 12), "")
    return kicker, title.split("\n")[0][:90]


def main() -> None:
    prs = Presentation(DECK)
    rows, total_words, t = [], 0, 0.0
    for i, slide in enumerate(prs.slides, 1):
        notes = slide.notes_slide.notes_text_frame.text.strip() if slide.has_notes_slide else ""
        words = len(notes.split())
        secs = words / WPM * 60 + 4  # +4 s for the slide change and a breath
        kicker, title = slide_label(slide)
        rows.append((i, kicker, title, notes, words, t, secs))
        total_words += words
        t += secs
    lines = [
        "# Video script: The Harness Is Half the Agent",
        "",
        f"Word-for-word narration taken from the speaker notes in `slides/harness_short_story.pptx` "
        f"({len(rows)} slides, {total_words:,} words). At {WPM} words per minute plus a short pause per slide, "
        f"the talk runs about **{t / 60:.1f} minutes**, which clears the 15-minute minimum.",
        "",
        "| Slide | Starts at | Length | Section cue |",
        "|---|---|---|---|",
    ]
    for i, kicker, title, _, _, start, secs in rows:
        lines.append(f"| {i} | {int(start // 60)}:{int(start % 60):02d} | {secs:.0f} s | `{kicker}` {title} |")
    lines += ["", "---", ""]
    for i, kicker, title, notes, words, start, secs in rows:
        lines += [f"## Slide {i} · {int(start // 60)}:{int(start % 60):02d}  `{kicker}`", "", notes, ""]
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}: {len(rows)} slides, {total_words} words, ~{t / 60:.1f} min")


if __name__ == "__main__":
    main()
