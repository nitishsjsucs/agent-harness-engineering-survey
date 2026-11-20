#!/usr/bin/env python3
"""Fill the published links into the README and the article once you have them.

Usage (run from the repo root, any subset of flags):

    python3 tools/update_links.py \
        --medium     https://medium.com/@you/your-story \
        --slideshare https://www.slideshare.net/slideshow/your-deck \
        --youtube    https://youtu.be/VIDEO_ID

How it works
- README.md uses reference-style links at the bottom of the file, e.g.
  `[medium]: article/medium_article.md`. The script rewrites those lines, so every
  badge and table cell that says `[...][medium]` points at the new URL.
- The article and video guide wrap links in HTML comment markers, e.g.
  <!--MEDIUM-->...<!--/MEDIUM-->, and the script replaces what is between them.
Re-running the script with a new URL is safe.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REF_FILES = [ROOT / "README.md", ROOT / "RUBRIC_CHECKLIST.md"]
MARKER_FILES = [ROOT / "article" / "medium_article.md", ROOT / "video" / "README.md"]


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--medium")
    p.add_argument("--slideshare")
    p.add_argument("--youtube")
    args = p.parse_args()
    links = {k: v.strip() for k, v in vars(args).items() if v}
    if not links:
        p.error("pass at least one of --medium / --slideshare / --youtube")

    for path in REF_FILES:
        if not path.exists():
            continue
        text, total = path.read_text(encoding="utf-8"), 0
        for key, url in links.items():
            text, n = re.subn(rf"^\[{key}\]: .*$", f"[{key}]: {url}", text, flags=re.M)
            total += n
        path.write_text(text, encoding="utf-8")
        print(f"{path.relative_to(ROOT)}: updated {total} reference link(s)")

    for path in MARKER_FILES:
        if not path.exists():
            continue
        text, total = path.read_text(encoding="utf-8"), 0
        for key, url in links.items():
            tag = key.upper()
            text, n = re.subn(rf"(<!--{tag}-->)(.*?)(<!--/{tag}-->)", lambda m: f"{m.group(1)}{url}{m.group(3)}", text, flags=re.S)
            total += n
        path.write_text(text, encoding="utf-8")
        print(f"{path.relative_to(ROOT)}: updated {total} marked link(s)")


if __name__ == "__main__":
    main()
