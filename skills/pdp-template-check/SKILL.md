---
name: "pdp-template-check"
description: "Check a SelectHub product page (PDP) draft against the product page template and return a Pass/Fix checklist. Use for a template, section, or format check, or with zac-edits-pdp for a full check."
---

# PDP Template Check

Check a SelectHub product page draft against the template, one section at a time, and give the writer a short checklist. This skill checks each section's format (shape, length, lists, links, order) and content standard (fit statements, the verdict, agreement between sections). It does not do the line edit (promotional words, vague wording, hedges, logic, flow); zac-edits-pdp does. For a full check, run both, put this checklist after the zac-edits-pdp report, and report each issue only once, under the skill that owns it.

## Scope and mode

- **Flag and suggest; do not rewrite.** A fix is a direction, a question, or a short example phrase. Do not change the source file.
- Read the whole draft first. Many checks compare sections.
- Check only the sections supplied. Mark the others "Not supplied."
- My Take, What Surprised Me, and Common Mistakes To Watch Out For are optional. If one is absent, mark it "Not included (optional)" and ask under Questions whether the writer plans to include it. Do not flag it or suggest adding it.
- Given only a SelectHub URL, ask for pasted content: the pages are bot-protected. Read Google Docs links with the Google Drive connector when connected.
- Do not research facts or open links. If a fix depends on a fact not in the draft or supplied sources, add it to Unsupported claims.
- Do not ask for changes to the automatic TL;DR rows (Analyst Score, User Sentiment, Starting Price, Pricing Model, Free Trial, Mobile App, Deployment). When other copy contradicts one, fix the other copy.

## Result labels

- **Pass** — meets the template.
- **Fix** — breaks a template rule.
- **Consider** — differs from a guideline or a tentative rule; the writer decides.
- **Not included (optional)** — an optional section is absent.
- **Not supplied** — not in the draft you got.

## Section checks

### Cross-section consistency (check first; own row at the top)

Many buyers read only the TL;DR, so it must agree with the rest of the page.

- Every Strong In item has support in the Review or the Pros. Every Watch Out For item matches a Con, a Common Mistake, or a Review statement.
- Best For and Not For do not overlap or contradict each other, the Bottom Line, or My Take (for example, "Best For: small businesses" beside an unexplained Con that the product is expensive for small companies).
- No strength appears elsewhere as a weakness without an explanation of the nuance.
- **Wrong section.** Feature explanations belong in features, implementation costs in pricing, fit advice in the TL;DR and Review, buyer warnings in Common Mistakes, money costs such as add-ons and paid services in Additional Cost Considerations, and integration caveats in the Integration Takeaway. Fix: name the section the text belongs in.

### How I Researched (light check; flag only clear misses)

- **Format.** One short intro line (one or two sentences at most), then bullets. Flag a missing intro or sources written as paragraphs. Do not check bullet wording or count.
- **User reviews as a source.** If the page uses user feedback anywhere ("users report," review-site names, User Sentiment), a bullet lists user reviews as a source.
- **No claimed comparison that the page does not show.** A bullet such as "I compared pricing across 10 tools" needs the comparison on the page (competitor prices, a comparison table). A reader who can't find it stops trusting the page. Fix: remove the claim or show the comparison.

### TL;DR

- **Best For** names a company size, user type, or use case, not "teams of all sizes."
- **Strong In** lists two or three specific capabilities, not adjectives ("strong reporting").
- **Not For** names a real poor-fit audience or operating context.
- **Alternatives:** two or three products, each with a reason tied to a buyer need that this product meets less well. "A popular alternative" is not a reason.
- **Alternatives link to SelectHub.** Each links to its selecthub.com product page, not to the vendor or a review site. Group unlinked alternatives into one finding. If links were probably lost in pasting, say so once under Questions instead.

### Review

- **Length (Consider).** Five to seven paragraphs, counting from the Bottom Line. Do not count My Take or What Surprised Me; count a list or table as one paragraph. Put the count in the Note.
- **Bottom Line first (Consider).** The first paragraph is the Bottom Line, labeled or clearly the verdict. Many readers stop after it. If it is missing or comes after background, mark Consider: move it to the top.
- **Bottom Line verdict (Fix).** It states who should buy, the main reason, and who it's not ideal for. Flag one that only describes the product.
- **No repeat of the Pros & Cons** in paragraph form.

### My Take (optional)

- One sentence with the key point. Flag more than one sentence, or one sentence stretched with semicolons or dashes to hold several points. Fix: keep the main point; move the rest to the Review.
- The point is an opinion the Review backs up, not a product description.

### What Surprised Me (optional)

- Names something specific and unexpected, not a routine feature or an expected strength.

### Common Mistakes To Watch Out For (optional)

The format may change, so its format checks use Consider.

