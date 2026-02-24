---
name: ralph-loop-prompt-builder
description: |
  Helps build effective prompts for the Ralph Loop autonomous work system.
  Asks clarifying questions about the task, then generates a structured prompt
  with clear requirements, verification steps, and completion criteria.
  Usage: /ralph-loop-prompt-builder
  Triggers: "ralph prompt", "build ralph prompt", "help me write a ralph loop prompt"
---

# Ralph Loop Prompt Builder

Help the user create an effective prompt for `/ralph-loop`. A good Ralph prompt has three mandatory parts: clear task, verification steps, and completion criteria.

## Step 1: Gather Information

Ask the user up to 4 questions using AskUserQuestion. Choose the most relevant questions from this list:

### Question 1: Task Type (always ask)
"What kind of task should the Ralph Loop handle?"
Options:
- Write tests
- Fix a bug
- Refactoring
- Implement a new feature

### Question 2: Scope (always ask)
"Which files/modules are affected?"
Options:
- Single file (e.g. validators.py)
- One module (e.g. src/services/)
- Multiple modules
- Entire project

### Question 3: Verification (ask if not obvious)
"How should Claude verify that progress is correct?"
Options:
- pytest (Unit Tests)
- ruff check (Linting)
- Both (pytest + ruff)
- Other (please describe)

### Question 4: Iteration Limit (ask if user didn't specify)
"How many iterations maximum?"
Options:
- 5 (small fix)
- 10 (medium task)
- 20 (larger task)
- 50 (Default, large task)

## Step 2: Build the Prompt

Based on the answers, construct a Ralph Loop prompt with this structure:

```
/ralph-loop max=<N> <TASK_SUMMARY>

Requirements:
1. <Requirement 1>
2. <Requirement 2>
3. <Requirement 3>

Verification after each iteration:
- <verification command 1>
- <verification command 2>

Done when:
- [ ] <Completion criterion 1>
- [ ] <Completion criterion 2>
- [ ] <Completion criterion 3>
```

### Rules for Building the Prompt

**Requirements:**
- Be specific and measurable, never vague
- Include file paths where relevant
- State what should NOT change (preserve existing behavior)

**Verification:**
- Must be automated commands Claude can run (pytest, ruff, mypy, etc.)
- Never "check manually" or "make sure it looks good"
- Include both correctness (tests) and quality (linting) checks if applicable

**Completion criteria:**
- Checkboxes that Claude can verify programmatically
- Each criterion maps to a verification command
- Include "all existing tests still pass" for refactoring tasks

**Max Iterations:**
- 5 for small, focused fixes
- 10-15 for medium tasks (tests, single-module refactoring)
- 20 for larger tasks (multi-file, new features)
- 50 only for batch operations across many files

## Step 3: Present and Refine

Present the generated prompt to the user. Ask if they want to adjust anything:
- Add or remove requirements
- Change iteration limit
- Modify verification steps

Once confirmed, the user can copy-paste the prompt directly.

## Examples of Good Output

### For "Write tests" + "Single file"

```
/ralph-loop max=15 Write unit tests for src/services/confidence.py.

Requirements:
1. Every public method of ConfidenceScorer needs at least 2 tests
2. Test edge cases: score 0.0, score 1.0, None values
3. Tests in tests/test_services/test_confidence.py

Verification after each iteration:
- pytest tests/test_services/test_confidence.py -q --tb=short

Done when:
- [ ] At least 10 tests written
- [ ] All tests green
- [ ] Edge cases covered
```

### For "Fix a bug" + "Single file"

```
/ralph-loop max=8 Fix the bug: <BUG_DESCRIPTION>.

Requirements:
1. Reproduce the bug with a failing test
2. Implement the fix in <FILE>
3. Ensure existing tests still pass

Verification after each iteration:
- pytest <TEST_FILE> -q --tb=short

Done when:
- [ ] Bug-reproducing test exists and is green
- [ ] Existing tests still green
- [ ] No linting errors
```
