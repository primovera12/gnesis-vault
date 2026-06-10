---
name: account-orchestrator
description: >
  Run many Claude Code accounts on one machine without the rate-limit storm.
  Pulls LIVE per-account usage (5-hour, 7-day, and per-model utilization %, plus
  reset clocks) straight from the OAuth usage endpoint — the gauge most people
  think Max accounts don't expose — and turns it into: a health registry that
  knows which accounts are usable vs maxed/expired/refreshable right now; a
  distributor that hands each VS Code project a different account (auto-discovers
  new project folders); an HTML dashboard; and — the headline — an AUTOMATIC
  switcher that moves a RUNNING chat to a fresh account before it hits the session
  limit, with NO window reload, by swapping the credential file the chat re-reads.
  Heavy tasks (probe/research/autopilot) get a reserved, uncontended account.
  Use when: you run 2+ Claude accounts and keep hitting "Server is temporarily
  limiting requests"; you want each project on its own rate budget; or you want
  chats to switch accounts automatically before they stop.
when_to_use:
  - "Running multiple Claude Max accounts and hitting rate limits across all sessions at once"
  - "Want a running chat to auto-switch accounts BEFORE it hits the session limit (no reload)"
  - "Want each VS Code project to use a different account automatically (auto-discovered)"
  - "Want a heavy probe/research/autopilot to keep its own uncontended account"
  - "Want to SEE live 5h / 7d / per-model usage % per account in one dashboard"
  - "Setting up / re-authenticating multiple ~/.claude-acctN profiles"
domain: orchestration
tier: 2
allowed_tools: [Bash, Read, Write, Edit]
version: 2.0.0
---

# Account Orchestrator

Run a fleet of Claude Code accounts like one pool — see every account's real usage,
route projects onto fresh accounts, and **auto-switch a running chat to a fresh account
before it hits the limit, no reload.**

## The key discovery

`GET https://api.anthropic.com/api/oauth/usage` (with a Max account's OAuth bearer + header
`anthropic-beta: oauth-2025-04-20`) returns **live utilization** (5h / 7d / per-model + reset
clocks). Identity comes from `GET /api/oauth/profile` `.account.email` (the local cache lies).

**The second discovery (what makes auto-switch possible):** a *running* Claude Code chat
**re-reads `CLAUDE_CONFIG_DIR/.credentials.json` on its next message.** So swapping that file
to a fresh account switches the live chat — without a window reload.

## The tools

| Tool | What it does |
|---|---|
| **`claude-acct-status`** | Health registry → `~/.claude-accounts.json`. Per account: email, 5h/7d/per-model %, reset clocks, status **VALID / MAXED / EXPIRED(+refreshable) / THROTTLED**. `--healthy` lists usable accounts; `--current [pct]` prints the freshest under a threshold. |
| **`claude-acct-distribute`** | Writes `claudeCode.environmentVariables.CLAUDE_CONFIG_DIR` per project `.vscode/settings.json` → each window a different account. **Auto-discovers** `~/projects/*` (worktrees excluded), balanced. `--apply` to write. |
| **`claude-acct-autoswap`** | **The automatic switcher.** Every 2 min: if a running chat's account ≥ threshold (90%), swap that chat's credential dir to a fresher account → it switches on its next message, no reload. Heavy tasks **reserved**. |
| **`claude-acct-redistribute`** | 30-min timer — re-balances all auto-discovered projects so new folders get an account. |
| **`claude-acct-dashboard`** | HTML widget — 5h/7d bars, per-model, duplicate + **MISSING** flags, light/dark, 3-min refresh. |
| **`claude-best`** | Drop-in for `claude` that launches on the freshest account (autopilots/loops/new windows). |

Plus `syswatch` + a PreToolUse **heavy-work governor**.

## Automatic switch — and its honest limit
The autoswap moves a near-limit chat onto the freshest account with headroom. It **cannot
create capacity**: if every account is maxed, there is nowhere to switch — it logs "capacity
tight" and waits for resets. The true ceiling is **total weekly token budget across accounts.**

## Heavy-task isolation
A chat running `probe` / `research` / an autopilot gets its account **reserved** — never
switched away from, never used as a switch target — so the heavy task stays uncontended.

## Multi-account auth (the gotcha)
`claude auth login --email X` **ignores** `--email` — the browser session wins. So: open an
**Incognito** window signed into the target account, run `claude auth login`, **confirm the
"Authorizing as ___" line**, then copy creds into the slot and verify via `/api/oauth/profile`.

## Install
```bash
bash install.sh   # tools → ~/.local/bin · governor hook · 3 timers (dashboard/redistribute/autoswap)
```
Then: `claude-acct-status` · `claude-acct-dashboard --open` · `claude-acct-distribute --apply`.
