**Master Kit** · Product bundle

---

# decision-page

_Generate an interactive single-file HTML decision page for any substantive alignment moment where reasonable people would disagree — replacing a reply-by-reply trade-off thread with a click-to-pick canvas: each decision shown with from/to/opinion/recommendation, a sticky picks rail, accept-recommendations/reset/export actions, and localStorage persistence so picks survive reloads._

**TRIGGER** — slash: `/decision`, `/decision-page`, `/alignment-canvas` · keywords: "decision page", "alignment moment", "click-to-pick", "surface the trade-offs", "make this decidable", "decisions to align on", "export my picks", "decision canvas", "sticky picks rail"

## What it does

A substantive alignment moment is one where reasonable people would disagree, or where the reader could reasonably want to override a recommendation. The wrong way to resolve it is a long reply thread of "what about X / what about Y / one more thing about Z," which loses fidelity by the third round. This skill produces the right way: a single self-contained HTML canvas where every decision is surfaced with its trade-offs, each option is a clickable button, a sticky rail shows the running state of all picks, and an export action produces a paste-friendly summary keyed to the decisions. localStorage keeps the picks across reloads. The canvas compresses a sprawling alignment conversation into one read, one set of clicks, and one structured export.

## Why it matters

Generate an interactive single-file HTML decision page for any substantive alignment moment where reasonable people would disagree — replacing a reply-by-reply trade-off thread with a click-to-pick canvas: each decision shown with from/to/opinion/recommendation, a sticky picks rail, accept-recommendations/reset/export actions, and localStorage persistence so picks survive reloads. This skill captures the discipline as a repeatable, reviewable procedure so the same decision is made the same defensible way every time, instead of being re-derived (and re-broken) per project.

## When to use

- A drafting or review step produced several trade-offs that need a reader's alignment before work continues.
- A decision involves multiple options where reasonable people would disagree on the choice.
- A reply-thread negotiation is degrading and you want to compress it into one canvas.
- A design review needs the reader to pick among rendered options (type stacks, palettes, layouts).
- A non-design decision (vendor, policy, scope) needs the same structured, exportable alignment.
- Several decisions must be aligned at once and you want the reader to see running pick state.

## When NOT to use

- **Don't** describe a trade-off in words when rendering both options would show it — the canvas exists to show, not narrate.
- **Don't** use `<label>`/radio pairs for options; use `<button type="button">` with `pointer-events: none` on inner spans.
- **Don't** pre-select the recommended option; the "Reco" tag is a cue, and the reader must still click.

## Chain references

- **Related →** `stakeholder-update`, `executive-summary`, `perspective-checks`

## Last updated

2026-05-23 — imported to Master Kit at the Mill-TMS production bar. Sanitized project-specific references and PS-only frontmatter; restructured to the 8-section scoring rubric while preserving all technical substance; added three worked examples and edge-case / anti-pattern coverage.

---

**Master Kit** · Product · 2026 · v1.0
