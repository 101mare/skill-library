<p align="center"><img src="docs/images/skill-library.webp" width="80%" alt="Skill Library"></p>

# Skill Library

27 skills, 5 agents, 4 rules — plug into Claude Code, skip the prompt engineering.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Skills: 27](https://img.shields.io/badge/Skills-27-blue.svg)](docs/CATALOG.md)
[![Agents: 5](https://img.shields.io/badge/Agents-5-green.svg)](docs/CATALOG.md)
[![Maintained: yes](https://img.shields.io/badge/Maintained-yes-brightgreen.svg)](https://github.com/101mare/skill-library)

> **Docs:** [CATALOG.md](docs/CATALOG.md) | [SKILLS-EXPLAINED.md](docs/SKILLS-EXPLAINED.md) | [ARTICLE.md](docs/ARTICLE.md) | [GLOBAL-VS-LOCAL.md](docs/GLOBAL-VS-LOCAL.md)
>
> Deutsche Version: [README_de.md](README_de.md) | [SKILLS-EXPLAINED_de.md](docs/SKILLS-EXPLAINED_de.md) | [ARTICLE_de.md](docs/ARTICLE_de.md)

## The Problem

CLAUDE.md files grow into 500-line monsters. The same rules get copy-pasted across projects. Agents labeled "You are an expert" barely outperform no label at all — but [specific experiential identities improve accuracy by 10-60%](https://arxiv.org/abs/2308.07702).

This library fixes that with three layers — **Rules** (always loaded) → **Skills** (on demand) → **Agents** (isolated subprocesses) — each with a clear job and nothing bleeding across. The full rationale is in [ARTICLE.md](docs/ARTICLE.md).

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

### Installing Rules

Rules are always loaded and must be added manually — copy them into `~/.claude/rules/` (global) or `.claude/rules/` (per project):

```bash
cp ~/skill-library/rules/*.md ~/.claude/rules/
```

Then tell Claude:

> Use the tdd skill to add a user registration endpoint

Claude reads the skill, runs RED-GREEN-REFACTOR, and ships tested code — no manual prompting needed.

## Start Here — The Core Five

If you only install five skills, these cover the entire development cycle:

| Skill | What it does | Phase |
|-------|-------------|-------|
| **prompt-builder** | Turns vague requests into structured prompts | Prompt |
| **plan-review** | 4 parallel agents check arch, conventions, risks, reqs | Plan |
| **tdd** | RED-GREEN-REFACTOR with agent orchestration | Build + Test |
| **systematic-debugging** | Reproduce → Isolate → Root-Cause → Fix | Debug |
| **session-verify** | End-of-session security + quality review | Verify |

**Prompt** → **Plan** → **Build + Test** → **Debug** → **Verify** — the entire cycle.

> [!TIP]
> plan-review and session-verify are token-intensive (multiple agents each). For speed: tdd + systematic-debugging alone cover the core work.

## How It Works

```
skill-library/
├── custom/                     # Your project-specific skills & agents
│   ├── skills/                 #   Fork it, add yours here
│   └── agents/                 #   Upstream updates won't touch this
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

<details>
<summary><strong>Design Principles</strong></summary>

**Agent Soul** — Generic labels ("You are an expert") barely move the needle, but specific experiential identities improve accuracy by 10-60% ([NAACL 2024](https://arxiv.org/abs/2308.07702)). What works: a "soul" with concrete experiences, anti-patterns to avoid, and productive weaknesses. Every agent in this library is built on that research.

**Progressive Disclosure** — Skill headers load so Claude knows what's available. Full `SKILL.md` loads on demand. Detailed `reference.md` files load only when needed. Context budget stays tight.

**Context Costs** — Every installed skill costs tokens through its header — on every API call. Install selectively.

</details>

## Custom Skills & Agents

Fork this repo and add your own skills to `custom/skills/` and agents to `custom/agents/`. This folder is yours — upstream updates won't touch it, so you can `git pull` without merge conflicts.

```
Copy the skill from ~/skill-library/custom/skills/my-skill/SKILL.md into my project
```

The meta skills ([skill-builder](skills/meta/skill-builder), [agent-builder](skills/meta/agent-builder)) can generate well-structured custom skills for you. See [custom/README.md](custom/README.md) for details.

## Development

After cloning, install the git hooks once:

```
bash scripts/install-hooks.sh
```

The pre-commit hook auto-regenerates `docs/CATALOG.md` whenever you change files under `skills/`, `agents/`, `rules/`, or `custom/`. The updated catalog is staged into your commit automatically — no manual step needed.

To regenerate manually: `python3 scripts/generate-catalog.py`

## Contributing

Found a bug? Have an idea for a new skill? [Open an issue](https://github.com/101mare/skill-library/issues) or submit a PR.

The meta skills ([skill-builder](skills/meta/skill-builder), [agent-builder](skills/meta/agent-builder), [team-builder](skills/meta/team-builder)) show how to create skills and agents that follow the library's patterns.

## Further Reading

- **[CATALOG.md](docs/CATALOG.md)** — Full catalog of all skills and agents
- **[SKILLS-EXPLAINED.md](docs/SKILLS-EXPLAINED.md)** — Why skills work: progressive disclosure, file system structure, and bundled resources
- **[ARTICLE.md](docs/ARTICLE.md)** — Deep dive: three layers vs. one big CLAUDE.md, agent "soul" design, context budgets, and lessons learned
- **[GLOBAL-VS-LOCAL.md](docs/GLOBAL-VS-LOCAL.md)** — Global vs. local configs: where your configuration lives, when you need this repo, and when you don't
- **[templates/CLAUDE.md.template](templates/CLAUDE.md.template)** — Production-ready CLAUDE.md for new projects

---

**Deutsche Version:** [README_de.md](README_de.md) | [SKILLS-EXPLAINED_de.md](docs/SKILLS-EXPLAINED_de.md) | [ARTICLE_de.md](docs/ARTICLE_de.md)
