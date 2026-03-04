---
name: brainstorm
description: |
  Structured brainstorming through divergent-then-convergent thinking.
  Generates multiple approaches using research-validated techniques
  (Reverse Brainstorming, SCAMPER, Perspective Shifts, Analogies)
  before converging on a recommended design.
  Works for any domain: software features, architecture, thesis structure,
  process design, concepts, strategies.
  Recognizes: "brainstorm", "brainstorming", "ideation", "ideas for",
  "let's think about", "explore options", "what are approaches for",
  "how could we", "alternatives for"
  Does NOT handle: implementation planning (use plan-review),
  prompt writing (use prompt-builder), code writing (use frontend-design/tdd),
  team coordination (use team-builder).
---


# Brainstorm


Structured ideation through divergent-then-convergent thinking.
No code, no implementation, no scaffolding — pure thinking space.


Adapt output language to match the user's language.


## Critical Constraints


- **No implementation until approval.** This skill produces ideas and designs, never code.
- **Minimum 3 alternatives.** Never present only one approach. Even when one is clearly superior, show why by contrasting.
- **Divergent BEFORE convergent.** Resist the urge to narrow too early. Fully explore the space first.
- **YAGNI ruthlessly.** Flag and remove unnecessary complexity in every approach.


## Phase 1: Context


Understand the problem space before generating ideas.


1. **Scan existing context**: Read relevant files, docs, or prior work if in a codebase.
2. **Clarify the goal**: Ask 1-2 focused questions using multiple-choice options.
   - What is the desired outcome?
   - What are the constraints (time, tech, scope)?
   - Who benefits and how?
3. **Frame the problem**: Restate the challenge in one sentence. Confirm with user.


Keep questions focused. One question per message. Multiple choice preferred over open-ended.


## Optional: Web Research


When the topic benefits from external knowledge (state of the art, existing solutions,
best practices, competitor analysis, academic research), ask the user via AskUserQuestion:


> "Would web research help inform this brainstorm? I can search for [specific topic]."


If approved, use WebSearch/WebFetch to gather relevant information before generating ideas.
Summarize findings concisely and feed them into Phase 2. Always cite sources.


Do NOT research automatically — always ask first. The user decides whether
external input is needed or whether the brainstorm should stay internal.


## Phase 2: Divergent — Generate Ideas


Apply techniques situationally. Pick 2-3 that fit the problem, not all four every time.


### Technique 1: Reverse Brainstorming


"How would we make this as bad as possible?"


1. List 3-5 ways to guarantee failure
2. Invert each into a design principle
3. Extract actionable approaches from the inversions


### Technique 2: SCAMPER


Run through these lenses on the problem:


| Lens | Question |
|------|----------|
| **S**ubstitute | What component could be replaced? |
| **C**ombine | What existing things could merge? |
| **A**dapt | What solved problem resembles this? |
| **M**odify | What if we scaled up/down a dimension? |
| **P**ut to other use | Can an existing tool serve this need? |
| **E**liminate | What can we remove entirely? |
| **R**everse | What if we flipped the flow/order? |


### Technique 3: Perspective Shifts


Evaluate through different stakeholder lenses:


- **User**: What feels simplest and most intuitive?
- **Developer**: What is easiest to build and maintain?
- **Ops/Admin**: What is easiest to deploy and monitor?
- **Security/Privacy**: What minimizes attack surface and data exposure?
- **Future Self**: What will we thank ourselves for in 6 months?


Add domain-specific perspectives as needed (e.g., Reviewer, Reader, Customer).


### Technique 4: Analogies


1. Identify the core pattern of the problem (not the domain)
2. Find 2-3 solved problems with the same pattern in different domains
3. Map their solutions back to the current problem
4. Extract novel approaches from the mapping


### Output of Phase 2


Present **3+ distinct approaches** as a comparison table:


| Approach | Core Idea | Strength | Weakness | Complexity |
|----------|-----------|----------|----------|------------|
| A        | ...       | ...      | ...      | Low/Med/High |
| B        | ...       | ...      | ...      | Low/Med/High |
| C        | ...       | ...      | ...      | Low/Med/High |


Include a clear recommendation with reasoning.


## Phase 3: Convergent — Evaluate & Refine


After user selects or combines approaches:


1. **Deep-dive the chosen approach**: Flesh out details, sub-decisions, edge cases.
2. **Stress-test**: What could go wrong? What assumptions are we making?
3. **Simplify**: Can anything be removed without losing the core value?
4. **Present section by section**: Break the design into logical sections.
   Get approval on each before moving to the next.


### Section Presentation Format


For each section:


### Section: [Name]


**What:** [One-sentence summary]
**Why:** [Why this choice over alternatives]
**Trade-off:** [What we're giving up]
**Open questions:** [If any remain]


Wait for user confirmation before presenting the next section.


## Phase 4: Wrap Up


1. **Summarize** the final design in a concise overview (5-10 bullet points max).
2. **List open questions** that remain unresolved.
3. **Suggest next steps**: Which skill or workflow to use next.
   - Implementation planning? Suggest `EnterPlanMode` or `plan-review`
   - Need tests first? Suggest `tdd`
   - Frontend work? Suggest `frontend-design`
   - More research needed? Suggest an `Explore` agent


Do NOT automatically save a design document. Only save if the user explicitly asks.


## Verification


Before delivering the final summary, check:


1. **Baseline test**: Would Claude without this skill produce something structurally similar?
   If yes — the brainstorming didn't add value. Redo Phase 2 with different techniques.
2. **Minimum alternatives**: Were at least 3 distinct approaches presented and evaluated?
3. **Technique evidence**: Can you point to specific ideas that came from applying
   a named technique (Reverse, SCAMPER, Perspective, Analogy)?
4. **YAGNI check**: Does the final design contain unnecessary complexity?
   Strip it before delivering.
5. **Divergent-before-convergent**: Did narrowing happen only AFTER broad exploration?
