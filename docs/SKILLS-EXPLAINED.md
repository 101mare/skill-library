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

### Contents

1. [The Habit](#the-habit) — How prompts naturally evolve into skills
2. [Why Prompting Still Matters](#why-prompting-still-matters) — Clear instructions improve any model
3. [What Actually Changes](#what-actually-changes-when-you-use-a-skill) — Progressive Disclosure, Structure, Resources
4. [Why This Matters for Teams](#why-this-matters-for-teams) — Codifying tacit knowledge
5. [In Practice](#in-practice) — When to turn a process into a skill

---

## The Habit

Most people who use AI tools have, at some point, ended up with a prompt that "mostly works." A checklist, a workflow, a set of rules like "don't do this" and "always check that." You tweak it a few times until the output looks right, then you save it somewhere to reuse later.

Over time, that prompt slowly changes. You add another rule after something breaks. You delete a line that no longer seems necessary. Someone else copies it into a different project and modifies it slightly.

Eventually, there are three or four versions of the same process floating around, and no one is quite sure which one produces the output you actually want. This is the natural lifecycle of a prompt — and it is exactly the problem that skills solve.

**A skill is a way of formalizing that habit.** At its core, a skill is a collection of prompts written down in a markdown file, sometimes with additional reference files or scripts that the model can use. It is not fundamentally different from prompting. It *is* prompting, made reusable.

Instead of keeping instructions in a document or a notes app, you place them into a folder — usually as a `SKILL.md` file — alongside any examples, templates, or scripts that make the workflow actually work end to end. That folder becomes something the agent can use as a repeatable process rather than a one-off attempt.

In this library, the same instinct is what turned 500-line CLAUDE.md files into separated rules, skills, and agents. The process described in [ARTICLE.md](ARTICLE.md) — where five projects had five diverging configs — is just this habit playing out at scale.

> [!IMPORTANT]
> **Key takeaway:** Skills are organized prompts with resources. They capture the prompting work you would otherwise redo every time.

---

## Why Prompting Still Matters

You might hear people say that prompting matters less now because models are getting better. That is true in the sense that you do not need to discover some magical phrasing or formatting trick to make the model behave.

But like talking to any human, clear and unambiguous instructions still help. The model cannot read your mind. It can only perform a task based on the instructions you provide and the context it receives.

The research confirms this. The NAACL 2024 paper ["Better Zero-Shot Reasoning with Role-Play Prompting"](https://arxiv.org/abs/2308.07702) found that generic labels like "You are an expert in X" had zero statistically significant improvement over no label at all. But specific, experiential instructions improved accuracy by 10–60%. The difference is not *whether* you prompt, but *how specifically* you prompt.

A skill is simply a way of doing the prompting work once. Instead of asking every user to rediscover the right set of instructions each time, the workflow is written down once in a way that reflects how the task is actually meant to be done.

With a well-designed skill, the person invoking it can give much simpler instructions and still get consistent results. "Use the tdd skill to add a user registration endpoint" replaces a paragraph of manual instructions about writing tests first, running them, then implementing, then refactoring.

> [!IMPORTANT]
> **Key takeaway:** Models getting better does not mean instructions matter less. A skill captures specific, tested instructions — not generic labels.

---

## What Actually Changes When You Use a Skill

There are three conceptual differences between a saved prompt and a skill. Each one addresses a different limitation of the copy-paste approach.

### Progressive Disclosure

A saved prompt loads everything into the context at once. Every rule, every edge case, every example — whether or not it is relevant to the current task.

A skill works differently. It reveals information progressively, from simple to complex. Each skill comes with a short description that explains what it is for. The agent reads that description and decides whether the skill is relevant. Only when it determines that the skill applies does it load the full instructions.

It is a bit like going to a library. You start with the catalogue to see what books exist on a topic. Once you have found the relevant book, you do not read the whole thing — you flip to the index to locate the exact chapter you need. The detailed instructions stay closed until they are actually relevant.

In this library, the three levels work like nested containers:

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

This matters because context windows are finite — and [research shows](https://arxiv.org/abs/2510.05381) that performance degrades with context length even when relevant information is perfectly retrievable. Loading only what is needed, when it is needed, is the answer.

### Structure

A saved prompt is a flat string of text. There is no inherent organization beyond what you put into the text itself.

A skill lives in a folder within a file system. Modern models are quite good at traversing file systems. The fact that something lives in a particular path already conveys information about how it should be used.

In the same way that you organize your own desktop by project or purpose, the structure of a skills directory yields context to the model:

```
skills/
├── build/
│   ├── backend/                 # Scaffolding & infrastructure
│   │   ├── ci-cd-builder/
│   │   ├── config-builder/
│   │   ├── docker-builder/
│   │   ├── exception-builder/
│   │   ├── logging-builder/
│   │   ├── project-scaffold/
│   │   └── prompt-builder/
│   └── frontend/                # Design & components
│       ├── frontend-design/
│       └── warmgold-frontend/
├── meta/                        # Building skills, agents & teams
│   ├── agent-builder/
│   ├── skill-builder/
│   └── team-builder/
├── patterns/                    # Reusable architecture patterns
│   ├── api-design/
│   ├── di-container/
│   ├── error-handling/
│   ├── protocol-design/
│   ├── resilience-patterns/
│   ├── strategy-registry/
│   ├── systematic-debugging/
│   └── testing-patterns/
└── workflow/                    # Multi-agent workflows
    ├── deep-research/
    ├── plan-review/
    ├── pr-review/
    ├── ralph-loop/
    ├── ralph-loop-prompt-builder/
    ├── session-verify/
    └── tdd/
```

This also introduces **modularity**. A skill becomes a packaged unit of workflow that can be reused, shared, versioned, or composed with other skills. Rather than copy-pasting slightly different versions of the same prompt into every project, you can treat workflows as modules that move between projects and team members.

For the practical details of the SKILL.md format — YAML frontmatter, trigger matching, and how to create your own skills — see the [SKILL.md Format](ARTICLE.md#the-skillmd-format) section in ARTICLE.md.

The [Agent Skills Standard](https://agentskills.io) takes this further — skills written in this format work across 30+ tools including Claude Code, OpenAI Codex, Cursor, Gemini CLI, and VS Code. All 27 skills in this library follow the standard.

### Access to Additional Resources

A reusable prompt is usually limited to whatever you remembered to paste in. A skill can include appendices, examples, scripts, evaluation rubrics, or even executable tooling that the model can use while carrying out the task.

Consider the `ralph-loop` skill in this library. It is not just a set of instructions — it bundles:

| File | Purpose |
|------|---------|
| `SKILL.md` | Core instructions for the `/ralph-loop` command |
| `init.md` | Installation script for setting up the hook |
| `prompt-template.md` | Template that Claude fills in for each task |
| `ralph-loop-stop.sh` | Bash hook script — the actual automation engine |

The workflow becomes grounded not only in instructions, but in context and tools. The difference between "here are instructions for running tests" and "here is a test runner that validates your work."

This might include calling MCP servers, running a CLI script, or referencing internal guidelines captured in a `reference.md`. In that sense, a skill is not just telling the model what to do, but also giving it access to the supporting materials needed to do it well.

> [!IMPORTANT]
> **Key takeaway:** Three things separate skills from saved prompts — progressive disclosure keeps context tight, file system structure conveys meaning, and bundled resources make workflows executable.

---

## Why This Matters for Teams

For individual developers, skills are a productivity tool. You capture what works and reuse it. The benefit is personal: less repetition, more consistency.

For teams, the benefit is different — and more significant. Much of what counts as expertise inside an organization is not a set of facts but a sequence of habits and checks. It is knowing what to verify before deploying something, what assumptions need to be tested, and what kind of output is considered acceptable.

Normally this knowledge is passed around informally or buried in outdated documentation. With skills, that procedural knowledge can be packaged into something the agent can follow directly.

Consider this library's `reviewer.md` agent. Its identity is not "You are an expert security reviewer." Instead, it carries specific experiences:

> *"…found SQL injection slip through three rounds of code review, watched silent `except: pass` blocks cause production incidents, traced GDPR violations to debug-level LLM response logs…"*

That is tacit knowledge — the kind that normally requires years of experience or pairing with a senior developer. Packaged as a skill or agent, it becomes instantly available to every team member.

In practice, this allows teams to codify and amplify expertise that would otherwise remain tacit or inconsistently applied. Everyone ends up running the same steps. New team members do not have to reverse-engineer the process from scratch.

When the process changes, you update the skill once rather than asking everyone to adjust their own prompts. This applies whether you are in a large enterprise or a small team.

> [!IMPORTANT]
> **Key takeaway:** Skills codify tacit knowledge — the habits, checks, and judgment calls that normally live only in people's heads.

---

## In Practice

Skills do not expand what the model is capable of doing. They do not make it smarter or give it new abilities. What they do: make it easier to perform repeatable tasks in a predictable way.

They let you codify and share processes instead of relying on memory or copy-paste. Same skill, same input patterns, same quality output — every time.

If you find yourself repeating the same process more than a few times, that is usually a sign that it can be turned into a skill. The signal is repetition. The solution is formalization.

What skills introduce is not new capability, but a way to turn tacit process into something explicit, shareable, and consistently executable.

> [!TIP]
> Want to create your own skills? The `skill-builder` meta-skill in this library teaches Claude the SKILL.md format, frontmatter conventions, and best practices — so you can say "create a skill for X" and get a well-structured result.

---

*This article is adapted from ["Skills, Explained"](https://x.com/gabrielchua/status/1936752568665473300) by [Gabriel Chua](https://x.com/gabrielchua), with concepts reframed for this library's context and enriched with examples from the skill-library repository.*

---

**Deutsche Version:** [SKILLS-EXPLAINED_de.md](SKILLS-EXPLAINED_de.md)
