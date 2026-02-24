---
name: plan-review
description: |
  Reviews implementation plans before coding begins. Checks completeness, architecture fit,
  risks, and requirement alignment. Uses specialized agents in parallel for thorough analysis.
  Proactively asks clarifying questions when uncertainties are found.
  Use when: reviewing plans, before implementation, user asks "ist der Plan gut?",
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
| `.claude/agents/python-reviewer.md` | Security, types, architecture fit |
| `.claude/agents/performance-analyzer.md` | Performance risks, bottlenecks |
| `.claude/agents/test-architect.md` | Test strategy completeness |
| `.claude/agents/privacy-auditor.md` | Offline compliance risks |
| `.claude/agents/dependency-auditor.md` | New dependency risks |
| `.claude/agents/warmgold-frontend-builder.md` | Frontend architecture fit |

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
Question: "Welchen Plan soll ich reviewen?"
Options:
  - "Den zuletzt erstellten Plan"
  - "Plan aus .claude/plans/"
  - "Ich beschreibe den Plan kurz"
  - "Abbrechen"
```

## Step 2: Clarify Context and Requirements

**WICHTIG**: Proaktiv nachfragen um den Kontext zu verstehen.

### Pflicht-Fragen

```
Use AskUserQuestion:
Question: "Was ist das Ziel dieses Plans? Was soll erreicht werden?"
Options:
  - "Neues Feature implementieren"
  - "Bug fixen"
  - "Refactoring"
  - "Performance verbessern"
```

### Kontext-Fragen (bei Bedarf)

Stelle weitere Fragen wenn:
- Das Ziel unklar ist
- Anforderungen implizit sind
- Constraints nicht genannt wurden
- Edge Cases nicht erwaehnt wurden

```
Use AskUserQuestion:
Question: "Gibt es spezielle Anforderungen oder Constraints?"
Options:
  - "Muss abwaertskompatibel sein"
  - "Performance-kritisch"
  - "Sicherheitsrelevant"
  - "Keine besonderen Constraints"
