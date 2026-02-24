# Skill Library

A curated, hierarchically organized collection of Claude Code skills and agents. Source of truth for reusable AI-assisted development workflows.

For a detailed walkthrough of the architecture, design decisions and usage patterns, see [article.md](article.md).

## Structure

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

## Setup

Browse the categories, pick what you need, and copy the `.md` files into your project's `.claude/` directory. Alternatively, you can symlink them from this repo to `~/.claude/rules/`, `~/.claude/skills/` and `~/.claude/agents/` for global availability.

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

For a full catalog of all skills and agents with descriptions, see [CATALOG.md](CATALOG.md).
