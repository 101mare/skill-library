# Skill Library — Catalog

All available skills, agents, and rules at a glance.

---

## Quickstart: Installing a Skill or Agent

Installation couldn't be simpler — you don't need to configure anything manually. Just tell Claude which skill or agent you want and provide the path to the file.

### How It Works

1. Choose a skill, rule or agent from the catalog below
2. Copy the file path
3. Tell Claude:

```
Copy the skill from /path/to/skill-library/skills/workflow/tdd/SKILL.md into my project
```

Claude reads the file, copies it into your project (`.claude/skills/` for skills, `.claude/agents/` for agents) and registers it automatically.

### Examples

**Install a skill:**
```
Copy the skill from ~/Schreibtisch/skill-library/skills/patterns/testing-patterns/SKILL.md into my project
```
→ Claude copies the file to `.claude/skills/testing-patterns/SKILL.md`

**Install an agent:**
```
Copy the agent from ~/Schreibtisch/skill-library/agents/review/reviewer.md into my project
```
→ Claude copies the file to `.claude/agents/reviewer.md`

### Customizing After Installation

After copying, you can customize the skill in `.claude/skills/` however you like:

- **Change trigger words** — When should Claude automatically activate the skill?
- **Add project-specific rules** — E.g., custom naming conventions, preferred libraries
- **Remove sections** — Delete what you don't need
- **Combine** — Merge parts from multiple skills into your own

---

## Rules (4)

Always-loaded behavioral rules that shape Claude's behavior across all tasks. Copy to `~/.claude/rules/` for global availability or to your project's `.claude/rules/`.

| Name | Description | Path |
|------|------------|------|
| coding-conventions | DRY principles, naming & imports, error handling, function design, type hints, and testing conventions. | [rules/coding-conventions.md](../rules/coding-conventions.md) |
| security | Input validation, PII protection in logs, secrets management, and dependency policies. | [rules/security.md](../rules/security.md) |
| agent-behavior | Read-first workflow, scope discipline, minimal changes, subagent strategy, and bug fixing approach. | [rules/agent-behavior.md](../rules/agent-behavior.md) |
| self-improvement | Learn from corrections, capture patterns in memory, iterate on lessons. | [rules/self-improvement.md](../rules/self-improvement.md) |

---

## Skills (27)

### Meta (3)

| Name | Description | Path |
|------|------------|------|
| skill-builder | Teaches knowledge for creating Claude Code skill files in SKILL.md format with best practices. | [skills/meta/skill-builder/SKILL.md](../skills/meta/skill-builder/SKILL.md) |
| agent-builder | Teaches knowledge for creating Claude Code subagent configuration files with YAML frontmatter and prompts. | [skills/meta/agent-builder/SKILL.md](../skills/meta/agent-builder/SKILL.md) |
| team-builder | Orchestration of Claude Code agent teams — multiple independent sessions, coordinated by a team lead with shared task list and inter-agent messaging. | [skills/meta/team-builder/SKILL.md](../skills/meta/team-builder/SKILL.md) |

### Build — Backend (7)

| Name | Description | Path |
|------|------------|------|
| prompt-builder | Transforms unstructured user requests into optimized, structured prompts through systematic clarification questions. | [skills/build/backend/prompt-builder/SKILL.md](../skills/build/backend/prompt-builder/SKILL.md) |
| logging-builder | Implements Python logging infrastructure with logger configuration, file rotation, and structured logging. | [skills/build/backend/logging-builder/SKILL.md](../skills/build/backend/logging-builder/SKILL.md) |
| config-builder | Creates Python configuration infrastructure with Pydantic models, YAML loading, and environment variable overrides. | [skills/build/backend/config-builder/SKILL.md](../skills/build/backend/config-builder/SKILL.md) |
| exception-builder | Designs Python exception hierarchies for layered applications with base exceptions, layer mapping, and chaining. | [skills/build/backend/exception-builder/SKILL.md](../skills/build/backend/exception-builder/SKILL.md) |
| docker-builder | Creates Dockerfile and docker-compose.yml with multi-stage builds, health checks, network isolation, and GPU setup. | [skills/build/backend/docker-builder/SKILL.md](../skills/build/backend/docker-builder/SKILL.md) |
| ci-cd-builder | Creates GitHub Actions CI/CD pipelines with pytest, linting, Docker build, and release workflows. | [skills/build/backend/ci-cd-builder/SKILL.md](../skills/build/backend/ci-cd-builder/SKILL.md) |
| project-scaffold | Creates production-ready Python project structures with directory layout, pyproject.toml, config, logging, and CI/CD. | [skills/build/backend/project-scaffold/SKILL.md](../skills/build/backend/project-scaffold/SKILL.md) |

### Build — Frontend (2)

| Name | Description | Path |
|------|------------|------|
| frontend-design | Creates distinctive, production-ready frontend interfaces with high design quality that avoid generic AI aesthetics. | [skills/build/frontend/frontend-design/SKILL.md](../skills/build/frontend/frontend-design/SKILL.md) |
| warmgold-frontend | Warm, iOS-inspired design system with component patterns for vanilla HTML/CSS/JS frontends. | [skills/build/frontend/warmgold-frontend/SKILL.md](../skills/build/frontend/warmgold-frontend/SKILL.md) |

