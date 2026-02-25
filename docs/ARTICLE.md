# Architecture Over Chaos: A Modern Skill Library for Claude Code & Co

> **Note:** This repo contains Anthropic's implementation of Skills for Claude. For information about the Agent Skills Standard, see [agentskills.io](https://agentskills.io).


## Chaos

<p align="center"><img src="images/chaos-vs-structure.png" width="50%" alt="Chaos vs Structure"></p>

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

This gives a clear structure:

```
skill-library/
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

The crucial point: **Rules replace the generic part of CLAUDE.md.** Once you've extracted fundamental standards like DRY, security, and agent behavior into rules, your CLAUDE.md only needs what truly makes your project unique. The DRY principle, applied to AI configuration.

### The Library as a Reference Collection

No annoying installs or setup scripts. This library is kept simple but effective as a pure reference and toolkit. For each project, you browse the categories and copy what you need:

Project A is a pure Python API and needs the database-analyzer agent but certainly not a react-component-builder. Project B is a frontend and needs exactly the opposite. No project drags along agents it doesn't use. This way you keep control over your project's dependencies.

Your agent can also fetch skills directly from the GitHub repo — no local clone needed. A simple call is enough:

```
Read https://github.com/101mare/skill-library/blob/main/docs/CATALOG.md and copy the tdd skill into my project
```

Alternatively, clone the library once and reference it locally:

```bash
git clone https://github.com/101mare/skill-library.git ~/skill-library
```

---

## Rules: What Claude Always Needs to Know

<p align="center"><img src="images/four-rules.png" width="50%" alt="The Four Rules"></p>

Four rules, four domains, no overlaps.

**`coding-conventions.md`** defines how code should look: DRY, Types, Error Handling, Testing. The most important sentence in it:

> DRY applies to knowledge, not code. If two functions have identical lines but represent different domain concepts, they are NOT duplicates. Forcing them into one abstraction creates coupling that makes future changes harder.

This isn't splitting hairs. Without this distinction, Claude produces abstractions that save two lines of code and confuse more than they help a few months later.

**`agent-behavior.md`** defines how Claude should work: Read first, Scope Discipline, minimal changes. The highlights:

> Read first, write second: Always read existing code before modifying. Understand patterns before proposing changes.

> Three similar lines are better than a premature helper.

> Ask, don't assume: When in doubt, ALWAYS ask. Better to ask once too many than to implement incorrectly.

**`security.md`** defines the basics that are never negotiable: Input Validation, PII-free Logging, Secrets in environment variables, no new dependencies without asking first.

**`self-improvement.md`** closes the feedback loop: After every correction, capture the pattern in `.claude/memory.md` — not the individual correction, but the general principle behind it. Review the lessons at session start. If the same mistake happens twice, the lesson wasn't specific enough.

Why exactly these four? Coding Conventions prevent stylistic drift. Agent Behavior prevents scope creep — the most common problem with AI-generated code. Security prevents the bugs that are hardest to find. Self-Improvement ensures Claude learns from corrections instead of repeating them.

These four files form the foundation for every new project from now on.

---

## Skills Teach, Agents Act

<p align="center"><img src="images/skills-teach-agents-act.png" width="50%" alt="Skills Teach, Agents Act"></p>

This is the distinction that makes the biggest difference.

**Skills** are knowledge in the current context. When Claude loads a skill, it's like opening a manual — the information is immediately available, in the same context, without handoff loss. Skills are suited for patterns, scaffolding recipes, workflows.

(Brief aside: "Scaffolding" refers to the automatic generation of a project's basic structure, e.g., generating the initial folder structure, config files, and base classes before the actual code is written.)

**Agents** are isolated subprocesses. They receive a task, their own tools, and zero context from the parent process. It's like commissioning a specialist — they bring their own expertise but only see what you explicitly give them.

Four skill categories:

**meta/** (3 Skills) — The library can extend itself. `skill-builder`, `agent-builder`, and `team-builder` teach Claude to create new skills, agents, and agent teams following the right patterns.

**build/** (9 Skills) — Split into `frontend/` and `backend/`. Frontend: Frontend Design, Warmgold Design System. Backend: Config (Pydantic + YAML + Env-Vars), Logging, Exceptions, Docker, CI/CD (GitHub Actions), Prompts, Project Structure.

> The two frontend skills deliberately solve different problems: `frontend-design` (based on [Impeccable](https://impeccable.style)) = Design quality. "Make it visually good, avoid AI slop." Generic principles for any project. `warmgold-frontend` = A specific design system. Concrete tokens, colors, components. Both skills compose naturally, without explicit dependency.

**workflow/** (7 Skills) — Orchestration of multi-agent workflows: Plan Review before implementation, Session Verification after work, PR Review for pull requests, TDD (RED-GREEN-REFACTOR cycle), Deep Research (structured research before technical decisions), Ralph Loop (autonomous iteration loop via hooks), and Ralph Loop Prompt Builder (interactive prompt builder for it).

**patterns/** (8 Skills) — Reusable architecture patterns: DI Container, Protocol Design, Strategy + Registry, Error Handling, Resilience Patterns (Retry, Circuit Breaker, Timeout), Testing Patterns (pytest + Hypothesis), API Design (FastAPI), Systematic Debugging (4-phase methodology).

### The SKILL.md Format

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

The meta-skill `skill-builder` in this library uses exactly these best practices to teach Claude how to create new skills following the right conventions.

### Progressive Disclosure

<p align="left"><img src="images/progressive-disclosure-bundling.webp" width="50%" alt="Progressive Disclosure"></p>

Skills can grow beyond a single SKILL.md. When the context gets too large or is only relevant in certain scenarios, a skill can bundle additional files in its folder and reference them by name from the SKILL.md. Claude navigates and reads these files only when needed.

```
Progressive Disclosure:

