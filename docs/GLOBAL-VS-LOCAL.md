# Global vs. Local: Where Your Configuration Lives

> [README](../README.md) | [CATALOG](CATALOG.md) | [SKILLS-EXPLAINED](SKILLS-EXPLAINED.md) | [ARTICLE](ARTICLE.md) | **GLOBAL-VS-LOCAL**

### TL;DR

- **Three locations, three purposes** — Global (`~/.claude/`) is your machine's runtime config, Local (`.claude/`) is a project's runtime config, this repository is the source of truth where content is maintained, versioned, and shared
- **The repo is not a competitor to global/local** — it's the source that feeds both. The relationship is: Repo → (copy/symlink) → Global or Local → Claude Code reads it
- **Honest answer:** A solo developer on one machine with two projects probably doesn't need this repo. A team, multiple machines, or anyone who shares configs does
- **Global ≠ "everything everywhere"** — install what you need, not what you might someday need. Every skill header costs tokens on every API call

### Contents

1. [The Three Locations](#the-three-locations) — Global, Local, and this Repository
2. [What Goes Where](#what-goes-where) — Recommendations for each type of content
3. [CLAUDE.md: The Full Hierarchy](#claudemd-the-full-hierarchy) — Multiple levels, scoped authority, loading order
4. [How They Interact](#how-they-interact) — Override, shadow, and merge behavior
5. [Where This Repository Fits](#where-this-repository-fits) — Source of truth, not runtime target
6. [Honest Assessment](#honest-assessment-when-you-need-this-repo-and-when-you-dont) — When you need this repo and when you don't
7. [Recommended Setup](#recommended-setup) — Three tiers from minimal to full

---

## The Three Locations

Claude Code reads configuration from two locations at runtime. This repository is a third location that exists outside of Claude Code's runtime — it's where the content is authored and maintained.

### Global: `~/.claude/`

Your machine-wide configuration. Everything here applies to **every project** you open with Claude Code.

| Directory | What it holds | Loading behavior |
|-----------|--------------|-----------------|
| `~/.claude/rules/*.md` | Behavior rules | Always loaded into every prompt |
| `~/.claude/skills/[name]/SKILL.md` | Skill definitions | Headers always loaded; full content on demand |
| `~/.claude/agents/[name].md` | Agent definitions | Loaded when explicitly referenced |
| `~/.claude/settings.json` | Tool permissions, model preferences | Merged with local settings |

**Use global for:** Standards that apply to all your work — coding conventions, security defaults, agent behavior, core workflow skills.

### Local: `.claude/`

Project-specific configuration. Lives inside the project directory and is typically committed to the project's Git repository.

| File / Directory | What it holds | Loading behavior |
|-----------------|--------------|-----------------|
| `.claude/CLAUDE.md` | Project context, constraints, architecture | Always loaded |
| `.claude/rules/*.md` | Project-specific rules | Always loaded; extends or overrides global |
| `.claude/skills/[name]/SKILL.md` | Project-specific skills | Headers always loaded; full content on demand |
| `.claude/agents/[name].md` | Project-specific agents | Loaded when explicitly referenced |
| `.claude/memory.md` | Lessons learned in this project | Loaded at session start |
| `.claude/settings.local.json` | Project settings, hooks | Merged with global settings |

**Use local for:** What makes this project different — its architecture, its commands, its domain-specific skills, its lessons learned.

### This Repository: `~/skill-library/`

A Git repository containing curated, documented, versioned content that you copy or symlink into global or local locations.

| Directory | What it holds | How it reaches Claude Code |
|-----------|--------------|---------------------------|
| `rules/` | 4 universal behavior rules | Copy to `~/.claude/rules/` or `.claude/rules/` |
| `skills/` | 27 reusable skills | Symlink to `~/.claude/skills/` or copy to `.claude/skills/` |
| `agents/` | 5 specialized agents | Copy to `.claude/agents/` when needed |
| `templates/` | CLAUDE.md template | Copy and customize per project |
| `custom/` | Your personal extensions | Fork area, upstream won't touch |
| `docs/` | Catalog, articles, explanations | Reference only, not installed |

**This is not a runtime location.** Claude Code never reads from `~/skill-library/` directly. The repo is where you maintain content; global and local are where Claude Code consumes it.

---

## What Goes Where

| Content | Where | Why |
|---------|-------|-----|
| Coding conventions (DRY, types, error handling) | **Global rules** | Same standards everywhere |
| Agent behavior (read-first, scope discipline) | **Global rules** | Same working style everywhere |
| Security defaults (input validation, PII, secrets) | **Global rules** | Non-negotiable, everywhere |
| Self-improvement (capture lessons, review at start) | **Global rules** | Same learning loop everywhere |
| Core workflow skills (tdd, debugging, plan-review) | **Global skills** | Used in most projects |
| Architecture pattern skills (DI, API design) | **Global skills** | Reusable across projects |
| Meta skills (skill-builder, agent-builder) | **Global skills** | Project-agnostic |
| Frontend design skills | **Global skills** (if you do frontend) | Reusable design principles |
| Project scaffold, Docker, CI/CD skills | **Global skills** or **don't install** | Used once per project; install on demand |
| Project architecture, constraints, commands | **Local CLAUDE.md** | Unique to this project |
| Domain-specific skills (your DB schema, your API quirks) | **Local skills** | Unique to this project |
| Lessons learned, workarounds discovered | **Local memory.md** | Per-project wisdom |
| Hook configuration (Ralph Loop, custom hooks) | **Local settings** | Per-project automation |

> [!TIP]
> **The litmus test:** If you'd copy-paste it into a new project unchanged, it belongs in global. If you'd customize it for the new project, it belongs in local. If you'd version-control and share it, it belongs in this repo.

---

## CLAUDE.md: The Full Hierarchy

CLAUDE.md is special — it's not just "one file at one location." Claude Code supports CLAUDE.md files at **multiple levels simultaneously**, and they all get loaded. Here's how it actually works:

### The Two-File Mental Model

Before diving into the full hierarchy, understand the fundamental split:

**Global file (`~/.claude/CLAUDE.md`): Who the agent IS.**

Identity and how to work with you. Core decision-making principles. What the agent won't do. How it learns and evolves.

**Project file (`/your-project/CLAUDE.md`): What the agent DOES here.**

Core execution philosophy for this project. Autonomy levels — what it can do without asking. Key paths — where things live. Pointers to reference docs (loaded on demand).

The most common mistake is putting everything in one place. Identity leaks into project specifics. Commands get mixed with philosophy. The agent gets confused about what is a rule versus what is context.

Separation solves this. Global = constant. Project = contextual.

But there's a second mistake that takes longer to see: treating both files as encyclopedias instead of routing layers. A CLAUDE.md shouldn't try to contain everything — it should point to the right rules, skills, and subdirectory CLAUDE.md files that hold the actual detail. Keep both files lean; let the three-layer architecture carry the weight.

### Where CLAUDE.md Can Exist

| Level | Location | When loaded | Scope |
|-------|----------|------------|-------|
| **Global** | `~/.claude/CLAUDE.md` | At startup | All projects on this machine |
| **Project root** | `./CLAUDE.md` or `./.claude/CLAUDE.md` | At startup, fully | This project |
| **Subdirectory** | `./src/CLAUDE.md`, `./packages/api/CLAUDE.md` | On-demand | That directory only |
| **Local (private)** | `./CLAUDE.local.md` | At startup | This project, not committed to git |

### Subdirectory CLAUDE.md: Scoped Authority

This is the part most people miss: **you can place a CLAUDE.md in any subdirectory, and it has authority over that subtree.** Claude loads it on-demand — not at startup, but when it accesses files in that directory.

```
my-project/
├── CLAUDE.md                    ← Project-wide (loaded at startup)
├── src/
│   ├── api/
│   │   └── CLAUDE.md            ← Only loaded when Claude works in src/api/
│   └── workers/
│       └── CLAUDE.md            ← Only loaded when Claude works in src/workers/
└── packages/
    └── billing/
        └── CLAUDE.md            ← Only loaded when Claude works in packages/billing/
```

**Why this matters:** You can scope instructions to the code they apply to. The billing module's CLAUDE.md can describe its schema quirks without polluting the global prompt. The API directory's CLAUDE.md can list its endpoint conventions. These only cost tokens when Claude actually works in those directories.

### Loading Order and Priority

Claude Code discovers CLAUDE.md files by recursing upward from the current working directory to the project root. More specific (deeper) instructions take precedence over general ones:

```
Priority (highest to lowest):
  1. Managed policy         (organization-wide, if configured)
  2. ~/.claude/CLAUDE.md    (global user)
  3. ./CLAUDE.md            (project root)
  4. ./CLAUDE.local.md      (private, not in git)
  5. Subdirectory CLAUDE.md (on-demand, scoped to subtree)
```

When instructions conflict, the **more specific file wins.** A subdirectory CLAUDE.md saying "use tabs" overrides a project root CLAUDE.md saying "use spaces" — but only for files in that subdirectory.

### CLAUDE.md vs. CLAUDE.local.md

| | `CLAUDE.md` | `CLAUDE.local.md` |
|---|---|---|
| **Committed to git** | Yes (shared with team) | No (gitignored, private) |
| **Use for** | Team standards, architecture, conventions | Personal preferences, local paths, API keys references |
| **Example** | "Use PostgreSQL, not MySQL" | "My local DB runs on port 5433" |

### Practical Implications for This Library

The library's `rules/` directory maps to `~/.claude/rules/` (global) — these are always loaded. But if you need project-scoped behavior, CLAUDE.md at the right level is more appropriate than a rule file:

- **Universal standards** → Global rules (`~/.claude/rules/*.md`)
- **Project-wide context** → Project root `CLAUDE.md`
- **Module-specific knowledge** → Subdirectory `CLAUDE.md`
- **Personal preferences** → `CLAUDE.local.md`

> [!TIP]
> Subdirectory CLAUDE.md files are a powerful alternative to project-specific skills. If the knowledge only matters for one directory, a CLAUDE.md there is simpler and more focused than a skill — and it costs zero tokens when Claude isn't working in that directory.

---

## How They Interact

### Priority: Local Shadows Global

When the same name exists in both locations, local wins:

```
Claude Code reads:
  1. ~/.claude/rules/security.md          (global)
  2. .claude/rules/security.md            (local — shadows global if same filename)

  1. ~/.claude/skills/tdd/SKILL.md        (global)
  2. .claude/skills/tdd/SKILL.md          (local — shadows global if same name)
```

### Rules: Coexist, Local Can Override

Global rules are loaded first. Local rules are loaded after. If a local rule has the same filename as a global rule, the local version replaces it. Different filenames coexist — you get both.

### Skills: First Match Wins

Claude checks local first, then global. If `.claude/skills/tdd/` exists, it uses that. If not, it falls back to `~/.claude/skills/tdd/`. They don't merge — it's one or the other.

### Settings: Merged, Local Overwrites Keys

```json
// ~/.claude/settings.json
{ "autoCompact": true }

// .claude/settings.local.json
{ "hooks": { "Stop": [...] } }

// Effective:
{ "autoCompact": true, "hooks": { "Stop": [...] } }
```

Same keys in local overwrite global. Different keys coexist.

### The Flow

```
┌─────────────────────┐
│  skill-library/     │  Source of truth
│  (this repo)        │  Versioned, documented, shared
└────────┬────────────┘
         │
         │  copy / symlink
         │
    ┌────▼──────────┐        ┌──────────────────┐
    │  ~/.claude/   │        │  .claude/        │
    │  (global)     │        │  (local/project) │
    │               │        │                  │
    │  rules/       │───────▶│  rules/          │  local shadows global
    │  skills/      │───────▶│  skills/         │  local shadows global
    │  agents/      │───────▶│  agents/         │  local shadows global
    │  settings     │───────▶│  settings.local  │  merged, local overwrites
    └───────────────┘        └──────────────────┘
              │                       │
              └───────────┬───────────┘
                          │
                          ▼
                  ┌───────────────┐
                  │  Claude Code  │  Runtime reads from both
                  └───────────────┘
```

---

## Where This Repository Fits

This repository is **not** a global or local configuration directory. It's a **source** that feeds into both.

### What the repo IS

- **A versioned collection** — Git history tracks every change. `~/.claude/` has no history; edits are permanent.
- **A distribution channel** — Others can fork, clone, browse, contribute. `~/.claude/` is private files on your machine.
- **A documentation hub** — Catalog, articles, explanations. Global/local configs are just files in a folder.
- **A sync mechanism** — Symlink once, `git pull` to update everywhere. Without the repo, you copy-paste and drift.
- **A fork point** — `custom/` folder lets you add your own skills without merge conflicts on upstream updates.

### What the repo IS NOT

- **Not a runtime dependency** — Claude Code never reads from `~/skill-library/` directly.
- **Not a framework** — No install scripts, no build steps, no lock files. It's just Markdown files.
- **Not required for Claude Code to work** — You can write rules, skills, and agents from scratch without it.

### Two installation patterns

**Symlink** (recommended for skills you want to keep updated):
```bash
ln -s ~/skill-library/skills/workflow/tdd ~/.claude/skills/tdd
```
- Changes in repo propagate immediately
- `git pull` updates all symlinked skills at once
- Best for: global skills you want to keep current

**Copy** (for content you want to own and customize):
```bash
cp ~/skill-library/rules/*.md ~/.claude/rules/
cp -r ~/skill-library/skills/workflow/tdd .claude/skills/tdd
```
- Your copy diverges independently
- Manual sync needed
- Best for: rules (rarely change) and project-local skills (customized per project)

---

## Honest Assessment: When You Need This Repo (and When You Don't)

### When you probably DON'T need this repo

**Solo developer, one machine, 1-2 projects with similar stacks:**

Copy the four rule files into `~/.claude/rules/`. Write your skills directly in `~/.claude/skills/`. Done. You get the same runtime behavior without maintaining a separate repository. The rules in this repo are good starting points, but once they're in `~/.claude/rules/`, the repo served its purpose.

**You only need 2-3 skills:**

Create them directly in `~/.claude/skills/`. No repo needed. The overhead of cloning, symlinking, and pulling updates isn't worth it for a handful of files you could write yourself.

**You never share your configuration:**

Global configs on your machine work fine for personal use. The repo's main advantage — sharing, collaboration, distribution — is irrelevant if nobody else ever sees your configs.

### When you DO need this repo

**Multiple machines:**

Clone the repo on each machine, symlink to `~/.claude/`. One `git pull` updates everything everywhere. Without the repo, you're manually syncing files across machines — and they will drift.

**Team or organization:**

Everyone clones the same repo. New team members have instant access to 27 tested skills, 5 specialized agents, and 4 rule files. Without the repo, each person builds their own setup from scratch and you end up with the exact problem this library was built to solve: five people, five diverging configs.

**You want version history:**

`~/.claude/rules/security.md` has no history. You edit it, the old version is gone. The repo gives you Git history, blame, diff, and the ability to revert.

**You want to contribute or receive updates:**

The repo is maintained and updated. Skills get refined, new ones get added, bugs get fixed. `git pull` gets you all of that. Without the repo, you're frozen at whatever version you copied.

**You build custom skills and want a clean separation:**

The `custom/` folder gives you a dedicated place for your own skills that won't be touched by upstream updates. Without the repo's structure, you mix your custom work with borrowed content and lose track of what came from where.

### Decision Matrix

| Scenario | Repo needed? | Recommended setup |
|----------|-------------|-------------------|
| Solo dev, one machine, one project | No | Copy rules to global, write skills manually |
| Solo dev, one machine, 5+ projects | Maybe | Symlink core skills for consistency |
| Solo dev, multiple machines | Yes | Clone repo, symlink to `~/.claude/` |
| Small team (2-5 people) | Yes | Shared repo, each member clones |
| Team + open source projects | Yes | Fork repo, add to `custom/`, share with team |
| Organization with standards | Yes | Fork repo, enforce rules via CI |

---

## Recommended Setup

### Minimal: Just Rules

Copy the four rule files and use Claude Code's built-in capabilities for everything else.

```bash
cp ~/skill-library/rules/*.md ~/.claude/rules/
```

**What you get:** Consistent coding conventions, security defaults, and agent behavior across all projects. No skill overhead.

**Best for:** Developers who want a solid baseline without committing to the full library.

### Standard: Rules + Core Five Skills

The rules plus the five skills that cover the entire development cycle.

```bash
# Rules
cp ~/skill-library/rules/*.md ~/.claude/rules/

# Core workflow skills (symlinked for updates)
ln -s ~/skill-library/skills/build/backend/prompt-builder ~/.claude/skills/prompt-builder
ln -s ~/skill-library/skills/workflow/plan-review ~/.claude/skills/plan-review
ln -s ~/skill-library/skills/workflow/tdd ~/.claude/skills/tdd
ln -s ~/skill-library/skills/patterns/systematic-debugging ~/.claude/skills/systematic-debugging
ln -s ~/skill-library/skills/workflow/session-verify ~/.claude/skills/session-verify
```

**What you get:** Prompt → Plan → Build+Test → Debug → Verify — the entire cycle.

**Best for:** Most developers who want a structured workflow without installing everything.

### Full: Symlinked Skill Categories

Symlink entire skill categories based on your work.

```bash
# Rules (always)
cp ~/skill-library/rules/*.md ~/.claude/rules/

# All workflow skills
for skill in ~/skill-library/skills/workflow/*/; do
  ln -s "$skill" ~/.claude/skills/$(basename "$skill")
done

# All pattern skills
for skill in ~/skill-library/skills/patterns/*/; do
  ln -s "$skill" ~/.claude/skills/$(basename "$skill")
done

# Backend build skills (if you do backend)
for skill in ~/skill-library/skills/build/backend/*/; do
  ln -s "$skill" ~/.claude/skills/$(basename "$skill")
done

# Meta skills (if you build custom skills)
for skill in ~/skill-library/skills/meta/*/; do
  ln -s "$skill" ~/.claude/skills/$(basename "$skill")
done
```

**What you get:** The full toolkit. Every skill available on demand.

**Trade-off:** More skill headers in every prompt = higher token cost per API call. Only install categories you actually use.

> [!WARNING]
> Every installed skill costs tokens through its header on every API call. The full setup adds ~27 headers. If you're cost-sensitive or work on short tasks, stick with Standard.

---

**Deutsche Version:** [GLOBAL-VS-LOCAL_de.md](GLOBAL-VS-LOCAL_de.md)
