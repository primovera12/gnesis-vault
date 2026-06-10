---
name: auto-advance
description: |
  Multi-account auto-rotate + auto-resume layer for Claude Code under rate/session
  limits. On a usage-limit pause it swaps the session's CLAUDE_CONFIG_DIR creds to the
  freshest healthy account and — for HEADLESS/autopilot loops — relaunches
  `claude --continue` so work continues fully hands-off. Interactive VS Code sessions are
  SWAP-ONLY by design (Claude Code has no supported hands-free interactive resume): the
  swap is instant + you press Up+Enter to continue on the fresh account.

  Builds on the `account-orchestrator` skill, which provides the account-health registry
  and the swap engine (claude-acct-status / claude-acct-autoswap / claude-acct-restore).

  Use when:
  - You run headless/autopilot Claude Code loops and want them to survive the 5h/weekly limit unattended
  - You want a session's account swapped automatically the moment it hits a usage limit
  - "/auto-advance", "auto advance", "auto-rotate accounts", "auto resume on limit"

  Examples:
  - "/auto-advance install"
  - "/auto-advance start"
  - "/auto-advance status"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
version: "1.0"
type: skill
domain: devops
triggers:
  slash_commands:
    - /auto-advance
    - /auto-rotate
  keywords:
    - auto advance
    - auto-advance
    - auto rotate accounts
    - auto resume on limit
    - keep autopilot going
    - account auto-rotation
depends_on:
  - account-orchestrator
---

# /auto-advance — multi-account auto-rotate + auto-resume for Claude Code

When a Claude Code session hits a 5-hour / weekly usage limit, `/auto-advance` swaps that
session's account to the freshest healthy one and keeps work moving. It is a thin layer on
top of the **`account-orchestrator`** skill, which owns account-health discovery, the
anti-monoculture cap, anti-flap cooldown, parking, and restore. The engine is the bundled
[`bin/claude-auto-advance`](bin/claude-auto-advance); this skill is the control surface.

## Fully-auto vs swap-only — be honest about it

| Mode | Resume | Status |
|------|--------|--------|
| Headless / autopilot (`claude -p`, CI) | swap creds → relaunch `claude --continue` | ✅ FULLY AUTO |
| Interactive (VS Code / CLI TUI) | swap instantly + notify; you press ↑+Enter | ⚠️ SWAP-ONLY |

There is **no** documented hook/IPC/signal to re-drive a *running* interactive Claude Code
session, and credentials load at process start — so interactive resume stays manual by
design. See [README.md](README.md) §Verification.

## The trigger

- **Reactive:** Claude Code `StopFailure` hook, matchers `rate_limit` + `overloaded`.
- **Proactive:** `/api/oauth/usage` 5h/7d utilization ≥ `switch_pct` (default 90) — swaps
  before the hard stop.
- **Hard cap:** never swaps onto a `MAXED` / 100%-util account.

## Control surface

```bash
claude-auto-advance install --bin --hook   # deploy tool + print StopFailure hook to wire
claude-auto-advance start                  # start the proactive watch daemon
claude-auto-advance status                 # daemon state + live account health + jobs + recent swaps
claude-auto-advance stop
claude-auto-advance run-job <name>         # FULLY-AUTO supervised headless loop
claude-auto-advance swap-now [DIR]         # one-shot proactive swap
# --dry-run on any subcommand writes nothing.
```

## How to drive it (for the agent)

1. Ensure the **`account-orchestrator`** skill is installed (it ships `claude-acct-status`,
   `claude-acct-autoswap`, `claude-acct-restore`). Then run `bash install.sh` here.
2. Help the user **merge** the printed `StopFailure` hook snippet into
   `~/.claude/settings.json` (merge the `hooks.StopFailure` array — never blind-overwrite).
3. For hands-off autopilot survival, add a `headless_jobs[]` entry to
   `~/.config/claude-auto-advance/config.json` (generic — no secrets), then
   `claude-auto-advance run-job <name>`.
4. `claude-auto-advance status` to verify.

## Safety

Only swaps cred files in your own account pool and only relaunches headless jobs you
registered. Never touches another project's processes. Every action logged; swapped-out
creds parked + restorable; `--dry-run` writes nothing.
