#!/usr/bin/env bash
# ralph-loop-stop.sh — Stop hook for autonomous Claude Code work loops.
#
# Keeps Claude working in a loop until:
#   1. Claude outputs <promise>COMPLETION_TEXT</promise>  (task done)
#   2. Max iterations reached                             (safety limit)
#   3. State file deleted by user                         (manual cancel)
#
# State file: .claude/ralph-loop.local.md (YAML frontmatter + prompt)
# Dependency: jq
#
# Install: Copy to .claude/hooks/ and add Stop hook to settings.local.json

set -euo pipefail

# --- State file path ---
STATE_FILE=".claude/ralph-loop.local.md"

# --- No state file? No loop active. Allow normal stop. ---
if [[ ! -f "$STATE_FILE" ]]; then
  exit 0
fi

# --- Read hook input from stdin ---
INPUT=$(cat)

# --- Extract last assistant message from hook input ---
LAST_MSG=$(echo "$INPUT" | jq -r '.last_assistant_message // ""')

# --- Parse YAML frontmatter from state file ---
ITERATION=$(sed -n 's/^iteration: *//p' "$STATE_FILE" | head -1)
MAX_ITERATIONS=$(sed -n 's/^max_iterations: *//p' "$STATE_FILE" | head -1)
COMPLETION_PROMISE=$(sed -n 's/^completion_promise: *"\(.*\)"/\1/p' "$STATE_FILE" | head -1)

# --- Validate numeric fields (fallback to safe defaults) ---
if ! [[ "$ITERATION" =~ ^[0-9]+$ ]]; then
  ITERATION=1
fi
if ! [[ "$MAX_ITERATIONS" =~ ^[0-9]+$ ]]; then
  MAX_ITERATIONS=50
fi
if [[ -z "$COMPLETION_PROMISE" ]]; then
  COMPLETION_PROMISE="COMPLETE"
fi

# --- Safety: max iterations reached → stop loop, clean up ---
if (( ITERATION >= MAX_ITERATIONS )); then
  rm -f "$STATE_FILE"
  exit 0
fi

# --- Completion promise detected → stop loop, clean up ---
if echo "$LAST_MSG" | grep -qF "<promise>${COMPLETION_PROMISE}</promise>"; then
  rm -f "$STATE_FILE"
  exit 0
fi

# --- Not done: increment iteration ---
NEW_ITERATION=$((ITERATION + 1))
sed -i "s/^iteration: .*/iteration: ${NEW_ITERATION}/" "$STATE_FILE"

# --- Extract original prompt (everything after second ---) ---
PROMPT=$(awk '/^---$/{n++; next} n>=2' "$STATE_FILE")

# --- Block stop: re-feed prompt to Claude ---
jq -n \
  --arg reason "Ralph Loop iteration ${NEW_ITERATION}/${MAX_ITERATIONS}. Continue working on the task. When fully done, output <promise>${COMPLETION_PROMISE}</promise>. Original task: ${PROMPT}" \
  '{"decision": "block", "reason": $reason}'
