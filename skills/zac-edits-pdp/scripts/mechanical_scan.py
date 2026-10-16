#!/usr/bin/env python3
"""Mechanical scan for SelectHub product review copy.

Flags candidate issues that are easy to detect by pattern. Every flag is a
candidate, not a verdict: the editor decides if the flag is a real problem
in context.

Usage:
    python mechanical_scan.py <file.txt|file.md|file.html|-> [--product "Name"] [--json]
                              [--max-words 30]

Reads plain text, Markdown, or HTML (tags are stripped). Use "-" for stdin.
"""
import argparse
import html
import json
import re
import sys
from collections import Counter, defaultdict

# --- Word lists -------------------------------------------------------------

PROMOTIONAL = [
    "award-winning", "industry-leading", "best-in-class", "best of breed",
    "user-friendly", "intuitive", "powerful", "seamless", "seamlessly",
    "robust", "blazing-fast", "lightning-fast", "lightning-quick",
    "cutting-edge", "next-generation", "next-gen", "world-class",
    "innovative", "revolutionary", "unparalleled", "game-changer",
    "game-changing", "state-of-the-art", "leading", "top-notch",
    "users love", "trusted by", "most popular", "mastery", "unmatched",
    "effortless", "effortlessly", "comprehensive", "all-in-one",
    "one-stop shop", "empower", "empowers", "supercharge", "elevate",
    "unlock", "unlocks", "leverage", "leverages", "synergy",
]

VAGUE_EVALUATIONS = [
    "strong", "stronger", "advanced", "depth", "deep", "robust",
    "transparent", "transparency", "solid", "flexible", "flexibility",
    "extensive", "rich", "feature-rich", "versatile", "scalable",
    "sophisticated", "limited", "lacks depth", "decent", "good", "great",
    "excellent", "impressive", "easy", "easy to use", "ease of use",
    "simple", "clunky", "outdated", "modern", "sleek",
]

HEDGES = [
    "may", "might", "could", "might not", "may not", "possibly",
    "potentially", "perhaps", "somewhat", "arguably", "tends to",
    "seems to", "appears to", "can be", "some users", "some reviewers",
    "in some cases",
]

FILLER = [
    "very", "really", "quite", "actually", "basically", "essentially",
    "just", "simply", "truly", "literally", "overall", "in order to",
    "a wide range of", "a variety of", "a number of", "various",
    "it is important to note", "it's important to note", "it is worth noting",
    "it's worth noting", "when it comes to", "in terms of", "the fact that",
    "at the end of the day", "due to the fact that", "in today's",
    "ensure that", "in consultation with", "according to the vendor",
    "allows users to", "allows you to", "enables users to",
    "helps users", "is able to", "are able to", "etc", "and more",
]

METAPHOR_JARGON = [
    "gated behind", "gated", "baked in", "out of the box", "out-of-the-box",
    "under the hood", "heavy lifting", "table stakes", "mobile-first",
    "best-of-both-worlds", "move the needle", "low-hanging fruit",
    "bells and whistles", "robust suite", "holistic", "end-to-end",
]

VAGUE_COMPARATIVES = ["more", "better", "higher", "lower", "fewer", "less", "faster", "cheaper"]

# Irregular participles that commonly follow "to be" in passive voice.
IRREGULAR_PP = {
    "built", "made", "done", "given", "shown", "known", "seen", "taken",
    "written", "sold", "bought", "held", "kept", "left", "paid", "put",
    "set", "sent", "spent", "found", "brought", "told", "thought", "run",
    "hidden", "chosen", "driven", "broken", "drawn", "grown", "begun",
}
BE_FORMS = r"(?:is|are|was|were|be|been|being|is\s+not|are\s+not|isn't|aren't|wasn't|weren't)"

# --- Helpers ----------------------------------------------------------------


