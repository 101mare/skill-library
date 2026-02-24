---
name: session-verify
description: |
  End-of-session verification skill that validates all changes made during a coding session.
  Checks for bugs, security vulnerabilities, dead code, efficiency issues, and documentation gaps.
  Use when: finishing a task, before committing, user says "verify", "check my changes",
  "review session", "are we done?", "everything correct?", or at end of coding sessions.
  Orchestrates specialized review agents and ensures documentation is updated.
---

# Session Verification

Comprehensive end-of-session review to ensure code quality and completeness.

## Workflow Overview

```
1. Clarify Requirements → 2. Identify Changes → 3. Load Agent Prompts → 4. Run Reviews → 5. Verify Requirements → 6. User Confirmation → 7. Update Docs
```

## Agent Loading (CRITICAL)

This workflow uses custom agent definitions in `.claude/agents/*.md`. Since the Task tool only supports
`general` and `explore` subagent types, you MUST load agent expertise by **reading their .md files**
and including the system prompt content in the Task prompt.

### How to Use Custom Agents

1. **Read the agent file** with the Read tool: `.claude/agents/{agent-name}.md`
2. **Extract the system prompt** (everything after the YAML frontmatter `---`)
3. **Pass it as context** in the Task tool prompt, prefixed with the role instruction

### Example

```
# Step 1: Read the agent file
Read(".claude/agents/reviewer.md")

# Step 2: Use its content in a Task call
Task(
  subagent_type="general",
  prompt="""
  You are acting as the reviewer agent. Follow these instructions:

  <agent-instructions>
  [paste the system prompt content from the .md file here]
  </agent-instructions>

  Now review these files: [file list]
  Original requirement: [requirement]
  """
)
```

### Available Agent Files

| Agent File | Use For |
|------------|---------|
| `.claude/agents/reviewer.md` | Security, types, logging, privacy, best practices |
| `.claude/agents/analyzer.md` | Architecture, performance, scalability, dead code, dependencies |
| `.claude/agents/code-simplifier.md` | Code clarity, simplification, maintainability |
| `.claude/agents/test-architect.md` | Test creation, test quality review |

**IMPORTANT**: Always use `subagent_type="general"` for agents that need write access (code-simplifier, test-architect)
and `subagent_type="explore"` for read-only review agents (reviewer, analyzer).

## Step 1: Clarify the Original Requirements

First, understand what was supposed to be accomplished:

```
Use AskUserQuestion:
Question: "What was the original task/requirement for this session?"
Options:
  - "Bug fix" → Ask: which bug?
  - "New feature" → Ask: what feature?
  - "Refactoring" → Ask: what was refactored?
  - "Other" → Free text input
```

Follow-up questions to clarify:
- What problem should be solved?
- What behavior is expected?
- Are there edge cases to consider?
- Any specific constraints mentioned?

## Step 2: Identify Changed Files

Use **conversation context** and **git** to find what was modified:

1. **Scan the conversation** for:
   - Files read with `Read` tool
   - Files edited with `Edit` tool
   - Files created with `Write` tool
   - Bash commands that modified files

2. **Supplementary check via git** (if available):
   ```bash
   git diff --name-only HEAD~5 2>/dev/null || git diff --name-only 2>/dev/null || echo "No git available"
   git status --short 2>/dev/null
   ```

3. **Fallback** (if no git and context unclear):
   ```bash
   find src tests -type f -name "*.py" -mmin -120 2>/dev/null | head -30
   ```

4. **Create change summary**:
   ```markdown
   ## Identified Changes
   - Modified: src/llm/service.py (added function X)
   - Created: src/extractors/new_format.py
   - Modified: tests/test_service.py (added tests)
   ```

## Step 3: Run Parallel Reviews

First **read the relevant agent .md files**, then spawn `general`/`explore` agents **in parallel** (single message, multiple Task calls), injecting each agent's system prompt into the Task prompt.

### Agent Selection Matrix

| Change Type | Agent File to Load | subagent_type |
|-------------|-------------------|---------------|
| Any Python code | `reviewer.md` | `explore` |
| Any Python code | `code-simplifier.md` | `general` |
| New functions without tests | `test-architect.md` | `general` |
| Performance / architecture / dependencies | `analyzer.md` | `explore` |

### Core Review Agents (Always Run for Code Changes)

1. **`reviewer`** - Security, types, logging, privacy, best practices
2. **`code-simplifier`** - Clean up, simplify, ensure maintainability

### Execution Steps

