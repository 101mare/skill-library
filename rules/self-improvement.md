---
name: self-improvement
description: Learn from corrections, capture patterns in memory, iterate on lessons.
---

# Self-Improvement

Activate when: user corrects a mistake, or says "remember this", "lesson learned", "never do that again".

## After Every Correction

- Capture the pattern in `.claude/memory.md`: concrete problem → why the old approach was wrong → what to do instead
- Extract the general principle, not just the specific fix
- Be specific: "Use `T | None` not `Optional[T]`" beats "follow modern Python style"

## What NOT to Write

- Session-specific state (current task, in-progress work, temporary context)
- Speculative conclusions — verify against project docs before writing
- Anything that duplicates CLAUDE.md or existing rules

## Memory Hygiene

- If a similar entry exists, update it — don't create a near-duplicate
- Prune when: architecture changed, user switched conventions, or entry is too vague to act on
- If the same mistake happens twice, the lesson wasn't specific enough — rewrite it

## At Session Start

- Review `.claude/memory.md` and apply learned lessons before they become repeat mistakes
