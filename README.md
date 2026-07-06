# The Vault — skills we share

Free, open-source [Claude Code](https://claude.com/claude-code) skills from **Gnesis**.
Browse and one-click-install them at **[gnesis.dev/vault](https://gnesis.dev/vault)**.

This repo is the single source of truth for those skills. Each skill lives in its
own top-level folder. On every push to `main`, CI packages each folder into a
`<skill>.tar.gz` and publishes it to the rolling [**latest**](../../releases/latest)
release — so the download on the Vault is always the newest build, with no site
redeploy.

## Skills

| Skill                                           | What it does                                                                                                                                                               | Download                                                                     |
| ----------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| [`account-orchestrator`](account-orchestrator/) | Run many Claude Code accounts as one pool — live per-account usage, one account per project, and an automatic no-reload switch of a running chat before it hits the limit. | [latest tarball](../../releases/latest/download/account-orchestrator.tar.gz) |
| [`auto-advance`](auto-advance/)                 | Auto-rotate + auto-resume under rate/session limits. Detects a usage-limit pause, swaps to the freshest account, and relaunches headless/autopilot loops (`claude --continue`) hands-off. Interactive sessions are swap-only by design. Builds on `account-orchestrator`.        | [latest tarball](../../releases/latest/download/auto-advance.tar.gz)         |
| [`decision-page`](decision-page/) | "Generate an interactive single-file HTML decision page for any substantive alignment moment where reasonable people would disagree — replacing a reply-by-reply trade-off thread   | [latest tarball](../../releases/latest/download/decision-page.tar.gz) |
| [`vscode-window-labeler`](vscode-window-labeler/) |   | [latest tarball](../../releases/latest/download/vscode-window-labeler.tar.gz) |

> **Verified & honest about limits.** `auto-advance` is explicit about what's actually
> hands-free. **Headless / autopilot** loops (`claude -p`) are **fully automatic** — on a
> limit it swaps accounts and relaunches `claude --continue`. **Interactive** VS Code / CLI
> sessions are **swap-only**: Claude Code has no supported way to re-drive a *running*
> interactive session, so the swap is instant + you press ↑+Enter to continue on the fresh
> account. We don't fake hands-free interactive resume — verified against the Claude Code
> docs. The swap engine is battle-tested (never swaps onto a maxed account; every swap is
> parked + reversible; `--dry-run` everywhere). See
> [`auto-advance/README.md`](auto-advance/README.md#verification-why-interactive-is-swap-only).

## Install a skill

```bash
# Replace <skill> with the folder name, e.g. account-orchestrator
curl -fsSL -o <skill>.tar.gz \
  https://github.com/primovera12/gnesis-vault/releases/latest/download/<skill>.tar.gz
tar xzf <skill>.tar.gz
cd <skill>
bash install.sh
```

Or grab it from the Vault UI at [gnesis.dev/vault](https://gnesis.dev/vault), which
generates a one-shot install prompt you can paste into Claude Code.

## Add / update a skill

1. Add a folder at the repo root containing at least a `SKILL.md` (plus
   `README.md`, `install.sh`, `bin/`, etc. as needed).
2. Keep it **sanitized** — no personal data. This repo is public; use placeholder
   values (e.g. `you@example.com`), never real emails or hostnames.
3. `git push`. CI repackages everything and refreshes the `latest` release.
   The Vault picks it up automatically.

## License / use

Shared as-is for the community to use and learn from. No warranty.