### Workflow (7)

| Name | Description | Path |
|------|------------|------|
| plan-review | Reviews implementation plans for completeness, architecture fit, risks, and requirement coverage using parallel specialized agents. | [skills/workflow/plan-review/SKILL.md](../skills/workflow/plan-review/SKILL.md) |
| session-verify | Validates all changes at session end for bugs, security vulnerabilities, dead code, and documentation gaps. | [skills/workflow/session-verify/SKILL.md](../skills/workflow/session-verify/SKILL.md) |
| pr-review | Orchestrates pull request reviews through parallel specialized agents that analyze the diff and aggregate results. | [skills/workflow/pr-review/SKILL.md](../skills/workflow/pr-review/SKILL.md) |
| tdd | Test-driven development workflow in the RED-GREEN-REFACTOR cycle: test-architect → implementation → code-simplifier. | [skills/workflow/tdd/SKILL.md](../skills/workflow/tdd/SKILL.md) |
| deep-research | Structured research workflow (question → sources → analysis → synthesis → documentation) for technical decisions. | [skills/workflow/deep-research/SKILL.md](../skills/workflow/deep-research/SKILL.md) |
| ralph-loop | Autonomous work mode — Claude continues working independently on a task until it's completed or the iteration limit is reached. | [skills/workflow/ralph-loop/SKILL.md](../skills/workflow/ralph-loop/SKILL.md) |
| ralph-loop-prompt-builder | Helps create effective prompts for the Ralph Loop system through clarification questions and structured output. | [skills/workflow/ralph-loop-prompt-builder/SKILL.md](../skills/workflow/ralph-loop-prompt-builder/SKILL.md) |

### Patterns (8)

| Name | Description | Path |
|------|------------|------|
| di-container | Implementation of dependency injection containers with Python Protocols for decoupled, testable applications. | [skills/patterns/di-container/SKILL.md](../skills/patterns/di-container/SKILL.md) |
| protocol-design | Correct use of Python `typing.Protocol` for structural subtyping and interface design between modules. | [skills/patterns/protocol-design/SKILL.md](../skills/patterns/protocol-design/SKILL.md) |
| strategy-registry | Strategy pattern with registry-based dispatch for extensible systems like plugin systems or file type handlers. | [skills/patterns/strategy-registry/SKILL.md](../skills/patterns/strategy-registry/SKILL.md) |
| error-handling | Exception handling across application layers: mapping, retry, severity, and logging. | [skills/patterns/error-handling/SKILL.md](../skills/patterns/error-handling/SKILL.md) |
| resilience-patterns | Retry with backoff, circuit breaker, timeout, and graceful degradation for external dependencies. | [skills/patterns/resilience-patterns/SKILL.md](../skills/patterns/resilience-patterns/SKILL.md) |
| testing-patterns | pytest patterns, fixtures, mocking, parametrize, and property-based testing for Python projects. | [skills/patterns/testing-patterns/SKILL.md](../skills/patterns/testing-patterns/SKILL.md) |
| api-design | REST API design with FastAPI: routing, response models, error handling, and dependencies. | [skills/patterns/api-design/SKILL.md](../skills/patterns/api-design/SKILL.md) |
| systematic-debugging | Structured 4-phase debugging methodology: reproduce → isolate → root-cause → fix and defend. | [skills/patterns/systematic-debugging/SKILL.md](../skills/patterns/systematic-debugging/SKILL.md) |

---

## Agents (5)

### Review (1)

| Name | Description | Path |
|------|------------|------|
| reviewer | Reviews Python code for security (OWASP), type safety, logging, privacy/offline compliance, and best practices. Consolidates python-reviewer, security-reviewer, logging-reviewer, and privacy-auditor. | [agents/review/reviewer.md](../agents/review/reviewer.md) |

### Analyze (1)

| Name | Description | Path |
|------|------------|------|
| analyzer | Analyzes codebases for architecture fit, performance, scalability, dead code, and dependency health. Consolidates architecture-analyzer, performance-analyzer, scalability-analyzer, dead-code-detector, and dependency-auditor. | [agents/analyze/analyzer.md](../agents/analyze/analyzer.md) |

### Plan (1)

| Name | Description | Path |
|------|------------|------|
| planner | Validates implementation plans for completeness, requirements coverage, and risks. Consolidates plan-completeness, requirements-verifier, and risk-assessor. | [agents/plan/planner.md](../agents/plan/planner.md) |

### Build (2)

| Name | Description | Path |
|------|------------|------|
| code-simplifier | Simplifies and refines code for clarity, consistency, and maintainability while preserving full functionality. | [agents/build/code-simplifier.md](../agents/build/code-simplifier.md) |
| test-architect | Creates pytest tests and reviews existing test suites for quality and coverage. | [agents/build/test-architect.md](../agents/build/test-architect.md) |
