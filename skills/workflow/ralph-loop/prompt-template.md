# Ralph Loop — Prompt Template

Use this template to write effective prompts for `/ralph-loop`.

## Template

```
/ralph-loop max=<N> <TASK>

Requirements:
1. <Concrete outcome 1>
2. <Concrete outcome 2>
3. <Concrete outcome 3>

Verification after each iteration:
- <Testable command, e.g. pytest, ruff, etc.>

Done when:
- [ ] <Checklist item 1>
- [ ] <Checklist item 2>
- [ ] <Checklist item 3>
```

## The Three Mandatory Components

### 1. Clear Task (What exactly?)

Concrete and verifiable, not vague.

| Bad | Good |
|-----|------|
| "Improve the tests" | "Write unit tests for validators.py. Every public function needs at least 2 tests." |
| "Make the code better" | "Refactor extract_json_object() — extract the regex logic into its own function." |
| "Find bugs" | "Run ruff check src/ and fix all reported errors." |

### 2. Verification Steps (How does Claude know it's working?)

Claude must be able to verify progress on its own in each iteration.

```
Verification after each iteration:
- pytest tests/test_validators.py -q --tb=short
- ruff check src/services/validators.py
```

Good verifications: `pytest`, `ruff check`, `mypy`, `bash script.sh`, file checks.
Bad verifications: "see if it looks good", "test manually".

### 3. Done Criterion (When is it finished?)

Explicit checklist so Claude knows when `<promise>COMPLETE</promise>` is appropriate.

```
Done when:
- [ ] All 5 functions have tests
- [ ] pytest runs green (0 failures)
- [ ] No linting errors
```

## Examples

### Example 1: Writing Tests

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

### Example 2: Refactoring

```
/ralph-loop max=10 Refactor src/extractors/pdf.py — the extract() method is too long.

Requirements:
1. Reduce extract() to max 30 lines
2. Extract logic into private helper methods
3. No behavior change (existing tests must stay green)

Verification after each iteration:
- pytest tests/test_extractors/ -q --tb=short
- ruff check src/extractors/pdf.py

Done when:
- [ ] extract() <= 30 lines
- [ ] All existing tests green
- [ ] No linting errors
```

### Example 3: Fixing a Bug

```
/ralph-loop max=8 Fix the bug: IBAN validation accepts IBANs with incorrect check digits.

Requirements:
1. Implement check digit validation in EntityValidator.validate_iban()
2. Test that reproduces the bug (incorrect check digit → None)
3. Test with valid IBANs that continue to be accepted

Verification after each iteration:
- pytest tests/test_services/test_validators.py -q --tb=short

Done when:
- [ ] Incorrect check digits are rejected
- [ ] Valid IBANs continue to be accepted
- [ ] All tests green
```

### Example 4: Batch Task

```
/ralph-loop max=20 Add type hints to all functions in src/utils/.

Requirements:
1. All public functions in src/utils/*.py need complete type hints
2. Annotate both parameters AND return types
3. mypy src/utils/ must run without errors

Verification after each iteration:
- mypy src/utils/ --ignore-missing-imports
- pytest -q --tb=short

Done when:
- [ ] All public functions in utils/ annotated
- [ ] mypy reports no errors
- [ ] Existing tests still green
```

## Anti-Patterns

| Avoid | Why | Better |
|-------|-----|--------|
| Vague goals | Claude doesn't know when it's done | Concrete checklist |
| No verification step | No progress check possible | Include `pytest`, `ruff`, etc. |
| Scope too large | Drift, context loss after many iterations | Split into phases |
| Design decisions left open | Claude guesses, you want something different | Make decisions in the prompt |
| max too high | Costs explode | max=10-20 for most tasks |

## Rule of Thumb

> If you could hand the task to a junior developer and they could complete it without asking questions — then the prompt is good for Ralph.
