# Skill Library — Katalog

Alle verfügbaren Skills, Agents und Rules auf einen Blick.

---

## Schnellstart: Skill oder Agent installieren

Die Installation ist denkbar einfach — du musst nichts manuell konfigurieren. Sag Claude einfach, welchen Skill oder Agent du haben willst, und gib den Pfad zur Datei an.

### So geht's

1. Wähle einen Skill oder Agent aus dem Katalog unten
2. Kopiere den Dateipfad
3. Sag Claude:

```
Kopiere den Skill aus /pfad/zur/skill-library/skills/workflow/tdd/SKILL.md in mein Projekt
```

Claude liest die Datei, kopiert sie in dein Projekt (`.claude/skills/` für Skills, `.claude/agents/` für Agents) und registriert sie automatisch.

### Beispiele

**Skill installieren:**
```
Kopiere den Skill aus ~/Schreibtisch/skill-library/skills/patterns/testing-patterns/SKILL.md in mein Projekt
```
→ Claude kopiert die Datei nach `.claude/skills/testing-patterns/SKILL.md`

**Agent installieren:**
```
Kopiere den Agent aus ~/Schreibtisch/skill-library/agents/review/python-reviewer.md in mein Projekt
```
→ Claude kopiert die Datei nach `.claude/agents/python-reviewer.md`

**Mehrere auf einmal:**
```
Kopiere folgende Skills in mein Projekt:
- ~/Schreibtisch/skill-library/skills/workflow/tdd/SKILL.md
- ~/Schreibtisch/skill-library/skills/patterns/testing-patterns/SKILL.md
- ~/Schreibtisch/skill-library/agents/build/test-architect.md
```

### Anpassen nach der Installation

Nach dem Kopieren kannst du den Skill in `.claude/skills/` beliebig anpassen:

- **Trigger-Wörter ändern** — Wann soll Claude den Skill automatisch aktivieren?
- **Projektspezifische Regeln ergänzen** — Z.B. eigene Naming Conventions, bevorzugte Libraries
- **Sektionen entfernen** — Was du nicht brauchst, einfach löschen
- **Kombinieren** — Teile aus mehreren Skills in einen eigenen Skill zusammenführen

---

## Rules (4)

Immer geladene Verhaltensregeln, die Claudes Verhalten bei allen Aufgaben prägen. Kopiere nach `~/.claude/rules/` für globale Verfügbarkeit oder ins `.claude/rules/`-Verzeichnis deines Projekts.

| Name | Beschreibung | Pfad |
|------|-------------|------|
| coding-conventions | DRY-Prinzipien, Naming & Imports, Error Handling, Funktionsdesign, Type Hints und Testing-Konventionen. | [rules/coding-conventions.md](../rules/coding-conventions.md) |
| security | Input-Validierung, PII-Schutz in Logs, Secrets-Management und Dependency-Richtlinien. | [rules/security.md](../rules/security.md) |
| agent-behavior | Read-First-Workflow, Scope-Disziplin, minimale Änderungen, Subagent-Strategie und Bug-Fixing-Ansatz. | [rules/agent-behavior.md](../rules/agent-behavior.md) |
| self-improvement | Aus Korrekturen lernen, Muster in Memory erfassen, Lektionen iterieren. | [rules/self-improvement.md](../rules/self-improvement.md) |

---

## Skills (27)

### Meta (3)

| Name | Beschreibung | Pfad |
|------|-------------|------|
| skill-builder | Vermittelt Wissen zum Erstellen von Claude Code Skill-Dateien im SKILL.md-Format mit Best Practices. | [skills/meta/skill-builder/SKILL.md](../skills/meta/skill-builder/SKILL.md) |
| agent-builder | Vermittelt Wissen zum Erstellen von Claude Code Subagent-Konfigurationsdateien mit YAML-Frontmatter und Prompts. | [skills/meta/agent-builder/SKILL.md](../skills/meta/agent-builder/SKILL.md) |
| team-builder | Orchestrierung von Claude Code Agent-Teams — mehrere unabhängige Sessions, koordiniert durch einen Team Lead mit geteilter Task-Liste und Inter-Agent-Messaging. | [skills/meta/team-builder/SKILL.md](../skills/meta/team-builder/SKILL.md) |

### Build — Backend (7)

