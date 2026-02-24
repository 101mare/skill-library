---
name: systematic-debugging
description: |
  Structured 4-phase debugging: Reproduce, Isolate, Root-Cause, Fix+Defend.
  Use when tracking bugs, diagnosing failures, or investigating unexpected behavior.
  Recognizes: "systematic-debugging", "debug this", "why does this fail",
  "find the bug", "track down", "root cause", "investigate error",
  "unexpected behavior", "it works sometimes", "flaky test"
---

# Systematic Debugging

Four-phase methodology to find and fix bugs without guessing. Every phase has a clear goal and exit criterion.

## The Four Phases

```
1. REPRODUCE  →  2. ISOLATE  →  3. ROOT-CAUSE  →  4. FIX + DEFEND
   "See it"       "Shrink it"     "Understand it"    "Kill it forever"
```

---

## Phase 1: Reproduce

**Goal:** See the bug happen reliably. If you can't reproduce it, you can't verify the fix.

### Steps

1. **Get the exact error** — full traceback, log output, or observed vs. expected behavior
2. **Reproduce locally** — same input, same config, same environment
3. **Make it deterministic** — if intermittent, find the trigger condition

### Techniques

```python
# Capture exact state for reproduction
import logging
logger = logging.getLogger(__name__)

def process_case(case_dir: Path, config: PipelineConfig) -> CaseResult:
    logger.debug("Processing", extra={
        "case_id": case_dir.name,
        "file_count": len(list(case_dir.iterdir())),
        "provider": config.provider.type,
    })
    # ...
```

```bash
# Reproduce with same config
python main.py --case case_042 --config config.yaml

# Check environment differences
python -c "import sys; print(sys.version)"
pip freeze | diff - requirements.txt
```

### Checklist

- [ ] Can reproduce the bug on demand
- [ ] Have exact error message / traceback
- [ ] Know the minimal input that triggers it
- [ ] Noted: environment, config, Python version

### Exit Criterion

You can make the bug appear at will with a specific command or test.

---

## Phase 2: Isolate

**Goal:** Shrink the problem space. Find the smallest code path that still shows the bug.

### Techniques

**Binary Search in Code:**

```python
# Add checkpoints to narrow down where it breaks
def pipeline(case_dir):
    files = discover_files(case_dir)
    logger.info(f"CHECKPOINT 1: {len(files)} files discovered")  # OK here?

    extracted = extract_all(files)
    logger.info(f"CHECKPOINT 2: {len(extracted)} extractions done")  # OK here?

    context = build_context(extracted)
    logger.info(f"CHECKPOINT 3: context length {len(context)}")  # OK here?

    result = classify(context)  # Bug is between last OK and first FAIL
    logger.info(f"CHECKPOINT 4: result={result.ca_type}")
```

**Minimal Reproduction:**

```python
# Strip away everything until the bug disappears, then add back the last thing
def test_minimal_reproduction():
    # Start with full case, remove files one by one
    # until bug disappears. The last removed file is the trigger.
    result = classify("just the text from file_3.pdf")
    assert result.ca_type != "UNKNOWN"  # This fails → bug is in this text
```

**Git Bisect (for regressions):**

```bash
git bisect start
git bisect bad              # Current commit has the bug
git bisect good abc123      # This commit was clean
# Git checks out middle commits. Test each:
git bisect good  # or  git bisect bad
# Repeat until git identifies the breaking commit
git bisect reset
```

### Checklist

