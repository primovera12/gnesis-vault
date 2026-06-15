---
name: decision-page
description: "Generate an interactive single-file HTML decision page for any substantive alignment moment where reasonable people would disagree — replacing a reply-by-reply trade-off thread with a click-to-pick canvas: each decision shown with from/to/opinion/recommendation, a sticky picks rail, accept-recommendations/reset/export actions, and localStorage persistence so picks survive reloads. Triggers on /decision, /decision-page, /alignment-canvas, 'decision page', 'alignment moment', 'click-to-pick', 'surface the trade-offs', 'make this decidable', 'decisions to align on', 'export my picks'."
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
version: "2.0"
type: skill
domain: product
owner: kit
triggers:
  slash_commands:
    - /decision
    - /decision-page
    - /alignment-canvas
  keywords:
    - decision page
    - alignment moment
    - click-to-pick
    - surface the trade-offs
    - make this decidable
    - decisions to align on
    - export my picks
    - decision canvas
    - sticky picks rail
last_updated: 2026-06-10
tier: production
related:
  - stakeholder-update
  - executive-summary
  - perspective-checks
depends_on: []
supersedes: []
score: 0
blocking: false
---

# Decision Page

## Purpose

A substantive alignment moment is one where reasonable people would disagree, or where the reader could reasonably want to override a recommendation. The wrong way to resolve it is a long reply thread of "what about X / what about Y / one more thing about Z," which loses fidelity by the third round. This skill produces the right way: a single self-contained HTML canvas where every decision is surfaced with its trade-offs, each option is a clickable button, a sticky rail shows the running state of all picks, and an export action produces a paste-friendly summary keyed to the decisions. localStorage keeps the picks across reloads. The canvas compresses a sprawling alignment conversation into one read, one set of clicks, and one structured export.

The format applies to design and non-design moments alike: typography, icon set, layout, color, spacing, information architecture, and copy tone — and equally to rule rewrites, governance changes, scope cuts, refactor proposals, content trade-offs, vendor choices, and policy revisions. Anywhere there are multiple substantive options and a recommended one, the decision page beats prose, because it shows the trade-off instead of describing it and captures the verdict instead of asking for one.

## When to invoke

- A drafting or review step produced several trade-offs that need a reader's alignment before work continues.
- A decision involves multiple options where reasonable people would disagree on the choice.
- A reply-thread negotiation is degrading and you want to compress it into one canvas.
- A design review needs the reader to pick among rendered options (type stacks, palettes, layouts).
- A non-design decision (vendor, policy, scope) needs the same structured, exportable alignment.
- Several decisions must be aligned at once and you want the reader to see running pick state.

## When to inline instead

Not every choice deserves a page. The threshold question is: "Would reasonable people disagree, or could the reader reasonably want to override?" If no — a single obvious binary, or `text-sm` versus `text-xs` on one label — inline the answer instead; a page for a trivial decision wastes the reader's attention on the wrong question. If unsure, generate: the cost of a page for a trivial decision is small, while the cost of not generating one for a substantive decision is a reply thread that loses fidelity fast. Reserve the canvas for moments with real optionality and a recommendation worth being able to override.

## Canonical design + auto-send (v5 — the default look and delivery)

Every decision page ships in ONE house style — the **War Ministry v5** skin — so the operator sees the same trusted artifact every time, not a per-project reinvention. The exact, render-verified baseline is bundled with this skill as **`canonical-template-v5.html`**: copy it, then edit only (1) the `<title>`, (2) the `.pill`/`h1`/`.lede`/`.src` header text, and (3) the `DECISIONS` array + `KEY` at the bottom. Do not touch the `<style>` block — that IS the global look.

The v5 design system (Genesis "blue" skin, light + dark):
- **Tokens:** brand ink `#1b3a67` (light) / sky `#8fb8d4` (dark); parchment `#f3e9d3` bg / warm near-black `#1e1e1e`; surface `#fffdf7` / `#262626`; success `#2d7a52`. A `◐ Theme` toggle persists to `localStorage('wm-theme')`.
- **Type:** Inter (body/display) + JetBrains Mono (labels, metadata) via the standard import.
- **Structure:** a pill kicker → `h1` → `.lede` → `.src` provenance line; each decision is a `.card` with a numbered `.ix`, the question, a `From:` / `My take:` meta block, and clickable `.opt` rows. The recommended option carries a `✓ RECOMMENDED` tag (a cue, never a pre-selected default).
- **Sticky bottom rail** (not a side rail): an `N / M picked` counter with dot indicators, a comment textarea (autosaved), and `Accept all recs` + `Copy & send →`.

