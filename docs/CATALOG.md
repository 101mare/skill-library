# Skill Library — Catalog

> [README](../README.md) | **CATALOG** | [SKILLS-EXPLAINED](SKILLS-EXPLAINED.md) | [ARTICLE](ARTICLE.md)

> [!TIP]
> To install any skill or agent below, see [Quickstart](../README.md#quickstart) in the README.

## Rules (4)

*Always loaded — shape every interaction.*

| Name | Description |
|------|------------|
| [coding-conventions](../rules/coding-conventions.md) | DRY principles, naming & imports, error handling, function design, type hints, and testing conventions. |
| [security](../rules/security.md) | Input validation, PII protection in logs, secrets management, and dependency policies. |
| [agent-behavior](../rules/agent-behavior.md) | Read-first workflow, scope discipline, minimal changes, subagent strategy, and bug fixing approach. |
| [self-improvement](../rules/self-improvement.md) | Learn from corrections, capture patterns in memory, iterate on lessons. |

---

## Skills (27)

*Load on demand — teach Claude specialized workflows.*

### Meta (3)

| Name | Description |
|------|------------|
| [skill-builder](../skills/meta/skill-builder/SKILL.md) | Teaches knowledge for creating Claude Code skill files in SKILL.md format with best practices. |
| [agent-builder](../skills/meta/agent-builder/SKILL.md) | Teaches knowledge for creating Claude Code subagent configuration files with YAML frontmatter and prompts. |
| [team-builder](../skills/meta/team-builder/SKILL.md) | Orchestration of Claude Code agent teams — multiple independent sessions, coordinated by a team lead with shared task list and inter-agent messaging. |

### Build — Backend (7)

| Name | Description |
|------|------------|
| [prompt-builder](../skills/build/backend/prompt-builder/SKILL.md) | Transforms unstructured user requests into optimized, structured prompts through systematic clarification questions. |
| [logging-builder](../skills/build/backend/logging-builder/SKILL.md) | Implements Python logging infrastructure with logger configuration, file rotation, and structured logging. |
| [config-builder](../skills/build/backend/config-builder/SKILL.md) | Creates Python configuration infrastructure with Pydantic models, YAML loading, and environment variable overrides. |
| [exception-builder](../skills/build/backend/exception-builder/SKILL.md) | Designs Python exception hierarchies for layered applications with base exceptions, layer mapping, and chaining. |
| [docker-builder](../skills/build/backend/docker-builder/SKILL.md) | Creates Dockerfile and docker-compose.yml with multi-stage builds, health checks, network isolation, and GPU setup. |
| [ci-cd-builder](../skills/build/backend/ci-cd-builder/SKILL.md) | Creates GitHub Actions CI/CD pipelines with pytest, linting, Docker build, and release workflows. |
| [project-scaffold](../skills/build/backend/project-scaffold/SKILL.md) | Creates production-ready Python project structures with directory layout, pyproject.toml, config, logging, and CI/CD. |

### Build — Frontend (2)

| Name | Description |
|------|------------|
| [frontend-design](../skills/build/frontend/frontend-design/SKILL.md) | Creates distinctive, production-ready frontend interfaces with high design quality that avoid generic AI aesthetics. |
| [warmgold-frontend](../skills/build/frontend/warmgold-frontend/SKILL.md) | Warm, iOS-inspired design system with component patterns for vanilla HTML/CSS/JS frontends. |

### Workflow (7)

| Name | Description |
|------|------------|
| [plan-review](../skills/workflow/plan-review/SKILL.md) | Reviews implementation plans for completeness, architecture fit, risks, and requirement coverage using parallel specialized agents. |
| [session-verify](../skills/workflow/session-verify/SKILL.md) | Validates all changes at session end for bugs, security vulnerabilities, dead code, and documentation gaps. |
| [pr-review](../skills/workflow/pr-review/SKILL.md) | Orchestrates pull request reviews through parallel specialized agents that analyze the diff and aggregate results. |
| [tdd](../skills/workflow/tdd/SKILL.md) | Test-driven development workflow in the RED-GREEN-REFACTOR cycle: test-architect → implementation → code-simplifier. |
| [deep-research](../skills/workflow/deep-research/SKILL.md) | Structured research workflow (question → sources → analysis → synthesis → documentation) for technical decisions. |
| [ralph-loop](../skills/workflow/ralph-loop/SKILL.md) | Autonomous work mode — Claude continues working independently on a task until it's completed or the iteration limit is reached. |
| [ralph-loop-prompt-builder](../skills/workflow/ralph-loop-prompt-builder/SKILL.md) | Helps create effective prompts for the Ralph Loop system through clarification questions and structured output. |

### Patterns (8)

| Name | Description |
|------|------------|
| [di-container](../skills/patterns/di-container/SKILL.md) | Implementation of dependency injection containers with Python Protocols for decoupled, testable applications. |
| [protocol-design](../skills/patterns/protocol-design/SKILL.md) | Correct use of Python `typing.Protocol` for structural subtyping and interface design between modules. |
| [strategy-registry](../skills/patterns/strategy-registry/SKILL.md) | Strategy pattern with registry-based dispatch for extensible systems like plugin systems or file type handlers. |
| [error-handling](../skills/patterns/error-handling/SKILL.md) | Exception handling across application layers: mapping, retry, severity, and logging. |
| [resilience-patterns](../skills/patterns/resilience-patterns/SKILL.md) | Retry with backoff, circuit breaker, timeout, and graceful degradation for external dependencies. |
| [testing-patterns](../skills/patterns/testing-patterns/SKILL.md) | pytest patterns, fixtures, mocking, parametrize, and property-based testing for Python projects. |
| [api-design](../skills/patterns/api-design/SKILL.md) | REST API design with FastAPI: routing, response models, error handling, and dependencies. |
| [systematic-debugging](../skills/patterns/systematic-debugging/SKILL.md) | Structured 4-phase debugging methodology: reproduce → isolate → root-cause → fix and defend. |

---

## Agents (5)

*Isolated subprocesses — zero parent context in, result out.*

| Name | Category | Description |
|------|----------|------------|
| [reviewer](../agents/review/reviewer.md) | Review | Reviews Python code for security (OWASP), type safety, logging, privacy/offline compliance, and best practices. Consolidates python-reviewer, security-reviewer, logging-reviewer, and privacy-auditor. |
| [analyzer](../agents/analyze/analyzer.md) | Analyze | Analyzes codebases for architecture fit, performance, scalability, dead code, and dependency health. Consolidates architecture-analyzer, performance-analyzer, scalability-analyzer, dead-code-detector, and dependency-auditor. |
| [planner](../agents/plan/planner.md) | Plan | Validates implementation plans for completeness, requirements coverage, and risks. Consolidates plan-completeness, requirements-verifier, and risk-assessor. |
| [code-simplifier](../agents/build/code-simplifier.md) | Build | Simplifies and refines code for clarity, consistency, and maintainability while preserving full functionality. |
| [test-architect](../agents/build/test-architect.md) | Build | Creates pytest tests and reviews existing test suites for quality and coverage. |
