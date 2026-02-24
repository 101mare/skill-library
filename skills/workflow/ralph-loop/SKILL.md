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

```
---
iteration: 0
max_iterations: <MAX>
completion_promise: "COMPLETE"
---
<TASK DESCRIPTION>
```

Replace `<MAX>` with the parsed max value and `<TASK DESCRIPTION>` with the actual task.

## Step 3: Confirm to User

Tell the user:
- Ralph Loop gestartet
- Max iterations: N
- Abbrechen: `.claude/ralph-loop.local.md` loeschen oder Escape/Ctrl+C

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
