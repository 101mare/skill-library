# Skill Library

A curated, hierarchically organized collection of Claude Code skills and agents. Source of truth for reusable AI-assisted development workflows.

For a detailed walkthrough of the architecture, design decisions and usage patterns, see [article.md](article.md).

## Structure

```
skill-library/
├── templates/
│   └── CLAUDE.md.template      # Generic CLAUDE.md for new projects
├── rules/                          # Always-loaded behavior rules
│   ├── coding-conventions.md   # DRY, naming, error handling, types, testing
│   ├── agent-behavior.md       # Scope discipline, when to ask, post-writing
│   ├── security.md             # Input validation, PII, secrets
│   └── self-improvement.md     # Learn from corrections, iterate on lessons
├── skills/
│   ├── meta/                    # Meta: Skills, Agents and Teams bauen
│   │   ├── skill-builder/       # How to create skills
│   │   ├── agent-builder/       # How to create agents
│   │   └── team-builder/        # How to orchestrate agent teams
│   ├── build/
│   │   ├── frontend/            # Frontend: Design & Components
│   │   │   ├── frontend-design/   # Production-grade frontend design (Impeccable)
│   │   │   └── warmgold-frontend/  # Warmgold design system (vanilla HTML/CSS/JS)
│   │   └── backend/             # Backend: Scaffolding & Infrastructure
│   │       ├── prompt-builder/      # Structured prompt generation
│   │       ├── logging-builder/     # Python logging infrastructure
│   │       ├── config-builder/      # Pydantic config + YAML + env-vars
│   │       ├── exception-builder/   # Exception hierarchy design
│   │       ├── docker-builder/      # Dockerfile + Compose scaffolding
│   │       ├── ci-cd-builder/       # GitHub Actions CI/CD pipelines
│   │       └── project-scaffold/    # Python project from scratch
│   ├── workflow/                # Orchestration: Multi-Agent Workflows
│   │   ├── plan-review/         # Plan review before implementation
│   │   ├── session-verify/      # End-of-session verification
│   │   ├── pr-review/           # Pull request review orchestration
│   │   ├── tdd/                 # Test-Driven Development (RED-GREEN-REFACTOR)
│   │   ├── deep-research/       # Structured research workflow
│   │   ├── ralph-loop/          # Autonomous iteration loop (hooks-based)
│   │   └── ralph-loop-prompt-builder/ # Interactive prompt builder for Ralph Loop
│   └── patterns/                # Reusable Architecture Patterns
│       ├── di-container/        # Dependency Injection with Protocols
│       ├── protocol-design/     # Python Protocol pattern
│       ├── strategy-registry/   # Strategy + Registry dispatch
│       ├── error-handling/      # Exception mapping & retry patterns
│       ├── resilience-patterns/ # Retry, Circuit Breaker, Timeout, Degradation
│       ├── testing-patterns/    # pytest, mocking, property-based testing
│       ├── api-design/          # REST API with FastAPI
│       └── systematic-debugging/ # 4-phase debugging methodology
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

Browse the categories, pick what you need, and copy the `.md` files into your project's `.claude/` directory. Alternatively, you can symlink them from this repo to `~/.claude/rules/`, `~/.claude/skills/` and `~/.claude/agents/` for global availability.

## Lifecycle Mapping

Which skills/agents to use at each development phase:

| Phase | Skills | Agents |
|-------|--------|--------|
| **Research** | deep-research | -- |
| **Plan** | plan-review | plan-completeness, risk-assessor, architecture-analyzer |
| **Scaffold** | project-scaffold, config-builder, exception-builder, docker-builder, ci-cd-builder | -- |
| **Code** | di-container, protocol-design, strategy-registry, error-handling, resilience-patterns, logging-builder, api-design, ralph-loop, ralph-loop-prompt-builder | -- |
| **Frontend** | frontend-design, warmgold-frontend | warmgold-frontend-builder |
| **Review** | pr-review, session-verify | python-reviewer, security-reviewer, logging-reviewer, privacy-auditor |
| **Test** | tdd, testing-patterns | test-architect |
| **Debug** | systematic-debugging | -- |
| **Analyze** | -- | performance-analyzer, scalability-analyzer, dead-code-detector, dependency-auditor |
| **Deploy** | docker-builder, ci-cd-builder | -- |
| **Maintain** | -- | dead-code-detector, dependency-auditor |

## Naming Conventions

- **Skills**: `kebab-case` directories with `SKILL.md` inside
- **Agents**: `kebab-case.md` files
- **Categories**: Verb-based (`review/`, `analyze/`, `plan/`, `build/`)

## CLAUDE.md Template

A comprehensive CLAUDE.md template is available at `templates/CLAUDE.md.template`. Copy it into new projects and fill in the `[placeholders]`:

```bash
cp ~/skill-library/templates/CLAUDE.md.template my-project/CLAUDE.md
```

Covers project-specific content: Critical Constraints, Architecture, Commands, Import Conventions, Key Patterns, Configuration, Quick Reference. Generic rules (DRY, agent behavior, security) are in `rules/` and don't need to be repeated in CLAUDE.md.

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
| Rules | 4 |
| Templates | 1 |
| Skills (total) | 27 |
| -- meta/ | 3 |
| -- build/frontend/ | 2 |
| -- build/backend/ | 7 |
| -- workflow/ | 7 |
| -- patterns/ | 8 |
| Agents (total) | 16 |
| -- review/ | 4 |
| -- analyze/ | 5 |
| -- plan/ | 3 |
| -- build/ | 4 |
