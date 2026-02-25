<p align="center"><img src="docs/images/skill-library.png" width="80%" alt="Skill Library"></p>

# Skill Library

27 Skills, 5 Agents, 4 Rules — kopiere was du brauchst, lass den Rest.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Skills: 27](https://img.shields.io/badge/Skills-27-blue.svg)](docs/CATALOG_de.md)
[![Agents: 5](https://img.shields.io/badge/Agents-5-green.svg)](docs/CATALOG_de.md)
[![Maintained: yes](https://img.shields.io/badge/Maintained-yes-brightgreen.svg)](https://github.com/101mare/skill-library)

> English version: [README.md](README.md) | [CATALOG.md](docs/CATALOG.md) | [ARTICLE.md](docs/ARTICLE.md)

## Schnellstart

Sag Claude, welchen Skill, Agent oder Rule du willst. Drei Wege zur Installation:

**Von GitHub** (kein Clone nötig):
```
Kopiere den Skill aus https://github.com/101mare/skill-library/tree/main/skills/workflow/tdd in mein Projekt
```

**Aus einem lokalen Clone:**
```
Kopiere den Skill aus ~/skill-library/skills/workflow/tdd/SKILL.md in mein Projekt
```

**Global** (Symlink nach `~/.claude/` — in allen Projekten verfügbar, Updates via `git pull` gelten überall):
```bash
ln -s ~/skill-library/skills/workflow/tdd ~/.claude/skills/tdd
```

Claude liest die Datei, kopiert sie in dein Projekt unter `.claude/skills/` (oder `.claude/agents/`) und aktiviert sie automatisch. Die vollständige Liste findest du in **[CATALOG_de.md](docs/CATALOG_de.md)**.

## Warum es das gibt

CLAUDE.md-Dateien wachsen zu 500-Zeilen-Monstern. Dieselben Regeln werden in jedes Projekt kopiert. Agents mit generischen Labels wie "You are an expert" zeigen [keine messbare Verbesserung](https://arxiv.org/abs/2308.07702) gegenüber gar keinem Label.

Diese Library löst das mit **drei Schichten**: Rules (immer geladen, prägen Verhalten) → Skills (on demand geladen, vermitteln Workflows) → Agents (isolierte Subprozesse, erledigen delegierte Arbeit). Jede Schicht hat eine klare Aufgabe, und nichts vermischt sich. Die vollständige Herleitung — inklusive der Forschung hinter dem Agent-Design — steht in **[ARTICLE_de.md](docs/ARTICLE_de.md)**.

## Hier starten — Die fünf Kern-Skills

Wenn du nur fünf Skills installierst, decken diese den gesamten Entwicklungszyklus ab:

1. **prompt-builder** — Stellt klärende Fragen zu deinem Ziel und formt daraus einen strukturierten Prompt — ob für einen Plan, die direkte Umsetzung oder jede andere Aufgabe.
2. **plan-review** — Vier parallele Review-Agents prüfen Architektur-Fit, Conventions, Risiken und Requirements. Ampel-Verdict *vor* dem Code.
3. **tdd** — Echtes RED-GREEN-REFACTOR mit Agent-Orchestrierung. Tests definieren Verhalten, nicht bestätigen Code.
4. **systematic-debugging** — 4-Phasen-Methodik: Reproduzieren → Isolieren → Root-Cause → Fix+Absichern.
5. **session-verify** — End-of-Session Review: Security, Code-Qualität, Architektur, saubere Imports, keine liegengebliebenen TODOs. Nichts geht ungeprüft raus.

Die Logik: **Prompt** → **Plan** → **Bauen + Testen** → **Debuggen** → **Verifizieren**. Der gesamte Zyklus, fünf Skills.

> **Hinweis:** Das ist ein defensiver, tokenintensiver Ansatz — plan-review und session-verify spawnen jeweils mehrere Agents. Wer schnell und günstig arbeiten will: tdd + systematic-debugging allein decken die Kernarbeit ab.

## Was drin steckt

```
skill-library/
├── docs/                       # CATALOG + ARTICLE (EN + DE)
├── templates/
│   └── CLAUDE.md.template      # Generische CLAUDE.md für neue Projekte
├── rules/                      # Immer geladene Verhaltensregeln
├── skills/
│   ├── meta/                   # Skills, Agents und Teams bauen
│   ├── build/
│   │   ├── frontend/           # Design & Komponenten
│   │   └── backend/            # Scaffolding & Infrastruktur
│   ├── workflow/               # Multi-Agent Workflows
│   └── patterns/               # Wiederverwendbare Architektur-Patterns
└── agents/
    ├── review/                 # Code Review & Audit
    ├── analyze/                # Analyse & Erkennung
    ├── plan/                   # Planung & Bewertung
    └── build/                  # Code-Generierung & Modifikation
```

**Skills** vermitteln Claude spezialisiertes Wissen — TDD-Zyklen, Debugging-Methodik, API-Design, DI-Container. Sie aktivieren sich automatisch, wenn Claude den richtigen Kontext erkennt.

**Agents** sind isolierte Subprozesse, die Claude für bestimmte Aufgaben startet — Code Review, Dead-Code-Erkennung, Tests schreiben. Sie erhalten keinen Parent-Kontext und liefern ein Ergebnis.

**Rules** setzen globales Verhalten: Coding Conventions, Scope-Disziplin, Security-Defaults, Selbstverbesserung durch Korrekturen.

Wichtiger Unterschied: Skills instruieren, Agents arbeiten. Ein Workflow-Skill wie `plan-review` startet 4 Agents parallel und aggregiert deren Ergebnisse zu einem einzigen Verdict.

## Kernkonzepte

**Drei Schichten** — Rules (immer geladen) → Skills (on demand) → Agents (delegiert). Rules prägen jede Interaktion. Skills aktivieren sich bei Bedarf. Agents laufen als isolierte Subprozesse mit eigenen Tools und eigenem Kontext.

**Agent Soul** — Generische Labels ("You are an expert") haben keinen statistisch signifikanten Effekt ([NAACL 2024](https://arxiv.org/abs/2308.07702)). Was funktioniert: spezifische Identität, Anti-Patterns zum Vermeiden, produktive Schwächen. Jede Agent-Datei in dieser Library baut auf dieser Forschung auf.

**Progressive Disclosure** — Skill-Header (Name + Beschreibung) sind immer geladen, damit Claude weiß, was verfügbar ist. Die vollständige `SKILL.md` lädt on demand. Detaillierte `reference.md`-Dateien laden nur bei Bedarf. Das hält das Context-Budget knapp.

## Context-Kosten

Jeder installierte Skill kostet Token durch seine Header-Beschreibung — bei jedem API-Call. 27 Skills mit je 3-4 Zeilen sind ~100 Zeilen permanenter System-Prompt. Installiere selektiv: Die fünf Kern-Skills oben decken die meisten Bedürfnisse ab. Füge Spezialisten hinzu, wenn dein Projekt sie braucht.

## CLAUDE.md Template

Ein produktionsreifes CLAUDE.md-Template findest du unter `templates/CLAUDE.md.template`.

Deckt Architektur, Commands, Import-Konventionen, Key Patterns und Konfiguration ab. Generische Regeln (DRY, Agent-Verhalten, Security) leben in `rules/` und müssen hier nicht wiederholt werden.

## Weiterführend

- **[CATALOG_de.md](docs/CATALOG_de.md)** — Vollständiger Katalog aller Skills und Agents
- **[ARTICLE_de.md](docs/ARTICLE_de.md)** — Der vollständige Deep Dive: Warum drei Schichten statt einer großen CLAUDE.md, wie man Agents eine "Seele" gibt (gestützt auf NAACL 2024 Forschung), Context-Budget-Management und die Lessons Learned beim Bau von 27 Skills. Wenn du das *Denken* hinter dieser Library verstehen willst, fang hier an.

---

**English version:** [README.md](README.md) | [CATALOG.md](docs/CATALOG.md) | [ARTICLE.md](docs/ARTICLE.md)