- **Short items (Consider).** One or two sentences each.
- **From user feedback (Consider).** Items come from user feedback, not only vendor docs. Flag an item that only restates a limit from the docs, with no sign that users run into it. Fix: tie it to a problem users report, or move it to another section.
- **Specific (Fix).** Each mistake is specific to this product or its category. "Not reading the contract" is generic.

### Pros & Cons

- **Influences a decision.** Would each item change a buyer's choice?
  - Routine updates are not a pro unless something unusual is documented.
  - More features in higher tiers is not a con by itself. It matters when a buyer-relevant feature costs extra, or comparable products include it at a lower tier (with evidence).
  - Flag weak points and suggest cutting them. Uneven counts are fine.
  - Flag competitor norms stated without evidence ("unlike most tools"); do not suggest new ones. A common capability can still matter if the item says why.
  - Flag a pro and a con that contradict each other ("easy to use" vs. "steep learning curve") with no explanation of the nuance.
- **User feedback when possible.** If no item reflects what users report, mark Fix when the draft shows feedback is available (user reviews in How I Researched, users cited in the Review), otherwise Consider. Never suggest invented feedback.
- **No repeats.** Flag an item that restates a point from the Review, Common Mistakes, Pricing, or Integrations. Fix: keep the point in one place. Overlap with the TL;DR is expected; do not flag it.

### Pricing Notes

- **Explains the overall pricing:** billing terms (monthly or annual, contract length, minimum seats) and plan structure (tiers, what changes between them, per-user or flat-rate). Flag notes that only restate a price or the Pricing Model row.
- **Does not repeat the starting price** from the Starting Price row, as the same figure or a "starts at $X" sentence. Other plans' prices are fine. Fix: use the space for billing terms or plan structure.

### Additional Cost Considerations

- **Money costs only:** add-ons, paid services (implementation packages, premium support, paid training), usage or overage fees, per-user charges as the team grows. Time costs (migration effort, training time, learning curve, setup hours) belong in another section. A paid migration or training service is a money cost and stays.
- **Partial sentences.** Flag full sentences: "Premium support add-on for 24/7 phone help," not "You'll have to pay extra for premium support if you want 24/7 phone help." Give a short phrase as the fix.

### Integrations

- **Same ✅/❌ format in every category.** ✅ for supported apps, ❌ for popular apps that are not supported, in the same position everywhere (not "✅ Slack" in one category, "Slack ✅" or "Slack (supported)" or a plain bullet in another). Flag other markers (✔, ✓, ✗, Yes/No) and mixed formats. A category with only ✅ items is fine.
- **Title case for category headings.** Lowercase short articles, conjunctions, and prepositions (a, an, the, and, or, for, of, to, in, on, at, by) unless first; keep brand and acronym spelling (CRM, QuickBooks). "Sales and marketing" → "Sales and Marketing." Do not flag disputed cases such as "With."
- **Integration Takeaway.** Present, about two or three sentences, and not a repeat of the list. It says where integrations add the most value and what complex environments must confirm before buying. "Integrates with many tools" is not a takeaway.

### Approach to Common Challenges

- Two to five scenarios; do not flag a count in this range. Call them scenarios, not cards.
- Each has a recognizable buyer problem, the features that respond to it, and two or three outcomes.
- Flag invented percentages, time savings, or ROI. For an unsupported outcome, suggest a described effect ("users finish routine tasks without help from IT") or add it to Unsupported claims.

### FAQs

- **High intent.** Four or more questions on fit, security, integrations, implementation, pricing, or other decision criteria.
- **Order of importance.** Questions that can change a buying decision come first (fit, total cost and pricing terms, a must-have capability, security and compliance, integration with current tools), then setup and use (implementation time, training, support, how-to). Flag only a clearly wrong order, such as "Does it have a dark mode?" above "Does it support SSO?" Fix: list the suggested order.
- **No repeats.** Flag an FAQ the page already answers elsewhere; suggest a replacement topic when you can.
- **Answer length.** One concise paragraph each.

## Deliver the result

Use the user's format if they gave one. Otherwise:

1. **Heading:** "Template check: <Product>"
2. **Summary line only:** "N sections pass, N need a fix, N to consider."
3. **Checklist table:** Section | Result | Note (a few words, such as the count found). Cross-section consistency first, then every template section in page order, including Not supplied and Not included rows. A section with any Fix gets Fix.
4. **Fixes:** one entry per finding, in table order: the section in bold, the location and a short quote, the problem in one sentence (the rule and why it matters to the buyer), then a separate paragraph starting **Fix:**. Group repeats.
5. **Unsupported claims:** each claim the writer must confirm, once. Omit if none.
6. **Questions:** absent optional sections, and anything you could not check. Omit if none.

Address the writer as "you," in short, direct sentences. No general praise, no rewritten sections.

## Final check

Before you deliver, confirm that guideline rules use Consider, absent optional sections and automatic TL;DR rows are not flagged, no finding is a line-edit point for zac-edits-pdp, and no fix adds certainty or facts the draft doesn't support.