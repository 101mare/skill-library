---
name: prompt-builder
description: |
  Transforms unstructured user requests into optimized, structured prompts.
  Systematically asks clarifying questions about goals, context, constraints,
  and output format. Suggests improvements before generating the final prompt.
  Adapts language to match user's input language automatically.
  Triggers: "prompt bauen", "strukturiere anfrage", "prompt optimieren",
  "besserer prompt", "mach prompt daraus", "build prompt", "improve prompt",
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

**1. Goal (Ziel)**
- What is the primary objective?
- What should the AI accomplish?
- Is this a single task or multi-step workflow?

**2. Context (Kontext)**
- What is the background/situation?
- Who is the target audience?
- What domain knowledge is relevant?

**3. Input (Eingabe)**
- What data/information will be provided?
- What format is the input in?
- Are there variable placeholders needed (use `{$VARIABLE_NAME}` format)?

**4. Output (Ausgabe)**
- What format should the response be in? (prose, list, JSON, XML, code, etc.)
- What length/detail level is expected?
- Are there specific sections or structure requirements?

**5. Constraints (Einschränkungen)**
- What must be avoided? (topics, styles, behaviors)
- What must be included? (mandatory elements)
- Are there word limits, tone requirements, or forbidden patterns?

**6. Quality Criteria (Qualitätskriterien)**
- How will success be measured?
- What makes a response "good" vs "bad"?
- Are there edge cases to handle?

**7. Examples (Beispiele)**
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

3. **Recommend best practices**
   - Would examples improve consistency?
   - Should chain-of-thought reasoning be included?
   - Would structured output tags help parsing?

4. **Get user confirmation (use AskUserQuestion)**
   - Present suggestions as text, then use `AskUserQuestion` for approval
   - Example: After listing suggestions, ask "Which improvements should I include?" with multiSelect: true
   - Only proceed to generation after confirmation

### Phase 3: Structured Prompt Generation

Generate the final prompt using this XML structure:

```xml
<system>
[Role definition: expertise, personality, perspective]
[Key behaviors and communication style]
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

## Anthropic Best Practices Checklist

Apply these principles from Claude 4/Opus documentation:

### Structure & Clarity
- [ ] Use XML tags to separate prompt sections
- [ ] Place long context/documents BEFORE instructions
- [ ] Use consistent tag names throughout
- [ ] Number instructions for complex tasks

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
Use the ui-architect-pro or frontend-warmgold-builder agent for UI implementation.

[If the task involves code review:]
Use the appropriate reviewer agent (python-backend-reviewer, frontend-warmgold-reviewer, logging-reviewer).

[If the task involves testing:]
Use the test-architect agent to create or review tests.

[If the task involves performance:]
Use the performance-analyzer agent to identify bottlenecks.

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
