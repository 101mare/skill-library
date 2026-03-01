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

You spent 45 minutes perfecting a prompt for code reviews. It finally catches edge cases, enforces your team's conventions, and outputs results in the right format. Two weeks later, your colleague asks for it — but you've already tweaked your version twice. They paste their copy into a notes app, add their own rules, remove some of yours. Within a month, three conflicting versions exist and nobody knows which one is "right."

This is the first failure mode: **drift.** Saved prompts evolve independently and silently diverge.

The second failure mode is **vagueness.** Even the "right" version of that prompt probably opens with something like "You are an expert code reviewer." Sounds reasonable — but [research on role-play prompting](https://arxiv.org/abs/2308.07702) (NAACL 2024) found that generic labels like this produce zero statistically significant improvement over no label at all. What *does* work are specific, experiential instructions — and those improved accuracy by 10–60% across 12 reasoning benchmarks. The model needs that specificity, but pasting dense blocks of context every time is inefficient and error-prone.

**A skill solves both problems at once.** Instead of a drifting text snippet, you place instructions into a dedicated folder (using a `SKILL.md` file) alongside templates and scripts. One canonical source, version-controlled and shareable. "Use the `tdd` skill to add an endpoint" replaces a paragraph of manual instructions. A one-off attempt becomes a repeatable workflow.

Here's what that shift looks like in practice:

```text
  SAVED PROMPT                        SKILL FOLDER
  ─────────────                       ─────────────
  "You are an expert code             tdd/
   reviewer. Always check              ├── SKILL.md          (core instructions)
   for SQL injection,                  ├── reference.md      (detailed checklists)
   ensure type hints..."               ├── anti-patterns.md  (what to avoid)
                                       └── examples/         (real-world samples)
  ┌──────────────────┐
  │  A flat string.  │                ┌──────────────────────────────────┐
  │  No structure.   │                │  A folder. Version-controlled.   │
  │  No versioning.  │                │  Modular. Composable. Shareable. │
  │  No resources.   │                │  Bundled with scripts & context. │
  └──────────────────┘                └──────────────────────────────────┘
```

---

## The Three Pillars of a Skill

What turns a folder of Markdown files into something fundamentally better than a saved prompt? Three things.

### 1. Progressive Disclosure

A saved prompt forces the model to read everything at once — every rule, every edge case — regardless of relevance. [Research shows](https://arxiv.org/abs/2510.05381) that context length alone degrades LLM performance by 14–85%, even when all relevant information is perfectly retrievable. More context isn't free; it actively hurts.

A skill solves this by revealing information in layers:

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

A saved prompt is a flat string. A skill lives in a folder — and that folder structure itself conveys meaning, the same way a well-organized package tells you what's inside before you open it. (See the full directory tree in [CATALOG.md](CATALOG.md)).

This introduces **modularity**. A skill is a self-contained unit that can be version-controlled, shared, and composed with others. All skills in this library follow the [Agent Skills Standard](https://agentskills.io), ensuring they work seamlessly across 30+ tools, including Claude Code, Cursor, and VS Code.

### 3. Bundled Resources

A saved prompt is limited to the text you paste. A skill can bundle appendices, evaluation rubrics, or even executable tooling.

Consider the `ralph-loop` skill — an autonomous iteration loop that keeps Claude working until a task is done:

| File | Purpose |
|------|---------|
| `SKILL.md` | Core instructions for the `/ralph-loop` command |
| `init.md` | Step-by-step setup guide for installing the hook |
| `prompt-template.md` | Template that the agent fills in for each task |
| `hooks/ralph-loop-stop.sh` | Bash hook script — the actual automation engine |

This is the difference between telling someone "here are instructions for running tests" and handing them a test runner that validates their work.

---

## Why This Matters for Teams

For individuals, skills save time. For teams, they scale expertise.

Much of what makes a senior developer valuable is "tacit knowledge" — knowing which assumptions to test, what to verify before deploying, and what "good enough" actually looks like. This knowledge usually lives in people's heads and transfers slowly, if at all.

This library's `reviewer.md` agent demonstrates the alternative. Its prompt isn't "You are a security expert." It carries specific, hard-won experiences:

> *"…found SQL injection slip through three rounds of code review, watched silent `except: pass` blocks cause production incidents, traced GDPR violations to debug-level LLM response logs…"*

Packaged as a skill, a junior developer running `/review` on their first pull request instantly applies the same battle-tested patterns that took a senior dev years to accumulate. When the team discovers a new anti-pattern, you update the skill once — not twenty personal notes across twenty developers.

---

## In Practice

Skills don't magically expand what an LLM can do. They make its output predictable and consistent. If you find yourself repeating the same prompting process more than three times, that repetition is a signal: it's time to turn it into a skill.

Remember the code review prompt from the beginning? The one that drifted into three conflicting versions? As a skill, it would live in one folder, evolve in one place, and work the same way for everyone.

> [!TIP]
> Want to create your own? The `skill-builder` meta-skill teaches your agent the SKILL.md format, frontmatter conventions, and best practices. Just ask: "Create a skill for [Task]" to get a perfectly structured starting point.

---

*This article is adapted from ["Skills, Explained"](https://x.com/gabrielchua/status/1936752568665473300) by [Gabriel Chua](https://x.com/gabrielchua), reframed for this library's context and enriched with repository examples.*

---

**Deutsche Version:** [SKILLS-EXPLAINED_de.md](SKILLS-EXPLAINED_de.md)
