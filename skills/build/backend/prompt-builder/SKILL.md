---
name: prompt-builder
description: |
  Transforms unstructured user requests into optimized, structured prompts.
  Systematically asks clarifying questions about goals, context, constraints,
  and output format. Suggests improvements before generating the final prompt.
  Adapts language to match user's input language automatically.
  Triggers: "build prompt", "structure request", "optimize prompt",
  "better prompt", "make a prompt from this", "improve prompt",
  "create a prompt for", "help me write a prompt"
user-invocable: true
---

# Prompt Builder

Transform unstructured requests into optimized, structured prompts using Anthropic's best practices.

## Language Adaptation

Match the user's language:
- German input → German questions and suggestions, prompt can be English or German based on context
- English input → English questions and suggestions

## Workflow: 3 Phases

### Phase 1: Analysis & Clarifying Questions

Before generating any prompt, systematically gather information across these 7 categories.
Present questions clearly and group related ones together.

**1. Goal**
- What is the primary objective?
- What should the AI accomplish?
- Is this a single task or multi-step workflow?

**2. Identity & Context (Soul Formula)**
- Does this prompt need a specialist role? If yes:
  - What specific experiences should the role have? (not "expert in X" but "has done Y, seen Z fail")
  - What mistakes has this specialist learned from? What hard lessons define their approach?
  - What does this specialist refuse to do? (anti-patterns, shortcuts they reject)
- What is the background/situation?
- Who is the target audience?
- What domain knowledge is relevant?

**3. Input**
- What data/information will be provided?
- What format is the input in?
- Are there variable placeholders needed (use `{$VARIABLE_NAME}` format)?

**4. Output**
- What format should the response be in? (prose, list, JSON, XML, code, etc.)
- What length/detail level is expected?
- Are there specific sections or structure requirements?

**5. Constraints**
- What must be avoided? (topics, styles, behaviors)
- What must be included? (mandatory elements)
- Are there word limits, tone requirements, or forbidden patterns?

**6. Quality Criteria**
- How will success be measured?
- What makes a response "good" vs "bad"?
- Are there edge cases to handle?

**7. Examples**
- Are there example inputs and desired outputs?
- Are there anti-examples (what NOT to produce)?
- Are there reference materials or style guides?

**Questioning Strategy - MANDATORY TOOL USAGE:**

You MUST use the `AskUserQuestion` tool for ALL questions. Never list questions as plain text.

**Rules:**
1. **Always use AskUserQuestion** - never write questions as prose that the user can't click on
2. **Group related questions** - up to 4 questions per tool call
3. **Provide options** - always include 2-4 clickable options (user can always add "Other")
4. **Ask in batches** - don't wait for one answer before asking the next batch

