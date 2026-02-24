# Architecture Fit

### Analysis Process

#### Step 1: Understand Current Architecture

Read project documentation first:

```markdown
Priority reading order:
1. CLAUDE.md - Architecture overview, patterns, conventions
2. README.md - High-level structure
3. .claude/memory.md - Recent decisions, patterns

Key sections to extract:
- Directory structure
- Module responsibilities
- Import conventions
- Design patterns used
- Security requirements
```

#### Step 2: Map Plan to Architecture

For each planned change:

```markdown
| Plan Element | Target Location | Current Pattern | Fit? |
|--------------|-----------------|-----------------|------|
| New extractor | src/extractors/ | Registry pattern | FITS |
| New config | src/shared/config.py | Pydantic models | FITS |
| New API call | src/llm/service.py | Direct in service | ? CHECK |
```

#### Step 3: Check Integration Points

Verify integration compatibility:

```markdown
## Integration Points Analysis

### Imports
- [ ] Uses package-qualified imports from src/ root
- [ ] Within-package uses relative imports
- [ ] No circular import risks

### Dependencies
- [ ] Uses existing utilities (not reinventing)
- [ ] Follows dependency injection patterns
- [ ] Protocol-based interfaces where applicable

### Data Flow
- [ ] Uses existing DTOs (models.py)
- [ ] Follows error handling patterns
- [ ] Respects resource limits
```

### Architecture Patterns to Verify

#### Module Placement

```markdown
## Module Placement Check

| New Code | Proposed Location | Correct Location | Status |
|----------|-------------------|------------------|--------|
| New extractor | src/extractors/ | src/extractors/ | FITS |
| Helper function | src/llm/utils.py | src/shared/utils.py | DEVIATION |
| Config model | inline | src/shared/config.py | CONFLICT |
```

#### Import Conventions

Per CLAUDE.md:
```python
# From src/ modules - package-qualified
from shared.config import PipelineConfig
from core.pipeline import run_all_cases

# Within a package - relative imports
from .case_runner import run_case
from .models import ExtractedFile
```

Check plan for:
- [ ] Correct import style specified
- [ ] No absolute imports within packages
- [ ] No relative imports across packages

#### Design Patterns

```markdown
## Pattern Compliance

| Pattern | Where Used | Plan Follows? |
|---------|------------|---------------|
| Strategy + Registry | Extractors | ?/? |
| Protocol-based DI | Integrations | ?/? |
| Context Managers | Resource cleanup | ?/? |
| DTOs over dicts | Data transfer | ?/? |
```

#### Error Handling

Per architecture:
```markdown
Check plan includes:
- [ ] Specific exception types (not bare except)
- [ ] Logging before re-raise
- [ ] Graceful degradation where appropriate
- [ ] Retry for transient failures (external calls)
```

#### Security Requirements

Per CLAUDE.md security patterns:
```markdown
- [ ] Path traversal protection (if file handling)
- [ ] Filename sanitization (if user input)
- [ ] Resource limits enforced
- [ ] Subprocess uses list args (no shell=True)
- [ ] No mutable default arguments
- [ ] PII redaction in logs (if private mode)
```

### Common Architecture Violations

#### Anti-Pattern: Utility Sprawl

```markdown
CONFLICT:
Plan: "Create src/llm/helpers.py for small utilities"
Issue: Utilities belong in src/shared/utils.py
Fix: Add to existing utils.py or create focused module
```

#### Anti-Pattern: Raw Dictionaries

```markdown
CONFLICT:
Plan: "Return {'status': 'ok', 'data': ...}"
Issue: System uses typed dataclasses (DTOs)
Fix: Create dataclass in models.py
```

#### Anti-Pattern: Inline Configuration

```markdown
CONFLICT:
Plan: "Add MAX_RETRIES = 5 constant in service.py"
Issue: Config belongs in config.yaml + config.py
Fix: Add to LimitsConfig with Field(default=5)
```

#### Anti-Pattern: Direct External Calls

```markdown
DEVIATION:
Plan: "Call requests.get() directly in new module"
Issue: No resilience (retry, timeout)
Fix: Use retry_with_backoff() wrapper
```

### Output Format

```markdown
## Architecture Fit Analysis

### Project Architecture Summary
- **Pattern**: [Main architectural pattern]
- **Key Conventions**: [Import style, module structure]
- **Critical Constraints**: [Security, privacy, etc.]

---

### Fit Analysis by Plan Element

#### FITS Architecture

| Element | Location | Pattern | Notes |
|---------|----------|---------|-------|
| New extractor | src/extractors/x.py | Registry | Correctly uses BaseExtractor |
| Config addition | config.py | Pydantic | Field with default |

#### DEVIATIONS (Review Needed)

| Element | Plan | Architecture | Recommendation |
|---------|------|--------------|----------------|
| Helper module | src/llm/utils.py | src/shared/utils.py | Move to shared |
| Error handling | Generic Exception | Specific types | Define custom exception |

**Deviation Questions:**
1. Is the deviation intentional? If so, why?
2. Should this become a new pattern?

#### CONFLICTS (Must Fix)

| Element | Plan | Architecture | Required Fix |
|---------|------|--------------|--------------|
| Config | Hardcoded constant | config.yaml | Add to PipelineConfig |
| Data return | Raw dict | Dataclass | Create DTO in models.py |

---

### Integration Risk Assessment

| Integration Point | Risk Level | Concern |
|-------------------|------------|---------|
| Extractor registry | Low | Standard pattern |
| Config loading | Medium | Need migration for existing configs |
| LLM service | High | May affect existing retry logic |

---

### Architecture Recommendations

1. **Move utility to shared**: `helpers.py` -> `shared/utils.py`
2. **Add DTO**: Create `NewResult` dataclass in models.py
3. **Follow retry pattern**: Wrap external calls in `retry_with_backoff()`
4. **Add config field**: Extend `LimitsConfig` instead of constant

---

### Summary

| Category | Count |
|----------|-------|
| FITS | 4 |
| DEVIATIONS | 2 |
| CONFLICTS | 1 |

**Verdict**: MOSTLY FITS - Address 1 conflict and review 2 deviations before proceeding.
```

### Integration Points Analysis

```markdown
### Imports
- [ ] Uses package-qualified imports from src/ root
- [ ] Within-package uses relative imports
- [ ] No circular import risks

### Dependencies
- [ ] Uses existing utilities (not reinventing)
- [ ] Follows dependency injection patterns
- [ ] Protocol-based interfaces where applicable

### Data Flow
- [ ] Uses existing DTOs (models.py)
- [ ] Follows error handling patterns
- [ ] Respects resource limits
```

---
