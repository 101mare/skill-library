# Skill Library

A curated, hierarchically organized collection of Claude Code skills and agents. Source of truth for reusable AI-assisted development workflows.

## Structure

```
skill-library/
├── skills/
│   ├── meta/                    # Meta: Skills and Agents bauen
│   │   ├── skill-builder/       # How to create skills
│   │   └── agent-builder/       # How to create agents
│   ├── build/                   # Builder: Scaffolding & Infrastructure
│   │   ├── prompt-builder/      # Structured prompt generation
│   │   ├── logging-builder/     # Python logging infrastructure
│   │   ├── config-builder/      # Pydantic config + YAML + env-vars
│   │   ├── exception-builder/   # Exception hierarchy design
│   │   ├── docker-builder/      # Dockerfile + Compose scaffolding
│   │   └── project-scaffold/    # Python project from scratch
│   ├── workflow/                # Orchestration: Multi-Agent Workflows
│   │   ├── plan-review/         # Plan review before implementation
│   │   ├── session-verify/      # End-of-session verification
│   │   └── pr-review/           # Pull request review orchestration
│   └── patterns/                # Reusable Architecture Patterns
│       ├── di-container/        # Dependency Injection with Protocols
│       ├── protocol-design/     # Python Protocol pattern
│       ├── strategy-registry/   # Strategy + Registry dispatch
│       └── error-handling/      # Exception mapping & retry patterns
└── agents/
    ├── review/                  # Code Review & Audit
    │   ├── python-reviewer.md
    │   ├── logging-reviewer.md
    │   ├── security-reviewer.md
    │   └── privacy-auditor.md
    ├── analyze/                 # Analysis & Detection
    │   ├── performance-analyzer.md
    │   ├── scalability-analyzer.md
    │   ├── dead-code-detector.md
    │   ├── dependency-auditor.md
    │   └── architecture-analyzer.md
    ├── plan/                    # Planning & Assessment
    │   ├── plan-completeness.md
    │   ├── risk-assessor.md
    │   └── requirements-verifier.md
    └── build/                   # Code Generation & Modification
        ├── code-simplifier.md
        ├── test-architect.md
        ├── warmgold-frontend-builder.md
        └── migration-writer.md
```

## Setup

Connect this library to Claude Code via symlinks.

### Skills

```bash
# Create skills directory if needed
mkdir -p ~/.claude/skills

# Link each skill directory
ln -sf ~/skill-library/skills/meta/skill-builder ~/.claude/skills/skill-builder
ln -sf ~/skill-library/skills/meta/agent-builder ~/.claude/skills/agent-builder
ln -sf ~/skill-library/skills/build/prompt-builder ~/.claude/skills/prompt-builder
ln -sf ~/skill-library/skills/build/logging-builder ~/.claude/skills/logging-builder
ln -sf ~/skill-library/skills/build/config-builder ~/.claude/skills/config-builder
ln -sf ~/skill-library/skills/build/exception-builder ~/.claude/skills/exception-builder
ln -sf ~/skill-library/skills/build/docker-builder ~/.claude/skills/docker-builder
ln -sf ~/skill-library/skills/build/project-scaffold ~/.claude/skills/project-scaffold
ln -sf ~/skill-library/skills/workflow/plan-review ~/.claude/skills/plan-review
ln -sf ~/skill-library/skills/workflow/session-verify ~/.claude/skills/session-verify
ln -sf ~/skill-library/skills/workflow/pr-review ~/.claude/skills/pr-review
ln -sf ~/skill-library/skills/patterns/di-container ~/.claude/skills/di-container
ln -sf ~/skill-library/skills/patterns/protocol-design ~/.claude/skills/protocol-design
ln -sf ~/skill-library/skills/patterns/strategy-registry ~/.claude/skills/strategy-registry
ln -sf ~/skill-library/skills/patterns/error-handling ~/.claude/skills/error-handling
```

### Agents

