# Architecture Over Chaos: A Modern Skill Library for Claude Code & Co

> [README](../README.md) | [CATALOG](CATALOG.md) | [SKILLS-EXPLAINED](SKILLS-EXPLAINED.md) | **ARTICLE**

> [!NOTE]
> This repo contains Anthropic's implementation of Skills for Claude. For information about the Agent Skills Standard, see [agentskills.io](https://agentskills.io).

### TL;DR

- **Three layers instead of one file** — Rules (always loaded) + Skills (on demand) + Agents (isolated subprocesses)
- **27 Skills, 5 Agents, 4 Rules** — a toolkit, not a framework. Copy what you need per project
- **Agent "Souls" beat flat labels** — research shows experiential identities improve accuracy by 10-60%
- **Skills teach, Agents act** — Skills load knowledge into the current context, Agents run in isolation
- **Less is more** — be deliberate about which skills and agents you install. Every header costs tokens on every call

### Contents

1. [Chaos](#chaos) — The problem with copied configs
2. [Three Layers, One Repo](#three-layers-one-repo) — Rules, Skills, Agents separated
3. [Rules](#rules-what-claude-always-needs-to-know) — Four files, four domains, no overlaps
4. [Skills Teach, Agents Act](#skills-teach-agents-act) — The distinction that matters most
5. [Soul](#dont-give-the-agent-a-flat-role-give-it-a-soul) — Experiential identities instead of flat labels
6. [Workflow Skills](#workflow-skills-skills-that-control-agents) — Skills that orchestrate agents
7. [Agent Teams](#agent-teams-when-subagents-arent-enough) — When subagents aren't enough
8. [Ralph Loop](#advanced-ralph-loop--autonomous-work-loops) — Autonomous iteration loops
9. [Context Management](#context-management-27-skills-but-please-not-all-at-once) — Which skills to actually install
10. [How to Use It](#how-to-use-it) — Workflow for adopting the library
11. [What I Got Wrong](#what-i-got-wrong-at-first) — Lessons from building this
12. [Closing](#closing)

## Chaos

<p align="center"><img src="images/chaos-vs-structure.png" width="50%" alt="Chaos vs Structure"></p>

<p align="center"><em>Five projects, five diverging configs — the problem this library solves.</em></p>

You know how it goes. You start a new project and the first thing you do is create a fresh CLAUDE.md configuration file. To save time, you copy your standard rules from an old project: "Never log PII", "Type hints mandatory". The problem: you adjust these rules over time, independently across different projects. Three months later, you have five projects with five completely different versions of your "standard rules" — and absolute chaos.

Or: You build a custom agent for security reviews. You give it the system prompt "You are an expert security reviewer." It runs, it finds a few things — but the analysis reads just as generic as without any system prompt. What's missing?

Or: You put skills and agents in the same folder, treat them the same way, and wonder why some work well and others don't. But they are fundamentally different things.

At some point I asked myself: What if I built the generic parts of my Claude Code configuration properly once and carried them into every project? Not as a monolithic framework, but as a toolkit — universal rules, callable knowledge, and delegated expertise, cleanly separated.

The result is a skill library with 4 rules, 27 skills, 5 agents, and a CLAUDE.md template. It has changed how every one of my projects works with Claude. Not because the individual pieces are so special, but because the separation of rules, knowledge, and expertise is right.

---

## Three Layers, One Repo

The library separates three concerns that are mixed together in most setups:

**Rules** are universal behavior. They are always loaded, in every project, on every prompt. Four files: Coding Conventions, Agent Behavior, Security, Self-Improvement.

**Skills** are callable knowledge. They are loaded when they're relevant — like opening a manual. 27 skills in four categories.

**Agents** are delegated expertise with their own scope. They run as isolated subprocesses, receive zero context from the parent process, and return a result. 5 agents in four categories.

Here is the full directory layout:

```
skill-library/
├── docs/                             # CATALOG + ARTICLE (EN + DE)
├── templates/
│   └── CLAUDE.md.template
├── rules/                            # Always-loaded behavior
│   ├── coding-conventions.md
│   ├── agent-behavior.md
│   ├── security.md
│   └── self-improvement.md
├── skills/
│   ├── meta/                         # Building Skills, Agents & Teams
│   │   ├── skill-builder/
│   │   ├── agent-builder/
│   │   └── team-builder/
│   ├── build/
│   │   ├── frontend/                 # Design & Components
│   │   │   ├── frontend-design/
│   │   │   └── warmgold-frontend/
│   │   └── backend/                  # Scaffolding & Infrastructure
│   │       ├── prompt-builder/
│   │       ├── logging-builder/
│   │       ├── config-builder/
│   │       ├── exception-builder/
│   │       ├── docker-builder/
│   │       ├── ci-cd-builder/
│   │       └── project-scaffold/
│   ├── workflow/                     # Multi-Agent Workflows
│   │   ├── plan-review/
│   │   ├── session-verify/
│   │   ├── pr-review/
│   │   ├── tdd/
│   │   ├── deep-research/
│   │   ├── ralph-loop/
│   │   └── ralph-loop-prompt-builder/
│   └── patterns/                     # Architecture Patterns
│       ├── di-container/
│       ├── protocol-design/
│       ├── strategy-registry/
│       ├── error-handling/
│       ├── resilience-patterns/
│       ├── testing-patterns/
│       ├── api-design/
│       └── systematic-debugging/
└── agents/
    ├── review/                       # Code Review & Audit
    │   └── reviewer.md
    ├── analyze/                      # Analysis & Detection
    │   └── analyzer.md
    ├── plan/                         # Planning & Assessment
    │   └── planner.md
    └── build/                        # Code Generation & Modification
        ├── code-simplifier.md
        └── test-architect.md
```

> [!NOTE]
> The `code-simplifier` agent is based on the one [Boris Cherny](https://x.com/bcherny/status/2009450715081789767) (creator of Claude Code) open-sourced from the Claude Code team's internal workflow.

The crucial point: **Rules replace the generic part of CLAUDE.md.** Once you've extracted fundamental standards like DRY, security, and agent behavior into rules, your CLAUDE.md only needs what truly makes your project unique. The DRY principle, applied to AI configuration.

### The Library as a Reference Collection

No annoying installs or setup scripts. This library is kept simple but effective as a pure reference and toolkit. For each project, you browse the categories and copy what you need:

Project A is a pure Python API and needs the analyzer agent but certainly not a frontend design skill. Project B is a frontend and needs exactly the opposite. No project drags along agents it doesn't use. This way you keep control over your project's dependencies.

Your agent can also fetch skills directly from the GitHub repo — no local clone needed. A simple call is enough:

```
Read https://github.com/101mare/skill-library/blob/main/docs/CATALOG.md and copy the tdd skill into my project
```

Alternatively, clone the library once and reference it locally:

```bash
git clone https://github.com/101mare/skill-library.git ~/skill-library
```

> [!IMPORTANT]
> **Key takeaway:** Separate universal behavior, callable knowledge, and delegated work — then your CLAUDE.md only needs what's project-specific.

The three layers are defined. Let's look at each one — starting with the foundation.

---

## Rules: What Claude Always Needs to Know

<p align="center"><img src="images/four-rules.png" width="50%" alt="The Four Rules"></p>

<p align="center"><em>Four Rules, four domains: Conventions, Behavior, Security, Self-Improvement.</em></p>

Four rules, four domains, no overlaps.

### `coding-conventions.md` — How Code Should Look

DRY, Types, Error Handling, Testing. The most important sentence:

> DRY applies to knowledge, not code. If two functions have identical lines but represent different domain concepts, they are NOT duplicates. Forcing them into one abstraction creates coupling that makes future changes harder.

Without this distinction, Claude produces abstractions that save two lines of code and confuse more than they help a few months later.

### `agent-behavior.md` — How Claude Should Work

Read first, Scope Discipline, minimal changes.

> Read first, write second: Always read existing code before modifying. Understand patterns before proposing changes.

> Three similar lines are better than a premature helper.

> Ask, don't assume: When in doubt, ALWAYS ask. Better to ask once too many than to implement incorrectly.

### `security.md` — What's Never Negotiable

Input Validation, PII-free Logging, Secrets in environment variables, no new dependencies without asking first.

### `self-improvement.md` — The Feedback Loop

After every correction, capture the pattern in `.claude/memory.md` — not the individual correction, but the general principle behind it. Review the lessons at session start. If the same mistake happens twice, the lesson wasn't specific enough.

---

Why exactly these four? Coding Conventions prevent stylistic drift. Agent Behavior prevents scope creep — the most common problem with AI-generated code. Security prevents the bugs that are hardest to find. Self-Improvement ensures Claude learns from corrections instead of repeating them.

These four files form the foundation for every new project from now on.

> [!IMPORTANT]
> **Key takeaway:** Four files, four domains, zero overlap — coding standards, agent behavior, security, and self-improvement form the unchanging foundation.

Rules set the baseline. But the real power comes from the interplay of the other two layers.

---

## Skills Teach, Agents Act

<p align="center"><img src="images/skills-teach-agents-act.png" width="50%" alt="Skills Teach, Agents Act"></p>

<p align="center"><em>Skills load knowledge into the current context. Agents run in isolated subprocesses.</em></p>

This is the distinction that makes the biggest difference.

**Skills** are knowledge in the current context. When Claude loads a skill, it's like opening a manual — the information is immediately available, in the same context, without handoff loss. Skills are suited for patterns, scaffolding recipes, workflows.

(Brief aside: "Scaffolding" refers to the automatic generation of a project's basic structure, e.g., generating the initial folder structure, config files, and base classes before the actual code is written.)

**Agents** are isolated subprocesses. They receive a task, their own tools, and zero context from the parent process. It's like commissioning a specialist — they bring their own expertise but only see what you explicitly give them.

### The Four Categories

Four skill categories:

**meta/** (3 Skills) — The library can extend itself. `skill-builder`, `agent-builder`, and `team-builder` teach Claude to create new skills, agents, and agent teams following the right patterns.

**build/** (9 Skills) — Split into `frontend/` and `backend/`. Frontend: Frontend Design, Warmgold Design System. Backend: Config (Pydantic + YAML + Env-Vars), Logging, Exceptions, Docker, CI/CD (GitHub Actions), Prompts, Project Structure.

**workflow/** (7 Skills) — Orchestration of multi-agent workflows: Plan Review before implementation, Session Verification after work, PR Review for pull requests, TDD (RED-GREEN-REFACTOR cycle), Deep Research (structured research before technical decisions), Ralph Loop (autonomous iteration loop via hooks), and Ralph Loop Prompt Builder (interactive prompt builder for it).

**patterns/** (8 Skills) — Reusable architecture patterns: DI Container, Protocol Design, Strategy + Registry, Error Handling, Resilience Patterns (Retry, Circuit Breaker, Timeout), Testing Patterns (pytest + Hypothesis), API Design (FastAPI), Systematic Debugging (4-phase methodology).

### The SKILL.md Format

> [!NOTE]
> For a conceptual introduction to *why* skills work — progressive disclosure, file system structure, and bundled resources — see [SKILLS-EXPLAINED.md](SKILLS-EXPLAINED.md). This section covers the *practical how*.

Skills are folders with instructions, scripts, and resources that Claude loads dynamically to perform better on specialized tasks. Skills teach Claude to accomplish certain tasks repeatably — whether it's creating documents according to your company's brand guidelines, analyzing data with your organization's specific workflows, or automating personal tasks.

Further reading:

- [What are skills?](https://support.claude.com/en/articles/12512176-what-are-skills)
- [Using skills in Claude](https://support.claude.com/en/articles/12512180-using-skills-in-claude)
- [How to create custom skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)
- [Equipping agents for the real world with Agent Skills](https://claude.com/blog/equipping-agents-for-the-real-world-with-agent-skills)

### Creating a Simple Skill

A skill is a folder with a `SKILL.md` file — YAML frontmatter plus instructions. The basic structure looks like this:

```yaml
---
name: my-skill-name
description: A clear description of what this skill does and when to use it
---

# My Skill Name

[Add your instructions here that Claude will follow when this skill is active]

## Examples
- Example usage 1
- Example usage 2

## Guidelines
- Guideline 1
- Guideline 2
```

The frontmatter needs only two fields:

- **`name`** — Unique identifier (lowercase, hyphens)
- **`description`** — Complete description of what the skill does and when it should be used

Important: The skill headers (`name` + `description`) are **always** included in Claude's prompt — this is how it knows at every task which skills are available and when to load them. The full SKILL.md content is only loaded when the skill becomes relevant.

> [!TIP]
> Want Claude to build skills for you? The `skill-builder` meta-skill teaches Claude the SKILL.md format, frontmatter conventions, and best practices — so you can say "create a skill for X" and get a well-structured result.

### How Skill Loading Actually Works

The matching is purely prompt-based — no embedding lookup, no magic. Claude reads all installed skill descriptions and decides itself whether a skill is relevant. This happens **proactively**: you don't need to type `/skill-name`. If you write "why does this test fail?", Claude matches that against the trigger phrases in `systematic-debugging` and loads the skill on its own. Or you start talking about API endpoints and Claude loads `api-design` without being asked.

When Claude loads a skill, it reads the `SKILL.md` file via the Read tool — this is **visible** in the conversation. It's not a silent background process; you see the tool call happen.

The weakness: matching is only as good as the descriptions. If trigger phrases are too generic, Claude loads the wrong skill or none at all. If they're too specific, Claude doesn't recognize the context. In ambiguous situations where multiple skills could match, it's a coin flip which one Claude picks. That's why this library puts significant effort into writing specific, varied trigger phrases in each skill's `description` field.

The meta-skill `skill-builder` in this library uses exactly these best practices to teach Claude how to create new skills following the right conventions.

### Progressive Disclosure

<p align="left"><img src="images/progressive-disclosure-bundling.webp" width="50%" alt="Progressive Disclosure"></p>

<p align="center"><em>Headers are always visible, details are loaded on demand.</em></p>

Skills can grow beyond a single SKILL.md. A skill can bundle additional files in its folder — `reference.md`, `examples.md`, `anti-patterns.md` — and reference them by name from the SKILL.md. Claude navigates and reads these files only when needed.

For the full conceptual explanation of progressive disclosure — the three-level model, the library analogy, and why context windows make this essential — see [SKILLS-EXPLAINED.md](SKILLS-EXPLAINED.md#progressive-disclosure).

**The practical rule:** SKILL.md files over 500 lines will only be partially processed. Keep SKILL.md compact; details live in separate files like `reference.md`.

More on this in the blog post: [Equipping agents for the real world with Agent Skills](https://claude.com/blog/equipping-agents-for-the-real-world-with-agent-skills)

### Lifecycle Mapping

The library maps skills and agents to development phases:

| Phase | Skills | Agents |
|---|---|---|
| **Research** | deep-research | -- |
| **Plan** | plan-review | planner |
| **Scaffold** | project-scaffold, config-builder, exception-builder, docker-builder, ci-cd-builder | -- |
| **Code** | di-container, protocol-design, strategy-registry, error-handling, resilience-patterns, logging-builder, api-design, ralph-loop, ralph-loop-prompt-builder | -- |
| **Frontend** | frontend-design, warmgold-frontend | -- |
| **Review** | pr-review, session-verify | reviewer |
| **Test** | tdd, testing-patterns | test-architect |
| **Debug** | systematic-debugging | -- |
| **Analyze** | -- | analyzer |

The **Frontend** phase deserves a closer look. Two skills work together here: `frontend-design` teaches universal design principles — typography, color theory, spatial rhythm, and how to avoid generic AI aesthetics. It's the skill that ensures visual quality regardless of which design system you use. `warmgold-frontend` is my preferred design system: a warm, iOS-inspired token set with gold accents and stone grays, complete with component patterns, dark mode, and accessibility built in. It's an opinionated choice — and that's the point. If you prefer a different aesthetic, create your own design system skill and swap it in. The `frontend-design` skill has a composition reference that points to the active design system; update that reference to your own skill, and the two will compose just as naturally.

> [!TIP]
> The two frontend skills deliberately solve different problems: `frontend-design` (based on [Impeccable](https://impeccable.style)) = Design quality. "Make it visually good, avoid AI slop." Generic principles for any project. `warmgold-frontend` = A specific design system. Concrete tokens, colors, components. Both skills compose naturally, without explicit dependency.

Skills for building, agents for reviewing. That's no coincidence — it reflects how the two mechanisms work.

> [!IMPORTANT]
> **Key takeaway:** Skills load knowledge into the conversation. Agents run in isolation. Mixing them up is the most common architectural mistake.

So much for what skills and agents *are*. The next question: what makes an agent actually *good*?

<p align="center"><em>So far: three-layer architecture, four rules, 27 skills and their mapping to development phases. From here: how to write effective agents, orchestrate workflows, and manage context budgets.</em></p>

---

## Don't Give the Agent a Flat Role, Give It a "Soul"

<p align="center"><img src="images/flat-role-vs-soul.png" width="50%" alt="Flat Role vs Soul"></p>

<p align="center"><em>Generic labels vs. experiential identities: the research-backed difference.</em></p>

When building agents, we instinctively reach for simple assignments. When I built the first agents, the system prompts looked like this: "You are an expert Python security reviewer." The result was okay. Not bad, but not better than without a label. Why isn't that enough?

The research on this is fairly clear by now. The NAACL 2024 paper "Better Zero-Shot Reasoning with Role-Play Prompting" ([Paper](https://arxiv.org/abs/2308.07702)) investigated this systematically: 162 different roles, four LLM families, 2,410 questions, 12 reasoning benchmarks. Result: Generic labels like "You are an expert in X" had **zero statistically significant improvement** over no label at all. Zero. But specific role prompts improved accuracy by 10-60%.

As researcher @tolibear_ aptly analyzed on Twitter ([Post](https://x.com/tolibear_/status/2024155081281560700)): The most important lever is the agent's "soul." A generic label only activates broad, shallow associations. What works are so-called *experiential identities* — specific experiences, beliefs, and working methods instead of rigid labels.

This fundamentally changed how I write agent files. Let's look at `reviewer.md`.

### Soul (Identity)

No label. Instead, an identity with specific experiences:

> You are a senior Python reviewer who has found SQL injection slip through three rounds of code review, watched silent `except: pass` blocks cause production incidents, traced GDPR violations to debug-level LLM response logs that "nobody would ever enable in production," and caught "100% offline" projects making DNS requests on startup via transitive dependencies. You review code the way a locksmith examines a door -- testing every assumption about what keeps attackers out, what data leaks, and what fails silently.

### Anti-Patterns (What I Refuse To Do)

What the agent does **not** do (and what you should devote a good 30-40% of the prompt to):

> I don't skim code and declare it "looks fine." Every external input path gets traced to its handler, every file operation gets checked for traversal, every subprocess call gets examined for injection.

> I don't prioritize style over safety. A beautifully formatted SQL injection is still a SQL injection.

> I don't assume internal code is safe from internal threats. Least privilege applies everywhere.

### Productive Weakness

> One productive weakness: I sometimes flag patterns as risky that are actually safe in context. That's the cost of thoroughness.

Why does this work? The formula is: *"I've learned that [insight] because [experience]."* It activates specific knowledge clusters in the model. "Security bugs cluster around boundaries" is a different instruction than "check for security issues" — it tells the model *where* to look, not just *that* it should look.

Every agent in the library follows this structure: Soul (Identity with experiences), Anti-Patterns (what I refuse), productive weakness, checklist, output format, Project Adaptation. The Soul makes the agent good. The Anti-Patterns make it reliable. The checklist makes the results consistent.

### Project Adaptation

The last point deserves its own attention. Every agent reads the project setup before analysis:

> Before analysis, read the project's `CLAUDE.md` and `.claude/memory.md` (if they exist) to understand: Module structure and boundaries, Design patterns and conventions in use, Known patterns to preserve.

This makes generic agents project-aware. The security reviewer doesn't just know what's insecure — it knows what counts as secure in *your* project.

> [!IMPORTANT]
> **Key takeaway:** Replace generic labels with experiential identities. Devote 30-40% of the prompt to what the agent refuses to do.

Well-designed agents are already powerful on their own. But orchestrating multiple agents together — that's where things get really interesting.

---

## Workflow Skills: Skills That Control Agents

<p align="center"><img src="images/workflow-skills-orchestrator.png" width="50%" alt="Workflow Skills"></p>

<p align="center"><em>Workflow skills orchestrate multiple agents in parallel.</em></p>

The most interesting category is workflow skills. They orchestrate multiple agents.

`plan-review` is the best example. When you have an implementation plan and say "review my plan," the following happens:

1. The skill identifies the plan and clarifies the context
2. It reads the agent files (`reviewer.md`, `analyzer.md`, `planner.md`)
3. It spawns four parallel review agents — Completeness, Architecture, Risk, Requirements
4. Each agent receives the system prompt from the corresponding agent file injected
5. The results are aggregated into a traffic light verdict: GREEN (approved), YELLOW (needs work), RED (blocked)

The pattern behind it: Workflow skills read the agent files and feed the task calls with exactly this expertise as context. Skills control, agents work. And because Claude Code can send multiple task calls in parallel, all four reviews run simultaneously.

`session-verify` uses the same pattern at the end of a session. The workflow: First clarify what the original task was. Then identify what changed — via Git diff if available, otherwise via conversation context. Then spawn review agents (at minimum Reviewer and Code Simplifier, situationally Analyzer for performance and architecture). Then check whether the requirement is met. Then ask whether the documentation should be updated.

That sounds like a lot. In practice, it's a `/verify` at the end of the session and two minutes of waiting. The alternative — manually going through all changed files and hoping you don't miss anything — takes longer and is less thorough.

> [!WARNING]
> Use multi-agent workflows wisely and not as spam on every small save. Each invoked agent opens its own context window — that burns through tokens extremely fast!

> [!IMPORTANT]
> **Key takeaway:** Skills control, agents work — workflow skills read agent files and orchestrate multiple specialists in parallel.

---

## Agent Teams: When Subagents Aren't Enough

<p align="center"><img src="images/subagents-vs-agent-teams.png" width="50%" alt="Subagents vs Agent Teams"></p>

<p align="center"><em>Subagents deliver results back. Agent Teams communicate with each other.</em></p>

Recently, a new feature was added to Claude Code: Agent Teams. Where subagents are isolated workers that deliver their result back to the caller, agent teams are complete sessions that communicate with each other — with a shared task list, direct messages, and a team lead that coordinates.

The strongest use case: tasks where parallel exploration provides real value. Code reviews with three different focus lenses simultaneously. Debugging with competing hypotheses, where teammates actively try to disprove each other's theories.

> [!WARNING]
> Agent Teams consume significantly more tokens. Each teammate is its own session with its own context window. For sequential tasks, edits in the same file, or work with many dependencies, subagents or a single session remain the better choice.

> [!NOTE]
> **Reference:** [Claude Code Agent Teams Documentation](https://code.claude.com/docs/en/agent-teams)

> [!IMPORTANT]
> **Key takeaway:** Use Agent Teams for parallel exploration with real value. For everything else, stick with subagents — teams cost significantly more tokens.

Agent Teams solve parallel collaboration. But what about tasks that need autonomous *iteration*?

---

## Advanced: Ralph Loop — Autonomous Work Loops

<p align="center"><img src="images/ralph-loop-spiral.png" width="50%" alt="Ralph Loop"></p>

<p align="center"><em>Autonomous iteration until the task is done.</em></p>

Sometimes a single pass isn't enough. You want to give Claude a task and walk away — write tests, push through a refactoring, fix linting errors. Claude should iterate until it's done.

That's exactly what the **Ralph Loop** does. Named after Ralph Wiggum from The Simpsons — who just keeps going despite setbacks.

The original technique comes from Geoffrey Huntley: A bash loop that keeps feeding an AI agent the same prompt until the task is complete. Anthropic built an official plugin from it, which has been broken since a security patch. The DIY variant using hooks works more reliably.

Here's what a typical Ralph Loop session looks like:

```
User: /ralph-loop max=15 Write tests for validators.py

    Claude works...
    ├── Iteration 1: Tests written, 3 of 8 green
    ├── Iteration 2: Errors fixed, 6 of 8 green
    ├── Iteration 3: Edge cases added, 8 of 8 green
    └── <promise>COMPLETE</promise> → Loop ends
```

The mechanism is a **stop hook** — a bash script that fires when Claude wants to stop:

```
Claude wants to stop
       │
       ▼
  Stop Hook fires
       │
  ┌────┴──────────────────┐
  │ State file present?   │
  └────┬──────────────────┘
       │
   Yes │  No → exit 0 (normal stop)
       ▼
  ┌────────────────────────┐
  │ <promise>COMPLETE</> ? │──→ Yes → Delete state, exit 0
  │ Max Iterations?        │──→ Yes → Delete state, exit 0
  └────────────────────────┘
       │ No
       ▼
  {"decision": "block", "reason": "<Original-Prompt>"}
  → Claude keeps working
```

No plugin needed. Three files are enough:

| File | Purpose |
|------|---------|
| `.claude/hooks/ralph-loop-stop.sh` | Stop Hook — the heart of it |
| `.claude/skills/ralph-loop/SKILL.md` | `/ralph-loop` command |
| `.claude/settings.local.json` | Hook configuration |

**When to use Ralph:** Clearly defined tasks with verifiable results — tests, linting, batch refactoring, type hints. **When not:** Design decisions, unclear requirements, debugging. The quality of the prompt matters — a vague prompt leads to drift. The **Ralph Loop Prompt Builder** (`/ralph-loop-prompt-builder`) helps here: it asks clarifying questions about the task and generates a structured prompt with clear requirements, verification steps, and completion criteria.

The complete implementation with installation guide (`init.md`), prompt template (`prompt-template.md`), and interactive prompt builder is at `skills/workflow/ralph-loop/`. Installation: Just tell your agent *"Read `skills/workflow/ralph-loop/init.md` and set this up in my project"* — it handles the rest.

> [!IMPORTANT]
> **Key takeaway:** Autonomous iteration works for clearly defined tasks with verifiable results. The quality of the prompt determines the quality of the loop.

The Ralph Loop closes the automation gap. But with all these tools, one practical question remains: how much should you actually install?

---

## Context Management: 27 Skills, But Please Not All at Once

<p align="center"><img src="images/context-management.png" width="50%" alt="Context Management"></p>

<p align="center"><em>Every installed skill costs tokens on every API call — choose wisely.</em></p>

The library has 27 skills. Does that mean you load all 27 into every project? No. And here it's important to understand why.

As described above: Skill headers (`name` + `description`) are included in Claude's prompt on every call. This is the mechanism by which Claude knows which skills are available.

But it comes at a cost: every installed skill costs tokens just through its header — on every single API call. 27 skills with 3-4 lines of description each are ~100 lines of system prompt that you permanently carry around. Those are tokens that you're missing for the actual work. On top of that come rules, CLAUDE.md, agent definitions, and the conversation context. The context window is finite.

This isn't just a hunch — it's backed by research. The [IFScale benchmark](https://arxiv.org/abs/2507.11538) (2025) shows that instruction-following accuracy degrades measurably starting at ~100-150 instructions, with models increasingly *omitting* rules rather than getting them wrong (30:1 omission-to-error ratio at high density). [Context Rot](https://research.trychroma.com/context-rot) (Chroma Research) demonstrates that performance degradation is universal across all models as input length grows — even when relevant information is perfectly retrievable. Most striking: [research presented at EMNLP 2025](https://arxiv.org/abs/2510.05381) found that context length *alone* causes 14-85% performance loss, even with perfect retrieval. The effective context window is much smaller than the nominal one. Progressive disclosure — loading only what's needed, when it's needed — is the answer.

### The Five That Cover the Entire Cycle

If I had to limit myself:

1. **prompt-builder** — Asks clarifying questions about your goal, then turns vague requests into structured prompts — whether for a plan, direct implementation, or any other task.
2. **plan-review** — The most impactful workflow. Four parallel review agents check architecture fit, conventions, risks, and requirements. Traffic light verdict *before* code exists. Avoiding rework > fixing rework.
3. **tdd** — Real workflow with agent orchestration. Enforces that tests define behavior instead of confirming code.
4. **systematic-debugging** — When something is broken, the 4-phase methodology prevents shotgun debugging.
5. **session-verify** — End-of-session review: security, code quality, architecture, clean imports, no leftover TODOs. Nothing ships unchecked.

The logic: **Prompt** (prompt-builder) → **Plan** (plan-review) → **Build + Test** (tdd) → **Debug** (systematic-debugging) → **Verify** (session-verify). The entire development cycle, five skills.

> [!IMPORTANT]
> This is a defensive, token-intensive setup — plan-review and session-verify both spawn multiple agents. If you want to move fast and cheap, tdd + systematic-debugging alone cover the core work.

### What's Deliberately Missing

**project-scaffold, docker-builder, ci-cd-builder, config-builder** — You use these once per project. Valuable during setup, never again after that.

**skill-builder, agent-builder** — Meta-skills for building new skills and agents. Powerful for power users, but not what you need day-to-day.

**deep-research** — Good, but Claude can research without a skill too. The skill makes it more structured, but it's not essential.

**frontend-design** — Only relevant if you're building frontend.

**strategy-registry** — The most frequently occurring pattern, but still a specific pattern — not universally needed.

The rest is specialization. The library is a toolkit, not a package. Copy what you need, not what you might someday need.

> [!IMPORTANT]
> **Key takeaway:** Five skills cover the entire development cycle. Install what you need, not what you might someday need — every header costs tokens on every call.

---

## How to Use It

The library is a reference. Here's what the workflow looks like:

**1. For each project: Select and copy.**

Browse the categories and manually copy the required .md files into your project.

**Tip for the lazy among us:** Just give the path to this library repo to your Claude or Codex agent and discuss with it which rules and skills your current project needs. Let it handle the copying.

**2. Fill out the CLAUDE.md template.**

This is where you should invest the most time at project start. Think carefully about how your project should be structured. What is your project? Why are you building it? Where are the technical boundaries? The template contains placeholders for everything project-specific — Architecture, Commands, Import Conventions, Key Patterns, Configuration. The generic rules are in the rules and don't need to be repeated here.

**3. Add custom skills in the project.**

Project-specific skills live in the project itself:

```
my-project/.claude/skills/my-domain-skill/SKILL.md
```

A good example: Maybe you've just built a complex database schema and want to capture its quirks, relations, and naming conventions in a skill. This way Claude always knows exactly how to write queries for this specific project. And if you need a new generic skill: `skill-builder` and `agent-builder` are meta-skills that teach Claude to create new skills following the right conventions.

---

## What I Got Wrong at First

**Agents started as checklists.** My first agent files were structured task lists: "Check for SQL injection. Check for path traversal." The agent worked through the list and delivered nothing beyond that. Only with Identity, Anti-Patterns, and productive weaknesses did the agents become useful.

**Everything was in CLAUDE.md first.** My early CLAUDE.md files were 400+ lines long, half of which was generic. Extracting the rules had the biggest impact — not because the rules got better, but because the CLAUDE.md finally became readable.

**Early SKILL.md files were novels.** 800+ lines, everything in one file. Claude only partially processed them. Progressive disclosure (compact SKILL.md plus separate reference.md) solved the problem.

**Not everything needs an agent.** The temptation is great to build an agent for every conceivable scenario. Build for your actual workflow, not the theoretically possible one. The library has 5 agents, but a typical project copies three or four of them. The rest is there when you need it.

---

## Closing

The number of skills and agents doesn't actually matter. What ultimately makes your setup reliable is solely a good separation of responsibilities.

Rules for what always applies. Skills for what Claude needs to know when it becomes relevant. Agents for what Claude should work on as an independent task. CLAUDE.md for what is unique to your project — and only for that.

Claude Code and Codex play well together. For complex, clearly defined execution tasks, Codex often feels more methodical. Claude Code shines in exploratory work, architectural decisions, and multi-agent reviews. It's worth finding a workflow mix — the tools don't exclude each other. Skills from this library work in both environments — and beyond. The SKILL.md format follows the open [Agent Skills Standard](https://agentskills.io), originally developed by Anthropic and now supported by 30+ tools including [OpenAI Codex](https://developers.openai.com/codex/skills/), Cursor, Gemini CLI, VS Code, and many more. Write a skill once, use it everywhere.

The best CLAUDE.md is the one that only contains what no other project would also need. Everything else belongs in a library.
