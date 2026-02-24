# Risk Assessment

### Risk Categories

```markdown
## Risk Categories

### Technical Risks
- Complexity beyond team capability
- Unproven technology/approach
- Performance degradation potential
- Resource exhaustion possible

### Integration Risks
- Breaking existing functionality
- API contract changes
- Data migration needed
- Backwards incompatibility

### Security Risks
- New attack vectors introduced
- Sensitive data exposure
- Authentication/authorization gaps
- Input validation gaps

### Operational Risks
- Deployment complexity
- Rollback difficulty
- Monitoring gaps
- Documentation debt
```

### Breaking Change Analysis

#### API/Interface Changes

| Change | Affected | Impact | Severity |
|--------|----------|--------|----------|
| Function signature | callers | Must update calls | HIGH |
| Return type | consumers | Type errors | HIGH |
| Config field removed | existing configs | Runtime error | BLOCKER |

#### Data Structure Changes

| Change | Affected | Impact | Severity |
|--------|----------|--------|----------|
| Model field added | serialization | New field in output | LOW |
| Model field removed | existing data | Data loss | BLOCKER |
| Field type changed | validation | Parse errors | HIGH |

#### Behavior Changes

| Change | Affected | Impact | Severity |
|--------|----------|--------|----------|
| Default value changed | implicit users | Different behavior | MEDIUM |
| Error handling changed | error consumers | Different exceptions | HIGH |
| Order of operations | dependent code | Race conditions | HIGH |

### Security Risk Checklist

```markdown
## Security Risk Checklist

### Input Handling
- [ ] User input validated? → Risk if not
- [ ] File paths sanitized? → Path traversal risk
- [ ] Filenames cleaned? → Injection risk

### External Calls
- [ ] Subprocess uses list args? → Command injection risk if shell=True
- [ ] Network calls have timeout? → DoS risk
- [ ] Retry logic present? → Reliability risk

### Data Protection
- [ ] PII logged safely? → Privacy violation risk
- [ ] Secrets hardcoded? → Exposure risk
- [ ] Temp files cleaned? → Data leak risk

### Resource Limits
- [ ] File size checked? → Memory exhaustion risk
- [ ] Recursion bounded? → Stack overflow risk
- [ ] Connection pooled? → Resource leak risk
```

### Complexity Assessment

#### Code Complexity

| Factor | Level | Concern |
|--------|-------|---------|
| New modules | X | More to maintain |
| New dependencies | X | Supply chain risk |
| Lines of code | ~X | Review burden |
| Cyclomatic complexity | Est. | Testability |

#### Cognitive Complexity

- How many concepts to understand?
- How many files to modify?
- How many edge cases?
- How much existing code to read?

#### Testing Complexity

- Unit tests feasible?
- Integration tests needed?
- Mocking complexity?
- Test data requirements?

### Risk Patterns

#### BLOCKER: Data Loss Risk

```markdown
BLOCKER: Potential Data Loss

Plan: "Remove `legacy_field` from CaseResult model"
Risk: Existing result.json files have this field
Impact: Data lost on re-serialization
Mitigation Required:
1. Migration script to preserve data
2. Deprecation period before removal
3. Or: Keep field as optional
```

#### HIGH: Breaking API Change

```markdown
HIGH: Breaking API Change

Plan: "Change classify_case() to return Optional[Classification]"
Risk: All callers expect Classification (not None)
Impact: Runtime AttributeError when None returned
Affected: case_runner.py:145, pipeline.py:89
Mitigation:
1. Update all call sites first
2. Or: Add default/fallback behavior
```

#### MEDIUM: Performance Degradation

```markdown
MEDIUM: Performance Risk

Plan: "Add validation loop over all extracted entities"
Risk: O(n^2) if nested loops with large entity lists
Impact: Slow processing for large cases
Mitigation:
1. Benchmark with max expected entities
2. Consider early termination
3. Set entity count limit
```

