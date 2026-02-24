---
name: agent-builder
description: |
  Knowledge for creating Claude Code subagent files with proper YAML frontmatter and prompts.
  Use when building new agents or configuring existing ones.
  Recognizes: "create an agent", "new agent for X", "agent that does Y", "how do I make an agent?",
  "agent configuration", "add a subagent", "agent frontmatter", "agent tools"
---

# Agent Builder

Use this knowledge to create well-designed subagent configuration files.

## Official Docs

- [Sub-agents](https://code.claude.com/docs/en/sub-agents) — Authoritative reference for agent format, frontmatter fields, and running modes

---

## Agent File Format

Agents are Markdown files with YAML frontmatter:

```markdown
---
name: agent-name
description: |
  When Claude should use this agent. Be specific.
  Include "use proactively" for automatic delegation.
tools: Read, Grep, Glob
model: sonnet
---

System prompt content here. This guides the agent's behavior.
The agent receives ONLY this prompt, not the full Claude Code system prompt.
```

### Storage Locations (Priority Order)

| Location | Scope | Priority |
|----------|-------|----------|
| `--agents` CLI flag | Current session only | 1 (highest) |
| `.claude/agents/` | Project (shared with team) | 2 |
| `~/.claude/agents/` | User (all your projects) | 3 |
| Plugin `agents/` | Where plugin is enabled | 4 (lowest) |

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
| `color` | None | Background color in UI |

---

## Built-in Subagents

| Agent | Model | Tools | Purpose |
|-------|-------|-------|---------|
| **Explore** | Haiku | Read-only | Fast codebase search and analysis |
| **Plan** | Inherit | Read-only | Research during plan mode |
| **general-purpose** | Inherit | All | Complex multi-step tasks |
| **Bash** | Inherit | Bash | Terminal commands in separate context |
| **Claude Code Guide** | Haiku | Read-only | Questions about Claude Code features |

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

# Full access (inherit all) - omit tools field

# Deny specific tools
disallowedTools: Write, Edit, Bash
```

---

## Model Selection

| Model | Use Case | Cost |
|-------|----------|------|
| `haiku` | Fast search, exploration, simple tasks | Low |
| `sonnet` | Balanced capability (default) | Medium |
| `opus` | Complex reasoning, nuanced analysis | High |
| `inherit` | Match parent conversation | Varies |

---

## Permission Modes

| Mode | Behavior | Use Case |
|------|----------|----------|
| `default` | Standard permission prompts | Most agents |
| `acceptEdits` | Auto-accept file edits | Trusted modification |
| `dontAsk` | Auto-deny prompts | Background tasks |
| `bypassPermissions` | Skip all checks | **Dangerous** |
| `plan` | Read-only exploration | Research agents |

---

## Running Modes

### Foreground (Default)
- Blocks main conversation until complete
- Permission prompts pass through to user
- Can ask clarifying questions

### Background
- Runs concurrently while you work
- Inherits permissions, auto-denies anything not pre-approved
- Cannot ask questions (tool calls fail silently)

Request background: "run this in the background" or press **Ctrl+B**

### Resuming Agents
Agents can be resumed with their agent ID:
```
Continue that code review and analyze the authorization logic
```

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

---

## Best Practices

### 1. Focused Purpose
```yaml
# GOOD: Focused
name: test-runner
description: Runs tests and reports failures with fix suggestions

# BAD: Too broad
name: code-helper
description: Helps with code stuff
```

### 2. Detailed Description
```yaml
# GOOD: Specific triggers
description: |
  Reviews code for security vulnerabilities, performance issues, and best practices.
  Use proactively after code changes.

# BAD: Vague
description: Reviews code
```

### 3. Minimal Tool Access
```yaml
# GOOD: Read-only for reviewer
tools: Read, Grep, Glob

# BAD: Full access when not needed
```

### 4. Clear System Prompt Structure
```markdown
You are a [ROLE] specializing in [DOMAIN].

When invoked:
1. [First action]
2. [Main task]
3. [Verification/output]

Guidelines:
- [Guideline 1]
- [Guideline 2]

Output format:
- [Structure]
```

---

## Agent Design Patterns

### Read-Only Reviewer
```yaml
tools: Read, Grep, Glob
model: sonnet
permissionMode: plan
```

### Code Modifier
```yaml
tools: Read, Grep, Glob, Edit, Write, Bash
model: inherit
```

### Background Worker
```yaml
tools: Read, Grep, Glob, Bash
permissionMode: dontAsk
model: haiku
```

### Domain Expert with Skills
```yaml
tools: Read, Grep, Glob, Bash, WebSearch
model: opus
skills:
  - domain-knowledge
```

---

## Output Format

When creating an agent, use this structure:

```markdown
## Agent: [name]

**File:** `.claude/agents/[name].md`

\`\`\`markdown
---
name: [name]
description: |
  [description]
tools: [tools]
model: [model]
---

[System prompt]
\`\`\`

**Summary:**
- Purpose: [one line]
- Tools: [list]
- Model: [model]
- Triggers: [when Claude will use it]
```

---

## Example Agents

### Minimal Read-Only
```markdown
---
name: code-explorer
description: |
  Explores and explains codebases.
  Use when user asks "how does X work" or "where is Y".
tools: Read, Grep, Glob
model: haiku
---

You are a codebase explorer. Find and explain code structure.

When invoked:
1. Search for relevant files
2. Read and analyze code
3. Explain clearly with file references
```

### Full-Featured with Hooks
```markdown
---
name: refactoring-assistant
description: |
  Refactors code for readability and maintainability.
  Use proactively when code needs cleanup.
tools: Read, Grep, Glob, Edit, Write, Bash
model: sonnet
hooks:
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "ruff check --fix"
---

You are a refactoring specialist focused on clean, maintainable code.

When invoked:
1. Analyze current code structure
2. Identify refactoring opportunities
3. Apply changes incrementally
4. Verify with tests

Priorities:
- Extract duplicated code
- Simplify complex functions
- Improve naming
- Add type hints

Always run tests after changes.
```
