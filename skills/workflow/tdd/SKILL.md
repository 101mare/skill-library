---
name: tdd
description: |
  Test-Driven Development workflow: RED-GREEN-REFACTOR cycle.
  Orchestrates test-architect (write failing test) → implementation → code-simplifier (refactor).
  Ensures tests define behavior BEFORE code exists — not after.
  Use when: building new features, adding functions, implementing logic, user says "TDD",
  "test first", "red green refactor", "write the test first", "test-driven".
---

# Test-Driven Development

Workflow that orchestrates RED-GREEN-REFACTOR with real agent delegation.

## Workflow Overview

```
1. Clarify Behavior → 2. RED (test-architect) → 3. Verify Failure → 4. GREEN (implement) → 5. Verify Pass → 6. REFACTOR (code-simplifier) → 7. Verify Pass → 8. Next Behavior
```

## Agent Loading (CRITICAL)

This workflow uses custom agent definitions in `.claude/agents/*.md`. Since the Task tool only supports
`general` and `explore` subagent types, you MUST load agent expertise by **reading their .md files**
and including the system prompt content in the Task prompt.

### How to Use Custom Agents

1. **Read the agent file** with the Read tool: `.claude/agents/{agent-name}.md`
2. **Extract the system prompt** (everything after the YAML frontmatter `---`)
3. **Pass it as context** in the Task tool prompt, prefixed with the role instruction
4. **Use `general`** for both agents (they need write access)

### Required Agent Files

| Agent File | Phase | Role |
|------------|-------|------|
| `.claude/agents/test-architect.md` | RED | Write the failing test |
| `.claude/agents/code-simplifier.md` | REFACTOR | Clean up code and tests |

---

## Step 1: Clarify the Behavior

Before writing any test, understand **exactly** what behavior to implement.

### If Behavior is Clear

User said something like "add IBAN validation that returns True/False" — proceed to Step 2.

### If Behavior is Vague

```
Use AskUserQuestion:
Question: "What exactly should the behavior be?"
Options:
  - "I'll describe the expected input/output"
  - "Look at the existing architecture and suggest tests"
  - "Start with the simplest case, we'll iterate"
```

### Define the Behavior Contract

Before spawning agents, write down:

```markdown
## Behavior to Implement
- **Function**: validate_iban(iban: str) -> bool
- **Happy path**: Valid German IBAN → True
- **Edge cases**: Empty string → False, too short → False, invalid checksum → False
- **File**: src/services/validators.py
- **Test file**: tests/test_services/test_validators.py
```

---

## Step 2: RED — Spawn test-architect to Write Failing Test

**Goal:** test-architect writes a test that FAILS because the behavior doesn't exist yet.

### Execution

1. **Read the agent file**:
   ```
   Read(".claude/agents/test-architect.md")
   ```

2. **Read existing code context** (so the test matches the project):
   ```
   Read("src/services/validators.py")   # or wherever the function will live
   Read("tests/conftest.py")            # existing fixtures
   ```

3. **Spawn test-architect**:

   ```
   Task(
     subagent_type="general",
     prompt="""You are acting as the test-architect agent.

     <agent-instructions>
     [content from test-architect.md after frontmatter]
     </agent-instructions>

     ## Your Task: Write a FAILING test (TDD RED phase)

     Write a test for behavior that DOES NOT EXIST YET. The test MUST fail when run.

     ### Behavior to Test
     [paste behavior contract from Step 1]

     ### Rules for This Test
     - Test describes BEHAVIOR, not implementation details
     - Do NOT mock internals — test inputs and outputs
     - One behavior per test function
     - Name: test_<what>_<condition>_<expected>
     - Include edge cases (empty, None, invalid, boundary values)
     - Use @pytest.mark.parametrize for similar cases
     - The function being tested DOES NOT EXIST YET — that's intentional

     ### Project Context
     [paste relevant existing code, conftest.py fixtures, import paths]

     ### Files to Create/Modify
     - Test file: [path]
     - Do NOT create the implementation — only the test

     Write the test, then STOP. Do not implement the function.
     """
   )
   ```

### Verify the RED Phase

After test-architect finishes:

```bash
pytest tests/test_validators.py -q --tb=line
# MUST fail (NameError, ImportError, or AssertionError)
```

**If the test passes:** Something is wrong. Either the behavior already exists, or the test is trivially true. Ask the user:

```
Use AskUserQuestion:
Question: "The test passes immediately. What should happen?"
Options:
  - "Behavior already exists — next behavior"
  - "Test is wrong — have it rewritten"
  - "Cancel"
```

### RED Exit Criterion

Test fails with the expected error. You understand WHY it fails.

---

## Step 3: GREEN — Write Minimal Implementation

**Goal:** Write the MINIMUM code to make the test pass. This happens in main context, not in an agent.

### Rules

- **Minimal code only** — resist the urge to add "obvious" extras
- **No refactoring yet** — ugly code is fine
- **No new features** — only what the failing test requires
- **If you want to add something, write a test for it first** — that's the next cycle

### Write the Implementation

Implement the function in the target file. Keep it simple.

### Verify the GREEN Phase

```bash
# Run the specific test
pytest tests/test_validators.py -q --tb=line
# MUST pass now

# Run ALL tests
pytest -q --tb=line
# ALL must pass — nothing else broke
```