1. **Read agent files** (parallel Read calls):
   ```
   Read(".claude/agents/reviewer.md")
   Read(".claude/agents/code-simplifier.md")
   # + any situational agents (analyzer.md, test-architect.md)
   ```

2. **Spawn Task agents in parallel** (single message, multiple Task calls):
   ```
   Task(
     subagent_type="explore",
     prompt="""You are acting as the reviewer agent.

     <agent-instructions>
     [content from reviewer.md after frontmatter]
     </agent-instructions>

     Review these files modified this session:
     [list files with specific functions/classes changed]

     Original requirement: [what user wanted]

     Focus on: security, types, best practices, bugs, logic errors.
     Return findings organized by severity: CRITICAL > HIGH > MEDIUM > LOW.
     """
   )

   Task(
     subagent_type="general",
     prompt="""You are acting as the code-simplifier agent.

     <agent-instructions>
     [content from code-simplifier.md after frontmatter]
     </agent-instructions>

     Review these files modified this session:
     [list files with specific functions/classes changed]

     Original requirement: [what user wanted]

     Focus on: clarity, maintainability, dead code, simplification opportunities.
     Return findings organized by severity: CRITICAL > HIGH > MEDIUM > LOW.
     """
   )
   ```

3. **Aggregate results** from all agents and proceed to Step 4.

## Step 4: Verify Requirements Fulfilled

After reviews complete, check requirement satisfaction:

### Requirements Checklist

Ask yourself (or the agents):
- [ ] Does the implementation match what was requested?
- [ ] Are all mentioned edge cases handled?
- [ ] Does it work with the existing architecture?
- [ ] Are error cases handled appropriately?

### Code Quality Checklist

- [ ] No TODO/FIXME left unaddressed
- [ ] No commented-out code blocks
- [ ] No debug print statements
- [ ] No hardcoded secrets/paths
- [ ] Clean imports (no unused)

### Security Checklist

- [ ] Path traversal protection (symlinks blocked)
- [ ] Subprocess uses list args (no shell=True)
- [ ] Resource limits enforced
- [ ] No mutable default arguments
- [ ] PII redaction where applicable

## Step 5: Present Findings & Get Confirmation

Summarize findings clearly:

```markdown
## Verification Results

### Requirement
[Original requirement restated]

### Fulfilled?
Yes / Partially / No

### Review Results

**Passed**
- Security: No vulnerabilities found
- Code style: Consistent

**Warnings**
- Missing test for `new_function()`
- Nested condition could be simplified

**Issues**
- Unused import in module.py
- Mutable default argument found
```

Then ask user:

```
Use AskUserQuestion:
Question: "Are you satisfied with the changes?"
Options:
  - "Yes, all good" → Proceed to docs
  - "No, please fix" → Fix issues first
  - "Show details" → Expand on specific findings
```

## Step 6: Update Documentation

If satisfied AND significant changes:

### What Needs Updating?

| Change Type | Documentation |
|-------------|---------------|
| New feature | README.md + CLAUDE.md |
| New module/class | CLAUDE.md (Architecture) |
| New config option | CLAUDE.md + config.yaml |
| Workaround discovered | .claude/memory.md |
| Architecture decision | .claude/memory.md |

### Ask Before Updating

```
Use AskUserQuestion:
Question: "Should the documentation be updated?"
Options:
  - "Yes, README + CLAUDE.md"
  - "Only CLAUDE.md"
  - "Only memory.md"
  - "No docs needed"
```

### Documentation Guidelines

**README.md**: User-facing changes (CLI, features, behavior)
**CLAUDE.md**: Developer context (architecture, patterns, config)
**memory.md**: Session-specific decisions, workarounds, patterns discovered

## Quick Mode (Small Changes)

For minor fixes, abbreviated flow:

1. "What was changed?" (1 question)
2. Read the changed file(s)
3. Quick security + logic check
4. "Looks good?" (confirmation)
5. Done (skip docs for trivial fixes)

## Triggers

Activates on:
- `/session-verify`
- "verify", "verification", "check"
- "check changes", "review session"
- "are we done?", "everything correct?"
- "final check", "final review"
- "end session", "wrap up"

## Important Notes

- **Agent loading**: ALWAYS read `.claude/agents/*.md` files and inject their prompts into `general`/`explore` Task agents
- **Parallel agents**: Spawn multiple reviews simultaneously (single message, multiple Task calls)
- **Match language**: Use German if user speaks German, English if user speaks English
- **Prioritize**: Don't overwhelm - focus on critical issues first
- **Context-aware**: Use the full conversation to understand what changed
- **Git-aware**: Use git diff/status when available, fall back to conversation context and file timestamps when not
