# Agent Builder — Technical Reference

All technical details for Claude Code agent configuration. The main [SKILL.md](SKILL.md) covers design philosophy; this file covers the mechanics.

## Table of Contents

- [Frontmatter Fields Reference](#frontmatter-fields-reference)
- [Available Tools](#available-tools)
- [Built-in Subagents](#built-in-subagents)
- [Model Selection Guide](#model-selection-guide)
- [Permission Modes](#permission-modes)
- [Running Modes](#running-modes)
- [Hooks Configuration](#hooks-configuration)
- [Agent Design Patterns](#agent-design-patterns)

---

## Frontmatter Fields Reference

### Required Fields

| Field | Description |
|-------|-------------|
| `name` | Unique identifier, lowercase with hyphens (e.g., `code-reviewer`) |
| `description` | When Claude should delegate. Use multiline `\|` for longer descriptions |

### Optional Fields

| Field | Default | Description |
|-------|---------|-------------|
| `tools` | All tools | Tools the agent can use (allowlist) |
| `disallowedTools` | None | Tools to deny (removed from inherited list) |
| `model` | `sonnet` | `sonnet`, `opus`, `haiku`, or `inherit` |
| `permissionMode` | `default` | How to handle permission prompts |
| `skills` | None | Skills to load into agent's context at startup |
| `hooks` | None | Lifecycle hooks scoped to this agent |
| `color` | None | Background color in UI (`blue`, `red`, `green`, `cyan`, `purple`, etc.) |

---

## Available Tools

### Read-Only Tools
```yaml
tools: Read, Grep, Glob
```

### Modification Tools
```yaml
tools: Read, Grep, Glob, Edit, Write
```

### Execution Tools
```yaml
tools: Bash
```

### Communication Tools
```yaml
tools: AskUserQuestion, WebFetch, WebSearch
```

### Special Tools
```yaml
tools: Task, TodoWrite, NotebookEdit
```

Note: Agents **cannot spawn other agents** (no nesting).

### Common Combinations

```yaml
# Read-only research
tools: Read, Grep, Glob

# Code modification
tools: Read, Grep, Glob, Edit, Write, Bash

# Full access (inherit all) — omit tools field entirely

# Deny specific tools from full set
disallowedTools: Write, Edit, Bash
```

---

## Built-in Subagents

These are always available in Claude Code without configuration:

| Agent | Model | Tools | Purpose |
|-------|-------|-------|---------|
| **Explore** | Haiku | Read-only | Fast codebase search and analysis |
| **Plan** | Inherit | Read-only | Research during plan mode |
| **general-purpose** | Inherit | All | Complex multi-step tasks |
| **Bash** | Inherit | Bash | Terminal commands in separate context |
| **Claude Code Guide** | Haiku | Read-only | Questions about Claude Code features |

---

## Model Selection Guide

| Model | Best For | Cost | Typical Agents |
|-------|----------|------|----------------|
| `haiku` | Fast search, exploration, simple classification | Low | Explorer, file finder |
| `sonnet` | Balanced capability — the default | Medium | Most agents |
| `opus` | Complex reasoning, nuanced multi-dimension analysis | High | Reviewer, planner, analyzer |
| `inherit` | Match parent conversation model | Varies | Code modifier, test runner |

**Guidelines:**
- Use `haiku` for agents that primarily search and summarize
- Use `sonnet` when you're unsure — it's the safe default
- Use `opus` for agents that make judgment calls across multiple dimensions
- Use `inherit` for agents that should match the user's current model choice

---

## Permission Modes

| Mode | Behavior | Use Case |
|------|----------|----------|
| `default` | Standard permission prompts | Most agents |
| `acceptEdits` | Auto-accept file edits | Trusted code modification |
| `dontAsk` | Auto-deny any permission prompts | Background tasks |
| `bypassPermissions` | Skip all permission checks | **Dangerous — use with caution** |
| `plan` | Read-only exploration mode | Research and analysis agents |

---

## Running Modes

### Foreground (Default)

- Blocks main conversation until the agent completes
- Permission prompts pass through to the user
- Agent can ask clarifying questions via `AskUserQuestion`
- Best for: interactive work, code review, analysis

### Background

- Runs concurrently while the user continues working
- Inherits permissions; auto-denies anything not pre-approved
- Cannot ask questions (tool calls fail silently)
- Best for: long-running searches, batch operations

Request background execution: "run this in the background" or press **Ctrl+B**

### Resuming Agents

Agents can be resumed with their agent ID to continue previous work:

```
Continue that code review and analyze the authorization logic
```

The agent picks up with its full previous context preserved.

---

## Hooks Configuration

### Agent-Scoped Hooks (in frontmatter)

```yaml
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate.sh $TOOL_INPUT"
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "./scripts/lint.sh"
  Stop:
    - hooks:
        - type: command
          command: "./scripts/cleanup.sh"
```

### Hook Types

| Event | When It Fires | Common Use |
|-------|---------------|------------|
| `PreToolUse` | Before a tool executes | Input validation, safety checks |
| `PostToolUse` | After a tool executes | Linting, formatting, verification |
| `Stop` | When the agent finishes | Cleanup, reporting |

### Matcher Patterns

- Single tool: `"Bash"`
- Multiple tools: `"Edit\|Write"`
- All tools: omit matcher entirely

---

## Agent Design Patterns

### Read-Only Reviewer

For agents that analyze but never modify code:

```yaml
tools: Read, Grep, Glob
model: opus
permissionMode: plan
```

### Code Modifier

For agents that make changes to the codebase:

```yaml
tools: Read, Grep, Glob, Edit, Write, Bash
model: inherit
```

### Background Worker

For long-running tasks that don't need user interaction:

```yaml
tools: Read, Grep, Glob, Bash
permissionMode: dontAsk
model: haiku
```

### Domain Expert with Skills

For agents that need specialized knowledge loaded:

```yaml
tools: Read, Grep, Glob, Bash, WebSearch
model: opus
skills:
  - domain-knowledge
```

### Consolidated Multi-Dimension Agent

For agents that cover multiple related specializations:

```yaml
tools: Read, Grep, Glob, WebFetch, WebSearch, Bash
model: opus
color: blue
```

With reference files for each dimension:
```
agents/review/
  reviewer.md                # Main agent — soul + all dimensions
  security-reference.md      # Dimension 1 details
  code-quality-reference.md  # Dimension 2 details
  logging-reference.md       # Dimension 3 details
  privacy-reference.md       # Dimension 4 details
```
