#!/usr/bin/env python3
"""Extract readable text and chart values from a SelectHub buyer report (HTML).

The buyer report artifact is a large HTML page. Its charts are inline SVGs that
keep each value in a `data-tip` attribute. This script turns the page into plain
text: headings, paragraphs, list items, and table rows stay as lines, and each
chart becomes a "[CHART] <title> | <subtitle>" line followed by its values.

Usage:
    python3 extract_report.py <report.html> [-o report.txt]

Without -o, the text goes to stdout.
"""
import argparse
import html
import re
import sys


def chart_to_text(match):
    svg = match.group(0)
    title = re.search(r"<title>(.*?)</title>", svg, flags=re.S)
    # The chart subtitle is the second-line <text> in the secondary ink colour.
    subtitle = re.search(
        r'font-size="11\.5" fill="var\(--ink-2[^"]*\)">([^<]*)</text>', svg
    )
    tips = re.findall(r'data-tip="([^"]*)"', svg)
    head = "[CHART] " + (title.group(1).strip() if title else "")
    if subtitle:
        head += " | " + subtitle.group(1).strip()
    lines = [head] + ["  - " + t for t in tips]
    return "\n" + "\n".join(lines) + "\n"


def extract(raw):
    s = re.sub(r"<style.*?</style>", "", raw, flags=re.S)
    s = re.sub(r"<script.*?</script>", "", s, flags=re.S)
    s = re.sub(r"<svg.*?</svg>", chart_to_text, s, flags=re.S)
    s = re.sub(r"<(h[1-4]|p|li|tr|blockquote)[^>]*>", "\n", s)
    s = re.sub(r"<t[dh][^>]*>", " | ", s)
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s)
    s = re.sub(r"[ \t]+\n", "\n", s)
    s = re.sub(r"\n\s*\n+", "\n", s)
    return s.strip() + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("html_file", help="Saved HTML of the buyer report")
    ap.add_argument("-o", "--output", help="Write text here instead of stdout")
    args = ap.parse_args()

    with open(args.html_file, encoding="utf-8", errors="replace") as f:
        text = extract(f.read())

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Wrote {len(text.splitlines())} lines to {args.output}", file=sys.stderr)
    else:
        sys.stdout.write(text)


if __name__ == "__main__":
    main()
