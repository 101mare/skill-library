---
name: pr-review
description: |
  Orchestrates pull request reviews using specialized agents in parallel.
  Reads PR diff, selects relevant reviewers, aggregates findings.
  Use when reviewing PRs, before merging, or when user asks "review this PR".
  Recognizes: "pr-review", "review PR", "review pull request", "check this PR",
  "PR review", "code review", "merge review", "review before merge"
---

# PR Review

Comprehensive pull request review using specialized agents in parallel.

## Workflow Overview

```
1. Get PR Diff -> 2. Analyze Changes -> 3. Select Agents -> 4. Parallel Reviews -> 5. Aggregate -> 6. Verdict
```

## Step 1: Get PR Diff

```bash
# Get PR information
gh pr view <PR_NUMBER> --json title,body,files,additions,deletions

# Get full diff
gh pr diff <PR_NUMBER>

# Get changed files list
gh pr view <PR_NUMBER> --json files --jq '.files[].path'
```

## Step 2: Analyze Changes

Categorize changed files:

| File Pattern | Category | Relevant Agent |
|-------------|----------|----------------|
| `*.py` (src/) | Python code | reviewer |
| `*.py` (tests/) | Tests | test-architect |
| `requirements*.txt`, `pyproject.toml` | Dependencies | analyzer |
| `Dockerfile`, `docker-compose*` | Infrastructure | (manual review) |
| `*.md` | Documentation | (manual review) |
| `*.html`, `*.css`, `*.js` | Frontend | (manual review) |

## Step 3: Select Agents

Based on changed file categories, select agents:

### Always Run (for code changes)
- **reviewer** -- Security, types, logging, privacy, best practices

### Conditional
| Condition | Agent |
|-----------|-------|
| New dependencies / performance-sensitive code / architecture changes | analyzer |
| Tests added/modified | test-architect |

## Step 4: Parallel Reviews

### Agent Loading

Read the relevant `.claude/agents/*.md` files, then spawn explore agents in parallel:

```
# Step 1: Read agent files (parallel)
Read(".claude/agents/reviewer.md")
Read(".claude/agents/analyzer.md")
# + any situational agents (test-architect.md)

# Step 2: Spawn agents in parallel (single message, multiple Task calls)
Task(
  subagent_type="explore",
  prompt="""You are acting as the reviewer agent.

  <agent-instructions>
  [content from reviewer.md]
  </agent-instructions>

  Review this PR diff:

  <diff>
  [PR diff content]
  </diff>

  PR Title: [title]
  PR Description: [description]

  Focus on: security, types, logging, privacy, best practices, bugs, logic errors.
  Return findings by severity: CRITICAL > HIGH > MEDIUM > LOW.
  Reference specific file paths and line numbers from the diff.
  """
)
```

## Step 5: Aggregate Findings

Collect all agent results and organize:

```markdown
## PR Review: [PR Title] (#[number])

### Summary
- Files changed: X
- Additions: +Y / Deletions: -Z
- Agents run: [list]

---

### CRITICAL (Must Fix Before Merge)
1. [Finding + agent source + file:line]

### HIGH (Should Fix)
1. [Finding + agent source + file:line]

### MEDIUM (Recommended)
1. [Finding + agent source + file:line]

### LOW (Suggestions)
1. [Finding]

### Positive Observations
- [What's good about this PR]
```

## Step 6: Verdict

| Condition | Verdict |
|-----------|---------|
| Any CRITICAL finding | REQUEST CHANGES |
| 2+ HIGH findings | REQUEST CHANGES |
| Only MEDIUM/LOW | APPROVE with comments |
| No findings | APPROVE |

```markdown
### Verdict: [APPROVE / REQUEST CHANGES / COMMENT]

**Reason:** [Brief explanation]

**Required before merge:**
1. [Action item if any]

**Suggestions (non-blocking):**
1. [Optional improvement]
```

## Posting Review

```bash
# Post review comment
gh pr review <PR_NUMBER> --comment --body "$(cat <<'EOF'
## PR Review

[Aggregated findings here]
EOF
)"

# Or request changes
gh pr review <PR_NUMBER> --request-changes --body "..."

# Or approve
gh pr review <PR_NUMBER> --approve --body "..."
```

## Important Notes

- **Agent loading**: Always read `.claude/agents/*.md` files and inject their prompts into explore Task agents
- **Parallelization**: Spawn all review agents simultaneously
- **Match language**: Use the language the user speaks
- **Constructive**: Don't just list problems -- suggest fixes
- **Prioritize**: Focus on CRITICAL/HIGH first
- **Context**: Read CLAUDE.md for project-specific patterns before reviewing