```bash
# Create agents directory if needed
mkdir -p ~/.claude/agents

# Link each agent file
ln -sf ~/skill-library/agents/review/python-reviewer.md ~/.claude/agents/python-reviewer.md
ln -sf ~/skill-library/agents/review/logging-reviewer.md ~/.claude/agents/logging-reviewer.md
ln -sf ~/skill-library/agents/review/security-reviewer.md ~/.claude/agents/security-reviewer.md
ln -sf ~/skill-library/agents/review/privacy-auditor.md ~/.claude/agents/privacy-auditor.md
ln -sf ~/skill-library/agents/analyze/performance-analyzer.md ~/.claude/agents/performance-analyzer.md
ln -sf ~/skill-library/agents/analyze/scalability-analyzer.md ~/.claude/agents/scalability-analyzer.md
ln -sf ~/skill-library/agents/analyze/dead-code-detector.md ~/.claude/agents/dead-code-detector.md
ln -sf ~/skill-library/agents/analyze/dependency-auditor.md ~/.claude/agents/dependency-auditor.md
ln -sf ~/skill-library/agents/analyze/architecture-analyzer.md ~/.claude/agents/architecture-analyzer.md
ln -sf ~/skill-library/agents/plan/plan-completeness.md ~/.claude/agents/plan-completeness.md
ln -sf ~/skill-library/agents/plan/risk-assessor.md ~/.claude/agents/risk-assessor.md
ln -sf ~/skill-library/agents/plan/requirements-verifier.md ~/.claude/agents/requirements-verifier.md
ln -sf ~/skill-library/agents/build/code-simplifier.md ~/.claude/agents/code-simplifier.md
ln -sf ~/skill-library/agents/build/test-architect.md ~/.claude/agents/test-architect.md
ln -sf ~/skill-library/agents/build/warmgold-frontend-builder.md ~/.claude/agents/warmgold-frontend-builder.md
ln -sf ~/skill-library/agents/build/migration-writer.md ~/.claude/agents/migration-writer.md
```

### Quick Setup (All at once)

```bash
# Skills
for skill in skill-builder agent-builder; do
  ln -sf ~/skill-library/skills/meta/$skill ~/.claude/skills/$skill
done
for skill in prompt-builder logging-builder config-builder exception-builder docker-builder project-scaffold; do
  ln -sf ~/skill-library/skills/build/$skill ~/.claude/skills/$skill
done
for skill in plan-review session-verify pr-review; do
  ln -sf ~/skill-library/skills/workflow/$skill ~/.claude/skills/$skill
done
for skill in di-container protocol-design strategy-registry error-handling; do
  ln -sf ~/skill-library/skills/patterns/$skill ~/.claude/skills/$skill
done

# Agents
for agent in python-reviewer logging-reviewer security-reviewer privacy-auditor; do
  ln -sf ~/skill-library/agents/review/$agent.md ~/.claude/agents/$agent.md
done
for agent in performance-analyzer scalability-analyzer dead-code-detector dependency-auditor architecture-analyzer; do
  ln -sf ~/skill-library/agents/analyze/$agent.md ~/.claude/agents/$agent.md
done
for agent in plan-completeness risk-assessor requirements-verifier; do
  ln -sf ~/skill-library/agents/plan/$agent.md ~/.claude/agents/$agent.md
done
for agent in code-simplifier test-architect warmgold-frontend-builder migration-writer; do
  ln -sf ~/skill-library/agents/build/$agent.md ~/.claude/agents/$agent.md
done
```

## Lifecycle Mapping

Which skills/agents to use at each development phase:

| Phase | Skills | Agents |
|-------|--------|--------|
| **Plan** | plan-review | plan-completeness, risk-assessor, architecture-analyzer |
| **Scaffold** | project-scaffold, config-builder, exception-builder, docker-builder | -- |
| **Code** | di-container, protocol-design, strategy-registry, error-handling, logging-builder | -- |
| **Review** | pr-review, session-verify | python-reviewer, security-reviewer, logging-reviewer, privacy-auditor |
| **Test** | -- | test-architect |
| **Analyze** | -- | performance-analyzer, scalability-analyzer, dead-code-detector, dependency-auditor |
| **Deploy** | docker-builder | -- |
| **Maintain** | -- | dead-code-detector, dependency-auditor |

## Naming Conventions

- **Skills**: `kebab-case` directories with `SKILL.md` inside
- **Agents**: `kebab-case.md` files
- **Categories**: Verb-based (`review/`, `analyze/`, `plan/`, `build/`)

## Adding Project-Specific Skills

For project-specific skills, add them to the project's `.claude/skills/` directory (not this library). This library contains only generic, reusable content.

```
my-project/
└── .claude/
    └── skills/
        └── my-project-specific-skill/
            └── SKILL.md
```

## Counts

| Category | Count |
|----------|-------|
| Skills (total) | 16 |
| -- meta/ | 2 |
| -- build/ | 6 |
| -- workflow/ | 3 |
| -- patterns/ | 4 |
| Agents (total) | 16 |
| -- review/ | 4 |
| -- analyze/ | 5 |
| -- plan/ | 3 |
| -- build/ | 4 |
