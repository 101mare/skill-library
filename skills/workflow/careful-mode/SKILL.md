---
name: careful-mode
description: |
  Structured, phase-based work mode for tasks that need quality without the overhead of multi-agent workflows.
  Activates a 6-phase cycle: Understand → Plan → Pre-Mortem → Execute → Verify → Deliver.
  Scales automatically — trivial tasks compress to one sentence, complex tasks get the full ceremony.
  Lightweight alternative to plan-review + session-verify for smaller to medium tasks.
  Recognizes: "don't make mistakes", "careful mode", "be thorough", "do this properly",
  "elevated mode", "no mistakes", "be careful with this", "quality mode"
user-invocable: true
---

# Careful Mode

Structured work mode. Better work, not longer answers. Every instruction below is a concrete action.

Say: **"Careful mode active."** Then begin Phase 1.

Deactivate when task is delivered or user says "relax" / "normal mode". Say: **"Task complete. Normal mode."**

**Scaling:** For trivial tasks (a rename, a one-line fix), compress phases 1-3 into one sentence and go straight to execution. Match effort to complexity.

---

## Phase 1: Understand

1. Restate the task in one sentence.
2. Name what the user probably needs beyond what they literally said.
3. If genuinely ambiguous, ask — one round max. If clear, say so and move. Do not manufacture questions to seem thorough.

## Phase 2: Plan

1. List the concrete steps needed.
2. For each step: what it produces, what it depends on.
3. Identify the minimal set of changes to complete this. Write only those steps.

Tell the user the plan before executing.

## Phase 3: Pre-Mortem

Assume the plan already failed catastrophically. Write a 3-line post-mortem:
- Most likely root cause of failure
- Assumption that turned out wrong
- Edge case that was missed

Adjust the plan to prevent these. For simple tasks, one sentence suffices.

## Phase 4: Execute

**Before changing anything:**
- Read first. Read every file you will modify — in full. Read callers of any function you will change. Never edit blind.
- Check state. Run `git status` or equivalent. Know what is already changed.

**While working:**
- Minimal changes only. Change what the task requires. Touch nothing else. Do not refactor adjacent code, add unrequested features, or "improve" things that are not broken.
- Flag uncertainty. If you are guessing instead of knowing, say so: "I'm not certain about X — here's my best assessment and why."
- Surface failures immediately. When a tool call fails, tell the user what failed and what you are trying instead. Never silently retry.
- Check scope before each step. Verify the current step is part of the plan. If it is not, stop and reconsider.
- Update at milestones. The user should never wonder what you are doing.

**If something breaks:**
1. Stop. Run `git diff` to see what changed.
2. Revert the breaking change before trying an alternative.
3. Tell the user what happened before changing approach.

## Phase 5: Verify

Switch to adversarial reviewer mode before delivering.

1. Re-read your output as if reviewing someone else's PR. Check for typos, wrong variable names, references to functions that don't exist.
2. Run tests. If tests exist, run them. If you wrote code, execute it. Do not deliver unvalidated code.
3. Check the diff. Run `git diff` and review every changed line. Confirm each change is intentional and necessary.
4. Answer honestly:
   - Does this do what the user asked, or did I drift?
   - Did I change anything beyond what was requested?
   - Are there edge cases I didn't handle?
5. Fix anything you find. Tell the user what you checked and what you adjusted.

## Phase 6: Deliver

- What was done (2-3 sentences)
- Key decisions and why
- What the user should know going forward

Then: **"Task complete. Normal mode."**

---

## Hard Rules

These apply across all phases, regardless of task size:

| Rule | Why |
|------|-----|
| Read before you write | The #1 agent mistake is editing code without understanding it |
| Minimal blast radius | Maximum effort means maximum quality on the right thing, not maximum changes |
| Verify with tools, not intuition | Run tests, check diffs, execute code — don't just think it's correct |
| Flag uncertainty, don't hide it | A confident wrong answer is worse than an honest "I'm not sure" |
| Never go silent | If work takes time, send brief updates — no exceptions |
| Scale to the task | A simple rename doesn't need a 6-phase ceremony |
| Don't swallow tool failures | Acknowledge failures before moving on |
| Plan changes require notice | If the plan changes, tell the user before changing it — not after |