#### LOW: Maintenance Burden

```markdown
LOW: Increased Maintenance

Plan: "Add 3 new configuration options"
Risk: More options = more combinations to test
Impact: Testing matrix grows
Note: Acceptable if options are independent
```

### Feasibility Check

#### Technical Feasibility

```markdown
## Feasibility Analysis

### Can We Build It?
| Requirement | Feasible? | Concern |
|-------------|-----------|---------|
| OCR accuracy >95% | Maybe | Model-dependent |
| <100ms response | No | LLM latency ~2-5s |
| Zero dependencies | No | Requires Ollama |

### Do We Have Resources?
| Resource | Available | Needed | Gap |
|----------|-----------|--------|-----|
| VRAM | 20GB | ~15GB | OK |
| Dev time | ? | ? | Ask |
| Test data | Limited | Comprehensive | Gap |
```

#### Dependency Feasibility

```markdown
### External Dependencies
| Dependency | Status | Risk |
|------------|--------|------|
| Ollama | Required, available | Low |
| New library X | Not evaluated | Medium |
| External API | Not allowed (offline) | BLOCKER |
```

### Risk Assessment Output Format

```markdown
## Implementation Risk Assessment

### Plan Summary
[Brief description of what's being implemented]

---

### Risk Matrix

| Risk | Category | Severity | Likelihood | Impact |
|------|----------|----------|------------|--------|
| Config field removal breaks existing | Breaking Change | BLOCKER | High | Data loss |
| No retry on new API call | Reliability | HIGH | Medium | Failures |
| Complex nested validation | Performance | MEDIUM | Low | Slowdown |
| New config options | Maintenance | LOW | Certain | Testing |

---

### BLOCKERS (Must Resolve)

#### 1. [Risk Title]
- **What**: [Description]
- **Why Blocker**: [Impact if ignored]
- **Resolution Options**:
  1. [Option A]
  2. [Option B]
- **Recommended**: [Which option and why]

---

### HIGH RISKS (Need Mitigation)

#### 1. [Risk Title]
- **What**: [Description]
- **Likelihood**: [Low/Medium/High]
- **Impact**: [What goes wrong]
- **Mitigation**: [How to reduce risk]
- **Fallback**: [If mitigation fails]

---

### MEDIUM RISKS (Should Address)

#### 1. [Risk Title]
- **What**: [Description]
- **Mitigation**: [Suggested approach]

---

### LOW RISKS (Awareness)

- [Risk 1]: [Brief note]
- [Risk 2]: [Brief note]

---

### MITIGATED RISKS

| Risk | Mitigation in Plan |
|------|--------------------|
| [Risk] | [How plan addresses it] |

---

### Feasibility Assessment

| Aspect | Status | Notes |
|--------|--------|-------|
| Technical | ✓ Feasible | Standard patterns |
| Resource | ✓ Feasible | Within VRAM limits |
| Timeline | ? Unknown | Needs estimate |
| Dependencies | Check | New library needed |

---

### Recommendations

1. **BLOCKER Resolution**: [Specific action needed]
2. **Risk Mitigation**: [Add X before Y]
3. **Testing Strategy**: [How to verify safety]
4. **Rollback Plan**: [If things go wrong]

---

### Summary

| Severity | Count |
|----------|-------|
| BLOCKER | 0 |
| HIGH | 2 |
| MEDIUM | 3 |
| LOW | 2 |

**Verdict**: [PROCEED / PROCEED WITH CAUTION / STOP AND RESOLVE]
```

### Risk-Related Questions to Surface

Critical questions to clarify:

```markdown
Risk-related questions:

1. Breaking change found - is backwards compatibility required?
2. New dependency needed - is it approved for use?
3. Performance impact unclear - what's the acceptable latency?
4. Security pattern missing - should we add validation here?
5. Rollback plan absent - what if deployment fails?
6. Test coverage gap - which scenarios must be tested?
```
