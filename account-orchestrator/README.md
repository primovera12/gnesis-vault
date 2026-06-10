# Account Orchestrator

Run many Claude Code accounts without the rate-limit storm. See live per-account usage,
give each project its own account, and **auto-switch a running chat to a fresh account
before it hits the session limit — no window reload.**

## The discovery
`GET https://api.anthropic.com/api/oauth/usage` (with a Max account's OAuth bearer) returns
real **5-hour** and **7-day** utilization %. This kit turns that into a registry, a
per-project distributor, a live dashboard, and an automatic switcher.

## Install
```bash
bash install.sh        # tools → ~/.local/bin, governor hook, 3 timers
```
Authenticate each account into its own config dir first: `~/.claude` (default) and
`~/.claude-acct1 … ~/.claude-acctN` (sign in with `CLAUDE_CONFIG_DIR=~/.claude-acctN claude /login`).

## The tools
| Tool | What it does |
|---|---|
| `claude-acct-status` | Live health registry — per account 5h / 7d / per-model %, status VALID/MAXED/EXPIRED. `--healthy` lists usable (incl. refreshable) accounts; `--current [pct]` prints the freshest under a threshold. |
| `claude-acct-distribute` | Gives each `~/projects/*` repo a **different account** via `.vscode/settings.json` `claudeCode.environmentVariables` → `CLAUDE_CONFIG_DIR`. Balanced; auto-discovers new project folders (worktrees excluded). `--apply` to write. |
| `claude-acct-dashboard` | One HTML widget for all accounts (light/dark). Shows a **MISSING** card for any expected account that got displaced. |
| `claude-acct-autoswap` | **Automatic, no-reload switch.** Every 2 min: if a running chat's account nears its limit, swaps that chat's credential dir to a fresher account — the chat re-reads creds on its next message and switches. Heavy tasks (probe/research/autopilot) are **reserved** and left alone. |
| `claude-acct-redistribute` | Re-runs the distributor across all auto-discovered projects (30-min timer) so new folders get balanced. |
| `claude-best` | Drop-in for `claude` that launches on the freshest account (for autopilots / loops / new windows). |
| `claude-usage` | Opens claude.ai usage page per account in a mapped browser. |

## How the automatic switch works (and its honest limit)
A running Claude Code chat **re-reads `CLAUDE_CONFIG_DIR/.credentials.json`** on its next
message. So swapping that file's creds to a fresh account switches the chat **without a
reload**. The orchestrator does this automatically at ~90%. It **cannot create capacity**:
if every account is maxed, there's nowhere to switch to — it says so and waits for resets.

## Heavy-task isolation
A chat running `probe` / `research` / an autopilot (sub-agent heavy) gets its account
**reserved** — never switched away from, never used as a switch target — so the heavy task
keeps an uncontended account.

## Governor
`hooks/heavy-work-governor.sh` (PreToolUse) paces heavy `claude -p` launches under CPU/rate
pressure. Wire it in `~/.claude/settings.json`:
```json
{ "hooks": { "PreToolUse": [ { "matcher": "Bash", "hooks": [ { "type": "command", "command": "$HOME/.claude/hooks/heavy-work-governor.sh", "timeout": 45 } ] } ] } }
```

## Config
- `~/.claude-accounts/expected.txt` — your account emails (for MISSING detection).
- `ACCT_SWITCH_PCT` (default 90) — the switch threshold.
