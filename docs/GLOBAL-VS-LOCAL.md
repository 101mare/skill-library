# Global vs. Local: Where Your Configuration Lives

> [README](../README.md) | [CATALOG](CATALOG.md) | [SKILLS-EXPLAINED](SKILLS-EXPLAINED.md) | [ARTICLE](ARTICLE.md) | **GLOBAL-VS-LOCAL**

### TL;DR

- **Three locations, three purposes** — Global (`~/.claude/`) applies to every project on your machine, Local (`.claude/`) is project-specific, this repository is the versioned source that feeds both via copy or symlink
- **Honest answer:** A solo developer on one machine with two projects probably doesn't need this repo. A team, multiple machines, or anyone who shares configs does
- **Global ≠ "everything everywhere"** — every installed skill header costs tokens on every API call. Install selectively

---

## Where Things Live

| What | Global `~/.claude/` | Local `.claude/` | This Repo |
|------|---------------------|------------------|-----------|
| Rules | `rules/*.md` — always loaded | `rules/*.md` — extends or overrides global | `rules/` — copy to either |
| Skills | `skills/[name]/SKILL.md` — headers always loaded, full content on demand | same — shadows global | `skills/` — symlink or copy |
| Agents | `agents/[name].md` — loaded on reference | same — shadows global | `agents/` — copy when needed |
| Settings | `settings.json` — merged with local | `settings.local.json` — overwrites matching keys | n/a |
| Project context | n/a | `CLAUDE.md`, `memory.md` — always loaded | `templates/` — copy & customize |

This repo is **not** a runtime location. Claude Code never reads from `~/skill-library/` directly.

**Symlink** skills you want to keep updated, **copy** content you want to own. See [README Quickstart](../README.md#quickstart) for commands.

> [!TIP]
> **The litmus test:** If you'd copy-paste it into a new project unchanged, it belongs in global. If you'd customize it, it belongs in local. If you'd version-control and share it, it belongs in this repo.

---

## How They Interact

### Resolution Rules

When the same name exists in both locations, **local wins**:

```
Claude Code reads:
  1. ~/.claude/rules/security.md          (global)
  2. .claude/rules/security.md            (local — replaces global if same filename)

  1. ~/.claude/skills/tdd/SKILL.md        (global)
  2. .claude/skills/tdd/SKILL.md          (local — shadows global if same name)
```

- **Rules:** Global loaded first, local after. Same filename → local replaces global. Different filenames coexist.
- **Skills:** Local checked first, then global. First match wins — they don't merge.
- **CLAUDE.md:** Loaded by walking up the directory tree — if you run Claude in `foo/bar/`, it loads both `foo/bar/CLAUDE.md` and `foo/CLAUDE.md`. CLAUDE.md files in subdirectories load on demand when Claude reads files there. ([docs](https://code.claude.com/docs/en/memory#how-claudemd-files-load))

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

## Do You Need This Repo?

| Scenario | Repo needed? | Recommended setup |
|----------|-------------|-------------------|
| Solo dev, one machine, one project | No | Copy rules to global, write skills manually |
| Solo dev, one machine, 5+ projects | Maybe | Symlink core skills for consistency |
| Solo dev, multiple machines | Yes | Clone repo, symlink to `~/.claude/` |
| Small team (2-5 people) | Yes | Shared repo, each member clones |
| Team + open source projects | Yes | Fork repo, add to `custom/`, share with team |
| Organization with standards | Yes | Fork repo, enforce rules via CI |

For installation commands, see [README Quickstart](../README.md#quickstart).

---

**Deutsche Version:** [GLOBAL-VS-LOCAL_de.md](GLOBAL-VS-LOCAL_de.md)