**Auto-send is the default delivery — the operator must NEVER copy-paste.** Bundled **`decision-server.py`** serves the project's `decisions/` folder on `127.0.0.1:<port>` and accepts `POST /decision`, writing the picks to `decisions/inbox/<ts>.json` and mirroring to `decisions/inbox/LATEST.json`. The page's send button POSTs the picks there; the agent reads the inbox file directly. Clipboard copy is only the **fallback** when the server is off (the page detects the failed POST and falls back automatically). On a successful send the page does a **full-page success transition** — a green check, "Decision received ✓", a recap of every pick, and "delivered to agent inbox" — so the operator has visible proof it landed and can close the tab. Never end on an ambiguous "Copy & send" with no confirmation.

## Inputs

- The topic or scope in one sentence.
- The decisions to surface — either listed explicitly, or a referenced draft from which to identify them.
- The reader: one person or several, and whether the page is handed over as a file or routed through a shared host.
- For each decision: the current ("from") state, the proposed ("to") state, the trade-off, and the recommendation.
- The project's brand application (fonts, colors, logo) so the page renders consistently with other artifacts.
- The project's hand-over convention for sharing the finished file.
- Whether the page will be opened offline or from a local file, which dictates inlining all assets and using the clipboard fallback rather than relying on a network or a secure context.
- Any grouping the decisions fall into, so the picks rail can show group labels and the reader can navigate a longer set by jumping between groups.

## Step-by-step

1. **Confirm the scope.** If invoked without specifics, ask for the topic, the decisions, and the reader before generating — a page built from a misunderstood scope wastes the reader's attention.
2. **Identify the decisions.** List each substantive decision with its from/to states and the trade-off in two or three sentences.
3. **Build the two-column layout.** Left column holds the decisions; right column holds the sticky picks rail. Set `align-self: start` on the rail's grid cell so `position: sticky` actually sticks.
4. **Render each decision visually.** Show the options, not descriptions of them — both type stacks rendered, both color swatches, both layouts — with a short opinion callout and a one-line recommendation tagged "Reco" (a cue, not a default selection).
5. **Make options clickable buttons.** Every pick is a `<button type="button">`, never a `<label>` wrapping a radio; give inner spans `pointer-events: none` so clicks register on the button.
6. **Wire the picks rail.** Progress bar (N of M picked), group labels, click-to-jump sum-items, and immediate update on each pick.
7. **Add the four actions.** Copy my picks (one-click, top slot), Export my picks (review-first modal with download), Accept all recommendations, Reset (with confirm if non-default).
8. **Persist with localStorage.** Key per page (`decision-picks-<slug>`); picks survive reload but not Reset.
9. **Self-test and hand over.** Confirm clicks resolve, the rail sticks, export copies in both HTTPS and file contexts, and picks persist; then hand over one line with the link in the project's convention.

## The interactive canvas anatomy

The page is a two-column CSS Grid: the main column lists each decision and the right column holds a sticky rail. Each decision block shows the from/to states, a short opinion callout (brand-accent background, brand-color left border) explaining the trade-off, the recommendation in one line, and a row of click-to-pick buttons (a typical set is keep / take recommendation / pick option B). The rail mirrors the decisions with a progress bar, group labels, and click-to-jump sum-items that update the instant a pick is made. The discipline that makes it work is rendering trade-offs rather than narrating them — a color decision shows both swatches, a typography decision renders both stacks — because the entire value of the canvas over a prose doc is that the reader sees what they are choosing.

## Click-to-pick mechanics that actually work

Several small implementation details separate a working canvas from a frustrating one. Every option must be a `<button type="button">`, not a `<label>`/radio pair, which fails at touch targets and routes clicks ambiguously when the button contains inline children. Inner `<span>` elements need `pointer-events: none` so a click lands on the button, not a child. The recommended option carries a "Reco" tag as a visual cue, never a pre-selected state — the reader still has to click, because a default selection silently biases the decision. The rail's grid cell needs `align-self: start`, since grid items default to `stretch`, which quietly breaks `position: sticky`. These are the regressions that re-appear every time the page is rebuilt from memory, which is why the self-test checks each.

## Multi-select card type (module pickers and set-selections)

The default decision card is single-select: one decision resolves to exactly one picked option
(`store.picks[id] = optionId`). Some alignment moments are instead **set-selections** — "pick which
of these N things to include" — where the reader toggles many items on or off. The canonical case is
the Master Kit Run Planner's module picker (`module-picker` skill + `templates/module-picker.html.tmpl`,
fed from `MODULE-REGISTRY.json`). For those, use the **multi-select card type**. It is additive and
non-breaking: a card opts in with `multiSelect: true`; every existing single-select page is unchanged.

