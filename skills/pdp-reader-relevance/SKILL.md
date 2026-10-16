---
name: pdp-reader-relevance
description: Check a SelectHub product page draft for relevance to its target buyer segment, using the category's buyer report, buyer CSV, and personas, and deliver a Claude Doc with a gaps tracker. Use for 'is this relevant to buyers', 'check against buyer research', or audience-fit reviews of any category's product page.
---

# Product Page Buyer-Relevance Review

Check whether a product page draft gives its target buyers what they need to decide. Compare the draft with buyer research for that software category. Find what works, find the gaps, and rank the gaps. Deliver a Claude Doc that the team can track, and save a text copy to the project.

This is a relevance review only. It answers "does the page speak to this buyer?" It does not fact-check product claims and it does not edit copy. For line edits, use `zac-edits-pdp`. For scores, use `product-page-rater`.

## Rules

- Do not change the draft. Do not add product claims. If a gap needs a product fact, list it as an open check against the product research.
- Every finding names its source with a short tag: `[BR §n]` buyer report section, `[CSV]` buyer data, `[P]` personas. Readers must be able to trace each number.
- Personas are directional only. Use them for color, never as the only evidence for a gap.
- Base every finding on SelectHub buyer data. Never fill a missing source with general knowledge about the category. A review without buyer data looks real but is not, so it is worse than no review.
- When sources disagree, say so. Do not hide the conflict. This includes conflicts between an old and a new version in the same draft.
- Write in plain, simple language: short sentences, active voice, one idea per sentence.

## Step 1: Get the draft

- Read the Google Doc with the Google Drive connector (`read_file_content`). A pasted draft is fine too.
- Drafts often hold a new version and an old version in one file. Review the new version. Use the old version only to spot conflicts (for example, the old page says "easy setup" and the new page says "complex implementation").
- Note the product name, the software category, and the TL;DR "Best For" and "Not For" rows.

## Step 2: Ask for the target reader

Always ask the user which buyer segment to check against before you start the analysis. Use AskUserQuestion. Offer the segments from the buyer report's size bands (for example small, mid-sized, large), and say what the draft's "Best For" row claims so the user can choose with that in view. The segment drives every number in the review, so a guess here makes the whole review wrong.

## Step 3: Gather the buyer research for that category

### Minimum evidence

The review needs at least one of these two files:

- the **buyer report** for the category, or
- the **buyer CSV** for the category.

Personas alone are not enough, because they are directional.

### Find the files

1. Look in the attached project first (project docs, project files, and a current-reports doc).
2. Then look in files the user attached, links in the conversation, and the connected buyer-insights folder.
3. If you cannot find a file, ask the user before you continue. Ask them to attach it, paste the report link, or connect the buyer-insights folder in the desktop app. Name the category and the file you looked for, so they know what to send.

If you still have neither the buyer report nor the buyer CSV, stop. Tell the user that you need at least one of these files to do the review. If the session is not in a project, or the project does not store these files, say that clearly: they must provide at least one file themselves. Do not start the review until they do.

If you have only one of the two files, record what is missing for the Scope table (Step 5).

**If the buyer report is missing, warn the user before you start the analysis.** Tell them, in plain words:

- The review will not include **pain-point rates**. A pain-point rate is the share of buyers in the segment who named a problem, for example "40.5% of large buyers named integration as a pain point." Only the buyer report has these rates, because it sorts every buyer comment into themes with a tested method.
- What this means for them: the review cannot show which problems matter most to the segment, or how much more one problem matters than another. The gap priorities (High, Medium, Low) will rest on module counts and buyer comments from the CSV, so they are less certain. The doc will have no pain-point chart.

Then ask if they want to continue with the CSV only, or send the buyer report first. Do not estimate pain-point rates from the CSV yourself: rates from a quick, unchecked grouping of comments look exact but are not.

### Read each source

1. **Buyer report.** Use the report that the project's current-reports doc (for example `claude/current-reports.md`) lists for the category, or the report the user gave you. Read it with the Artifact tool's `read` action; the result names the file where it saved the full HTML. The HTML is large, so do not read all of it. Run the bundled script to turn it into text, with each chart's values listed under a `[CHART]` line:

   ```bash
   python3 <skill-dir>/scripts/extract_report.py <saved report.html> -o report.txt
   ```

   Then read `report.txt` with grep and line ranges. For the chosen segment, pull: pain-point rates, modules wanted, the decision-maker vs. researcher split, top titles, vendors named, and typical buyer language.