def load_text(path):
    raw = sys.stdin.read() if path == "-" else open(path, encoding="utf-8", errors="replace").read()
    if re.search(r"<(p|div|h\d|li|span|br|body)\b", raw, re.I):
        raw = re.sub(r"(?is)<(script|style).*?</\1>", " ", raw)
        raw = re.sub(r"(?i)<br\s*/?>|</(p|div|h\d|li|tr)>", "\n", raw)
        raw = re.sub(r"<[^>]+>", " ", raw)
        raw = html.unescape(raw)
    return raw


def split_sentences(line):
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'(])", line.strip())
    return [p for p in parts if p.strip()]


def phrase_regex(phrase):
    esc = re.escape(phrase).replace(r"\ ", r"\s+")
    return re.compile(r"(?<![\w-])" + esc + r"(?![\w-])", re.I)


def compile_list(words):
    # Longest first so "might not" wins over "might".
    return [(w, phrase_regex(w)) for w in sorted(set(words), key=len, reverse=True)]


def find_terms(sentence, compiled):
    hits, taken = [], []
    for word, rx in compiled:
        for m in rx.finditer(sentence):
            if any(m.start() < e and m.end() > s for s, e in taken):
                continue
            taken.append((m.start(), m.end()))
            hits.append(m.group(0))
    return hits


def short(s, n=160):
    s = re.sub(r"\s+", " ", s).strip()
    return s if len(s) <= n else s[: n - 1] + "…"


# --- Checks -----------------------------------------------------------------


def scan(text, product=None, max_words=30):
    findings = defaultdict(list)
    lists = {
        "promotional": compile_list(PROMOTIONAL),
        "vague_evaluation": compile_list(VAGUE_EVALUATIONS),
        "hedge": compile_list(HEDGES),
        "filler": compile_list(FILLER),
        "metaphor_jargon": compile_list(METAPHOR_JARGON),
    }
    passive_rx = re.compile(
        r"\b" + BE_FORMS + r"\s+(?:\w+ly\s+)?(\w+ed|" + "|".join(IRREGULAR_PP) + r")\b(\s+by\b)?",
        re.I,
    )
    comp_rx = re.compile(r"\b(" + "|".join(VAGUE_COMPARATIVES) + r")\b(?![^.]*\bthan\b)", re.I)
    double_rx = re.compile(r"\b(\w+)\s+\1\b", re.I)
    pronoun_start_rx = re.compile(r"^(It|This|That|These|They|Its)\b(?!\s+\w+ly\b)")

    openers = Counter()
    opener_examples = defaultdict(list)
    sentence_count = 0
    word_count = 0

    for ln, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        for sent in split_sentences(line):
            words = re.findall(r"[A-Za-z0-9'’-]+", sent)
            if not words:
                continue
            sentence_count += 1
            word_count += len(words)
            loc = {"line": ln, "text": short(sent)}

            for key, compiled in lists.items():
                hits = find_terms(sent, compiled)
                if hits:
                    findings[key].append({**loc, "terms": hits})

            hyph = re.findall(r"\b[A-Za-z]+(?:-[A-Za-z]+)+\b", sent)
            if len(hyph) >= 3:
                findings["hyphen_heavy"].append({**loc, "terms": hyph})

            if len(words) > max_words:
                findings["long_sentence"].append({**loc, "words": len(words)})

            for m in passive_rx.finditer(sent):
                findings["passive_voice"].append({**loc, "terms": [m.group(0)]})

            comps = [m.group(1) for m in comp_rx.finditer(sent)]
            if comps:
                findings["incomplete_comparison"].append({**loc, "terms": comps})

            for m in double_rx.finditer(sent):
                if m.group(1).lower() not in {"that", "had"}:
                    findings["doubled_word"].append({**loc, "terms": [m.group(0)]})

            if pronoun_start_rx.match(sent.strip()):
                findings["unclear_pronoun_start"].append({**loc, "terms": [sent.split()[0]]})

            if len(words) >= 2:
                op = " ".join(w.lower() for w in words[:2])
                openers[op] += 1
                opener_examples[op].append(ln)

    for op, n in openers.items():
        if n >= 3:
            findings["repeated_opener"].append({"opener": op, "count": n, "lines": opener_examples[op][:10]})

    # Product name consistency.
    if product:
        core = re.escape(product.strip())
        variant_rx = re.compile(core.replace(r"\ ", r"[\s-]?"), re.I)
        variants = Counter(m.group(0) for m in variant_rx.finditer(text))
        bad = {v: n for v, n in variants.items() if v != product}
        if bad:
            findings["product_name_variant"].append({"expected": product, "variants": bad})

    # Mixed spelling/format signals.
    mixed = []
    pairs = [("e-mail", "email"), ("log-in", "login"), ("set-up", "setup"),
             ("on-premise", "on-premises"), ("SaaS", "Saas"), ("add-on", "addon"),
             ("real time", "real-time")]
    for a, b in pairs:
        na, nb = len(phrase_regex(a).findall(text)), len(phrase_regex(b).findall(text))
        if na and nb:
            mixed.append({"forms": {a: na, b: nb}})
    if re.search(r"\$\d", text) and re.search(r"\b\d+\s*(?:USD|dollars)\b", text, re.I):
        mixed.append({"forms": {"$ amounts": "yes", "USD/dollars": "yes"}})
    if mixed:
        findings["inconsistent_form"].extend(mixed)

    summary = {
        "sentences": sentence_count,
        "words": word_count,
        "avg_sentence_words": round(word_count / sentence_count, 1) if sentence_count else 0,
        "counts": {k: len(v) for k, v in findings.items()},
    }
    return {"summary": summary, "findings": findings}


