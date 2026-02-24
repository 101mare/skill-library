---
name: plan-review
description: |
  Reviews implementation plans before coding begins. Checks completeness, architecture fit,
  risks, and requirement alignment. Uses specialized agents in parallel for thorough analysis.
  Proactively asks clarifying questions when uncertainties are found.
  Use when: reviewing plans, before implementation, user asks "is the plan good?",
  "review my plan", "check this approach", "before I start coding".
---

# Plan Review

Comprehensive plan review to catch issues before implementation begins.

## Workflow Overview

```
1. Identify Plan -> 2. Clarify Context -> 3. Load Agent Prompts -> 4. Parallel Reviews -> 5. Aggregate & Clarify -> 6. Verdict
```

## Agent Loading (CRITICAL)

This skill relies on custom agent definitions in `.claude/agents/*.md`. Since the Task tool only supports
`general` and `explore` subagent types, you MUST load agent expertise by **reading their .md files**
and including the system prompt content in the Task prompt.

### How to Use Custom Agents

1. **Read the agent file** with the Read tool: `.claude/agents/{agent-name}.md`
2. **Extract the system prompt** (everything after the YAML frontmatter `---`)
3. **Pass it as context** in the Task tool prompt, prefixed with the role instruction
4. **Use `explore`** for read-only review agents, `general` for agents that need write access

### Available Agent Files for Plan Review

| Agent File | Review Focus |
|------------|-------------|
| `.claude/agents/reviewer.md` | Security, types, logging, privacy, best practices |
| `.claude/agents/analyzer.md` | Architecture fit, performance, dependencies, scalability |
| `.claude/agents/planner.md` | Completeness, requirements, risks |
| `.claude/agents/test-architect.md` | Test strategy completeness |

## Step 1: Identify the Plan

Locate the plan to review:

### Search Locations

1. **Plan files**: Check `.claude/plans/` directory
2. **Conversation context**: Look for recent plan output
3. **Plan mode output**: Check if ExitPlanMode was recently used

```bash
# Check for plan files
ls -la .claude/plans/ 2>/dev/null || echo "No plans directory"
```

### If Plan Unclear

```
Use AskUserQuestion:
Question: "Which plan should I review?"
Options:
  - "The most recently created plan"
  - "Plan from .claude/plans/"
  - "I'll describe the plan briefly"
  - "Cancel"
```

## Step 2: Clarify Context and Requirements

**IMPORTANT**: Proactively ask questions to understand the context.

### Required Questions

```
Use AskUserQuestion:
Question: "What is the goal of this plan? What should it achieve?"
Options:
  - "Implement new feature"
  - "Fix a bug"
  - "Refactoring"
  - "Improve performance"
```

### Context Questions (as needed)

Ask further questions when:
- The goal is unclear
- Requirements are implicit
- Constraints have not been mentioned
- Edge cases have not been addressed

```
Use AskUserQuestion:
Question: "Are there specific requirements or constraints?"
Options:
  - "Must be backward compatible"
  - "Performance-critical"
  - "Security-relevant"
  - "No special constraints"
```

## Step 3: Run Parallel Reviews

First **read the relevant agent .md files**, then spawn `explore` agents **in parallel** (single message, multiple Task calls), injecting each agent's system prompt + a plan-review-specific role into the Task prompt.

### Agent Assignments

| Review Role | Agent File to Load | Focus | Key Questions |
|-------------|-------------------|-------|---------------|
| Completeness Checker | `reviewer.md` | Completeness + Code Quality | All steps? Dependencies? Tests? Types? |
| Architecture Analyzer | `analyzer.md` | Architecture Fit | Matches patterns? Correct modules? DI? |
| Risk Assessor | `analyzer.md` | Risks + Performance | Breaking Changes? Security? Complexity? N+1? |
| Requirements Verifier | `planner.md` | Requirements | Does the plan meet the goals? |

### Execution Steps

1. **Read agent files** (parallel Read calls):
   ```
   Read(".claude/agents/reviewer.md")
   Read(".claude/agents/analyzer.md")
   Read(".claude/agents/planner.md")
   # + any additional agents based on plan content
   ```