- **Data model.** A multi-select card stores a set, not a scalar: `store.modules = { "<id>": true|false, ... }`
  (kept beside `store.picks`/`store.notes` so single- and multi-select cards coexist on one page).
  Persist it under the same per-page localStorage key.
- **Checkbox-buttons, not checkboxes.** Keep the `<button type="button">` aesthetic and the
  `pointer-events: none` inner-span rule; add a checked state (`aria-pressed="true"` + a `.checked`
  class + a visible ✓ in the `opt-check` slot). A click toggles the item rather than replacing a pick.
- **Locked items.** Items that must always be on (e.g. Core/`required:true` modules) render checked
  and `disabled` (or `aria-disabled`), so the reader sees they are included but cannot uncheck them.
- **Preset buttons.** A row of preset buttons at the top sets the whole set in one click (e.g. Quick
  Demo / Client Proposal / Full Build pre-check their module sets). Presets only seed the toggles;
  the reader can change any non-locked item afterward.
- **Grouped sections.** Render items under group headers (Core, Engineering, Operations, Commercial,
  Specialized) with a per-group count in the rail; the click-to-jump sum-items become group anchors.
- **Dependency + conflict feedback.** When an item declares `depends_on`, toggling it on auto-checks
  its dependencies (and toggling a dependency off warns that dependents will be disabled); declared
  `conflicts_with` pairs warn when both are on. This mirrors the rules `kit-run-plan-lint.sh` enforces,
  so the page rarely produces a plan the linter will reject.
- **Machine-readable export.** In addition to the Markdown export, a multi-select page adds a
  **Copy run-plan JSON** action (and a Download) that emits a structured object the agent consumes
  deterministically — for the module picker that is the run-plan schema
  (`templates/run-plan.schema.json`): `{ version, mode, automation, deliverable, enabled_modules[],
  disabled_modules[], derived_config, depth, mapped_path, source }`. Use the same
  `textarea + execCommand('copy')` fallback so it works from `file://`.

The single-select discipline (render don't narrate, no pre-selected default for *decisions*, sticky
rail, self-contained delivery) all still applies; multi-select only changes how one card stores and
exports its state. Note the one intentional difference: a preset *does* pre-check items, because a
set-selection's whole point is to start from a sensible default and let the reader trim — unlike a
single-select decision, where pre-selecting silently biases the choice.

## Copy and export

The rail carries four actions in a deliberate order. Copy my picks sits at the top because it is the most-used: one click, no modal, a toast confirms, and it uses the `textarea + execCommand('copy')` fallback rather than `navigator.clipboard`, which fails silently in HTTP and sandboxed contexts. Export my picks opens a modal showing the same paste-friendly summary with a heading-by-heading view, a download-as-Markdown button, and an in-modal copy — the review-first path for when the reader wants to check picks before pasting elsewhere. Accept all recommendations fills every pick with the reco for a reader who trusts them. Reset clears picks with a confirm. Copy and Export surface the same content by design; do not merge them, because the one-click and review-first shapes both get used in different moments.

## Persistence and self-contained delivery

Picks are stored in localStorage under a per-page key so they survive a reload — the reader can close the tab, return, and find their picks intact — but a Reset clears them deliberately. The page must be self-contained: inline the CSS and JavaScript it needs and avoid CDN dependencies, because a decision page is often opened offline or from a local file and a missing external asset breaks it. This self-containment also makes the export reliable in a `file://` context, which is exactly why the clipboard fallback matters. The finished artifact is a single HTML file that works anywhere it is opened, with no build step and no network dependency. This self-containment is also what makes the page durable: a decision page handed over today still opens and functions a year later, regardless of what CDN was up or what framework version was current when it was made, because it carries everything it needs inside one file. A page that depends on external assets is a page that quietly stops working the moment one of those assets moves, which is precisely the wrong outcome for a document whose job is to be the durable record of a decision.

## File location and hand-over

Decision pages live in a single canonical location per project — a `decisions/` folder — named in descriptive kebab-case with today's date and an `.html` extension, appending `-v2`/`-v3` if a name collides. Scattering them across design, audit, or scratch folders loses the one feature that makes the format usable across a project: every decision is reachable from one place. After generating, do two things so the reader spends zero effort opening it: (1) **launch it for them** — on WSL, `"/mnt/c/Program Files/Google/Chrome/Application/chrome.exe" '\\wsl.localhost\<distro>\<win-path>'` backgrounded; on macOS `open`, on Linux `xdg-open` — and (2) hand exactly one line ("Decision page ready: <link>") with a **clickable `http://localhost:<port>/<file>.html`** link served by the bundled `decision-server.py`, because localhost links are clickable in terminals/IDEs and open in the browser. Never hand over a raw `file://` path or a bare posix path — neither opens reliably (a `file://` does not open across browsers/platforms, and a `/home/...` path is not clickable from a Windows browser on WSL). Serving the folder through `decision-server.py` is what makes both the clickable link AND the auto-send (POST → inbox) work from the same origin.

