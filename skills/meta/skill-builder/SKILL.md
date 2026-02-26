---
name: skill-builder
description: |
  Knowledge for creating Claude Code skill files with SKILL.md format and best practices.
  Use when building skills to teach Claude specialized knowledge or workflows.
  Recognizes: "create a skill", "new skill for X", "teach Claude how to", "skill that does Y",
  "SKILL.md format", "skill vs agent?", "add knowledge to Claude", "skill frontmatter"
---

# Skill Builder

Use this knowledge to create well-designed skill files that teach Claude specialized knowledge.

**Key distinction from agents:**
- **Skills** = Knowledge/instructions loaded into the current conversation
- **Agents** = Isolated subprocesses with their own context and tools

Use skills when you want to teach Claude HOW to do something. Use agents when you want to DELEGATE a task.

---

## Official Docs

- [Skills](https://code.claude.com/docs/en/skills) — Authoritative reference for skill format, frontmatter fields, and storage locations

---

## Skill File Format

Skills are directories with a `SKILL.md` file:

```
my-skill/
├── SKILL.md           # Required - main instructions
├── reference.md       # Optional - detailed docs (loaded on demand)
├── examples.md        # Optional - usage examples
└── scripts/
    └── helper.py      # Optional - utility scripts (executed, not read)
```

### SKILL.md Structure

```markdown
---
name: skill-name
description: |
  What this skill does and when to use it.
  Include trigger keywords. Write in third person.
---

# Skill Name

## Instructions
Clear, step-by-step guidance for Claude.

## Examples
Concrete input/output examples.
```

### Storage Locations (Priority Order)

| Location | Scope | Priority |
|----------|-------|----------|
| Managed settings | Enterprise (all org users) | 1 (highest) |
| `~/.claude/skills/` | User (all your projects) | 2 |
| `.claude/skills/` | Project (shared with team) | 3 |
| Plugin `skills/` | Where plugin is enabled | 4 (lowest) |

---

## Frontmatter Fields Reference

### Required Fields

| Field | Rules | Description |
|-------|-------|-------------|
| `name` | Max 64 chars, lowercase + hyphens, no "anthropic"/"claude" | Unique identifier |
| `description` | Max 1024 chars, non-empty, third person | When to use. **Critical for discovery** |

### Optional Fields

| Field | Description |
|-------|-------------|
| `allowed-tools` | Tools Claude can use without permission when skill is active |
| `model` | Full model name (e.g., `claude-sonnet-4-20250514`) |
| `context` | Set to `fork` to run in isolated sub-agent context |
| `agent` | Agent type when `context: fork` (e.g., `Explore`, `Plan`, `general-purpose`) |
| `hooks` | Lifecycle hooks: `PreToolUse`, `PostToolUse`, `Stop` |
| `user-invocable` | `false` hides from slash menu (Claude can still use it) |
| `disable-model-invocation` | `true` blocks programmatic invocation via Skill tool |

---

## Writing Effective Descriptions

**The description is critical** - Claude uses it to decide when to apply the skill.

### Rules

1. **Always write in third person** (injected into system prompt)
   ```yaml
   # GOOD
   description: Processes Excel files and generates reports

   # BAD
   description: I can help you process Excel files
   ```

2. **Be specific with trigger keywords**
   ```yaml
   # GOOD
   description: |
     Extract text and tables from PDF files, fill forms, merge documents.
     Use when working with PDF files or when the user mentions PDFs, forms,
     or document extraction.

   # BAD
   description: Helps with documents
   ```

3. **Include WHAT and WHEN**
   - What: The capabilities
   - When: Trigger conditions/keywords

4. **Define negative boundaries — what the skill does NOT handle**
   ```yaml
   # GOOD: Clear boundaries prevent false triggers
   description: |
     Designs REST API endpoints with FastAPI, including routing,
     models, and error responses. Recognizes: "API endpoint",
     "FastAPI route", "REST design".
     Does NOT handle: GraphQL, WebSocket connections, or
     database migration logic.

   # BAD: No boundaries — fires on anything API-related
   description: Helps with API development
   ```

   Why this matters: Without negative boundaries, skills activate on adjacent-but-wrong requests. A skill for "API design" shouldn't fire when someone asks about database migrations just because both involve backend work. Explicit exclusions help Claude route to the right skill and stay silent when none applies.

---

## allowed-tools Configuration

Restrict tools when skill is active:

```yaml
# Comma-separated
allowed-tools: Read, Grep, Glob

# Or YAML list
allowed-tools:
  - Read
  - Grep
  - Glob
```

Common patterns:
- **Read-only**: `Read, Grep, Glob`
- **Code modification**: `Read, Grep, Glob, Edit, Write, Bash`
- **Python analysis**: `Read, Grep, Glob, Bash(python:*)`

---

## MCP Tool References

When using MCP (Model Context Protocol) tools, use fully qualified names:

```markdown
Use the BigQuery:bigquery_schema tool to retrieve table schemas.
Use the GitHub:create_issue tool to create issues.
```

Format: `ServerName:tool_name`

---

## Hooks Configuration

```yaml
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate.sh $TOOL_INPUT"
          once: true  # Run only once per session
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

### 1. Concise is Key

Claude is already smart. Only add context Claude doesn't have.

```markdown
# BAD: Too verbose (~150 tokens)
PDF (Portable Document Format) files are a common file format...

# GOOD: Concise (~50 tokens)
## Extract PDF text

Use pdfplumber:
```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```
```

### 2. Content Placement (Recency Bias)

LLMs pay strongest attention to the **beginning** and **end** of their context. The middle gets weakest attention. Use this:

```markdown
---
name: my-skill
description: ...
---

# Skill Name

## Critical Constraints          ← START: non-negotiable rules here
- Never do X
- Always enforce Y

## Workflow                      ← MIDDLE: main instructions
Step 1: ...
Step 2: ...

## Verification                  ← END: quality gate here (freshest in memory)
Before delivering, check:
1. Baseline test
2. Differentiation check
```

For **reference files**, use explicit loading triggers in SKILL.md:

```markdown
# GOOD: Specific trigger — gets followed
Read anti-patterns.md before delivering final output.

# BAD: Vague trigger — gets skipped under context pressure
Check anti-patterns.md if relevant.
```

### 3. Progressive Disclosure

Keep SKILL.md **under 500 lines**. Put detailed content in separate files.

```markdown
# SKILL.md
## Quick start
[Essential instructions here]

## Additional resources
- For complete API details, see [reference.md](reference.md)
- For usage examples, see [examples.md](examples.md)
```

Claude loads additional files **only when needed** - no context penalty.

### 4. One Level Deep References

```markdown
# BAD: Too deep (Claude may partially read)
SKILL.md → advanced.md → details.md → actual info

# GOOD: Direct references
SKILL.md → reference.md
SKILL.md → examples.md
SKILL.md → forms.md
```

### 5. Table of Contents for Long Files

For reference files >100 lines, add TOC at top:

```markdown
# API Reference

## Contents
- Authentication and setup
- Core methods (create, read, update, delete)
- Advanced features
- Error handling
- Code examples

## Authentication and setup
...
```

### 6. Use Gerund Naming

```yaml
# GOOD
name: processing-pdfs
name: analyzing-spreadsheets
name: writing-documentation

# AVOID
name: helper
name: utils
name: pdf  # Too vague
```

### 7. Provide Templates

```markdown
## Report structure

Use this template:

```markdown
# [Analysis Title]

## Executive summary
[One-paragraph overview]

## Key findings
- Finding 1 with data
- Finding 2 with data

## Recommendations
1. Actionable recommendation
```
```

### 8. Include Examples

```markdown
## Commit message format

**Example 1:**
Input: Added user authentication with JWT tokens
Output:
```
feat(auth): implement JWT-based authentication

Add login endpoint and token validation middleware
```
```

### 9. Implement Feedback Loops

```markdown
## Document editing process

1. Make edits to `document.xml`
2. **Validate immediately**: `python scripts/validate.py`
3. If validation fails:
   - Review error message
   - Fix the issue
   - Run validation again
4. **Only proceed when validation passes**
5. Rebuild document
```

---

## Degrees of Freedom

Match specificity to task fragility:

### High Freedom (Text Instructions)
Use when multiple approaches are valid:
```markdown
## Code review process
1. Analyze code structure
2. Check for bugs
3. Suggest improvements
```

### Medium Freedom (Pseudocode/Parameters)
Use when a preferred pattern exists:
```python
def generate_report(data, format="markdown", include_charts=True):
    # Customize as needed
```

### Low Freedom (Exact Scripts)
Use when operations are fragile:
```markdown
## Database migration

Run exactly this script:
```bash
python scripts/migrate.py --verify --backup
```
Do not modify the command.
```

---

## Workflow Pattern

For complex tasks, provide checklists:

```markdown
## PDF Form Filling Workflow

Copy this checklist:

```
Task Progress:
- [ ] Step 1: Analyze form (run analyze_form.py)
- [ ] Step 2: Create field mapping
- [ ] Step 3: Validate mapping
- [ ] Step 4: Fill form
- [ ] Step 5: Verify output
```

**Step 1: Analyze the form**
Run: `python scripts/analyze_form.py input.pdf`
...
```

---

## Utility Scripts

Bundle scripts for zero-context execution:

```
my-skill/
└── scripts/
    ├── analyze.py    # Executed, not loaded into context
    ├── validate.py
    └── process.py
```

In SKILL.md, tell Claude to **run** (not read) the script:
```markdown
Run the validation script:
```bash
python scripts/validate.py input.txt
```
```

Scripts are **executed**, not read - only output consumes tokens.

---

## Skills and Subagents

### Give a Subagent Access to Skills

Subagents don't inherit skills. List them explicitly:

```yaml
# .claude/agents/code-reviewer.md
---
name: code-reviewer
description: Review code for quality
skills: pr-review, security-check
---
```

### Run a Skill in Forked Context

```yaml
---
name: code-analysis
description: Analyze code quality
context: fork
agent: general-purpose
---
```

---

## Skills vs Other Options

| Use | When you want to... | Trigger |
|-----|---------------------|---------|
| **Skills** | Give Claude specialized knowledge | Auto (Claude chooses) |
| **Slash commands** | Create reusable prompts | Manual (`/command`) |
| **CLAUDE.md** | Set project-wide instructions | Always loaded |
| **Subagents** | Delegate to separate context | Auto or explicit |
| **Hooks** | Run scripts on events | On tool events |
| **MCP servers** | Connect to external tools | Claude calls as needed |

---

## Output Format

When creating a skill, use this structure:

```markdown
## Skill: [name]

**Directory:** `.claude/skills/[name]/`

### SKILL.md

\`\`\`markdown
---
name: [name]
description: |
  [description with trigger keywords, third person]
allowed-tools: [if restricted]
---

[Instructions]
\`\`\`

### Additional Files (if needed)

**reference.md**: [purpose]
**scripts/[name].py**: [purpose]

### Summary
- Purpose: [one line]
- Triggers: [when Claude will use it]
- Tools: [restrictions if any]
```

---

## Verification Gate

Every skill should include a built-in quality check that catches baseline output — generic results the AI would produce without the skill loaded.

### Why

Without a verification gate, skills produce "better-formatted slop": output that looks structured but hasn't actually shifted the AI's reasoning. The gate forces a re-evaluation before delivery.

### How to Add One

Add a final section to your skill's workflow:

```markdown
## Verification

Before delivering, check:
1. **Baseline test**: Would a default Claude without this skill produce something structurally similar? If yes, the skill didn't activate properly — redo the core step.
2. **Differentiation check**: Point to the specific elements that ONLY exist because this skill was loaded (a specific framework applied, a domain constraint enforced, an unusual angle taken).
3. **Anti-pattern scan**: Does the output contain any patterns from the banned list? If yes, fix before delivering.
```

### Verification Levels

Match the gate's strictness to the skill's purpose:

| Skill Type | Verification Level | Example Check |
|------------|-------------------|---------------|
| **Workflow** (tdd, plan-review) | Structural — did each phase produce a visible artifact? | "Phase 2 must output a failing test before Phase 3 begins" |
| **Pattern** (api-design, testing) | Conformance — does output follow the prescribed pattern? | "Every endpoint must have error responses defined" |
| **Build** (scaffold, config) | Completeness — are all required pieces present? | "Config must include env-var overrides and validation" |
| **Meta** (skill-builder, agent-builder) | Recursive — does the built artifact itself contain a verification gate? | "Generated skill must include a Verification section" |

### Example: Verification Gate for a Copy-Writing Skill

```markdown
## Verification

Before delivering:
1. Run output against banned-words list (see anti-patterns.md) — zero matches required
2. Compare structure to "generic version" defined below — must differ in at least 2 structural choices
3. If output reads like a LinkedIn post (hook → 3 bullets → CTA), it failed — restructure

### Generic version (what to avoid)
- Opens with a question or bold claim
- Three-item bullet list in the middle
- Ends with "ready to get started?" CTA
- Uses words: compelling, leverage, unlock, game-changer
```

---

## Anti-Patterns & Checklist

For common anti-patterns to avoid and a pre-flight checklist, see [anti-patterns.md](anti-patterns.md).