2. **Spawn 4 Task agents in parallel** (single message, multiple Task calls):

   ```
   # Agent 1: Completeness Checker
   Task(
     subagent_type="explore",
     prompt="""You are a Plan Completeness Checker with code review expertise.

     <agent-expertise>
     [content from reviewer.md after frontmatter]
     </agent-expertise>

     Review this implementation plan for COMPLETENESS:

     <plan>
     [Plan content]
     </plan>

     Goal: [user's goal]
     Constraints: [known constraints]

     Check:
     1. Are all implementation steps listed?
     2. Are dependencies between steps identified?
     3. Is a test strategy included?
     4. Are error handling steps planned?
     5. Are security considerations addressed?

     Return findings by severity: BLOCKER > GAP > SUGGESTION.
     """
   )

   # Agent 2: Architecture Fit Analyzer
   Task(
     subagent_type="explore",
     prompt="""You are an Architecture Fit Analyzer with codebase analysis expertise.

     <agent-expertise>
     [content from analyzer.md after frontmatter]
     </agent-expertise>

     Review this implementation plan for ARCHITECTURE FIT:

     <plan>
     [Plan content]
     </plan>

     Goal: [user's goal]

     Check against the project's patterns (read CLAUDE.md if needed):
     1. Does it follow the project's dependency injection patterns?
     2. Are interfaces/protocols defined for new components?
     3. Are constants centralized, not magic numbers?
     4. Does it follow the existing module structure?
     5. Are config models used for new configuration?

     Return findings by severity: BLOCKER > DEVIATION > SUGGESTION.
     """
   )

   # Agent 3: Risk Assessor
   Task(
     subagent_type="explore",
     prompt="""You are an Implementation Risk Assessor with analysis expertise.

     <agent-expertise>
     [content from analyzer.md after frontmatter]
     </agent-expertise>

     Review this implementation plan for RISKS:

     <plan>
     [Plan content]
     </plan>

     Goal: [user's goal]

     Assess:
     1. Breaking changes to existing APIs/interfaces?
     2. Performance risks (N+1, blocking I/O, memory)?
     3. Security vulnerabilities introduced?
     4. Complexity - is the approach over-engineered?
     5. Privacy risks (unintended external calls, data leakage)?

     Return findings by severity: CRITICAL > HIGH > MEDIUM > LOW.
     """
   )

   # Agent 4: Requirements Verifier
   Task(
     subagent_type="explore",
     prompt="""You are a Requirements Verifier with planning expertise.

     <agent-expertise>
     [content from planner.md after frontmatter]
     </agent-expertise>

     Review this plan against the stated requirements:

     <plan>
     [Plan content]
     </plan>

     Original Goal: [user's goal]
     Constraints: [known constraints]

     Verify:
     1. Does the plan fully address the stated goal?
     2. Are all explicit requirements covered?
     3. Are implicit requirements handled (error cases, edge cases)?
     4. Are there unstated assumptions that should be clarified?
     5. Will the result be testable/verifiable?

     Return findings by severity: BLOCKER > GAP > SUGGESTION.
     """
   )
   ```

3. **Aggregate results** from all agents and proceed to Step 4.

## Step 4: Aggregate Results and Clarify

### Collect Results

After all reviews are complete, create an overview:

```markdown
## Plan Review Results

### Overview

| Agent | Status | Findings |
|-------|--------|----------|
| Completeness | pass/warn/fail | X issues |
| Architecture | pass/warn/fail | X issues |
| Risks | pass/warn/fail | X issues |
| Requirements | pass/warn/fail | X issues |
```

### Categorize Findings

```markdown
### BLOCKER (Must be resolved before implementation)
1. [Finding + Source]
2. [Finding + Source]

### GAPS (Missing elements in the plan)
1. [Missing element]
2. [Incomplete step]

### DEVIATIONS (Deviations from standards)
1. [Pattern not followed]
2. [Convention not adhered to]

### RISKS (Identified risks)
1. [Risk + Severity]
2. [Risk + Severity]

### POSITIVES
1. [What is good about the plan]
```