## Why the canvas beats the thread

The decision page exists because the reply thread is a uniquely bad medium for multi-option alignment, and understanding why keeps the format honest. A thread degrades on three axes simultaneously. Fidelity: by the third round, half the trade-offs have been re-litigated, the recommended options have drifted, and the original framing is lost in quoted-reply nesting. Capture: the verdicts arrive as prose scattered across messages, so someone has to reconstruct "what did we actually decide" from memory, introducing errors. State: nobody can see the running picture of which decisions are settled and which are open, so the same decision gets re-opened. The canvas fixes all three: every trade-off is rendered once and stays fixed, every verdict is captured as a structured pick, and the rail shows the running state at a glance. The reader does one read and one pass of clicks instead of N rounds of degrading conversation, and the export transits the picks out as structured data rather than as a summary someone typed from memory. The canvas is not a nicer thread — it is a different shape that removes the failure modes the thread is built from.

## Outputs

- A single self-contained HTML decision page in the project's `decisions/` folder.
- A two-column layout with rendered (not described) trade-offs and a sticky picks rail.
- Click-to-pick buttons per decision with a recommendation cue and no pre-selected default.
- Copy, Export (with Markdown download), Accept-all-recommendations, and Reset actions.
- localStorage persistence keyed per page, surviving reloads.
- A one-line hand-over message with the link in the project's convention.

## Examples

### Example 1 — RevSignal aligns a typography revisit

RevSignal's design lead had eight typography decisions to align with the founder. Instead of a reply thread, the skill produced a decision page rendering both type stacks for each choice, with a one-line recommendation and a "Reco" tag per decision. The founder clicked through all eight in one sitting, accepted six recommendations, overrode two, and hit Copy my picks to paste the structured summary back into chat. What would have been three rounds of degrading email became one read and one export, with the picks captured exactly rather than summarized from memory.

### Example 2 — Salt & Stride decides a vendor choice (non-design)

Salt & Stride faced a non-design alignment: choosing among three analytics vendors. The skill surfaced each decision (vendor, data-residency option, contract term) with from/to framing, an opinion callout on the trade-offs, and click-to-pick options. Because the canvas worked for non-design moments, the operations lead could align the whole vendor decision in one page, export the picks as Markdown for the procurement record, and the picks persisted across the two days it took to confirm budget — thanks to the per-page localStorage key.

### Example 3 — Continuum catches a sticky-rail regression in self-test

Continuum rebuilt a decision page and the rail stopped sticking on scroll. The skill's self-test caught it before hand-over: scrolling the main column past the fold revealed the rail scrolling away. The cause was the grid cell defaulting to `stretch`; adding `align-self: start` fixed it. The same self-test confirmed the export copied in both an HTTPS context and a local `file://` open, validating the `execCommand` fallback, so the page was handed over working rather than with a silent clipboard failure.

## Edge cases

- **Invoked with no specifics.** Ask for topic, decisions, and reader first; do not generate from a guessed scope.
- **A trivial decision slips in.** Inline the obvious ones; reserve the page for moments with real optionality.
- **Reader on HTTP or in a sandbox.** Use the `textarea + execCommand` clipboard fallback, not `navigator.clipboard`, which fails silently there.
- **Offline open.** Inline all CSS/JS; a CDN dependency that fails to load breaks the page exactly when it is opened from a local file.
- **Name collision for today.** Append `-v2`/`-v3` rather than overwriting the earlier page.
- **Many decisions.** Group them with labels in both the main column and the rail so the reader can navigate; the click-to-jump sum-items become essential past a handful.
- **Reader wants a written doc instead.** A decision page is interactive; when the same trade-offs must land as prose, pair it with a written executive summary rather than forcing the canvas.

## What NOT to do

- **Don't** describe a trade-off in words when rendering both options would show it — the canvas exists to show, not narrate.
- **Don't** use `<label>`/radio pairs for options; use `<button type="button">` with `pointer-events: none` on inner spans.
- **Don't** pre-select the recommended option; the "Reco" tag is a cue, and the reader must still click.
- **Don't** rely on `navigator.clipboard`; it fails silently in HTTP and sandboxed contexts — use the `execCommand` fallback.
- **Don't** depend on CDN assets; inline everything so the page works offline and from `file://`.
- **Don't** scatter pages across folders; keep them all in one `decisions/` location so every decision is reachable.
- **Don't** hand over a raw `file://` link; use the project's hand-over convention.
- **Don't** merge Copy and Export; the one-click and review-first paths both get used.
