# Skills, Explained: Why Folders of Markdown Files Are So Effective

> [README](../README.md) | [CATALOG](CATALOG.md) | **SKILLS-EXPLAINED** | [ARTICLE](ARTICLE.md)

> [!NOTE]
> This article explains the conceptual foundations of skills — why the format works and what makes it different from saved prompts. For the library's architecture and how to use it, see [ARTICLE.md](ARTICLE.md).

### TL;DR

- **Skills formalize habits:** Instead of losing track of evolved prompts, skills capture them in a canonical, reusable format.
- **Specificity still wins:** AI models can't read minds. Skills do the heavy lifting of specific prompting once, saving you from repeating it.
- **Beyond flat text:** Skills beat saved prompts through **progressive disclosure** (loading context only when needed), **system structure** (organization conveys meaning), and **resource bundling** (scripts, templates, and APIs).
- **A multiplier for teams:** Skills codify tacit knowledge, standardizing workflows and quality across entire teams.
- **Predictability over capability:** Skills don't give models new abilities; they make complex, repeatable tasks reliable.

---

## The Problem with "Saved Prompts"

Most AI users eventually end up with a prompt that "mostly works." You tweak it, save it in a notes app, and paste it when needed. Over time, someone copies it, adds rules, deletes lines—and soon, three conflicting versions exist.

Furthermore, simply relying on generic instructions like "You are an expert" isn't enough. A [NAACL 2024 paper](https://arxiv.org/abs/2308.07702) demonstrated that specific, experiential instructions improve accuracy by 10–60%, while generic labels offer zero statistically significant improvement. The model needs specific context, but pasting massive blocks of text every time is inefficient and error-prone.

**A skill formalizes this process.** Instead of a messy text snippet, you place instructions into a dedicated folder (using a `SKILL.md` file) alongside templates and scripts. "Use the `tdd` skill to add an endpoint" replaces a paragraph of manual instructions. It turns a one-off attempt into a repeatable workflow.

---

## The Three Pillars of a Skill

What actually changes when you transition from a saved prompt to a skill? It comes down to three conceptual differences.

### 1. Progressive Disclosure

A saved prompt forces the model to read everything at once—every rule, every edge case—regardless of relevance. Because [research shows](https://arxiv.org/abs/2510.05381) that AI performance degrades as context windows get crowded, this is highly inefficient.

A skill solves this by revealing information progressively:

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

The agent reads a short header and decides if the skill applies. Detailed instructions and reference files stay hidden until they are actually needed, keeping the context window clean and sharp.

### 2. File System Structure

A saved prompt is a flat string. A skill lives in a folder. The directory structure itself conveys meaning, just like organizing your desktop by project. (See the full directory tree in [CATALOG.md](CATALOG.md)).

This introduces **modularity**. A skill is a packaged unit that can be version-controlled, shared, and composed with others. All skills in this library follow the [Agent Skills Standard](https://agentskills.io), ensuring they work seamlessly across 30+ tools, including Claude Code, Cursor, and VS Code.

### 3. Bundled Resources

While a saved prompt is limited to the text you paste, a skill is a self-contained ecosystem. It can bundle appendices, evaluation rubrics, or even executable tooling.

Consider the `ralph-loop` skill:

| File | Purpose |
|------|---------|
| `SKILL.md` | Core instructions for the `/ralph-loop` command |
| `init.md` | Installation script for setting up the hook |
| `prompt-template.md` | Template that the agent fills in for each task |
| `ralph-loop-stop.sh` | Bash hook script — the actual automation engine |

This is the difference between saying "here are instructions for running tests" and "here is a test runner that validates your work."

---

## Why This Matters for Teams

For individuals, skills save time. For teams, they scale expertise.

Much of what makes a senior developer or expert valuable is "tacit knowledge"—knowing what assumptions to test, what to verify before deploying, and what output is acceptable. This library's `reviewer.md` agent demonstrates this. Its prompt isn't "You are a security expert." It carries specific, hard-won experiences:

> *"…found SQL injection slip through three rounds of code review, watched silent `except: pass` blocks cause production incidents, traced GDPR violations to debug-level LLM response logs…"*

Packaged as a skill, this tacit knowledge becomes instantly accessible to junior and senior team members alike. When a process evolves, you update the skill once centrally, rather than asking a whole team to update their personal notes.

---

## In Practice

Skills do not magically expand what an LLM is capable of; they make its output predictable and consistent. If you find yourself repeating the same prompting process more than three times, it's time to turn it into a skill.

> [!TIP]
> Want to create your own? The `skill-builder` meta-skill teaches your agent the SKILL.md format, frontmatter conventions, and best practices. Just ask: "Create a skill for [Task]" to get a perfectly structured starting point.

---

*This article is adapted from ["Skills, Explained"](https://x.com/gabrielchua/status/1936752568665473300) by [Gabriel Chua](https://x.com/gabrielchua), reframed for this library's context and enriched with repository examples.*

---

**Deutsche Version:** [SKILLS-EXPLAINED_de.md](SKILLS-EXPLAINED_de.md)
