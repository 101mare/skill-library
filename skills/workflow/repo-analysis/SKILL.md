---
name: repo-analysis
description: |
  Scans a repository for inconsistencies, anti-patterns, and optimization opportunities.
  Checks naming conventions, file structure, code style coherence, dead patterns, documentation gaps,
  dependency health, and configuration drift. Reports findings as suggestions, not mandates.
  Adapts language to match user input.
  Triggers: "check repo", "repo inconsistencies", "repo health", "analyze repository",
  "optimization suggestions", "code consistency check", "repo audit", "codebase review",
  "find inconsistencies", "was kann verbessert werden", "Repository prüfen"
user-invocable: true
---

# Repo Analysis

Scan a repository for inconsistencies, anti-patterns, and actionable optimization suggestions.
All findings are **suggestions, not mandates** -- the developer decides what to act on.

## Language Adaptation

Match the user's language:
- German input -> German output
- English input -> English output

## Workflow Overview

```
1. Scope -> 2. Structure Scan -> 3. Parallel Deep Analysis -> 4. Aggregate -> 5. Report
```

## Step 1: Determine Scope

Use `AskUserQuestion` to clarify what should be analyzed:

```
Question: "What should I focus on?"
Header: "Scope"
Options:
  - "Full scan (all categories)"
  - "Structure & naming only"
  - "Code patterns & consistency"
  - "Dependencies & config"
multiSelect: false
```

```
Question: "Are there areas I should skip or pay special attention to?"
Header: "Focus"
Options:
  - "No special focus -- scan everything"
  - "Focus on new/recently changed files"
  - "Skip tests/generated files"
multiSelect: false
```

## Step 2: Structure Scan

Before deep analysis, build a mental map of the repository:

### 2.1 Read Project Context

```
Read CLAUDE.md (if exists) -> understand conventions
Read README.md -> understand purpose and setup
Read package.json / pyproject.toml / Cargo.toml / go.mod -> understand tech stack
Read .editorconfig / .prettierrc / eslint config / ruff config -> understand style rules
```

### 2.2 Map Directory Structure

```bash
# Get directory tree (depth 3)
find . -type f -not -path './.git/*' -not -path './node_modules/*' -not -path './.venv/*' | head -200
```

Note: Adapt exclusions to project type (node_modules, .venv, target, build, dist, etc.)

### 2.3 Quick Pattern Scan

Identify the dominant conventions before looking for deviations:

| Signal | What to Look For |
|--------|-----------------|
| Naming | camelCase vs snake_case vs kebab-case in files and directories |
| Exports | Default exports vs named exports (JS/TS) |
| Imports | Relative vs absolute, ordering conventions |
| Config | Env vars vs config files vs hardcoded values |
| Error handling | Try/catch style, custom exceptions, error types |
| Test placement | Co-located vs separate `tests/` directory |

## Step 3: Parallel Deep Analysis

Spawn **3-4 Task agents in parallel** (single message, multiple Task calls) using `subagent_type="Explore"`.

Each agent receives the project context from Step 2 and a focused analysis mandate.

### Agent 1: Structure & Naming Consistency

```
Analyze the repository for structural and naming inconsistencies:

<project-context>
[Project context from Step 2]
</project-context>

Check:
1. **File naming**: Are all files following one convention? Mixed camelCase/snake_case/kebab-case?
2. **Directory naming**: Consistent casing and pluralization? (utils vs helpers, models vs model)
3. **Module organization**: Similar concerns grouped together? Orphaned files?
4. **Index/barrel files**: Used consistently or sporadically?
5. **Test file naming**: Consistent pattern? (*.test.ts vs *.spec.ts vs test_*.py)
6. **Config file placement**: Root level vs config directory? Consistent?

For each finding, report:
- Location (file or pattern)
- What the dominant convention is
- What deviates from it
- Severity: INCONSISTENCY (breaks pattern) | DRIFT (minor deviation) | SUGGESTION (could be cleaner)
```

### Agent 2: Code Pattern Consistency

```
Analyze the repository for code-level pattern inconsistencies:

<project-context>
[Project context from Step 2]
</project-context>

Check:
1. **Error handling**: Mixed patterns? (try/catch vs .catch vs Result types, bare except vs specific)
2. **Async patterns**: Mixed callbacks/promises/async-await? Inconsistent error propagation?
3. **Import style**: Mixed relative/absolute? Inconsistent ordering? Unused imports?
4. **Type usage**: Mixed typed/untyped? Inconsistent type annotation coverage?
5. **Logging**: Mixed console.log/logger? Inconsistent log levels? Missing structured logging?
6. **Constants**: Hardcoded values that should be constants? Mixed UPPER_CASE/regular naming?
7. **Function signatures**: Mixed return styles? Inconsistent parameter patterns?
8. **Comments/docs**: Some files documented, others not? Stale comments? TODO/FIXME/HACK markers?

For each finding, report:
- Example locations (file:line)
- The two (or more) conflicting patterns
- Which pattern dominates
- Severity: INCONSISTENCY | DRIFT | SUGGESTION
```

