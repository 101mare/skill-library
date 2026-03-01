# Skills, Explained: Why Folders of Markdown Files Are So Effective

> [README](../README.md) | [CATALOG](CATALOG.md) | **SKILLS-EXPLAINED** | [ARTICLE](ARTICLE.md)

> [!NOTE]
> This article explains the conceptual foundations of skills — why the format works and what makes it different from saved prompts. For the library's architecture and how to use it, see [ARTICLE.md](ARTICLE.md).

### TL;DR

- **Skills formalize habits:** Instead of losing track of evolved prompts, skills capture them in a canonical, reusable format.
- **Specificity still wins:** AI models can't read minds. Skills do the heavy lifting of specific prompting once, saving you from repeating it.
- **Beyond flat text:** Skills beat saved prompts through progressive disclosure, system structure, and resource bundling.
- **A multiplier for teams:** Skills codify tacit knowledge, standardizing workflows and quality across entire teams.
- **Predictability over capability:** Skills don't give models new abilities; they make complex, repeatable tasks reliable.

---

## The Problem with "Saved Prompts"

You spend 45 minutes perfecting a prompt for code reviews. Two weeks later, your colleague copies it, tweaks it, and within a month three conflicting versions exist. That's **drift** — saved prompts evolve independently and silently diverge.

Then there's **vagueness.** Even the "right" version probably opens with "You are an expert code reviewer." But [research on role-play prompting](https://arxiv.org/abs/2308.07702) (NAACL 2024) found that generic labels produce zero statistically significant improvement. Specific, experiential instructions improved accuracy by 10–60%. The model needs that specificity — but pasting dense blocks of context every time is inefficient and error-prone.

**A skill solves both.** You place instructions into a folder (`SKILL.md`) alongside templates and scripts — one canonical source, version-controlled and shareable. "Use the `tdd` skill" replaces a paragraph of manual instructions.

---

## The Three Pillars of a Skill

### 1. Progressive Disclosure

A saved prompt forces the model to read everything at once. But [research shows](https://arxiv.org/abs/2510.05381) that context length alone degrades LLM performance by 14–85%, even with perfect retrieval. More context isn't free; it actively hurts.

Skills reveal information in layers instead:

```text
┌─────────────────────────────────────────────────────┐
│  Level 1: Skill Headers (Always loaded)             │
│  Name + description → Agent knows what's available  │
│                                                     │
│  ┌───────────────────────────────────────────────┐  │
│  │  Level 2: SKILL.md (Loaded on demand)         │  │
│  │  Core instructions, triggers, and examples    │  │
│  │                                               │  │
│  │  ┌───────────────────────────────────────┐    │  │
│  │  │  Level 3+: Additional Files           │    │  │
│  │  │  reference.md, templates, scripts     │    │  │
│  │  │  (Only read when truly required)      │    │  │
│  │  └───────────────────────────────────────┘    │  │
│  └───────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

The context window stays clean. Details surface only when they matter.

### 2. File System Structure

A saved prompt is a flat string. A skill lives in a folder — and that structure conveys meaning, like a well-organized package that tells you what's inside before you open it. This introduces **modularity**: version-controlled, shareable, composable. All skills in this library follow the [Agent Skills Standard](https://agentskills.io), working across 30+ tools including Claude Code, Cursor, and VS Code. (See the full directory tree in [CATALOG.md](CATALOG.md)).

### 3. Bundled Resources

A saved prompt is limited to text. A skill can bundle appendices, rubrics, or executable tooling. Consider the `ralph-loop` skill:

| File | Purpose |
|------|---------|
| `SKILL.md` | Core instructions for the `/ralph-loop` command |
| `init.md` | Step-by-step setup guide for installing the hook |
| `prompt-template.md` | Template that the agent fills in for each task |
| `hooks/ralph-loop-stop.sh` | Bash hook script — the actual automation engine |

The difference between handing someone instructions and handing them a working tool.

---

## Why This Matters for Teams

For individuals, skills save time. For teams, they scale expertise — specifically the "tacit knowledge" that lives in senior developers' heads and transfers slowly, if at all.

This library's `reviewer.md` agent demonstrates the alternative. Its prompt isn't "You are a security expert." It carries specific, hard-won experiences:

> *"…found SQL injection slip through three rounds of code review, watched silent `except: pass` blocks cause production incidents, traced GDPR violations to debug-level LLM response logs…"*

A junior developer running `/review` on their first PR instantly applies battle-tested patterns that took a senior dev years to accumulate. When the team discovers a new anti-pattern, you update the skill once — not twenty personal notes across twenty developers.

---

## In Practice

Skills don't expand what an LLM can do — they make its output predictable. If you find yourself repeating the same prompting process more than three times, it's time to turn it into a skill. One folder, one source of truth, no more drift.

> [!TIP]
> Want to create your own? The `skill-builder` meta-skill teaches your agent the SKILL.md format, frontmatter conventions, and best practices. Just ask: "Create a skill for [Task]" to get a perfectly structured starting point.

---

*This article is adapted from ["Skills, Explained"](https://x.com/gabrielchua/status/1936752568665473300) by [Gabriel Chua](https://x.com/gabrielchua), reframed for this library's context and enriched with repository examples.*

---

**Deutsche Version:** [SKILLS-EXPLAINED_de.md](SKILLS-EXPLAINED_de.md)