### Proactive Clarification on Uncertainties

**IMPORTANT**: Actively ask questions when uncertainties are found:

```
Use AskUserQuestion:
Question: "The plan mentions 'improved error handling' - what exactly is meant?"
Options:
  - "Add retry logic"
  - "Better error messages"
  - "Extend logging"
  - "All of the above"
```

```
Use AskUserQuestion:
Question: "Step 3 has no test strategy - should tests be added?"
Options:
  - "Yes, unit tests"
  - "Yes, unit + integration tests"
  - "No, later"
  - "I'll test manually"
```

### Verification Questions

Involve the user on critical points:

```
Use AskUserQuestion:
Question: "The risk assessment shows potential breaking changes. Is backward compatibility important?"
Options:
  - "Yes, critical"
  - "Would be nice, but not critical"
  - "No, it can break"
```

## Step 5: Present Verdict

### Verdict Matrix

```markdown
## Plan Review Verdict

### Traffic Light Status

| Category | Status | Reason |
|----------|--------|--------|
| Completeness | GREEN/YELLOW/RED | [Brief justification] |
| Architecture Fit | GREEN/YELLOW/RED | [Brief justification] |
| Risk Level | GREEN/YELLOW/RED | [Brief justification] |
| Requirements | GREEN/YELLOW/RED | [Brief justification] |

### Overall Assessment

GREEN **PLAN APPROVED** - Ready for implementation
YELLOW **PLAN NEEDS WORK** - Clarify points before implementation
RED **PLAN BLOCKED** - Critical issues must be resolved
```

### Recommendations

```markdown
### Recommended Changes to the Plan

1. **[Priority 1]**: [Specific change]
2. **[Priority 2]**: [Specific change]
3. **[Priority 3]**: [Specific change]

### Questions to Clarify

1. [Open question 1]
2. [Open question 2]
```

### User Decision

```
Use AskUserQuestion:
Question: "How would you like to proceed?"
Options:
  - "Adjust the plan and review again"
  - "Implement anyway (risks accepted)"
  - "More details on a finding"
  - "Cancel review"
```

## Proactive Questions - Checklist

The skill should **proactively** use AskUserQuestion for:

### When the plan is unclear
- [ ] Ambiguous wording ("improve", "optimize", "clean up")
- [ ] Missing details (which file? which method?)
- [ ] Unclear step ordering

### When risk findings arise
- [ ] Breaking changes - Is that acceptable?
- [ ] Security concerns - How important is this?
- [ ] Performance impact - Acceptable latency?

### When architecture deviations are found
- [ ] Intentional deviation or oversight?
- [ ] Should this become a new pattern?

### For verification
- [ ] Are the extracted requirements correct?
- [ ] Were all requirements captured?
- [ ] Are there implicit requirements?

## Triggers

Activates on:
- `/plan-review`
- "review plan", "check plan", "validate plan"
- "check the plan", "is the plan good?", "review the plan"
- "review implementation plan", "check my approach"
- "before I start coding", "before I begin"
- "is this a good approach?", "does this make sense?"

## Important Notes

- **Agent loading**: ALWAYS read `.claude/agents/*.md` files and inject their prompts into `explore` Task agents
- **Parallelization**: Start all 4 agents simultaneously (one message, multiple Task calls)
- **Match language**: Use the language the user speaks
- **Ask proactively**: Use AskUserQuestion for EVERY uncertainty
- **Be specific**: Provide findings with File:Line where possible
- **Priorities**: Blocker > Gaps > Deviations > Risks > Positives
- **Be constructive**: Don't just name problems, also suggest solutions
- **Additional agents**: The `analyzer` agent covers dependency and architecture analysis. Spawn additional Task agents as needed.
- **Project-agnostic**: This skill works for any project. Read the project's CLAUDE.md to understand its specific architecture, patterns, and constraints before running reviews.
- **Research first**: If the plan involves unfamiliar technology or open technical decisions, use the `deep-research` skill first to gather evidence before reviewing.