┌─────────────────────────────────────────────────────┐
│  Level 1: Skill Headers (always loaded)              │
│  name + description → Claude knows what's available  │
│                                                      │
│  ┌───────────────────────────────────────────────┐   │
│  │  Level 2: SKILL.md (loaded on demand)         │   │
│  │  Core instructions, triggers, examples        │   │
│  │                                               │   │
│  │  ┌───────────────────────────────────────┐    │   │
│  │  │  Level 3+: Additional files           │    │   │
│  │  │  reference.md, forms.md, examples.md  │    │   │
│  │  │  (only read when truly needed)        │    │   │
│  │  └───────────────────────────────────────┘    │   │
│  └───────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

Like a well-organized manual: table of contents first, then specific chapters, then the detailed appendix. Since agents with filesystem access don't need to load the entire skill into the context window, the amount of context a skill can bundle is practically unlimited.

SKILL.md files over 500 lines will only be partially processed. The solution: keep SKILL.md compact, details live in separate files like `reference.md`.

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

Skills for building, agents for reviewing. That's no coincidence — it reflects how the two mechanisms work.

---

## Don't Give the Agent a Flat Role, Give It a "Soul"

<p align="center"><img src="images/flat-role-vs-soul.png" width="50%" alt="Flat Role vs Soul"></p>

When building agents, we instinctively reach for simple assignments. When I built the first agents, the system prompts looked like this: "You are an expert Python security reviewer." The result was okay. Not bad, but not better than without a label. Why isn't that enough?