| Name | Beschreibung | Pfad |
|------|-------------|------|
| prompt-builder | Transformiert unstrukturierte Benutzeranfragen in optimierte, strukturierte Prompts durch systematische Klärungsfragen. | [skills/build/backend/prompt-builder/SKILL.md](../skills/build/backend/prompt-builder/SKILL.md) |
| logging-builder | Implementiert Python-Logging-Infrastruktur mit Logger-Konfiguration, Datei-Rotation und strukturiertem Logging. | [skills/build/backend/logging-builder/SKILL.md](../skills/build/backend/logging-builder/SKILL.md) |
| config-builder | Erstellt Python-Konfigurationsinfrastruktur mit Pydantic-Modellen, YAML-Loading und Environment-Variable-Overrides. | [skills/build/backend/config-builder/SKILL.md](../skills/build/backend/config-builder/SKILL.md) |
| exception-builder | Entwirft Python-Exception-Hierarchien für geschichtete Anwendungen mit Base Exceptions, Layer Mapping und Chaining. | [skills/build/backend/exception-builder/SKILL.md](../skills/build/backend/exception-builder/SKILL.md) |
| docker-builder | Erstellt Dockerfile und docker-compose.yml mit Multi-Stage Builds, Health Checks, Netzwerkisolation und GPU-Setup. | [skills/build/backend/docker-builder/SKILL.md](../skills/build/backend/docker-builder/SKILL.md) |
| ci-cd-builder | Erstellt GitHub Actions CI/CD-Pipelines mit pytest, Linting, Docker Build und Release-Workflows. | [skills/build/backend/ci-cd-builder/SKILL.md](../skills/build/backend/ci-cd-builder/SKILL.md) |
| project-scaffold | Erstellt produktionsreife Python-Projektstrukturen mit Verzeichnislayout, pyproject.toml, Config, Logging und CI/CD. | [skills/build/backend/project-scaffold/SKILL.md](../skills/build/backend/project-scaffold/SKILL.md) |

### Build — Frontend (2)

| Name | Beschreibung | Pfad |
|------|-------------|------|
| frontend-design | Erstellt markante, produktionsreife Frontend-Interfaces mit hoher Designqualität, die generische KI-Ästhetik vermeiden. | [skills/build/frontend/frontend-design/SKILL.md](../skills/build/frontend/frontend-design/SKILL.md) |
| warmgold-frontend | Warmes, iOS-inspiriertes Design-System mit Component-Patterns für Vanilla-HTML/CSS/JS-Frontends. | [skills/build/frontend/warmgold-frontend/SKILL.md](../skills/build/frontend/warmgold-frontend/SKILL.md) |

### Workflow (7)

| Name | Beschreibung | Pfad |
|------|-------------|------|
| plan-review | Prüft Implementierungspläne auf Vollständigkeit, Architektur-Passung, Risiken und Anforderungsabdeckung mittels paralleler Spezial-Agenten. | [skills/workflow/plan-review/SKILL.md](../skills/workflow/plan-review/SKILL.md) |
| session-verify | Validiert am Session-Ende alle Änderungen auf Bugs, Sicherheitslücken, toten Code und Dokumentationslücken. | [skills/workflow/session-verify/SKILL.md](../skills/workflow/session-verify/SKILL.md) |
| pr-review | Orchestriert Pull-Request-Reviews durch parallele spezialisierte Agenten, die den Diff analysieren und Ergebnisse aggregieren. | [skills/workflow/pr-review/SKILL.md](../skills/workflow/pr-review/SKILL.md) |
| tdd | Test-Driven-Development-Workflow im RED-GREEN-REFACTOR-Zyklus: test-architect → Implementierung → code-simplifier. | [skills/workflow/tdd/SKILL.md](../skills/workflow/tdd/SKILL.md) |
| deep-research | Strukturierter Research-Workflow (Frage → Quellen → Analyse → Synthese → Dokumentation) für technische Entscheidungen. | [skills/workflow/deep-research/SKILL.md](../skills/workflow/deep-research/SKILL.md) |
| ralph-loop | Autonomer Arbeitsmodus — Claude arbeitet selbstständig an einer Aufgabe weiter, bis sie abgeschlossen oder das Iterationslimit erreicht ist. | [skills/workflow/ralph-loop/SKILL.md](../skills/workflow/ralph-loop/SKILL.md) |
| ralph-loop-prompt-builder | Hilft beim Erstellen effektiver Prompts für das Ralph-Loop-System durch Klärungsfragen und strukturierte Ausgabe. | [skills/workflow/ralph-loop-prompt-builder/SKILL.md](../skills/workflow/ralph-loop-prompt-builder/SKILL.md) |

### Patterns (8)

| Name | Beschreibung | Pfad |
|------|-------------|------|
| di-container | Implementierung von Dependency-Injection-Containern mit Python Protocols für entkoppelte, testbare Anwendungen. | [skills/patterns/di-container/SKILL.md](../skills/patterns/di-container/SKILL.md) |
| protocol-design | Korrekter Einsatz von Python `typing.Protocol` für strukturelles Subtyping und Interface-Design zwischen Modulen. | [skills/patterns/protocol-design/SKILL.md](../skills/patterns/protocol-design/SKILL.md) |
| strategy-registry | Strategy-Pattern mit Registry-basiertem Dispatch für erweiterbare Systeme wie Plugin-Systeme oder Dateityp-Handler. | [skills/patterns/strategy-registry/SKILL.md](../skills/patterns/strategy-registry/SKILL.md) |
| error-handling | Exception-Handling über Anwendungsschichten hinweg: Mapping, Retry, Severity und Logging. | [skills/patterns/error-handling/SKILL.md](../skills/patterns/error-handling/SKILL.md) |
| resilience-patterns | Retry mit Backoff, Circuit Breaker, Timeout und Graceful Degradation für externe Abhängigkeiten. | [skills/patterns/resilience-patterns/SKILL.md](../skills/patterns/resilience-patterns/SKILL.md) |
| testing-patterns | pytest-Patterns, Fixtures, Mocking, Parametrize und Property-Based Testing für Python-Projekte. | [skills/patterns/testing-patterns/SKILL.md](../skills/patterns/testing-patterns/SKILL.md) |
| api-design | REST-API-Design mit FastAPI: Routing, Response-Modelle, Error Handling und Dependencies. | [skills/patterns/api-design/SKILL.md](../skills/patterns/api-design/SKILL.md) |
| systematic-debugging | Strukturierte 4-Phasen-Debugging-Methodik: Reproduzieren → Isolieren → Root-Cause → Fixen und Absichern. | [skills/patterns/systematic-debugging/SKILL.md](../skills/patterns/systematic-debugging/SKILL.md) |