- [ ] Narrowed to specific function or module
- [ ] Know which input triggers it (and which doesn't)
- [ ] Eliminated unrelated code paths

### Exit Criterion

You can point to a specific function or code block (< 50 lines) where the bug lives.

---

## Phase 3: Root-Cause

**Goal:** Understand WHY it fails, not just WHERE. The "5 Whys" technique.

### The 5 Whys

```
Bug: classify() returns "UNKNOWN" for valid tax documents.

Why 1: The LLM response JSON has ca_type = "UNKNOWN"
Why 2: The prompt doesn't include the extracted text
Why 3: context_builder returns empty string
Why 4: All extracted files have empty text
Why 5: PdfExtractor silently catches OCR timeout and returns ""
       ← ROOT CAUSE: silent exception swallowing
```

### Read the Code, Don't Guess

```python
# BAD: "I think the problem might be..."
# GOOD: Read the actual code path

# 1. Read the function
def extract_pdf(path: Path, vision: VisionEngine) -> str:
    pages = convert_to_images(path)
    texts = []
    for page in pages:
        try:
            text = vision.ocr(page)
            texts.append(text)
        except Exception:        # ← HERE: catches everything silently
            pass                  # ← HERE: returns empty, no logging
    return "\n".join(texts)

# Root cause: broad except + silent pass = lost errors
```

### Debugging Tools

**pdb / breakpoint():**

```python
def classify(text: str) -> CaseResult:
    prompt = build_prompt(text)
    breakpoint()  # Drops into interactive debugger
    # inspect: print(prompt), print(len(text)), check variables
    response = client.complete(prompt)
    return parse_response(response)
```

```
# In debugger:
(Pdb) p len(text)       # Check text length
(Pdb) p prompt[:200]    # Check prompt content
(Pdb) n                 # Next line
(Pdb) c                 # Continue execution
(Pdb) pp vars()         # Pretty-print all local variables
```

**Targeted Logging:**

```python
# Add temporary DEBUG logging around the suspect area
logger.debug("Before classify", extra={
    "text_length": len(text),
    "prompt_length": len(prompt),
    "has_entities": bool(entities),
})

result = client.complete(prompt)

logger.debug("After classify", extra={
    "response_length": len(result.text),
    "response_preview": result.text[:100],  # OK for debugging, remove after
})
```

**Type Inspection:**

```python
# When "it should work but doesn't" — check types
print(type(value))              # str? bytes? None?
print(repr(value))              # See invisible characters, encoding
print(value == expected)        # Equality check
print(value is expected)        # Identity check (for None, singletons)
```

### Common Root Causes

| Symptom | Likely Root Cause |
|---------|-------------------|
| Works locally, fails in Docker | Path differences, missing env vars, file permissions |
| Works for some inputs | Input-dependent branch, encoding issues, edge case |
| Intermittent failures | Race condition, timeout, external dependency |
| Returns None / empty | Silent exception, early return, wrong branch |
| Wrong type at runtime | Missing validation, implicit conversion, mock leaking |
| "It used to work" | Regression: dependency update, config change, data change |

**Tip:** If the root cause involves unfamiliar library behavior or system internals, use the `deep-research` skill to investigate before guessing.

### Checklist

- [ ] Can explain WHY the bug happens (not just where)
- [ ] Identified the root cause (not a symptom)
- [ ] Applied "5 Whys" to dig past surface issues

### Exit Criterion

You can explain the bug's cause to someone else in one sentence, and they'd agree it explains the symptoms.

---

## Phase 4: Fix + Defend

**Goal:** Fix the bug AND prevent it from returning.

### The Fix

```python
# 1. Write a failing test FIRST (proves the bug exists)
def test_pdf_extractor_logs_ocr_timeout():
    vision = MagicMock(spec=VisionEngine)
    vision.ocr.side_effect = ModelTimeoutError("timeout")

    with pytest.raises(ModelTimeoutError):
        extract_pdf(Path("test.pdf"), vision)

# 2. Fix the code
def extract_pdf(path: Path, vision: VisionEngine) -> str:
    pages = convert_to_images(path)
    texts = []
    for page in pages:
        try:
            text = vision.ocr(page)
            texts.append(text)
        except VisionConnectionError as e:
            logger.warning("OCR failed for page", extra={
                "file_name": path.name,
                "error": str(e),
            })
            # Continue with other pages — graceful degradation
        # No broad except — let unexpected errors propagate
    return "\n".join(texts)

# 3. Run the test — it passes now
# 4. Run ALL tests — nothing else broke
```

### Defend Against Recurrence

```python
# Add a regression test with the exact input that triggered the bug
def test_regression_case_042_empty_pdf():
    """Regression: case_042 had a PDF that caused OCR timeout,
    resulting in empty classification. Fixed in commit abc123."""
    result = extract_pdf(empty_pdf_path, mock_vision_with_timeout)
    # Should gracefully degrade, not silently return empty
    assert "OCR failed" in caplog.text or len(result) > 0
```

### Fix Verification

```bash
# 1. Tests pass
pytest -q --tb=line

# 2. Original reproduction case works
python main.py --case case_042

# 3. No new warnings in logs
grep -i "error\|warning" logs/$(date +%Y-%m-%d).log
```

### Checklist

- [ ] Failing test written BEFORE the fix
- [ ] Fix addresses root cause (not symptom)
- [ ] Test passes after fix
- [ ] All other tests still pass
- [ ] Regression test added for the specific trigger
- [ ] No broad `except` introduced

### Exit Criterion

The bug is fixed, tests prove it, and a regression test guards against recurrence.

---

## Debugging Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| "Shotgun debugging" — change random things | Introduces new bugs, wastes time | Follow the 4 phases sequentially |
| `except: pass` | Hides the real error | Catch specific exceptions, always log |
| print() scattered everywhere | Noisy, forgotten in production | Use logger.debug with structured extra |
| "It works on my machine" | Environment blindness | Reproduce in the target environment |
| Fixing the symptom | Bug returns in different form | Apply "5 Whys" to find root cause |
| Skipping reproduction | Can't verify the fix | Always reproduce before fixing |
| No regression test | Bug comes back next refactor | Write a test with the exact trigger |
| Debugging in production | Risky, stressful | Reproduce locally with production data/config |

## Quick Reference

```
BUG REPORTED
    │
    ▼
┌──────────────┐     Can't reproduce?
│ 1. REPRODUCE │────────────────────────→ Get more info (logs, config, input)
│   "See it"   │
└──────┬───────┘
       │ Reproducible
       ▼
┌──────────────┐     Still too broad?
│ 2. ISOLATE   │────────────────────────→ Binary search, remove components
│  "Shrink it" │
└──────┬───────┘
       │ Narrowed to ~50 lines
       ▼
┌──────────────┐     Can't explain why?
│ 3. ROOT-CAUSE│────────────────────────→ 5 Whys, read code, use debugger
│"Understand it"│
└──────┬───────┘
       │ Root cause known
       ▼
┌──────────────┐
│ 4. FIX+DEFEND│────→ Test first → Fix → Verify → Regression test
│ "Kill it"    │
└──────────────┘
```
