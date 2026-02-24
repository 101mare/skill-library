---
name: ralph-loop-init
description: |
  Install the Ralph Loop (autonomous work loop) into the current project.
  Creates the Stop hook, configures settings, and copies the skill file.
  Usage: /ralph-loop-init
---

# Ralph Loop — Installation

Install the Ralph Loop autonomous work system into the current project.

## Prerequisites

Check that `jq` is installed:

```bash
jq --version
```

If missing, tell the user to install it (`sudo apt install jq` / `brew install jq`) and stop.

## Step 1: Create Hook Directory and Script

Create `.claude/hooks/ralph-loop-stop.sh` with this exact content:

```bash
#!/usr/bin/env bash
# ralph-loop-stop.sh — Stop hook for autonomous Claude Code work loops.
set -euo pipefail

STATE_FILE=".claude/ralph-loop.local.md"

if [[ ! -f "$STATE_FILE" ]]; then
  exit 0
fi

INPUT=$(cat)
STOP_HOOK_ACTIVE=$(echo "$INPUT" | jq -r '.stop_hook_active // false')
LAST_MSG=$(echo "$INPUT" | jq -r '.last_assistant_message // ""')

ITERATION=$(sed -n 's/^iteration: *//p' "$STATE_FILE" | head -1)
MAX_ITERATIONS=$(sed -n 's/^max_iterations: *//p' "$STATE_FILE" | head -1)
COMPLETION_PROMISE=$(sed -n 's/^completion_promise: *"\(.*\)"/\1/p' "$STATE_FILE" | head -1)

if ! [[ "$ITERATION" =~ ^[0-9]+$ ]]; then ITERATION=1; fi
if ! [[ "$MAX_ITERATIONS" =~ ^[0-9]+$ ]]; then MAX_ITERATIONS=50; fi
if [[ -z "$COMPLETION_PROMISE" ]]; then COMPLETION_PROMISE="COMPLETE"; fi

if (( ITERATION >= MAX_ITERATIONS )); then
  rm -f "$STATE_FILE"
  exit 0
fi

if [[ "$STOP_HOOK_ACTIVE" == "true" ]] && (( ITERATION == 0 )); then
  rm -f "$STATE_FILE"
  exit 0
fi

if echo "$LAST_MSG" | grep -qF "<promise>${COMPLETION_PROMISE}</promise>"; then
  rm -f "$STATE_FILE"
  exit 0
fi

NEW_ITERATION=$((ITERATION + 1))
sed -i "s/^iteration: .*/iteration: ${NEW_ITERATION}/" "$STATE_FILE"

PROMPT=$(awk '/^---$/{n++; next} n>=2' "$STATE_FILE")

# Re-orient every 5 iterations (combat context degradation)
if (( NEW_ITERATION % 5 == 0 )); then
  REORIENT="IMPORTANT: Before continuing, re-read the relevant files from disk (do NOT rely on memory). Briefly summarize what is done and what remains. Then continue. "
else
  REORIENT=""
fi

jq -n \
  --arg reason "${REORIENT}Ralph Loop iteration ${NEW_ITERATION}/${MAX_ITERATIONS}. Continue working on the task. When fully done, output <promise>${COMPLETION_PROMISE}</promise>. Original task: ${PROMPT}" \
  '{"decision": "block", "reason": $reason}'
```

Then make it executable:

```bash
chmod +x .claude/hooks/ralph-loop-stop.sh
```

## Step 2: Configure the Stop Hook

Read `.claude/settings.local.json`. If it exists, merge the `hooks` key into the existing JSON. If it does not exist, create it.

The hooks configuration to add:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/ralph-loop-stop.sh",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

Important: Preserve all existing keys (like `permissions`) when merging.

## Step 3: Install the Ralph Loop Skill

Create `.claude/skills/ralph-loop/SKILL.md` with this exact content:

```yaml
---
name: ralph-loop
description: |
  Start an autonomous work loop. Claude keeps working on the given task
  until it signals completion or the iteration limit is reached.
  Usage: /ralph-loop <task description>
  Optional: /ralph-loop max=20 <task description>
  Cancel: delete .claude/ralph-loop.local.md or press Escape/Ctrl+C
---

# Ralph Loop — Autonomous Work Mode

You have been asked to enter an autonomous work loop. Follow these steps exactly.

## Step 1: Parse Arguments

Extract from the user's input:
- **max**: Optional iteration limit (default: 50). Look for `max=N` at the start.
- **task**: Everything else is the task description.

Examples:
- `/ralph-loop Fix all linting errors` → max=50, task="Fix all linting errors"
- `/ralph-loop max=20 Add unit tests for validators.py` → max=20, task="Add unit tests for validators.py"

## Step 2: Create State File

Use the Write tool to create `.claude/ralph-loop.local.md` with this exact format:

    ---
    iteration: 0
    max_iterations: <MAX>
    completion_promise: "COMPLETE"
    ---
    <TASK DESCRIPTION>

Replace `<MAX>` with the parsed max value and `<TASK DESCRIPTION>` with the actual task.

## Step 3: Confirm to User

Tell the user:
- Ralph Loop started
- Max iterations: N
- Cancel: delete `.claude/ralph-loop.local.md` or press Escape/Ctrl+C

## Step 4: Work on the Task

Begin immediately. Work methodically, step by step. Each iteration you will receive the original task as a reminder — use it to stay on track and check what's still missing.

## Step 5: Signal Completion

When ALL work is truly finished (implemented, tested if applicable), include this exact tag in your response:

<promise>COMPLETE</promise>

## Rules

- NEVER output `<promise>COMPLETE</promise>` until the task is genuinely done
- If blocked and need user input: output `<promise>COMPLETE</promise>` and explain the blocker
- If you notice you're going in circles: output `<promise>COMPLETE</promise>` and summarize what was accomplished vs. what remains
- Stay focused on the original task — don't drift into unrelated improvements
```

## Step 4: Enable Auto-Compact

The Ralph Loop benefits greatly from auto-compact, which prevents context degradation during long loops. Tell the user to enable it via `/config` and set `autoCompact` to `true` (or verify it is already enabled). This is strongly recommended for any Ralph Loop usage.

## Step 5: Optional — Install Prompt Template and Prompt Builder

Two additional files from this library can help the user write effective Ralph Loop prompts:

1. **Prompt Template** (`prompt-template.md` in this skill's directory) — Reference with the template structure, 4 examples, and anti-patterns. Copy to `.claude/skills/ralph-loop/prompt-template.md` so Claude can reference it when needed.

2. **Prompt Builder Skill** (`ralph-loop-prompt-builder/SKILL.md` in the parent directory) — Interactive skill that asks clarifying questions and generates a structured Ralph Loop prompt. Copy to `.claude/skills/ralph-loop-prompt-builder/SKILL.md` to enable the `/ralph-loop-prompt-builder` command.

Both are optional but recommended.

## Step 6: Confirm Installation

Tell the user:

```
Ralph Loop installed.

Files:
  .claude/hooks/ralph-loop-stop.sh    (Stop Hook)
  .claude/settings.local.json         (Hook configuration)
  .claude/skills/ralph-loop/SKILL.md  (Skill file)

Next step: Restart Claude Code (hooks are loaded at session start).

Usage:
  /ralph-loop <task>
  /ralph-loop max=20 <task>

Cancel:
  rm .claude/ralph-loop.local.md
  or press Escape/Ctrl+C
```

## Step 7: Remind About Restart

Hooks are loaded at session start. The user MUST restart Claude Code for the Stop hook to take effect. Emphasize this clearly.