2. **Buyer CSV.** Use the category's buyer data file from the project, an attachment, or the connected buyer-insights folder. The bundled script runs in this session, so stage a file from a connected folder into the session first. Find the buyers who already talked to this vendor with the bundled script. Pass every name buyers may use for the vendor and the product (for example "Microsoft" and "Dynamics"):

   ```bash
   python3 <skill-dir>/scripts/vendor_buyers.py <buyers.csv> --vendor "<Vendor>" --vendor "<Product>"
   ```

   It matches names only in the "Vendors Evaluated" column. It prints company size bands, modules wanted, a rough authority split, and one block per buyer with the title, authority text, and reason for change. Add `--sizes medium,large` to keep only the chosen segment, or `--json` for structured output. The authority split is a keyword guess: read the buyer blocks and correct the count before you use it. Note the modules the product lacks (for example payroll) and the reasons for change. This small group is the closest match to the page's real reader, so it is worth the extra step.

3. **Personas.** Read the category's persona docs in the project for the chosen segment. Use goals, objections, and decision criteria as color. If there are no personas, continue without them and note it in the Scope table. Do not ask the user for them.

## Step 4: Map the draft to the buyer needs

Go through the draft section by section and ask: which top need does this section answer, and for which part of the segment?

**What works.** List the parts of the draft that answer a top need. For each one, give the section names, the need, its number, and the source tag.

**Gaps and problems.** Look for these, in this order:

1. Contradictions about who the page is for (for example, "Best For" says mid-to-large and "My Take" says large only).
2. Top needs of the segment that the page does not answer, or answers only in scattered places.
3. Wanted modules that the page does not mention, or mentions in one line.
4. Buyer concerns with no answer: implementation time, support model, migration from an old system, total cost.
5. Language that the segment's top titles will not understand (vendor jargon).
6. Alternatives that do not match the vendors buyers actually compare.
7. Strong proof points that are hard to find.

Rank each gap:

- **High:** it touches the segment's top one or two needs, or it confuses who the page is for.
- **Medium:** about 10% or more of the segment raises the need, or a top-six module is missing or thin.
- **Low:** a small share raises it, or the fix may be out of scope (for example, the alternatives set comes from platform data).

With the CSV only, rank by module counts, use buyer comments as quoted examples (not as counts), and mark the Priority column header "Priority (no report: less certain)".

For each gap, give the evidence with numbers and tags, and a short suggested fix. A fix that needs a product fact says "check the product research" first.

**Open checks.** List the claims to check against the product research, decisions for the author, and any conflicts between versions or sources.

## Step 5: Build the Claude Doc

Load the `docs` skill and follow the docs connector's instructions. In short:

1. The first call creates the doc skeleton: title `<Product> Page: Relevance Review`, the byline chips, and one pending block for each section: Scope and sources; What the target reader cares about; What works; Gaps and problems; Open checks and next steps. Open the doc for the user right after.
2. Fill one section per call, prose sections first.
   - **Lead** (above Scope): one to three sentences with the verdict and the high-priority gaps. If a source is missing, add one sentence that says the review uses less buyer data than usual and which source is missing.
   - **Scope and sources:** a two-column table: draft link, ClickUp task link (search ClickUp for the product name when the connector is available), target reader, and one row for each of the three sources (buyer report, buyer CSV, personas) with its tag. For each source, say "Used" with the file name and date, or "Not available". Under the table, add one line on what a missing source means for the review. For example: "No buyer CSV: the review cannot show which buyers already talked to this vendor." or "No buyer report: this review has no pain-point rates (the share of buyers in the segment who named each problem), so it cannot show which problems matter most. Gap priorities rest on module counts and buyer comments in the CSV and are less certain."
   - **What works:** a numbered list.
   - **Gaps and problems:** a pipe table with columns `# | Priority | Gap | Evidence | Suggested fix | Status`. Make Priority (High, Medium, Low) and Status (Open, In progress, Fixed, Won't fix) dropdown enums so the team can track the gaps. Set every Status to Open.
   - **Open checks and next steps:** a task list, then a Sources list with links.
3. Fill **What the target reader cares about** last, with a chart of the segment's top pain-point rates (read `topic.charts` first). Two size bands: a dot plot with one row per pain point and one dot per band, sorted by the larger band. One band: a horizontal bar chart. Put the finding in the chart title. With the CSV only (no report), chart what the CSV counts directly, such as modules wanted by the segment (`vendor_buyers.py <buyers.csv> --sizes <segment> --summary-only`, with no `--vendor`, counts the whole segment), and do not invent pain-point categories with rates. Under the chart, add short bullets for modules wanted, who reads the page (researcher share), the buyers who already talked to this vendor, and persona color. Take a screenshot of the chart and fix any label overlap.

## Step 6: Save a copy to the project

A Claude Doc cannot go into a Project, so save a text copy for other chats to use:

1. Export the tab as markdown with the docs `export` tool.
2. Replace the chart placeholder with a table of the same values.
3. At the top, add the live doc link and this line: "This file is a text snapshot. If the two differ, the live doc wins."
4. Write it with `project_write` to `claude/<product-slug>-relevance-review.md`.

## Step 7: Hand off

Reply in one or two short lines: the doc link, and what the user can do (edit inline, comment, set gap status). Then ask, in one line, if they want the findings as comments on the Google Doc or a comment on the ClickUp task. Do not change ClickUp or the draft without approval.
