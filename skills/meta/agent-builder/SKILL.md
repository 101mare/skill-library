---
name: agent-builder
description: |
  Knowledge for designing Claude Code agents with research-backed identity design (Soul Formula).
  Teaches experiential identities, anti-patterns, multi-file structure, and consolidation patterns.
  Use when building new agents or improving existing ones.
  Recognizes: "create an agent", "new agent for X", "agent that does Y", "how do I make an agent?",
  "agent configuration", "add a subagent", "agent frontmatter", "agent tools",
  "agent soul", "agent identity", "agent design"
---

# Agent Builder

Build agents that perform like specialists, not generic assistants.

This skill teaches the **design philosophy** behind effective agents. For technical reference (frontmatter fields, tool lists, permission modes), see [reference.md](reference.md). For real examples from this repo, see [examples.md](examples.md).

## Official Docs

- [Sub-agents](https://code.claude.com/docs/en/sub-agents) — Authoritative reference for agent format, frontmatter fields, and running modes

---

## Agent File Format

Agents are Markdown files with YAML frontmatter. The frontmatter controls *how* Claude launches the agent. The markdown body *is* the agent's entire system prompt.

```markdown
---
name: agent-name
description: |
  When Claude should use this agent. Be specific.
  Include "use proactively" for automatic delegation.
tools: Read, Grep, Glob
model: sonnet
---

The agent's system prompt goes here.
It receives ONLY this content, not the full Claude Code system prompt.
```

### Key Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Lowercase with hyphens (e.g., `code-reviewer`) |
| `description` | Yes | When Claude should delegate — specific trigger phrases |
| `tools` | No | Tool allowlist (omit for all tools) |
| `model` | No | `haiku`, `sonnet`, `opus`, or `inherit` (default: `sonnet`) |

For the full field reference (permissions, hooks, skills, colors), see [reference.md](reference.md).

### Storage Locations (Priority Order)

| Location | Scope | Priority |
|----------|-------|----------|
| `--agents` CLI flag | Current session only | 1 (highest) |
| `.claude/agents/` | Project (shared with team) | 2 |
| `~/.claude/agents/` | User (all your projects) | 3 |
| Plugin `agents/` | Where plugin is enabled | 4 (lowest) |

---

## The Soul Formula

The most important part of an agent is its system prompt. Research shows that **generic labels have zero statistically significant improvement** over no label at all — but specific experiential identities improve accuracy by 10-60%.

> **Research basis:** NAACL 2024 paper "Better Zero-Shot Reasoning with Role-Play Prompting" ([arxiv.org/abs/2308.07702](https://arxiv.org/abs/2308.07702)) — 162 roles, 4 LLM families, 2,410 questions, 12 reasoning benchmarks.

The Soul Formula has four parts:

### Part 1: Experiential Identity

Don't assign a label. Give the agent specific experiences that activate relevant knowledge clusters.

```markdown
# BAD — generic label (zero improvement over no label)
You are an expert Python security reviewer.

# GOOD — experiential identity (10-60% improvement)
You are a senior Python reviewer who has found SQL injection slip through
three rounds of code review, watched silent `except: pass` blocks cause
production incidents, traced GDPR violations to debug-level LLM response
logs that "nobody would ever enable in production," and caught "100% offline"
projects making DNS requests on startup via transitive dependencies.
```

The formula: **"You are a [role] who has [specific experience 1], [specific experience 2], and [specific experience 3]."**

Why it works: Each experience activates a specific knowledge cluster. "Found SQL injection slip through three rounds of code review" tells the model *what to look for* and *how hard to look*, not just *that* it should look.

Follow with a learned insight:

```markdown
I've learned that [insight] because [experience].
```

Example: *"I've learned that security bugs cluster around boundaries — where user input enters, where data crosses trust zones, where assumptions about 'internal only' break down."*

This tells the model *where* to focus, not just *what* to find.

### Part 2: Anti-Patterns — "What I Refuse To Do"

Devote **30-40% of the prompt** to what the agent refuses to do. This is the reliability lever.

```markdown
## What I Refuse To Do

- I don't review code without checking security first.
- I don't accept `except` blocks without logging.
- I don't skip sensitive data checks.
- I don't trust import names at face value.
- I don't accept functions without type hints.
```

Why 30-40%? LLMs tend toward agreeable, surface-level responses. Anti-patterns create hard boundaries that prevent the agent from cutting corners. Each refusal should be:

- **Specific** — not "I don't write bad code" but "I don't accept `except` blocks without logging"
- **Experiential** — tied to a real failure mode the identity would have encountered
- **Actionable** — describes what gets flagged, not abstract philosophy

### Part 3: Productive Weakness

Give the agent one honest limitation. This paradoxically improves quality by preventing overconfident outputs.

```markdown
One productive weakness: I sometimes flag patterns as risky that are
actually safe in context. That's the cost of thoroughness. The benefit
is I've caught real vulnerabilities that passed three rounds of code review.
```

The formula: **"I sometimes [limitation]. That's the cost of [strength]. The benefit is [why it's worth it]."**

### Part 4: Project Adaptation

Every agent should read the project context before working:

```markdown
## Project Adaptation

Before analysis, read the project's `CLAUDE.md` and `.claude/memory.md`
(if they exist) to understand:
- Module structure and boundaries
- Design patterns and conventions in use
- Known patterns to preserve
- Test conventions and security requirements

Adapt your analysis to the project's actual patterns rather than assuming defaults.
```

This turns a generic agent into a project-aware specialist.

### Part 5: Cognitive Profile (Optional)

The Soul defines *who* the agent is. The Cognitive Profile defines *how* it thinks — the mental frameworks it applies when making judgment calls.

Not every agent needs one. A code-simplifier that follows clear rules doesn't need decision frameworks. But agents that exercise **judgment under ambiguity** — reviewers, analyzers, planners — benefit significantly from explicit thinking patterns.

A Cognitive Profile has five components:

#### Decision Frameworks

The mental models the agent applies to classify situations. These are the "if-then" heuristics that guide judgment.

```markdown
## Decision Frameworks

- **Trust Boundary Test:** "Who controls this value?" → If not our code → validate
- **Blast Radius Test:** "If this fails, what else breaks?" → Multiple callers → add safeguards
- **Reversibility Test:** "Can we undo this?" → No → require explicit confirmation
```

#### Prioritization Logic

What the agent cares about first, second, third. This prevents the agent from spending tokens on style issues when security holes are open.

```markdown
## Prioritization

Security → Data Integrity → Code Quality → Style
(Never comment on formatting when there's an unvalidated input path.)
```

#### Red Flags — Patterns That Always Get Flagged

Concrete code patterns that trigger immediate attention, regardless of context. These are non-negotiable.

```markdown
## Red Flags

These patterns ALWAYS get flagged, no exceptions:
- `except: pass` or `except Exception: pass` without re-raise
- `shell=True` in subprocess calls
- `pickle.loads()` on user-controlled data
- String formatting in SQL queries
- `chmod 777` or world-writable permissions
```

#### Question Sequences

The ordered questions the agent asks itself when examining code. This structures the agent's thinking process and ensures consistent depth.

```markdown
## For Every File I Review, I Ask:

1. What enters from outside? (user input, env vars, file reads, API responses)
2. Where does data cross trust boundaries? (internal → external, user → system)
3. What assumptions does this code make about its inputs?
4. What happens when those assumptions are wrong?
```

#### Strategic Ignorance

What the agent **deliberately deprioritizes** in favor of higher-value work. This prevents scope dilution.

```markdown
## What I Deliberately Ignore (When Higher Issues Exist)

- Code style and formatting (when security issues are open)
- Performance micro-optimizations (when correctness is in question)
- Naming conventions (when architectural problems exist)
```

#### When to Use a Cognitive Profile

| Agent Type | Needs Cognitive Profile? | Why |
|------------|------------------------|-----|
| Reviewer | **Yes** | Exercises judgment on severity, prioritizes across dimensions |
| Analyzer | **Yes** | Must decide what matters, classify risks, weigh trade-offs |
| Planner | **Yes** | Must assess completeness, identify gaps, evaluate risk |
| Code Simplifier | **No** | Follows clear rules: simpler = better, don't change behavior |
| Test Architect | **Maybe** | Benefits from prioritization logic for test coverage |

#### Placement in the Agent File

The Cognitive Profile goes **after** the Anti-Patterns and **before** the Process section:

```
1. Experiential Identity (opening paragraph)
2. "What I Refuse To Do" (anti-patterns)
3. Cognitive Profile (decision frameworks, priorities, red flags)  ← here
4. Process / Dimensions / Checklist
5. Output Format
6. Project Adaptation
```

### Complete Soul Structure

```
1. Experiential Identity (opening paragraph)
2. Learned Insight (optional second paragraph)
3. "What I Refuse To Do" (30-40% of prompt)
4. Cognitive Profile (optional — decision frameworks, priorities, red flags)
5. Process / Dimensions / Checklist (the actual work)
6. Severity Levels (classification system)
7. Output Format (consistent structure)
8. Project Adaptation (read CLAUDE.md first)
```

---

## Multi-File Agent Structure

Complex agents split into a main file and reference files:

```
agents/
  review/
    reviewer.md              # Soul + process + output format
    security-reference.md    # OWASP checklist, code examples
    code-quality-reference.md
    logging-reference.md
    privacy-reference.md
```

### Main File (the agent)

Contains the soul, process overview, and output format. This is what gets loaded as the system prompt. Keep it focused — under 200 lines ideally.

The main file references detailed checklists:

```markdown
## Review Dimensions

Every review covers these four dimensions. Load the relevant reference
file for detailed checklists:
- [security-reference.md](security-reference.md) — OWASP, injection, secrets
- [code-quality-reference.md](code-quality-reference.md) — Types, patterns
- [logging-reference.md](logging-reference.md) — Levels, sensitive data
- [privacy-reference.md](privacy-reference.md) — External calls, telemetry
```

### Reference Files (loaded on demand)

Contain detailed checklists, code examples, and lookup tables. The agent loads these when it needs specifics for a particular dimension. Reference files are pure content — no frontmatter, no soul.

**Rule of thumb:** If it's *judgment* (what to look for, what matters, what to refuse), it goes in the main file. If it's *data* (checklists, code patterns, configuration tables), it goes in a reference file.

---

## Consolidation Pattern

Multiple specialized agents doing related work should be consolidated into one agent with **dimensions**.

### Why Consolidate

- **Fewer agents = better delegation.** Claude picks from available agents — 5 choices is easier than 15.
- **Shared soul.** Related specializations share the same quality standards and project adaptation.
- **Cross-cutting concerns.** A security issue in a logging statement needs both security and logging expertise.

### How to Consolidate

1. **Identify related agents** — agents that review the same codebase from different angles
2. **Write one soul** that encompasses all specializations
3. **Create dimensions** — each former agent becomes a dimension with its own section
4. **Extract checklists** into reference files — one per dimension
5. **Union the tools** — the consolidated agent gets all tools any dimension needs

### Structure After Consolidation

```
# Before: 4 separate agents
security-reviewer.md    → archived
python-reviewer.md      → archived
logging-reviewer.md     → archived
privacy-auditor.md      → archived

# After: 1 consolidated agent + 4 reference files
reviewer.md                  # Soul + 4 dimensions + output format
security-reference.md        # Detailed OWASP checklist
code-quality-reference.md    # Type safety, patterns
logging-reference.md         # Log levels, sensitive data
privacy-reference.md         # External calls, telemetry
```

The soul paragraph naturally combines experiences from all dimensions:

```markdown
You are a senior Python reviewer who has found SQL injection slip through
three rounds of code review [security], watched silent `except: pass`
blocks cause production incidents [code quality], traced GDPR violations
to debug-level LLM response logs [logging + privacy], and caught "100%
offline" projects making DNS requests on startup [privacy].
```

---

## Directory Organization

Organize agents by role:

```
agents/
  review/      # Code review, security audit, quality check
  analyze/     # Architecture, performance, scalability, dependencies
  plan/        # Plan validation, requirements, risk assessment
  build/       # Code generation, refactoring, testing
```

Each directory contains one consolidated agent and its reference files.

---

## Best Practices

### Description Field

The `description` is how Claude decides when to delegate. Make it specific:

```yaml
# GOOD: Specific triggers, clear scope
description: |
  Reviews Python code for security vulnerabilities, performance issues,
  and best practices. Use proactively after code changes.
  Recognizes: "review my code", "is this secure?", "check for vulnerabilities"

# BAD: Vague, no triggers
description: Reviews code
```

### Tool Selection

Grant only what's needed. See [reference.md](reference.md) for the full tool list.

```yaml
# Read-only reviewer — can't accidentally modify code
tools: Read, Grep, Glob

# Code modifier — needs write access
tools: Read, Grep, Glob, Edit, Write, Bash
```

### Model Selection

| Model | Use Case |
|-------|----------|
| `haiku` | Fast search, exploration, simple classification |
| `sonnet` | Default — balanced capability and cost |
| `opus` | Complex reasoning, nuanced judgment, multi-dimension analysis |
| `inherit` | Match parent conversation model |

### Prompt Length

- **Under 200 lines** for the main agent file
- Keep the soul paragraph to 2-4 sentences
- 4-6 anti-patterns (more dilutes impact)
- One productive weakness (more than one undermines confidence)

---

## Output Template

When creating an agent, produce this structure:

````markdown
## Agent: [name]

**File:** `.claude/agents/[category]/[name].md`

```markdown
---
name: [name]
description: |
  [What this agent does. When Claude should delegate to it.]
  [Include "use proactively" if it should auto-activate.]
  Recognizes: "[trigger 1]", "[trigger 2]", "[trigger 3]"
tools: [minimal tool set]
model: [model]
---

[Experiential identity paragraph — specific experiences, not labels]

[Optional: learned insight paragraph]

## What I Refuse To Do

- I don't [specific anti-pattern 1].
- I don't [specific anti-pattern 2].
- I don't [specific anti-pattern 3].
- I don't [specific anti-pattern 4].

---

## Process

1. **Read CLAUDE.md** if present — understand project conventions
2. [Main analysis/work steps]
3. [Verification step]
4. **Report findings** with file:line references

---

## Output Format

[Consistent output structure with severity levels or status indicators]

---

## Project Adaptation

Before analysis, read the project's `CLAUDE.md` and `.claude/memory.md`
(if they exist) to understand:
- [Relevant project context points]

Adapt your analysis to the project's actual patterns rather than assuming defaults.
```

**Summary:**
- Purpose: [one line]
- Tools: [list]
- Model: [model]
- Triggers: [when Claude will use it]
````

If the agent needs detailed checklists or code examples, create reference files alongside it.
