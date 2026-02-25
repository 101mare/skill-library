<p align="center"><img src="docs/images/skill-library.png" width="80%" alt="Skill Library"></p>

# Skill Library

27 skills, 5 agents, 4 rules — copy what you need, skip the rest.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Skills: 27](https://img.shields.io/badge/Skills-27-blue.svg)](docs/CATALOG.md)
[![Agents: 5](https://img.shields.io/badge/Agents-5-green.svg)](docs/CATALOG.md)
[![Maintained: yes](https://img.shields.io/badge/Maintained-yes-brightgreen.svg)](https://github.com/101mare/skill-library)

> **Docs:** [CATALOG.md](docs/CATALOG.md) | [ARTICLE.md](docs/ARTICLE.md)
>
> Deutsche Version: [README_de.md](README_de.md) | [CATALOG_de.md](docs/CATALOG_de.md) | [ARTICLE_de.md](docs/ARTICLE_de.md)

## The Problem

CLAUDE.md files grow into 500-line monsters. The same rules get copy-pasted across projects. Agents labeled "You are an expert" show [no measurable improvement](https://arxiv.org/abs/2308.07702) over no label at all.

This library fixes that with three layers — **Rules** (always loaded) → **Skills** (on demand) → **Agents** (isolated subprocesses) — each with a clear job and nothing bleeding across. The full rationale is in [ARTICLE.md](docs/ARTICLE.md).

## Start Here — The Core Five

If you only install five skills, these cover the entire development cycle:

1. **prompt-builder** — Asks clarifying questions, then turns vague requests into structured prompts.
2. **plan-review** — Four parallel agents check architecture, conventions, risks, and requirements. Traffic light verdict *before* code exists.
3. **tdd** — Real RED-GREEN-REFACTOR with agent orchestration. Tests define behavior, not confirm code.
4. **systematic-debugging** — Reproduce → Isolate → Root-Cause → Fix+Defend.
5. **session-verify** — End-of-session review: security, code quality, architecture, clean imports, no leftover TODOs.

**Prompt** → **Plan** → **Build + Test** → **Debug** → **Verify** — the entire cycle.

> **Note:** plan-review and session-verify are token-intensive (multiple agents each). For speed: tdd + systematic-debugging alone cover the core work.

## Quickstart

Browse **[CATALOG.md](docs/CATALOG.md)**, pick what you need, tell Claude to install it:

**From GitHub** (no clone needed):
```
Copy the skill from https://github.com/101mare/skill-library/tree/main/skills/workflow/tdd into my project
```

**From a local clone:**
```
Copy the skill from ~/skill-library/skills/workflow/tdd/SKILL.md into my project
```

**Global** (symlink — available everywhere, updates via `git pull`):
```bash
ln -s ~/skill-library/skills/workflow/tdd ~/.claude/skills/tdd
```

Claude reads the file, copies it to `.claude/skills/` (or `.claude/agents/`), and activates it automatically.

## How It Works

```
skill-library/
├── docs/                       # CATALOG + ARTICLE (EN + DE)
├── templates/
│   └── CLAUDE.md.template      # Production-ready CLAUDE.md for new projects
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

**Rules** set global behavior — coding conventions, scope discipline, security defaults. Always loaded, shape every interaction.

**Skills** teach Claude specialized workflows — TDD cycles, debugging methodology, API design. Headers always visible; full content loads on demand.

**Agents** are isolated subprocesses for specific jobs — code review, dead code detection, test writing. Zero parent context in, result out.

The key difference: Skills instruct, Agents work. A workflow skill like `plan-review` spawns 4 agents in parallel and aggregates their verdicts.

## Design Principles

**Agent Soul** — Generic labels ("You are an expert") have zero significant effect ([NAACL 2024](https://arxiv.org/abs/2308.07702)). What works: specific identity, anti-patterns to avoid, productive weaknesses. Every agent in this library is built on that research.

**Progressive Disclosure** — Skill headers load so Claude knows what's available. Full `SKILL.md` loads on demand. Detailed `reference.md` files load only when needed. Context budget stays tight.

**Context Costs** — Every installed skill costs tokens through its header — on every API call. 27 skills ≈ 100 lines of permanent system prompt. Install selectively.

## Further Reading

- **[CATALOG.md](docs/CATALOG.md)** — Full catalog of all skills and agents
- **[ARTICLE.md](docs/ARTICLE.md)** — Deep dive: three layers vs. one big CLAUDE.md, agent "soul" design, context budgets, and lessons from building 27 skills
- **[templates/CLAUDE.md.template](templates/CLAUDE.md.template)** — Production-ready CLAUDE.md for new projects

---

**Deutsche Version:** [README_de.md](README_de.md) | [CATALOG_de.md](docs/CATALOG_de.md) | [ARTICLE_de.md](docs/ARTICLE_de.md)
