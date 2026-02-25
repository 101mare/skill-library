<p align="center"><img src="docs/images/skill-library.png" width="80%" alt="Skill Library"></p>

# Skill Library

27 skills, 5 agents, 4 rules — copy what you need, skip the rest.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Skills: 27](https://img.shields.io/badge/Skills-27-blue.svg)](docs/CATALOG.md)
[![Agents: 5](https://img.shields.io/badge/Agents-5-green.svg)](docs/CATALOG.md)
[![Maintained: yes](https://img.shields.io/badge/Maintained-yes-brightgreen.svg)](https://github.com/101mare/skill-library)

> **Important Docs:** [README.md](README.md) | [CATALOG.md](docs/CATALOG.md) | [ARTICLE.md](docs/ARTICLE.md)
>
> Deutsche Version: [README_de.md](README_de.md) | [CATALOG_de.md](docs/CATALOG_de.md) | [ARTICLE_de.md](docs/ARTICLE_de.md)

## Quickstart

Browse **[CATALOG.md](docs/CATALOG.md)** to see what's available, pick what you need, then tell Claude to install it. Three ways:

**From GitHub** (no clone needed):
```
Copy the skill from https://github.com/101mare/skill-library/tree/main/skills/workflow/tdd into my project
```

**From a local clone:**
```
Copy the skill from ~/skill-library/skills/workflow/tdd/SKILL.md into my project
```

**Global** (symlink into `~/.claude/` — available in all projects, updates via `git pull` apply everywhere):
```bash
ln -s ~/skill-library/skills/workflow/tdd ~/.claude/skills/tdd
```

Claude reads the file, copies it to your project's `.claude/skills/` (or `.claude/agents/`), and activates it automatically. Browse the full list in **[CATALOG.md](docs/CATALOG.md)**.

## Why This Exists

CLAUDE.md files grow into 500-line monsters. The same rules get copy-pasted across projects. Agents with generic labels like "You are an expert" show [no measurable improvement](https://arxiv.org/abs/2308.07702) over no label at all.

This library solves that with **three layers**: Rules (always loaded, shape behavior) → Skills (loaded on demand, teach workflows) → Agents (isolated subprocesses, do delegated work). Each layer has a clear job, and nothing bleeds across. The full rationale — including the research behind our agent design — is in **[ARTICLE.md](docs/ARTICLE.md)**.

## Start Here — The Core Five

If you only install five skills, these cover the entire development cycle:

1. **prompt-builder** — Asks clarifying questions about your goal, then turns vague requests into structured prompts — whether for a plan, direct implementation, or any other task.
2. **plan-review** — Four parallel review agents check architecture fit, conventions, risks, and requirements. Traffic light verdict *before* code exists.
3. **tdd** — Real RED-GREEN-REFACTOR with agent orchestration. Tests define behavior, not confirm code.
4. **systematic-debugging** — 4-phase methodology: Reproduce → Isolate → Root-Cause → Fix+Defend.
5. **session-verify** — End-of-session review: security, code quality, architecture, clean imports, no leftover TODOs. Nothing ships unchecked.

The logic: **Prompt** → **Plan** → **Build + Test** → **Debug** → **Verify**. The entire cycle, five skills.

> **Note:** This is a defensive, token-intensive setup — plan-review and session-verify both spawn multiple agents. If you want to move fast and cheap, tdd + systematic-debugging alone cover the core work.

## What's Inside

```
skill-library/
├── docs/                       # CATALOG + ARTICLE (EN + DE)
├── templates/
│   └── CLAUDE.md.template      # Generic CLAUDE.md for new projects
├── rules/                      # Always-loaded behavior rules
├── skills/
│   ├── meta/                   # Building Skills, Agents & Teams
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

**Skills** teach Claude specialized knowledge — TDD cycles, debugging methodology, API design, DI containers. They activate automatically when Claude recognizes the right context.

**Agents** are isolated subprocesses Claude spawns for specific jobs — code review, dead code detection, test writing. They receive zero parent context and return a result.

**Rules** set global behavior: coding conventions, scope discipline, security defaults, self-improvement from corrections.

Key difference: Skills instruct, Agents work. A workflow skill like `plan-review` spawns 4 agents in parallel and aggregates their results into a single verdict.

## Key Concepts

**Three Layers** — Rules (always loaded) → Skills (on demand) → Agents (delegated). Rules shape every interaction. Skills activate when relevant. Agents run as isolated subprocesses with their own tools and context.

**Agent Soul** — Generic labels ("You are an expert") have zero statistically significant effect ([NAACL 2024](https://arxiv.org/abs/2308.07702)). What works: specific identity, anti-patterns to avoid, productive weaknesses. Each agent file in this library is built on that research.

**Progressive Disclosure** — Skill headers (name + description) are always loaded so Claude knows what's available. The full `SKILL.md` loads on demand. Detailed `reference.md` files load only when needed. This keeps the context budget tight.

## Context Costs

Every installed skill costs tokens through its header description — on every API call. 27 skills with 3-4 lines each are ~100 lines of permanent system prompt. Install selectively: the Core Five above cover most needs. Add specialists as your project demands them.

## CLAUDE.md Template

A production-ready CLAUDE.md template is available at `templates/CLAUDE.md.template`.

Covers architecture, commands, import conventions, key patterns, and configuration. Generic rules (DRY, agent behavior, security) live in `rules/` and don't need to be repeated.

## Further Reading

- **[CATALOG.md](docs/CATALOG.md)** — Full catalog of all skills and agents
- **[ARTICLE.md](docs/ARTICLE.md)** — The full deep dive: why three layers instead of one big CLAUDE.md, how to give agents a "soul" backed by NAACL 2024 research, context budget management, and the lessons learned building 27 skills. If you want to understand the *thinking* behind this library, start here.

---

**Deutsche Version:** [README_de.md](README_de.md) | [CATALOG_de.md](docs/CATALOG_de.md) | [ARTICLE_de.md](docs/ARTICLE_de.md)