**Example - WRONG (don't do this):**
```
"I have some questions:
1. What is the target audience?
2. What format should the output be?
3. Are there any constraints?"
```

**Example - CORRECT (always do this):**
```
Use AskUserQuestion tool with:
questions: [
  {question: "Who is the target audience?", header: "Audience", options: [{label: "Developers", ...}, {label: "End users", ...}, ...]},
  {question: "What output format do you need?", header: "Format", options: [{label: "JSON", ...}, {label: "Prose", ...}, ...]},
  ...
]
```

**Open-ended info that genuinely can't have predefined options:** Only then ask as text, but this should be rare (e.g., "Paste your example input/output here").

### Phase 2: Improvement Suggestions

After gathering information, before generating the prompt:

1. **Identify potential issues**
   - Ambiguous requirements
   - Missing information that could cause problems
   - Conflicting constraints

2. **Suggest enhancements**
   - Additional constraints that might be helpful
   - Alternative approaches to consider
   - Edge cases that should be addressed

3. **Evaluate Soul quality** (for prompts with a role)
   - Is the identity experiential or just a flat label? Suggest specific experiences if flat
   - Are anti-patterns specific and actionable? ("I don't accept X" not "I don't do bad things")
   - Would a productive weakness improve output quality?
   - Does each experience map to a concrete behavior?

4. **Recommend best practices**
   - Would examples improve consistency?
   - Should chain-of-thought reasoning be included?
   - Would structured output tags help parsing?

5. **Get user confirmation (use AskUserQuestion)**
   - Present suggestions as text, then use `AskUserQuestion` for approval
   - Example: After listing suggestions, ask "Which improvements should I include?" with multiSelect: true
   - Only proceed to generation after confirmation

### Phase 3: Structured Prompt Generation

Generate the final prompt using this XML structure. The `<system>` section uses the **Soul Formula** — research shows generic labels ("You are an expert in X") have zero improvement, while experiential identities improve accuracy by 10-60% (NAACL 2024).

```xml
<system>
[Soul — Experiential Identity, NOT a flat role label]

Structure:
1. "You are a [role] who has [specific experience 1], [specific experience 2],
   and [specific experience 3]."
   → Each experience activates a specific knowledge cluster
   → End with a metaphor that captures the approach (optional)

2. "I've learned that [insight] because [experience]."
   → Tells the model WHERE to focus, not just WHAT to find

3. "What I Refuse To Do:" (devote 30-40% of prompt to this)
   - "I don't [specific anti-pattern 1]."
   - "I don't [specific anti-pattern 2]."
   → Each refusal: specific, experiential, actionable
   → Prevents the model from cutting corners

4. "I sometimes [limitation]. That's the cost of [strength].
   The benefit is [concrete outcome]." (optional productive weakness)
</system>

<context>
[Background information]
[Relevant domain knowledge]
[Situational details]
</context>

<instructions>
[Numbered, clear, actionable steps]
[Use positive framing: "Do X" not "Don't do Y"]
[Include chain-of-thought guidance if complex]
</instructions>

<constraints>
[Hard rules and boundaries]
[Required elements]
[Forbidden patterns or topics]
</constraints>

<output_format>
[Expected structure of the response]
[Formatting requirements]
[Length guidelines]
</output_format>

<examples>
[Optional: 2-3 diverse input/output examples]
[Include both good examples and edge cases if helpful]
</examples>
```

**Note:** Not all sections are required for every prompt. Omit sections that aren't relevant.

#### Soul Formula — Quick Reference

| Part | Formula | Purpose |
|------|---------|---------|
| Identity | "You are a [role] who has [experience 1], [experience 2]..." | Activates specific knowledge clusters |
| Learned Insight | "I've learned that [insight] because [experience]." | Directs focus |
| Anti-Patterns | "I don't [specific refusal]." (30-40% of `<system>`) | Creates reliability boundaries |
| Productive Weakness | "I sometimes [limitation]. That's the cost of [strength]." | Prevents overconfidence |

**When to apply the full Soul Formula:**
- Prompts for **specialist roles** (reviewers, analysts, advisors) — always use full Soul
- Prompts for **simple transformations** (formatter, converter) — identity + 2-3 anti-patterns suffice
- Prompts with **no role** (pure task instructions) — Soul is optional, but anti-patterns still help

## Anthropic Best Practices Checklist

Apply these principles from Claude 4/Opus documentation:

### Structure & Clarity
- [ ] Use XML tags to separate prompt sections
- [ ] Place long context/documents BEFORE instructions
- [ ] Use consistent tag names throughout
- [ ] Number instructions for complex tasks

### Identity (Soul Formula)
- [ ] Use experiential identity, not flat labels ("expert in X" → zero improvement)
- [ ] Each experience maps to a specific behavior the model should exhibit
- [ ] Anti-patterns are specific, experiential, and actionable (30-40% of `<system>`)
- [ ] Productive weakness included for specialist roles (prevents overconfidence)

### Instruction Quality
- [ ] Be specific and explicit about desired behavior
- [ ] Use positive framing ("Write concisely" not "Don't be verbose")
- [ ] Avoid the word "think" → use "consider", "evaluate", "assess"
- [ ] Don't use aggressive language (no "CRITICAL", "MUST", "NEVER" in caps)

### Reasoning & Examples
- [ ] Include chain-of-thought guidance for complex tasks
- [ ] Provide 3-5 diverse examples for format-sensitive tasks
- [ ] Use `<scratchpad>` or `<analysis>` tags to encourage reasoning
- [ ] Request justification before conclusions for evaluative tasks

### Output Control
- [ ] Specify output format explicitly
- [ ] Match prompt formatting style to desired output style
- [ ] Use `{$VARIABLE}` placeholders for dynamic content
- [ ] Include length/detail guidance

## Variable Placeholder Format

When prompts need dynamic input, use this format:
- `{$VARIABLE_NAME}` - ALL_CAPS with underscores
- Example: `{$DOCUMENT}`, `{$USER_QUERY}`, `{$CONTEXT}`

## Tool & Agent Integration

When the prompt topic aligns with available specialized tools, include instructions for Claude to use them:

**Add to `<instructions>` section when relevant:**
```xml
<instructions>
...
[If the task involves frontend/UI work:]
Use the warmgold-frontend skill for UI implementation.

[If the task involves code review:]
Use the reviewer agent for code quality, security, logging, and privacy review.

[If the task involves testing:]
Use the test-architect agent to create or review tests.

[If the task involves performance or architecture analysis:]
Use the analyzer agent to identify bottlenecks, architecture issues, and dependency health.

[General pattern:]
Before implementing, check if a specialized skill or agent is available for this task type and use it.
</instructions>
```

**Key principle:** Prompts should instruct Claude to leverage specialized agents/skills when the task domain matches, rather than doing everything manually.

## Output Presentation

When presenting the final prompt:

1. Show the complete prompt in a code block
2. Explain key design decisions briefly
3. Note any assumptions made
4. Suggest how to test/iterate on the prompt
5. Recommend relevant skills/agents if the prompt topic matches available specializations

## Additional Resources

For complex prompts, reference [examples.md](examples.md) for transformation patterns.