The research on this is fairly clear by now. The NAACL 2024 paper "Better Zero-Shot Reasoning with Role-Play Prompting" ([Paper](https://arxiv.org/abs/2308.07702)) investigated this systematically: 162 different roles, four LLM families, 2,410 questions, 12 reasoning benchmarks. Result: Generic labels like "You are an expert in X" had **zero statistically significant improvement** over no label at all. Zero. But specific role prompts improved accuracy by 10-60%.

As researcher @tolibear_ aptly analyzed on Twitter ([Post](https://x.com/tolibear_/status/2024155081281560700)): The most important lever is the agent's "soul." A generic label only activates broad, shallow associations. What works are so-called *experiential identities* — specific experiences, beliefs, and working methods instead of rigid labels.

This fundamentally changed how I write agent files. Let's look at the security review dimension of `reviewer.md`.

### Soul (Identity)

No label. Instead, an identity with specific experiences:

> You are a senior security engineer who has spent a decade conducting code audits and penetration tests for production Python applications. You've found authentication bypasses hiding in middleware, watched SQL injection slip through code review because reviewers focused on style instead of semantics, and learned that the most dangerous vulnerabilities look like ordinary code.

And an insight that comes from this experience:

> I've learned that security bugs cluster around boundaries — where user input enters, where data crosses trust zones, where assumptions about "internal only" break down. That's because developers think about the happy path, and attackers think about the edges.

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

---

## Workflow Skills: Skills That Control Agents

<p align="center"><img src="images/workflow-skills-orchestrator.png" width="50%" alt="Workflow Skills"></p>

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

**Important note:** Use such multi-agent workflows wisely and not as spam on every small save. Each invoked agent opens its own context window — that burns through tokens extremely fast!

---

## Agent Teams: When Subagents Aren't Enough

<p align="center"><img src="images/subagents-vs-agent-teams.png" width="50%" alt="Subagents vs Agent Teams"></p>

Recently, a new feature was added to Claude Code: Agent Teams. Where subagents are isolated workers that deliver their result back to the caller, agent teams are complete sessions that communicate with each other — with a shared task list, direct messages, and a team lead that coordinates.

The strongest use case: tasks where parallel exploration provides real value. Code reviews with three different focus lenses simultaneously. Debugging with competing hypotheses, where teammates actively try to disprove each other's theories.

**Important to know:** Agent Teams consume significantly more tokens. Each teammate is its own session with its own context window. For sequential tasks, edits in the same file, or work with many dependencies, subagents or a single session remain the better choice.

> **Reference:** [Claude Code Agent Teams Documentation](https://code.claude.com/docs/en/agent-teams)

---

## Advanced: Ralph Loop — Autonomous Work Loops

<p align="center"><img src="images/ralph-loop-spiral.png" width="50%" alt="Ralph Loop"></p>

Sometimes a single pass isn't enough. You want to give Claude a task and walk away — write tests, push through a refactoring, fix linting errors. Claude should iterate until it's done.

That's exactly what the **Ralph Loop** does. Named after Ralph Wiggum from The Simpsons — who just keeps going despite setbacks.

The original technique comes from Geoffrey Huntley: A bash loop that keeps feeding an AI agent the same prompt until the task is complete. Anthropic built an official plugin from it, which has been broken since a security patch. The DIY variant using hooks works more reliably.

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

---

## Context Management: 27 Skills, But Please Not All at Once

<p align="center"><img src="images/context-management.png" width="50%" alt="Context Management"></p>

The library has 27 skills. Does that mean you load all 27 into every project? No. And here it's important to understand why.

As described above: Skill headers (`name` + `description`) are included in Claude's prompt on every call. This is the mechanism by which Claude knows which skills are available. But it comes at a cost: every installed skill costs tokens just through its header — on every single API call. 27 skills with 3-4 lines of description each are ~100 lines of system prompt that you permanently carry around. Those are tokens that you're missing for the actual work. On top of that come rules, CLAUDE.md, agent definitions, and the conversation context. The context window is finite.

### The Five That Cover the Entire Cycle

If I had to limit myself:

1. **prompt-builder** — Asks clarifying questions about your goal, then turns vague requests into structured prompts — whether for a plan, direct implementation, or any other task.
2. **plan-review** — The most impactful workflow. Four parallel review agents check architecture fit, conventions, risks, and requirements. Traffic light verdict *before* code exists. Avoiding rework > fixing rework.
3. **tdd** — Real workflow with agent orchestration. Enforces that tests define behavior instead of confirming code.
4. **systematic-debugging** — When something is broken, the 4-phase methodology prevents shotgun debugging.
5. **session-verify** — End-of-session review: security, code quality, architecture, clean imports, no leftover TODOs. Nothing ships unchecked.

The logic: **Prompt** (prompt-builder) → **Plan** (plan-review) → **Build + Test** (tdd) → **Debug** (systematic-debugging) → **Verify** (session-verify). The entire development cycle, five skills.

> **Note:** This is a defensive, token-intensive setup — plan-review and session-verify both spawn multiple agents. If you want to move fast and cheap, tdd + systematic-debugging alone cover the core work.

### What's Deliberately Missing

**project-scaffold, docker-builder, ci-cd-builder, config-builder** — You use these once per project. Valuable during setup, never again after that.

**skill-builder, agent-builder** — Meta-skills for building new skills and agents. Powerful for power users, but not what you need day-to-day.

**deep-research** — Good, but Claude can research without a skill too. The skill makes it more structured, but it's not essential.

**frontend-design** — Only relevant if you're building frontend.

**strategy-registry** — The most frequently occurring pattern, but still a specific pattern — not universally needed.

The rest is specialization. The library is a toolkit, not a package. Copy what you need, not what you might someday need.

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

## Don't Forget Codex

Claude Code and Codex play well together. For complex, clearly defined execution tasks, Codex often feels more methodical. Claude Code shines in exploratory work, architectural decisions, and multi-agent reviews. It's worth finding a workflow mix — the tools don't exclude each other.

Skills from this library work in both environments — and beyond. The SKILL.md format follows the open [Agent Skills Standard](https://agentskills.io), originally developed by Anthropic and now supported by 30+ tools including [OpenAI Codex](https://developers.openai.com/codex/skills/), Cursor, Gemini CLI, VS Code, and many more. Write a skill once, use it everywhere.

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

The best CLAUDE.md is the one that only contains what no other project would also need. Everything else belongs in a library.
