#!/usr/bin/env python3
"""Build a paste-ready HTML version of the article for the Medium editor.

Medium cannot render Markdown tables or relative image paths, so this script:
  * turns every Markdown table into a bulleted list (one bullet per row),
  * points images at the public GitHub copy of the repo (raw.githubusercontent.com),
  * drops the HTML comment markers used by tools/update_links.py,
  * converts the result to HTML with pandoc (figures get their alt text as captions).

Usage:  python3 tools/build_medium_html.py [--repo nitishsjsucs/agent-harness-engineering-survey] [--branch main]
Then open article/medium_article.html in a browser, select all, copy, and paste into a new Medium story.
"""
from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "article" / "medium_article.md"
OUT = ROOT / "article" / "medium_article.html"


def table_to_list(block: str) -> str:
    rows = [r.strip() for r in block.strip().splitlines()]
    header = [c.strip() for c in rows[0].strip("|").split("|")]
    items = []
    for r in rows[2:]:
        cells = [c.strip() for c in r.strip("|").split("|")]
        head, rest = cells[0], cells[1:]
        parts = [f"{h}: {c}" if h and h not in ("#",) else c for h, c in zip(header[1:], rest) if c]
        if header[0] == "#":  # numbered survey table: lead with the title column
            head, parts = rest[0], [f"{h}: {c}" for h, c in zip(header[2:], rest[1:]) if c]
        lead = head if ("*" in head or "[" in head) else f"**{head}**"
        items.append(f"- {lead} — " + " · ".join(parts))
    return "\n".join(items) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default="nitishsjsucs/agent-harness-engineering-survey")
    ap.add_argument("--branch", default="main")
    args = ap.parse_args()
    md = SRC.read_text(encoding="utf-8")
    md = re.sub(r"(?m)(^\|.*\|\s*\n)+", lambda m: table_to_list(m.group(0)), md)
    raw = f"https://raw.githubusercontent.com/{args.repo}/{args.branch}/"
    md = md.replace("](../", f"]({raw}")
    md = re.sub(r"<!--/?[A-Z]+-->", "", md)
    html = subprocess.run(["pandoc", "-f", "markdown", "-t", "html5", "--standalone",
                           "--metadata", "title=The Harness Is Half the Agent", "--wrap=none"],
                          input=md, capture_output=True, text=True, check=True).stdout
    # pandoc's standalone template repeats the title; Medium takes the first H1 as the story title
    html = re.sub(r'<header id="title-block-header">.*?</header>', "", html, flags=re.S)
    OUT.write_text(html, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(re.findall('<img', html))} images, "
          f"{html.count('<table')} tables left)")


if __name__ == "__main__":
    main()
