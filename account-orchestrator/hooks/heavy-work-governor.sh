#!/usr/bin/env bash
# heavy-work-governor — PreToolUse governor (global).
# PURPOSE: auto-pace HEAVY launches (Workflow fan-outs, /probe & autopilot runs,
# Bash spawning `claude -p` fleets) when the machine is already oversubscribed,
# so concurrent Claude work does not peg the 16 cores OR burst the per-account
# API rate limit. Fully automatic: it WAITS for room, then proceeds. No rerun,
# no web, no paste.
#
# SAFETY: FAIL-OPEN. It NEVER emits exit 2 (deny). Worst case it waits MAXWAIT
# seconds then allows anyway. Any error/parse-failure => allow immediately.
# Disable instantly:  export HEAVY_GOVERNOR_OFF=1   OR   touch ~/.heavy-governor-off
# Tune: HEAVY_GOVERNOR_CAP (max concurrent `claude -p`, default = nproc)
#       HEAVY_GOVERNOR_MAXWAIT (seconds, default 30)
# Observe: ~/.local/state/heavy-governor.log   (healing is never silent)
#
# Slow and steady wins the race — RULES/GOLDEN-RULE.md

LOG="$HOME/.local/state/heavy-governor.log"

# --- fast escape hatches (fail-open) ---
[ "${HEAVY_GOVERNOR_OFF:-0}" = "1" ] && exit 0
[ -f "$HOME/.heavy-governor-off" ] && exit 0

input="$(cat 2>/dev/null)"
tool="$(printf '%s' "$input" | jq -r '.tool_name // empty' 2>/dev/null)"
cmd="$(printf '%s'  "$input" | jq -r '.tool_input.command // empty' 2>/dev/null)"

# --- is this a HEAVY launch? (otherwise allow instantly) ---
heavy=0
case "$tool" in
  Workflow) heavy=1 ;;
  Bash)
    printf '%s' "$cmd" | grep -qE 'claude +-p |probe-autopilot|gsd-autopilot|kit-autopilot|system-atlas-probe|fake-pass-poll-watcher' && heavy=1 ;;
esac
[ "$heavy" = "1" ] || exit 0

CORES="$(nproc 2>/dev/null || echo 8)"
CAP="${HEAVY_GOVERNOR_CAP:-$CORES}"
MAXWAIT="${HEAVY_GOVERNOR_MAXWAIT:-30}"
mkdir -p "$(dirname "$LOG")" 2>/dev/null || true

oversub() {
  # oversubscribed if 1-min load > cores*1.3  OR  concurrent `claude -p` >= CAP
  local l1 hc
  l1="$(awk '{print $1}' /proc/loadavg 2>/dev/null || echo 0)"
  hc="$(pgrep -fc 'claude -p ' 2>/dev/null || echo 0)"
  if awk -v l="$l1" -v c="$CORES" 'BEGIN{exit !(l > c*1.3)}'; then return 0; fi
  [ "${hc:-0}" -ge "$CAP" ] && return 0
  return 1
}

if oversub; then
  ts="$(date '+%F %T' 2>/dev/null)"
  waited=0
  while oversub && [ "$waited" -lt "$MAXWAIT" ]; do
    sleep 3 2>/dev/null || break
    waited=$((waited + 3))
  done
  l1="$(awk '{print $1}' /proc/loadavg 2>/dev/null)"
  hc="$(pgrep -fc 'claude -p ' 2>/dev/null || echo 0)"
  echo "$ts throttle tool=$tool waited=${waited}s load=$l1 headless=$hc cap=$CAP -> allow" >> "$LOG" 2>/dev/null || true
fi

exit 0