---

## Agents (16)

### Review (4)

| Name | Beschreibung | Pfad |
|------|-------------|------|
| python-reviewer | Prüft Python-Code auf Sicherheitslücken, Typsicherheit und Best Practices. | [agents/review/python-reviewer.md](../agents/review/python-reviewer.md) |
| logging-reviewer | Prüft Python-Code auf Logging-Best-Practices, fehlende Logs, falsche Log-Levels und Offenlegung sensibler Daten. | [agents/review/logging-reviewer.md](../agents/review/logging-reviewer.md) |
| security-reviewer | Prüft Python-Code auf Sicherheitslücken nach OWASP-Top-10 — Input-Validierung, Injection, Path Traversal, Secrets und Auth. | [agents/review/security-reviewer.md](../agents/review/security-reviewer.md) |
| privacy-auditor | Auditiert Code auf Offline-Konformität und Datenschutz — findet externe API-Aufrufe, Telemetrie und Cloud-Zugriffe. | [agents/review/privacy-auditor.md](../agents/review/privacy-auditor.md) |

### Analyze (5)

| Name | Beschreibung | Pfad |
|------|-------------|------|
| performance-analyzer | Analysiert Python-Code auf Performance-Probleme: N+1-Queries, Memory-Leaks, blockierendes I/O, O(n²)-Komplexität. | [agents/analyze/performance-analyzer.md](../agents/analyze/performance-analyzer.md) |
| scalability-analyzer | Analysiert Code auf Skalierungsprobleme: fehlendes Caching, Connection-Pooling, zustandsbehaftetes Design, horizontale Skalierung. | [agents/analyze/scalability-analyzer.md](../agents/analyze/scalability-analyzer.md) |
| dead-code-detector | Erkennt toten, unerreichbaren und verwaisten Code — ungenutzte Funktionen, Klassen, Imports und Variablen. | [agents/analyze/dead-code-detector.md](../agents/analyze/dead-code-detector.md) |
| dependency-auditor | Auditiert Python-Abhängigkeiten auf CVEs, veraltete Versionen und Lizenzprobleme. | [agents/analyze/dependency-auditor.md](../agents/analyze/dependency-auditor.md) |
| architecture-analyzer | Analysiert, ob Implementierungspläne zur bestehenden Codebase-Architektur passen — Modulstruktur, Import-Konventionen, Integrationspunkte. | [agents/analyze/architecture-analyzer.md](../agents/analyze/architecture-analyzer.md) |

### Plan (3)

| Name | Beschreibung | Pfad |
|------|-------------|------|
| plan-completeness | Prüft Implementierungspläne auf Vollständigkeit: alle Schritte definiert, Abhängigkeiten klar, Randfälle abgedeckt. | [agents/plan/plan-completeness.md](../agents/plan/plan-completeness.md) |
| risk-assessor | Bewertet Implementierungsrisiken: Breaking Changes, Sicherheitsbedenken, Komplexität und Machbarkeit. | [agents/plan/risk-assessor.md](../agents/plan/risk-assessor.md) |
| requirements-verifier | Verifiziert, dass die Implementierung mit Benutzeranforderungen übereinstimmt — identifiziert Lücken und Randfälle. | [agents/plan/requirements-verifier.md](../agents/plan/requirements-verifier.md) |

### Build (4)

| Name | Beschreibung | Pfad |
|------|-------------|------|
| code-simplifier | Vereinfacht und verfeinert Code hinsichtlich Klarheit, Konsistenz und Wartbarkeit bei voller Funktionserhaltung. | [agents/build/code-simplifier.md](../agents/build/code-simplifier.md) |
| test-architect | Erstellt pytest-Tests und prüft bestehende Testsuiten auf Qualität und Abdeckung. | [agents/build/test-architect.md](../agents/build/test-architect.md) |
| warmgold-frontend-builder | Baut UI-Komponenten mit dem warmgold-Designsystem: warme Goldakzente, warme Grautöne, iOS-inspiriert. | [agents/build/warmgold-frontend-builder.md](../agents/build/warmgold-frontend-builder.md) |
| migration-writer | Generiert Datenbank- und Schema-Migrationsskripte nach Alembic-Patterns mit Sicherheitsprüfungen gegen Datenverlust. | [agents/build/migration-writer.md](../agents/build/migration-writer.md) |