### Agent 3: Dependencies & Configuration

```
Analyze the repository for dependency and configuration issues:

<project-context>
[Project context from Step 2]
</project-context>

Check:
1. **Unused dependencies**: Packages in manifest but never imported?
2. **Duplicate functionality**: Multiple packages doing the same thing? (e.g., axios + fetch, lodash + ramda)
3. **Version pinning**: Inconsistent pinning strategy? (exact vs range vs unpinned)
4. **Dev vs prod separation**: Test/build tools in production dependencies?
5. **Config drift**: Environment-specific configs that have diverged? Missing env vars?
6. **Scripts**: Package scripts that are outdated, broken, or redundant?
7. **Lockfile health**: Lockfile present and committed? Matches manifest?
8. **Deprecated packages**: Dependencies with known deprecations?

For each finding, report:
- The specific package or config
- Why it's an issue
- Severity: ISSUE (should fix) | DRIFT (minor) | SUGGESTION (nice-to-have)
```

### Agent 4: Documentation & DX (optional, for full scan)

```
Analyze the repository for documentation and developer experience gaps:

<project-context>
[Project context from Step 2]
</project-context>

Check:
1. **README completeness**: Setup instructions? Usage examples? Contributing guide?
2. **API documentation**: Public interfaces documented? Return types clear?
3. **Stale docs**: Documentation that contradicts current code?
4. **Missing .env.example**: Env vars used but no template?
5. **Missing CI config**: Tests exist but no CI? Linting locally but not in CI?
6. **Git hygiene**: .gitignore complete? Sensitive files tracked? Large binaries committed?
7. **Editor config**: .editorconfig or equivalent present? Consistent with actual formatting?

For each finding, report:
- What's missing or inconsistent
- Impact on developer experience
- Severity: GAP (missing) | STALE (outdated) | SUGGESTION (improvement)
```

## Step 4: Aggregate Results

Collect all agent results and deduplicate. Group findings into categories:

### Categorization

```markdown
## Repo Analysis Results

### Overview

| Category | Findings | Top Severity |
|----------|----------|-------------|
| Structure & Naming | X findings | ... |
| Code Patterns | X findings | ... |
| Dependencies & Config | X findings | ... |
| Documentation & DX | X findings | ... |
```

### Deduplication Rules

- If multiple agents flag the same file/pattern, merge into one finding
- Prefer the most specific description
- Keep the highest severity

## Step 5: Present Report

### Report Format

```markdown
## Repository Health Report

### Quick Summary

One-paragraph assessment of overall repository health.

### Inconsistencies Found

Items where the codebase contradicts its own patterns.

| # | Category | Finding | Location | Dominant Pattern | Deviation |
|---|----------|---------|----------|-----------------|-----------|
| 1 | Naming | Mixed file casing | src/Utils.ts, src/helpers.ts | kebab-case | 3 files use camelCase |
| ... | | | | | |

### Optimization Suggestions

Optional improvements that could make the codebase cleaner.

| # | Category | Suggestion | Impact | Effort |
|---|----------|-----------|--------|--------|
| 1 | DX | Add .env.example | Faster onboarding | Low |
| ... | | | | |

### What's Working Well

Patterns the codebase follows consistently (positive reinforcement).

- Consistent test placement in __tests__/ directories
- Clean import ordering throughout
- ...

### Recommended Actions (Priority Order)

1. **Quick wins**: [Low effort, high impact items]
2. **Worth addressing**: [Medium effort items]
3. **Nice to have**: [When time permits]
```

### Tone Guidelines

- **Constructive, not critical**: "3 files use camelCase while the rest use kebab-case" not "Inconsistent mess"
- **Acknowledge good patterns**: Always include a "What's working well" section
- **Suggest, don't demand**: Use "consider", "could", "might benefit from" -- never "must", "should", "needs to"
- **Explain impact**: Why does this matter? (readability, onboarding, bugs, maintenance)
- **Estimate effort**: Low / Medium / High so the developer can prioritize

### User Decision

```
Use AskUserQuestion:
Question: "How would you like to proceed?"
Header: "Next"
Options:
  - "Deep-dive into a specific finding"
  - "Fix the quick wins now"
  - "Export report as markdown file"
  - "Done, thanks"
```

## Important Notes

- **Non-prescriptive**: Every finding is a suggestion. The developer decides what to act on.
- **Project-aware**: Always read CLAUDE.md and project config first. What looks like an inconsistency might be intentional.
- **Positive framing**: Lead with what's working, then show what could improve.
- **Parallelization**: Run analysis agents simultaneously (one message, multiple Task calls).
- **Match language**: Use the language the user speaks.
- **Adapt to stack**: Python projects get different checks than Node.js or Rust projects. Read the manifest files and adjust.
- **Skip generated code**: Don't flag auto-generated files, lockfiles, or build output.
- **Respect .gitignore**: Only analyze tracked/trackable files.
