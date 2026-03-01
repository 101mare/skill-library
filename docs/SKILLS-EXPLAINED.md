# Skills, Explained: Why Folders of Markdown Files Are So Effective

> [README](../README.md) | [CATALOG](CATALOG.md) | **SKILLS-EXPLAINED** | [ARTICLE](ARTICLE.md)

> [!NOTE]
> This article explains the conceptual foundations of skills — why the
> format works and what makes it different from saved prompts. For the
> library's architecture and how to use it, see [ARTICLE.md](ARTICLE.md).

### TL;DR

- **Skills formalize what you already do** — people naturally evolve prompts over time; skills capture that evolution in a reusable format
- **Clear instructions still matter** — models are getting better, but they cannot read your mind. A skill does the prompting work once instead of rediscovering it every time
- **Three things separate skills from saved prompts** — progressive disclosure (load only what's needed), file system structure (organization conveys meaning), and access to additional resources (scripts, examples, APIs)
- **Teams benefit most** — skills codify tacit knowledge and standardize processes across people and projects
- **Skills don't expand capability** — they make repeatable tasks predictable and consistent

---

## The Habit

Most people who use AI tools have, at some point, ended up with a prompt that "mostly works." You tweak it a few times, save it, and reuse it. Over time, rules get added, lines get deleted, someone copies it into another project — and soon three versions exist, none of them canonical.

**A skill formalizes that habit.** Instead of keeping instructions in a document or notes app, you place them into a folder — usually as a `SKILL.md` file — alongside any examples, templates, or scripts that make the workflow work end to end. That folder becomes a repeatable process rather than a one-off attempt.

---

## Why Prompting Still Matters

You might hear that prompting matters less because models are getting better. But like talking to any human, clear and unambiguous instructions still help. The model cannot read your mind.

The [NAACL 2024 paper](https://arxiv.org/abs/2308.07702) found that generic labels like "You are an expert in X" had zero statistically significant improvement. But specific, experiential instructions improved accuracy by 10–60%. The difference is not *whether* you prompt, but *how specifically*.

A skill does the prompting work once. "Use the tdd skill to add a user registration endpoint" replaces a paragraph of manual instructions about writing tests first, running them, implementing, then refactoring.

---

## What Actually Changes When You Use a Skill

Three conceptual differences separate a skill from a saved prompt.

### Progressive Disclosure

A saved prompt loads everything at once — every rule, every edge case — whether or not it is relevant.

A skill reveals information progressively. Each skill has a short header description. The agent reads it and decides whether the skill applies. Only then does it load the full instructions. Detailed reference files stay closed until actually needed.

```
┌─────────────────────────────────────────────────────┐
│  Level 1: Skill Headers (always loaded)              │
│  name + description → agent knows what's available   │
│                                                      │
│  ┌───────────────────────────────────────────────┐   │
│  │  Level 2: SKILL.md (loaded on demand)         │   │
│  │  Core instructions, triggers, examples        │   │
│  │                                               │   │
│  │  ┌───────────────────────────────────────┐    │   │
│  │  │  Level 3+: Additional files           │    │   │
│  │  │  reference.md, examples.md, forms.md  │    │   │
│  │  │  (only read when truly needed)        │    │   │
│  │  └───────────────────────────────────────┘    │   │
│  └───────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

This matters because context windows are finite — and [research shows](https://arxiv.org/abs/2510.05381) that performance degrades with context length even when relevant information is perfectly retrievable.

### Structure

A saved prompt is a flat string. A skill lives in a folder within a file system. The path already conveys information about how it should be used — just like you organize your desktop by project or purpose. See the full directory tree in [CATALOG.md](CATALOG.md).

This introduces **modularity**: a skill becomes a packaged unit of workflow that can be reused, shared, versioned, or composed with other skills. For the practical details of the SKILL.md format — YAML frontmatter, trigger matching, and how to create your own — see [ARTICLE.md](ARTICLE.md#the-skillmd-format).

The [Agent Skills Standard](https://agentskills.io) takes this further — skills in this format work across 30+ tools including Claude Code, OpenAI Codex, Cursor, Gemini CLI, and VS Code. All skills in this library follow the standard.

### Access to Additional Resources

A saved prompt is limited to whatever you pasted in. A skill can bundle appendices, examples, scripts, evaluation rubrics, or executable tooling.

Consider the `ralph-loop` skill:

| File | Purpose |
|------|---------|
| `SKILL.md` | Core instructions for the `/ralph-loop` command |
| `init.md` | Installation script for setting up the hook |
| `prompt-template.md` | Template that Claude fills in for each task |
| `ralph-loop-stop.sh` | Bash hook script — the actual automation engine |

The difference between "here are instructions for running tests" and "here is a test runner that validates your work." A skill can call MCP servers, run CLI scripts, or reference internal guidelines in a `reference.md`.

---

## Why This Matters for Teams

For individuals, skills reduce repetition. For teams, the benefit is more significant: much of what counts as expertise is not facts but a sequence of habits and checks — knowing what to verify before deploying, what assumptions to test, what output is acceptable.

This library's `reviewer.md` agent demonstrates the difference. Its identity is not "You are an expert security reviewer." Instead, it carries specific experiences:

> *"…found SQL injection slip through three rounds of code review, watched silent `except: pass` blocks cause production incidents, traced GDPR violations to debug-level LLM response logs…"*

That is tacit knowledge — the kind that normally requires years of experience. Packaged as a skill or agent, it becomes instantly available to every team member. When the process changes, you update the skill once rather than asking everyone to adjust their own prompts.

---

## In Practice

Skills do not expand what the model can do. They make repeatable tasks predictable. If you find yourself repeating the same process more than a few times — that is the signal to turn it into a skill.

> [!TIP]
> Want to create your own skills? The `skill-builder` meta-skill teaches Claude the SKILL.md format, frontmatter conventions, and best practices — say "create a skill for X" and get a well-structured result.

---

*This article is adapted from ["Skills, Explained"](https://x.com/gabrielchua/status/1936752568665473300) by [Gabriel Chua](https://x.com/gabrielchua), with concepts reframed for this library's context and enriched with examples from the skill-library repository.*

---

**Deutsche Version:** [SKILLS-EXPLAINED_de.md](SKILLS-EXPLAINED_de.md)
