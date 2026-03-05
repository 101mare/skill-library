---
name: make-no-mistakes
description: |
  Precision mode that raises the bar for accuracy and correctness.
  Activates systematic self-verification: every response is drafted,
  verified, and finalized before output. Based on Chain of Verification
  (CoVe) research and self-checking prompting techniques.
  Recognizes: "make no mistakes", "no mistakes", "be precise",
  "be extra careful", "precision mode", "verify everything",
  "this is critical", "production-critical", "zero errors"
  Does NOT handle: planning (use plan-review), debugging (use
  systematic-debugging), code review (use session-verify/pr-review).
---

# Make No Mistakes — Precision Mode

> Inspired by [pashov's MAKE NO MISTAKES](https://gist.github.com/pashov/36122682738b10a4b90a9736b6674dc2), extended with [Chain of Verification](https://arxiv.org/abs/2309.11495) (Meta AI) and [Self-Verification](https://arxiv.org/abs/2212.09561) research.

## Core Directive

Treat every prompt in this session as if it ends with **"MAKE NO MISTAKES."**

This is not about being slow — it's about being right. Prioritize correctness over speed. Acknowledge uncertainty rather than guess. Verify before committing.

## The Verification Protocol

Apply this three-step process to every non-trivial response:

### 1. Draft

Produce the answer, code, or analysis as you normally would.

### 2. Verify

Before outputting, run these checks silently in your thinking:

**For code:**
- Trace the logic step-by-step with a concrete example input
- Check edge cases: empty input, None, zero, negative, boundary values
- Verify imports exist and types align
- Confirm no silent failures (bare `except`, swallowed errors)
- Check: does this actually solve what was asked, or an adjacent problem?

**For facts and claims:**
- Can I point to where I know this from?
- If uncertain, say so explicitly — "I believe X, but verify this"
- Numbers and versions: double-check, don't approximate

**For modifications to existing code:**
- Re-read the code being changed before modifying
- Verify the change doesn't break callers or dependents
- Check that the fix addresses root cause, not symptoms

### 3. Finalize

Output only the verified result. If verification found issues, fix them before responding. If something remains uncertain, flag it explicitly.

## Behavioral Shifts in This Mode

| Default Behavior | Precision Mode Behavior |
|---|---|
| Assume reasonable defaults | Ask when ambiguous |
| Generate code fluently | Trace logic before committing |
| State facts confidently | Qualify uncertain claims |
| Fix the immediate ask | Verify fix doesn't break surroundings |
| Move fast | Move correctly |

## When to Activate

- Production deployments and critical hotfixes
- Security-sensitive code (auth, crypto, permissions)
- Data migrations and schema changes
- Financial calculations
- Public-facing API contracts
- Anything where "almost right" equals wrong

## When NOT to Activate

- Exploratory prototyping and spikes
- Brainstorming sessions
- Quick one-off scripts
- Early-stage iteration where speed matters more than polish

## Anti-Patterns to Catch

- **Plausible but wrong**: Code that looks correct at a glance but fails on edge cases
- **Copy-paste drift**: Adapting a pattern without updating all references
- **Version assumptions**: Using API syntax from a different library version
- **Off-by-one**: Loop bounds, slice indices, range endpoints
- **Silent type coercion**: String/int confusion, truthy/falsy surprises

---

## Verification

Before delivering any response in this mode, check:

1. **Trace test**: For code — did you mentally trace at least one concrete input through the logic? If not, do it now.
2. **Uncertainty audit**: Are there any claims you're less than 90% confident about? Flag them explicitly with "I believe X, but verify this."
3. **Baseline test**: Would you have given the same answer without this skill active? If yes, the verification protocol didn't engage — redo the Verify step.
4. **Edge case scan**: Did you consider empty input, None, zero, boundary values? If the question didn't involve code, did you consider the most likely counterargument to your answer?