**If tests fail after implementation:** Fix the implementation, not the test. The test defines the contract.

### GREEN Exit Criterion

The failing test now passes. All other tests still pass.

---

## Step 4: REFACTOR — Spawn code-simplifier to Clean Up

**Goal:** Improve code quality without changing behavior. Tests are the safety net.

### Execution

1. **Read the agent file** (if not already in context):
   ```
   Read(".claude/agents/code-simplifier.md")
   ```

2. **Spawn code-simplifier**:

   ```
   Task(
     subagent_type="general",
     prompt="""You are acting as the code-simplifier agent.

     <agent-instructions>
     [content from code-simplifier.md after frontmatter]
     </agent-instructions>

     ## Your Task: Refactor for clarity (TDD REFACTOR phase)

     These files were just written/modified in a TDD cycle. Clean them up WITHOUT changing behavior.

     ### Files to Review
     - Implementation: [path to implementation file]
     - Tests: [path to test file]

     ### Rules for This Refactor
     - All existing tests MUST still pass after your changes
     - Do NOT add new behavior — that requires a new RED phase
     - Do NOT delete or weaken any test
     - Focus on: naming, duplication, clarity, structure
     - Refactor BOTH code and tests (add parametrize where similar tests exist)
     - Run tests after each change to verify behavior is preserved

     ### What to Look For
     - Duplicated logic → extract helper
     - Poor naming → rename for clarity
     - Similar test cases → @pytest.mark.parametrize
     - Unnecessary complexity → simplify
     - Missing type hints → add them
     """
   )
   ```

### Verify the REFACTOR Phase

```bash
pytest -q --tb=line
# ALL tests must still pass
```

**If tests fail after refactor:** The refactor changed behavior. Revert and try again with smaller changes.

### REFACTOR Exit Criterion

Code is clean, well-named, no duplication. All tests pass.

---

## Step 5: Next Behavior or Done

After one cycle completes:

```
Use AskUserQuestion:
Question: "TDD cycle completed. What next?"
Options:
  - "Next behavior — continue with RED"
  - "Done for now"
  - "Show me a summary of the cycles"
```

If continuing, go back to Step 1 with the next behavior.

---

## Quick Reference: Phase Rules

| Phase | Who | Creates | Exit |
|-------|-----|---------|------|
| RED | `test-architect` agent | Failing test | Test fails with expected error |
| GREEN | Main context | Minimal implementation | Test passes, all tests pass |
| REFACTOR | `code-simplifier` agent | Cleaner code + tests | All tests still pass |

## What Makes a Good TDD Test

**Good — Tests Behavior:**
```python
def test_extract_returns_text_from_pdf():
    result = extract(sample_pdf_path)
    assert "Steuererklärung" in result
```

**Bad — Tests Implementation:**
```python
def test_extract_calls_pymupdf_and_joins_pages():
    with patch("extractors.pdf.fitz.open") as mock_fitz:
        mock_fitz.return_value.__enter__.return_value = [mock_page]
        result = extract(sample_pdf_path)
        mock_fitz.assert_called_once_with(str(sample_pdf_path))
```

**Good — Tests Edge Cases:**
```python
@pytest.mark.parametrize("input_val, expected", [
    ("", False),
    ("DE", False),
    ("XX12345678901234", False),
    ("DE89370400440532013000", True),
])
def test_validate_iban_edge_cases(input_val, expected):
    assert validate_iban(input_val) is expected
```

## When NOT to Use TDD

- **Exploratory prototyping** — when you don't know what behavior should be yet
- **UI/visual work** — hard to test visually, write tests after
- **One-off scripts** — not worth the overhead
- **Prompt engineering** — LLM outputs are non-deterministic

Use TDD for: business logic, validators, transformers, parsers, APIs, anything with clear input/output contracts.

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|---|---|---|
| Writing test after code | Test confirms status quo | Always RED first — spawn test-architect BEFORE implementing |
| Test passes immediately | Behavior already exists or test is trivially true | Verify failure before proceeding to GREEN |
| Testing implementation details | Brittle, breaks on refactor | Instruct test-architect to test behavior and outputs |
| Skipping REFACTOR phase | Technical debt accumulates | Always spawn code-simplifier after GREEN |
| Refactoring in GREEN phase | Mixing concerns, harder to debug | Strict phase separation — GREEN is minimal only |
| Implementing in RED phase | Defeats the purpose of TDD | test-architect must NOT create the implementation |
| Main context writes tests | No separation, temptation to "cheat" | Delegate to test-architect who doesn't see implementation |

## Important Notes

- **Agent loading**: ALWAYS read `.claude/agents/*.md` files and inject their prompts into Task agents
- **Sequential, not parallel**: RED → GREEN → REFACTOR must run in order (each depends on the previous)
- **test-architect writes ONLY tests**: Never let the RED agent also write the implementation
- **GREEN stays in main context**: The implementation needs full project awareness
- **Run tests between every phase**: Tests are the proof that TDD works
- **Match the user's language**: Respond in the same language the user uses
- **Project-agnostic**: Read the project's CLAUDE.md to understand testing conventions, import paths, and fixture patterns before starting