```

## Step 3: Run Parallel Reviews

First **read the relevant agent .md files**, then spawn `explore` agents **in parallel** (single message, multiple Task calls), injecting each agent's system prompt + a plan-review-specific role into the Task prompt.

### Agent Assignments

| Review Role | Agent File to Load | Focus | Key Questions |
|-------------|-------------------|-------|---------------|
| Completeness Checker | `python-reviewer.md` | Vollstaendigkeit + Code Quality | Alle Schritte? Abhaengigkeiten? Tests? Types? |
| Architecture Analyzer | `python-reviewer.md` | Architektur-Fit | Passt zu Patterns? Module richtig? DI? |
| Risk Assessor | `performance-analyzer.md` | Risiken + Performance | Breaking Changes? Security? Komplexitaet? N+1? |
| Requirements Verifier | (no agent file needed) | Anforderungen | Erfuellt Plan die Ziele? |

### Execution Steps

1. **Read agent files** (parallel Read calls):
   ```
   Read(".claude/agents/python-reviewer.md")
   Read(".claude/agents/performance-analyzer.md")
   # + any additional agents based on plan content (e.g., frontend changes -> warmgold-frontend-builder.md)
   ```

2. **Spawn 4 Task agents in parallel** (single message, multiple Task calls):

   ```
   # Agent 1: Completeness Checker
   Task(
     subagent_type="explore",
     prompt="""You are a Plan Completeness Checker with Python backend expertise.

     <agent-expertise>
     [content from python-reviewer.md after frontmatter]
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
     prompt="""You are an Architecture Fit Analyzer with Python backend expertise.

     <agent-expertise>
     [content from python-reviewer.md after frontmatter]
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
     prompt="""You are an Implementation Risk Assessor with performance analysis expertise.

     <agent-expertise>
     [content from performance-analyzer.md after frontmatter]
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

   # Agent 4: Requirements Verifier (no agent file needed - uses general knowledge)
   Task(
     subagent_type="explore",
     prompt="""You are a Requirements Verifier for an implementation plan.

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

### Sammle Ergebnisse

Nach Abschluss aller Reviews, erstelle Uebersicht:

```markdown
## Plan Review Ergebnisse

### Uebersicht

| Agent | Status | Findings |
|-------|--------|----------|
| Completeness | pass/warn/fail | X issues |
| Architecture | pass/warn/fail | X issues |
| Risks | pass/warn/fail | X issues |
| Requirements | pass/warn/fail | X issues |
```

### Kategorisiere Findings

```markdown
### BLOCKER (Muss vor Implementierung geloest werden)
1. [Finding + Quelle]
2. [Finding + Quelle]

### GAPS (Luecken im Plan)
1. [Missing element]
2. [Incomplete step]

### DEVIATIONS (Abweichungen von Standards)
1. [Pattern nicht eingehalten]
2. [Convention nicht befolgt]

### RISKS (Identifizierte Risiken)
1. [Risk + Severity]
2. [Risk + Severity]

### POSITIV
1. [Was gut ist am Plan]
```

### Proaktive Klaerung bei Unsicherheiten

**WICHTIG**: Bei gefundenen Unsicherheiten AKTIV nachfragen:

```
Use AskUserQuestion:
Question: "Der Plan erwaehnt 'verbesserte Fehlerbehandlung' - was genau ist gemeint?"
Options:
  - "Retry-Logik hinzufuegen"
  - "Bessere Fehlermeldungen"
  - "Logging erweitern"
  - "Alles davon"
```

```
Use AskUserQuestion:
Question: "Step 3 hat keine Test-Strategie - sollen Tests hinzugefuegt werden?"
Options:
  - "Ja, Unit Tests"
  - "Ja, Unit + Integration Tests"
  - "Nein, spaeter"
  - "Teste ich manuell"
```

### Verifizierungs-Fragen

Bei kritischen Punkten den User einbeziehen:

```
Use AskUserQuestion:
Question: "Das Risk Assessment zeigt potentielle Breaking Changes. Ist Abwaertskompatibilitaet wichtig?"
Options:
  - "Ja, kritisch"
  - "Waere gut, aber nicht kritisch"
  - "Nein, kann brechen"
```

## Step 5: Present Verdict

### Verdict Matrix

```markdown
## Plan Review Verdict

### Ampel-Status

| Kategorie | Status | Grund |
|-----------|--------|-------|
| Vollstaendigkeit | GREEN/YELLOW/RED | [Kurze Begruendung] |
| Architektur-Fit | GREEN/YELLOW/RED | [Kurze Begruendung] |
| Risiko-Level | GREEN/YELLOW/RED | [Kurze Begruendung] |
| Requirements | GREEN/YELLOW/RED | [Kurze Begruendung] |

### Gesamt-Bewertung

GREEN **PLAN APPROVED** - Kann implementiert werden
YELLOW **PLAN NEEDS WORK** - Punkte klaeren vor Implementierung
RED **PLAN BLOCKED** - Kritische Issues muessen geloest werden
```

### Empfehlungen

```markdown
### Empfohlene Aenderungen am Plan

1. **[Prioritaet 1]**: [Konkrete Aenderung]
2. **[Prioritaet 2]**: [Konkrete Aenderung]
3. **[Prioritaet 3]**: [Konkrete Aenderung]

### Fragen zum Klaeren

1. [Offene Frage 1]
2. [Offene Frage 2]
```

### User-Entscheidung

```
Use AskUserQuestion:
Question: "Wie moechtest du fortfahren?"
Options:
  - "Plan anpassen und nochmal reviewen"
  - "Trotzdem implementieren (Risiken akzeptiert)"
  - "Mehr Details zu einem Finding"
  - "Review abbrechen"
```

## Proaktive Fragen - Checkliste

Der Skill soll **proaktiv** AskUserQuestion nutzen fuer:

### Bei Unklarheiten im Plan
- [ ] Ambige Formulierungen ("verbessern", "optimieren", "aufraeumen")
- [ ] Fehlende Details (welche Datei? welche Methode?)
- [ ] Unklare Reihenfolge der Schritte

### Bei Risiko-Findings
- [ ] Breaking Changes - Ist das akzeptabel?
- [ ] Security-Bedenken - Wie wichtig ist das?
- [ ] Performance-Impact - Akzeptable Latenz?

### Bei Architektur-Abweichungen
- [ ] Absichtliche Abweichung oder Versehen?
- [ ] Soll das ein neues Pattern werden?

### Zur Verifizierung
- [ ] Stimmen die extrahierten Requirements?
- [ ] Wurden alle Anforderungen erfasst?
- [ ] Gibt es implizite Anforderungen?

## Triggers

Aktiviert bei:
- `/plan-review`
- "review plan", "check plan", "validate plan"
- "plan pruefen", "ist der Plan gut?", "Plan ueberpruefen"
- "review implementation plan", "check my approach"
- "before I start coding", "bevor ich anfange"
- "ist das ein guter Ansatz?", "macht das Sinn?"

## Wichtige Hinweise

- **Agent loading**: ALWAYS read `.claude/agents/*.md` files and inject their prompts into `explore` Task agents
- **Parallelisierung**: Alle 4 Agents gleichzeitig starten (ein Message, mehrere Task-Calls)
- **Sprache matchen**: Deutsch wenn User Deutsch spricht
- **Proaktiv fragen**: Bei JEDER Unsicherheit AskUserQuestion nutzen
- **Konkret sein**: Findings mit File:Line wo moeglich
- **Prioritaeten**: Blocker > Gaps > Deviations > Risks > Positives
- **Konstruktiv**: Nicht nur Probleme nennen, auch Loesungen vorschlagen
- **Additional agents**: If the plan involves frontend changes, also read `warmgold-frontend-builder.md`. If it involves new dependencies, also read `dependency-auditor.md`. Spawn additional Task agents as needed.
- **Project-agnostic**: This skill works for any project. Read the project's CLAUDE.md to understand its specific architecture, patterns, and constraints before running reviews.
- **Research first**: If the plan involves unfamiliar technology or open technical decisions, use the `deep-research` skill first to gather evidence before reviewing.
