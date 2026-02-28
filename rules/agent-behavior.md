---
name: agent-behavior
description: Read-first workflow, scope discipline, minimal changes, subagent strategy, and bug fixing approach.
---

# Agent Behavior

## Before Writing Code

- **Read first, write second**: Always read existing code before modifying. Understand patterns before proposing changes.
- **Follow existing conventions**: If the project uses `snake_case`, don't introduce `camelCase`. If it uses `dataclasses`, don't switch to `attrs`. Match what's there.
- **Plan non-trivial work**: Enter plan mode for tasks with 3+ steps or architectural decisions. Write a clear plan before touching code. If something goes sideways mid-implementation, STOP and re-plan — don't keep pushing a broken approach.
- **Ask, don't assume**: When in doubt, ALWAYS ask. Better to ask once too many than to implement incorrectly. Prefer one round of 4 good questions over 4 rounds of 1 question.

## While Writing Code

- **Scope discipline**: Only change what was asked. A bug fix doesn't need surrounding code cleaned up. A new feature doesn't need neighboring code refactored.
- **Minimal changes**: Smallest diff that solves the problem. No drive-by refactors.
- **No over-engineering**: Don't add features, abstractions, or configurability that wasn't requested. Three similar lines are better than a premature helper.
- **No unnecessary comments**: Code should be self-explanatory. Only comment WHY, never WHAT. Don't add docstrings to code you didn't change.
- **No backwards-compatibility hacks**: No unused `_vars`, no `# removed` comments, no re-exports of deleted functions. Delete means delete.

## After Writing Code

- **Verify before done**: Never mark a task complete without proving it works. Run tests, check logs, demonstrate correctness. Ask: "Would a staff engineer approve this?"
- **Challenge non-trivial changes**: For anything beyond a simple fix, pause and ask "is there a more elegant way?" Skip this for obvious one-liners — don't over-engineer.
- Use `code-simplifier` agent proactively after writing significant code chunks
- Check: redundancy, clarity (>30 line functions), consistency, over-engineering
- Don't simplify code you didn't change

## Subagent Strategy

- Use subagents liberally to keep the main context window clean
- Offload research, exploration, and parallel analysis to subagents
- One focused task per subagent — don't overload them

## Bug Fixing

- When given a bug report with clear symptoms: just fix it. Don't ask for hand-holding.
- Point at logs, errors, failing tests — then resolve them. Zero context switching required from the user.
- Find root causes. No temporary workarounds. No suppressing errors to make them go away.

## Memory

- Write to `.claude/memory.md` for architecture decisions and workarounds
- Keep concise — this persists across sessions
- Don't duplicate what's already in CLAUDE.md
