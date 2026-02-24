# Skill Library

Teach Claude Code how to build like a senior engineer. A collection of 27 skills, 16 agents, and battle-tested rules that give Claude reusable knowledge about architecture patterns, development workflows, and code quality.

**[CATALOG.md](CATALOG.md)** — Browse all 27 skills and 16 agents with descriptions and file paths. Your starting point for picking what to install.

**[ARTICLE.md](ARTICLE.md)** — The full deep dive: Why this library exists, how rules/skills/agents work together, how to give agents a "soul," and lessons learned building it.

> Deutsche Version: [README_de.md](README_de.md) | [CATALOG_de.md](CATALOG_de.md) | [ARTICLE_de.md](ARTICLE_de.md)

## Quickstart

Tell Claude which skill or agent you want. That's it.

```
Kopiere den Skill aus ~/skill-library/skills/workflow/tdd/SKILL.md in mein Projekt
```

Claude reads the file, copies it to your project's `.claude/skills/` (or `.claude/agents/`), and activates it automatically. Browse the full list in [CATALOG.md](CATALOG.md).

## What's Inside

```
skill-library/
├── templates/
│   └── CLAUDE.md.template      # Generic CLAUDE.md for new projects
├── rules/                      # Always-loaded behavior rules
├── skills/
│   ├── meta/                   # Skills, Agents and Teams bauen
│   ├── build/
│   │   ├── frontend/           # Design & Components
│   │   └── backend/            # Scaffolding & Infrastructure
│   ├── workflow/               # Multi-Agent Workflows
│   └── patterns/               # Reusable Architecture Patterns
└── agents/
    ├── review/                 # Code Review & Audit
    ├── analyze/                # Analysis & Detection
    ├── plan/                   # Planning & Assessment
    └── build/                  # Code Generation & Modification
```

**Skills** teach Claude specialized knowledge and workflows — from TDD cycles and systematic debugging to DI containers and API design. They activate automatically when Claude recognizes the right context.

**Agents** are focused subagents that Claude spawns for specific jobs — reviewing code for security issues, detecting dead code, writing tests, or assessing implementation risks.

**Rules** set global behavior: coding conventions, scope discipline, security defaults, and self-improvement from corrections.

## How It Works

Skills and agents use Claude Code's native extension system. A skill is a `SKILL.md` file with structured knowledge. An agent is a `.md` file with YAML frontmatter that defines a specialized subagent. Rules are always-loaded `.md` files that shape Claude's behavior across all tasks.

Copy what you need into your project's `.claude/` directory — or symlink from this repo to `~/.claude/` for global availability. Customize triggers, add project-specific rules, or combine pieces from multiple skills into your own.

## CLAUDE.md Template

A production-ready CLAUDE.md template is available at `templates/CLAUDE.md.template`:

```bash
cp ~/skill-library/templates/CLAUDE.md.template my-project/CLAUDE.md
```

Covers architecture, commands, import conventions, key patterns, and configuration. Generic rules (DRY, agent behavior, security) live in `rules/` and don't need to be repeated.

## Further Reading

- **[CATALOG.md](CATALOG.md)** — Full catalog of all skills and agents
- **[ARTICLE.md](ARTICLE.md)** — Architecture, design decisions, and usage patterns
