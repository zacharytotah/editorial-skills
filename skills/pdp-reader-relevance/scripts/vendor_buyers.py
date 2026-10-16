#!/usr/bin/env python3
"""Profile the buyers in a SelectHub buyer CSV who already talked to a vendor.

Matches the vendor names only against the "Vendors Evaluated" column, so a name
that appears in another column (a page title, a pain point) does not count.

For the matched buyers it reports:
  - company size bands (Small 1-100, Medium 101-1,000, Large 1,000+, Unknown)
  - modules wanted (suite and standalone, combined)
  - a rough authority split (researcher/consultant, decision-maker, other),
    from keywords in the Title and Authority columns
  - one block per buyer: size, title, industry, modules, authority text,
    reason for change, and vendors evaluated, so you can check every count

The authority split is a keyword guess. Read the per-buyer blocks and correct
it before you put a number in a review.

Usage:
    python3 vendor_buyers.py <buyers.csv> [--vendor "Microsoft" --vendor "Dynamics"]
        [--sizes medium,large] [--json] [--summary-only]

--vendor     a name to search for (case-insensitive); repeat for aliases.
             Leave it out to profile every buyer, for example the whole
             segment's modules wanted when there is no buyer report.
--sizes      keep only these bands: small, medium, large, unknown.
--json       print structured JSON instead of text.
--summary-only  print the counts without one block per buyer.
"""
import argparse
import csv
import json
import re
import sys
from collections import Counter

COLUMNS = {
    "vendors": ["Vendors Evaluated"],
    "employees": ["No. of Employees", "Employees", "Company Size"],
    "suite": ["Suite Modules"],
    "standalone": ["Standalone Modules"],
    "title": ["Title"],
    "authority": ["Authority"],
    "reason": ["Reason for Change and Pain Points", "Reason for Change"],
    "industry": ["Industry"],
    "company": ["Company / Account", "Company"],
}

RESEARCHER_WORDS = re.compile(
    r"research|tasked with|hired (?:to|as)|consultant|bring (?:it|his|her|their|the) "
    r"(?:findings|research)|present (?:his|her|their) findings|gathering options",
    re.I,
)
DECIDER_WORDS = re.compile(
    r"final decision|make the (?:final )?decision|decision[- ]maker|will decide|"
    r"joint decision|sign(?:s|ing)? off|final say",
    re.I,
)


def find_col(header, names):
    lower = {h.strip().lower(): h for h in header}
    for n in names:
        if n.lower() in lower:
            return lower[n.lower()]
    return None


def size_band(value):
    m = re.search(r"\d[\d,]*", value or "")
    if not m:
        return "unknown"
    n = int(m.group(0).replace(",", ""))
    if n <= 100:
        return "small"
    if n <= 1000:
        return "medium"
    return "large"


def split_modules(*cells):
    out = []
    for c in cells:
        for part in re.split(r"[;\n]", c or ""):
            part = part.strip()
            if part:
                out.append(part)
    return sorted(set(out))


def authority_class(title, authority):
    text = f"{title} {authority}"
    if RESEARCHER_WORDS.search(text):
        return "researcher/consultant"
    if DECIDER_WORDS.search(text):
        return "decision-maker"
    return "other/unclear"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("csv_file")
    ap.add_argument("--vendor", action="append", default=[],
                    help="Vendor or product name to match; repeat for aliases. "
                         "Leave out to profile every buyer (use with --sizes).")
    ap.add_argument("--sizes", help="Comma list: small,medium,large,unknown")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--summary-only", action="store_true",
                    help="Print the counts without the per-buyer blocks")
    args = ap.parse_args()

    with open(args.csv_file, encoding="utf-8-sig", errors="replace", newline="") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames or []
        rows = list(reader)

    col = {k: find_col(header, v) for k, v in COLUMNS.items()}
    if not col["vendors"]:
        sys.exit("No 'Vendors Evaluated' column found. Columns: " + ", ".join(header))

    get = lambda r, k: (r.get(col[k]) or "").strip() if col[k] else ""
    patterns = [re.compile(r"\b" + re.escape(v.strip()) + r"\b", re.I) for v in args.vendor]
    keep_sizes = set(s.strip().lower() for s in args.sizes.split(",")) if args.sizes else None

    buyers = []
    for i, r in enumerate(rows, start=2):  # row 1 is the header
        vendors = get(r, "vendors")
        if patterns and not any(p.search(vendors) for p in patterns):
            continue
        band = size_band(get(r, "employees"))
        if keep_sizes and band not in keep_sizes:
            continue
        buyers.append({
            "csv_row": i,
            "company": get(r, "company"),
            "employees": get(r, "employees"),
            "size_band": band,
            "industry": get(r, "industry"),
            "title": get(r, "title"),
            "modules": split_modules(get(r, "suite"), get(r, "standalone")),
            "authority_class": authority_class(get(r, "title"), get(r, "authority")),
            "authority": get(r, "authority"),
            "reason": get(r, "reason"),
            "vendors_evaluated": vendors,
        })

    sizes = Counter(b["size_band"] for b in buyers)
    modules = Counter(m for b in buyers for m in b["modules"])
    authority = Counter(b["authority_class"] for b in buyers)
    summary = {
        "csv_rows": len(rows),
        "vendor_terms": args.vendor,
        "size_filter": sorted(keep_sizes) if keep_sizes else None,
        "matched_buyers": len(buyers),
        "size_bands": dict(sizes),
        "modules_wanted": dict(modules.most_common()),
        "authority_split_keyword_guess": dict(authority),
    }

    if args.json:
        json.dump({"summary": summary, "buyers": [] if args.summary_only else buyers}, sys.stdout, indent=2, ensure_ascii=False)
        print()
        return

    n = len(buyers)
    print(f"Matched {n} of {len(rows)} buyers on: {', '.join(args.vendor) or 'all vendors'}"
          + (f" (sizes: {', '.join(sorted(keep_sizes))})" if keep_sizes else ""))
    if not n:
        return
    print("\nCompany size")
    for band in ["small", "medium", "large", "unknown"]:
        if sizes[band]:
            print(f"  {band}: {sizes[band]} of {n}")
    print("\nModules wanted")
    for m, c in modules.most_common():
        print(f"  {m}: {c} of {n}")
    print("\nAuthority (keyword guess - check the blocks below)")
    for a, c in authority.most_common():
        print(f"  {a}: {c} of {n}")
    if args.summary_only:
        return
    print("\nBuyers")
    for b in buyers:
        print(f"\n--- CSV row {b['csv_row']}: {b['company'] or '(no company)'}")
        print(f"  Size: {b['employees'] or '?'} ({b['size_band']}) | Industry: {b['industry']}")
        print(f"  Title: {b['title']} | Authority class: {b['authority_class']}")
        print(f"  Modules: {', '.join(b['modules']) or '(none listed)'}")
        print(f"  Authority: {b['authority']}")
        print(f"  Reason for change: {b['reason']}")
        print(f"  Vendors evaluated: {b['vendors_evaluated']}")


if __name__ == "__main__":
    main()
