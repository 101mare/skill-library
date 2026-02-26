# Skill Library — Katalog

> [README](../README_de.md) | **KATALOG** | [ARTICLE](ARTICLE_de.md)

> [!TIP]
> Um einen Skill oder Agent zu installieren, siehe [Schnellstart](../README_de.md#schnellstart) in der README.

## Empfohlen: Die fünf Kern-Skills

Wenn du nur fünf Skills installierst, decken diese den gesamten Entwicklungszyklus ab:

| Skill | Was er tut | Phase |
|-------|-----------|-------|
| [prompt-builder](../skills/build/backend/prompt-builder/SKILL.md) | Formt vage Anfragen in strukturierte Prompts | Prompt |
| [plan-review](../skills/workflow/plan-review/SKILL.md) | 4 parallele Agents prüfen Arch, Conventions, Risiken, Reqs | Plan |
| [tdd](../skills/workflow/tdd/SKILL.md) | RED-GREEN-REFACTOR mit Agent-Orchestrierung | Bauen + Testen |
| [systematic-debugging](../skills/patterns/systematic-debugging/SKILL.md) | Reproduzieren → Isolieren → Root-Cause → Fix | Debug |
| [session-verify](../skills/workflow/session-verify/SKILL.md) | End-of-Session Security- + Qualitäts-Review | Verify |

---

## Rules (4)

*Immer geladen — prägen jede Interaktion.*

| Name | Beschreibung |
|------|-------------|
| [coding-conventions](../rules/coding-conventions.md) | DRY-Prinzipien, Naming & Imports, Error Handling, Funktionsdesign, Type Hints und Testing-Konventionen. |
| [security](../rules/security.md) | Input-Validierung, PII-Schutz in Logs, Secrets-Management und Dependency-Richtlinien. |
| [agent-behavior](../rules/agent-behavior.md) | Read-First-Workflow, Scope-Disziplin, minimale Änderungen, Subagent-Strategie und Bug-Fixing-Ansatz. |
| [self-improvement](../rules/self-improvement.md) | Aus Korrekturen lernen, Muster in Memory erfassen, Lektionen iterieren. |

---

## Skills (27)

*Laden on demand — vermitteln Claude spezialisierte Workflows.*

### Meta (3)

| Name | Beschreibung |
|------|-------------|
| [skill-builder](../skills/meta/skill-builder/SKILL.md) | Vermittelt Wissen zum Erstellen von Claude Code Skill-Dateien im SKILL.md-Format mit Best Practices. |
| [agent-builder](../skills/meta/agent-builder/SKILL.md) | Vermittelt Wissen zum Erstellen von Claude Code Subagent-Konfigurationsdateien mit YAML-Frontmatter und Prompts. |
| [team-builder](../skills/meta/team-builder/SKILL.md) | Orchestrierung von Claude Code Agent-Teams — mehrere unabhängige Sessions, koordiniert durch einen Team Lead mit geteilter Task-Liste und Inter-Agent-Messaging. |

### Build — Backend (7)

| Name | Beschreibung |
|------|-------------|
| [prompt-builder](../skills/build/backend/prompt-builder/SKILL.md) | Transformiert unstrukturierte Benutzeranfragen in optimierte, strukturierte Prompts durch systematische Klärungsfragen. |
| [logging-builder](../skills/build/backend/logging-builder/SKILL.md) | Implementiert Python-Logging-Infrastruktur mit Logger-Konfiguration, Datei-Rotation und strukturiertem Logging. |
| [config-builder](../skills/build/backend/config-builder/SKILL.md) | Erstellt Python-Konfigurationsinfrastruktur mit Pydantic-Modellen, YAML-Loading und Environment-Variable-Overrides. |
| [exception-builder](../skills/build/backend/exception-builder/SKILL.md) | Entwirft Python-Exception-Hierarchien für geschichtete Anwendungen mit Base Exceptions, Layer Mapping und Chaining. |
| [docker-builder](../skills/build/backend/docker-builder/SKILL.md) | Erstellt Dockerfile und docker-compose.yml mit Multi-Stage Builds, Health Checks, Netzwerkisolation und GPU-Setup. |
| [ci-cd-builder](../skills/build/backend/ci-cd-builder/SKILL.md) | Erstellt GitHub Actions CI/CD-Pipelines mit pytest, Linting, Docker Build und Release-Workflows. |
| [project-scaffold](../skills/build/backend/project-scaffold/SKILL.md) | Erstellt produktionsreife Python-Projektstrukturen mit Verzeichnislayout, pyproject.toml, Config, Logging und CI/CD. |

### Build — Frontend (2)

| Name | Beschreibung |
|------|-------------|
| [frontend-design](../skills/build/frontend/frontend-design/SKILL.md) | Erstellt markante, produktionsreife Frontend-Interfaces mit hoher Designqualität, die generische KI-Ästhetik vermeiden. |
| [warmgold-frontend](../skills/build/frontend/warmgold-frontend/SKILL.md) | Warmes, iOS-inspiriertes Design-System mit Component-Patterns für Vanilla-HTML/CSS/JS-Frontends. |

### Workflow (7)

| Name | Beschreibung |
|------|-------------|
| [plan-review](../skills/workflow/plan-review/SKILL.md) | Prüft Implementierungspläne auf Vollständigkeit, Architektur-Passung, Risiken und Anforderungsabdeckung mittels paralleler Spezial-Agenten. |
| [session-verify](../skills/workflow/session-verify/SKILL.md) | Validiert am Session-Ende alle Änderungen auf Bugs, Sicherheitslücken, toten Code und Dokumentationslücken. |
| [pr-review](../skills/workflow/pr-review/SKILL.md) | Orchestriert Pull-Request-Reviews durch parallele spezialisierte Agenten, die den Diff analysieren und Ergebnisse aggregieren. |
| [tdd](../skills/workflow/tdd/SKILL.md) | Test-Driven-Development-Workflow im RED-GREEN-REFACTOR-Zyklus: test-architect → Implementierung → code-simplifier. |
| [deep-research](../skills/workflow/deep-research/SKILL.md) | Strukturierter Research-Workflow (Frage → Quellen → Analyse → Synthese → Dokumentation) für technische Entscheidungen. |
| [ralph-loop](../skills/workflow/ralph-loop/SKILL.md) | Autonomer Arbeitsmodus — Claude arbeitet selbstständig an einer Aufgabe weiter, bis sie abgeschlossen oder das Iterationslimit erreicht ist. |
| [ralph-loop-prompt-builder](../skills/workflow/ralph-loop-prompt-builder/SKILL.md) | Hilft beim Erstellen effektiver Prompts für das Ralph-Loop-System durch Klärungsfragen und strukturierte Ausgabe. |

### Patterns (8)

| Name | Beschreibung |
|------|-------------|
| [di-container](../skills/patterns/di-container/SKILL.md) | Implementierung von Dependency-Injection-Containern mit Python Protocols für entkoppelte, testbare Anwendungen. |
| [protocol-design](../skills/patterns/protocol-design/SKILL.md) | Korrekter Einsatz von Python `typing.Protocol` für strukturelles Subtyping und Interface-Design zwischen Modulen. |
| [strategy-registry](../skills/patterns/strategy-registry/SKILL.md) | Strategy-Pattern mit Registry-basiertem Dispatch für erweiterbare Systeme wie Plugin-Systeme oder Dateityp-Handler. |
| [error-handling](../skills/patterns/error-handling/SKILL.md) | Exception-Handling über Anwendungsschichten hinweg: Mapping, Retry, Severity und Logging. |
| [resilience-patterns](../skills/patterns/resilience-patterns/SKILL.md) | Retry mit Backoff, Circuit Breaker, Timeout und Graceful Degradation für externe Abhängigkeiten. |
| [testing-patterns](../skills/patterns/testing-patterns/SKILL.md) | pytest-Patterns, Fixtures, Mocking, Parametrize und Property-Based Testing für Python-Projekte. |
| [api-design](../skills/patterns/api-design/SKILL.md) | REST-API-Design mit FastAPI: Routing, Response-Modelle, Error Handling und Dependencies. |
| [systematic-debugging](../skills/patterns/systematic-debugging/SKILL.md) | Strukturierte 4-Phasen-Debugging-Methodik: Reproduzieren → Isolieren → Root-Cause → Fixen und Absichern. |

---

## Agents (5)

*Isolierte Subprozesse — kein Parent-Kontext rein, Ergebnis raus.*

| Name | Kategorie | Beschreibung |
|------|-----------|-------------|
| [reviewer](../agents/review/reviewer.md) | Review | Prüft Python-Code auf Sicherheit (OWASP), Typsicherheit, Logging, Datenschutz/Offline-Konformität und Best Practices. Konsolidiert python-reviewer, security-reviewer, logging-reviewer und privacy-auditor. |
| [analyzer](../agents/analyze/analyzer.md) | Analyze | Analysiert Codebasen auf Architektur-Passung, Performance, Skalierbarkeit, toten Code und Abhängigkeits-Gesundheit. Konsolidiert architecture-analyzer, performance-analyzer, scalability-analyzer, dead-code-detector und dependency-auditor. |
| [planner](../agents/plan/planner.md) | Plan | Validiert Implementierungspläne auf Vollständigkeit, Anforderungsabdeckung und Risiken. Konsolidiert plan-completeness, requirements-verifier und risk-assessor. |
| [code-simplifier](../agents/build/code-simplifier.md) | Build | Vereinfacht und verfeinert Code hinsichtlich Klarheit, Konsistenz und Wartbarkeit bei voller Funktionserhaltung. |
| [test-architect](../agents/build/test-architect.md) | Build | Erstellt pytest-Tests und prüft bestehende Testsuiten auf Qualität und Abdeckung. |
