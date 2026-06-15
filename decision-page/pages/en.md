# decision-page

Turn any "reasonable people would disagree" moment into an interactive, click-to-pick HTML
decision sheet — one self-contained file, skinned in the Genesis design system (light + dark).
Each fork shows where it stands, your honest take, and the options with a recommendation; the
reviewer picks, comments, and sends — replacing a long reply-by-reply trade-off thread.

## What it does
- One self-contained HTML file per decision — no build step, nothing to view it but a browser.
- Each decision card: **From** (current state) · **My take** · selectable options with a
  ✓ RECOMMENDED pick. A sticky bottom rail shows progress, an auto-growing comment box,
  "Accept all recs", and "Copy & send".
- **Images:** side-by-side A/B screenshot comparison, single full-width image options, and a
  gallery lightbox — click to zoom, then ‹ › / arrow keys / Esc. Ideal for comparing designs.
- Picks persist in `localStorage`; an optional local server auto-delivers picks to the agent.
- Genesis skin: Outfit headings, Inter body, exact ink/paper/sky tokens, light + dark themes.

## Install
```bash
curl -fsSL -o decision-page.tar.gz \
  https://github.com/primovera12/gnesis-vault/releases/latest/download/decision-page.tar.gz
tar xzf decision-page.tar.gz
cd decision-page
bash install.sh
```

## Usage
Paste into Claude Code:
> Make a decision sheet for these forks: <list your decisions>. Use the Genesis-styled
> decision-page template and give me the link.

Or trigger with `/decision`, `/decision-page`, or `/alignment-canvas`.

## Source
https://github.com/primovera12/gnesis-vault/tree/main/decision-page
