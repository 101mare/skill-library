---
name: team-builder
description: |
  Knowledge for orchestrating Claude Code agent teams — multiple independent sessions
  coordinated by a team lead with shared tasks and inter-agent messaging.
  Use when work benefits from parallel exploration with communication between workers.
  Recognizes: "create a team", "agent team", "team-builder", "parallel teammates",
  "coordinate multiple agents", "spawn teammates", "team lead", "shared task list"
---

# Team Builder

Knowledge for designing and running Claude Code agent teams — multiple independent Claude Code sessions working together.

## Official Docs

- [Agent Teams](https://code.claude.com/docs/en/agent-teams) — Authoritative reference for team setup, display modes, task coordination, and limitations

---

## When to Use Teams vs Subagents

| | Subagents | Agent Teams |
|---|---|---|
| **Context** | Own context; results return to caller | Own context; fully independent |
| **Communication** | Report back to main agent only | Teammates message each other directly |
| **Coordination** | Main agent manages all work | Shared task list with self-coordination |
| **Best for** | Focused tasks where only the result matters | Complex work requiring discussion and collaboration |
| **Token cost** | Lower: results summarized back | Higher: each teammate is a separate Claude instance |

**Use subagents** when you need quick, focused workers that report back.
**Use agent teams** when teammates need to share findings, challenge each other, and coordinate on their own.

### Strong Use Cases for Teams

- **Research and review**: multiple teammates investigate different aspects simultaneously, then share and challenge findings
- **New modules or features**: teammates each own a separate piece without stepping on each other
- **Debugging with competing hypotheses**: teammates test different theories in parallel and converge faster
- **Cross-layer coordination**: changes spanning frontend, backend, and tests, each owned by a different teammate

### When NOT to Use Teams

Teams add coordination overhead and use significantly more tokens. Avoid when:
- Tasks are sequential (each step depends on the previous)
- Work involves same-file edits (leads to overwrites)
- The task has many dependencies between parts
- A single session or subagents would suffice

---

## Setup

Agent teams are experimental and disabled by default. Enable via settings:

```json
// settings.json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

Or set the environment variable directly: `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`

---

## Starting a Team

Describe the task and team structure in natural language. Claude creates the team, spawns teammates, and coordinates:

```
Create an agent team to review PR #142. Spawn three reviewers:
- One focused on security implications
- One checking performance impact
- One validating test coverage
Have them each review and report findings.
```

Claude decides the number of teammates based on the task, or you can specify exactly what you want:

```
Create a team with 4 teammates to refactor these modules in parallel.
Use Sonnet for each teammate.
```

---

## Architecture

| Component | Role |
|---|---|
| **Team lead** | Main session that creates the team, spawns teammates, coordinates work |
| **Teammates** | Separate Claude Code instances working on assigned tasks |
| **Task list** | Shared list of work items that teammates claim and complete |
| **Mailbox** | Messaging system for communication between agents |

Storage:
- Team config: `~/.claude/teams/{team-name}/config.json`
- Task list: `~/.claude/tasks/{team-name}/`

---

## Display Modes

| Mode | Behavior | Requirement |
|---|---|---|
| `auto` (default) | Split panes if in tmux, in-process otherwise | -- |
| `in-process` | All teammates in main terminal, Shift+Down to cycle | Any terminal |
| `tmux` | Each teammate in own pane, auto-detects tmux vs iTerm2 | tmux or iTerm2 |

```json
// settings.json
{ "teammateMode": "in-process" }
```

Or per-session: `claude --teammate-mode in-process`

---

## Controlling the Team

### Talk to teammates directly

- **In-process**: Shift+Down to cycle, type to message. Enter to view session, Escape to interrupt. Ctrl+T for task list.
- **Split panes**: Click into a pane to interact directly.

### Require plan approval

For complex or risky tasks, teammates plan in read-only mode until the lead approves:

```
Spawn an architect teammate to refactor the authentication module.
Require plan approval before they make any changes.
```

### Task coordination

Tasks have three states: pending, in progress, completed. Tasks can depend on other tasks. The lead assigns tasks or teammates self-claim. File locking prevents race conditions.

### Shutdown

```
Ask the researcher teammate to shut down
```

Then when all are stopped:

```
Clean up the team
```

Always use the lead for cleanup — teammates should not run cleanup.

---

## Best Practices

### Give teammates enough context

Teammates load project context (CLAUDE.md, MCP, skills) but **not** the lead's conversation history. Include task-specific details in spawn prompts:

```
Spawn a security reviewer teammate with the prompt: "Review the authentication
module at src/auth/ for security vulnerabilities. Focus on token handling,
session management, and input validation. The app uses JWT tokens stored in
httpOnly cookies. Report issues with severity ratings."
```

### Right-size the team

- Start with **3-5 teammates** for most workflows
- Aim for **5-6 tasks per teammate**
- Token costs scale linearly with teammates
- Three focused teammates often outperform five scattered ones

### Size tasks appropriately

- **Too small**: coordination overhead exceeds benefit
- **Too large**: teammates work too long without check-ins
- **Just right**: self-contained units with clear deliverables (a function, a test file, a review)

### Avoid file conflicts

Two teammates editing the same file leads to overwrites. Break work so each teammate owns different files.

### Monitor and steer

Check progress, redirect approaches that aren't working, synthesize findings as they come in. Unattended teams risk wasted effort.

---

## Hooks for Quality Gates

| Hook | Trigger | Use |
|---|---|---|
| `TeammateIdle` | Teammate about to go idle | Exit code 2 sends feedback, keeps teammate working |
| `TaskCompleted` | Task being marked complete | Exit code 2 prevents completion, sends feedback |

---

## Prompt Patterns

### Parallel Code Review

```
Create an agent team to review PR #142. Spawn three reviewers:
- One focused on security implications
- One checking performance impact
- One validating test coverage
Have them each review and report findings.
```

### Competing Hypotheses

```
Users report the app exits after one message instead of staying connected.
Spawn 5 agent teammates to investigate different hypotheses. Have them talk to
each other to try to disprove each other's theories, like a scientific
debate. Update the findings doc with whatever consensus emerges.
```

### Research from Multiple Angles

```
I'm designing a CLI tool that helps developers track TODO comments across
their codebase. Create an agent team to explore this from different angles: one
teammate on UX, one on technical architecture, one playing devil's advocate.
```

---

## Limitations

- **No session resumption**: `/resume` and `/rewind` don't restore in-process teammates
- **Task status can lag**: teammates sometimes fail to mark tasks completed, blocking dependents
- **One team per session**: clean up current team before starting a new one
- **No nested teams**: teammates cannot spawn their own teams
- **Lead is fixed**: can't promote a teammate to lead
- **Permissions set at spawn**: all teammates start with lead's mode, changeable after
- **Split panes**: not supported in VS Code terminal, Windows Terminal, or Ghostty

---

## Checklist

- [ ] `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` enabled
- [ ] Task genuinely benefits from parallel work with communication
- [ ] Team size appropriate (3-5 for most workflows)
- [ ] Tasks sized correctly (5-6 per teammate)
- [ ] No same-file edits between teammates
- [ ] Spawn prompts include enough context
- [ ] Display mode configured (in-process vs split panes)
- [ ] Plan approval required for risky tasks
- [ ] Quality gate hooks configured if needed
- [ ] Cleanup via lead after shutdown