LABELS = {
    "promotional": "Promotional language (SelectHub Tier 0 — remove or back with evidence)",
    "vague_evaluation": "Vague evaluations (Check 1 — name the actual capability or limit)",
    "hedge": "Hedges (Check 2 — state it, name the condition, or flag verification)",
    "incomplete_comparison": "Possible incomplete comparisons (Check 5 — more/better than what?)",
    "unclear_pronoun_start": "Sentences that start with a pronoun (Check 6 — confirm the referent)",
    "metaphor_jargon": "Metaphor or jargon (Check 6 — use a direct description)",
    "filler": "Filler and wordy phrases (Check 7 — cut or tighten)",
    "long_sentence": "Long sentences",
    "hyphen_heavy": "Sentences with many hyphenated words (Check 6)",
    "passive_voice": "Possible passive voice",
    "repeated_opener": "Repeated sentence openers",
    "doubled_word": "Doubled words",
    "product_name_variant": "Product name variants",
    "inconsistent_form": "Inconsistent spelling or format",
}


def to_markdown(result):
    s = result["summary"]
    out = [f"# Mechanical scan\n",
           f"{s['sentences']} sentences, {s['words']} words, average {s['avg_sentence_words']} words per sentence.\n",
           "Each flag is a candidate. Confirm it in context before you report it.\n"]
    for key, label in LABELS.items():
        items = result["findings"].get(key)
        if not items:
            continue
        out.append(f"\n## {label} — {len(items)}\n")
        for it in items[:40]:
            if key == "repeated_opener":
                out.append(f"- \"{it['opener']}…\" × {it['count']} (lines {', '.join(map(str, it['lines']))})")
            elif key == "product_name_variant":
                out.append(f"- Expected \"{it['expected']}\"; found {it['variants']}")
            elif key == "inconsistent_form":
                out.append(f"- {it['forms']}")
            elif key == "long_sentence":
                out.append(f"- L{it['line']} ({it['words']} words): {it['text']}")
            else:
                out.append(f"- L{it['line']} [{', '.join(it['terms'])}]: {it['text']}")
        if len(items) > 40:
            out.append(f"- …and {len(items) - 40} more")
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path")
    ap.add_argument("--product", help="Canonical product name, as the vendor spells it")
    ap.add_argument("--max-words", type=int, default=30)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    result = scan(load_text(a.path), a.product, a.max_words)
    print(json.dumps(result, indent=2) if a.json else to_markdown(result))


if __name__ == "__main__":
    main()
