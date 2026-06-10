# auto-advance

Auto-rotate + auto-resume for Claude Code under rate/session limits. On a usage-limit
pause it swaps your session to the freshest healthy account and — for headless/autopilot
loops — relaunches `claude --continue` so work never stops. Interactive VS Code / CLI
sessions are swap-only by design. Builds on `account-orchestrator`.

## What it does
- Detects the usage-limit pause and swaps to the freshest account (anti-monoculture cap,
  anti-flap cooldown, never onto a maxed account).
- **Headless / autopilot** (`claude -p`): fully automatic — swaps **and** relaunches
  `claude --continue`.
- **Interactive**: swap-only — the swap is instant, you press ↑+Enter to continue on the
  fresh account. No faked hands-free interactive resume.

## Install
```bash
curl -fsSL -o auto-advance.tar.gz \
  https://github.com/primovera12/gnesis-vault/releases/latest/download/auto-advance.tar.gz
tar xzf auto-advance.tar.gz
cd auto-advance
bash install.sh
```
Requires `jq`, `curl`, and the `claude-acct-*` tools (from `account-orchestrator`).

## Usage
Paste into Claude Code:
> Install auto-advance from the Gnesis Vault, then start it so my autopilot auto-swaps
> accounts when it hits the limit.

Or run directly: `/auto-advance start` · `/auto-advance status` · `/auto-advance stop`.

## Source
https://github.com/primovera12/gnesis-vault/tree/main/auto-advance
