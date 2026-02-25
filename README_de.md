<p align="center"><img src="docs/images/skill-library.png" width="80%" alt="Skill Library"></p>

# Skill Library

27 Skills, 5 Agents, 4 Rules — kopiere was du brauchst, lass den Rest.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Skills: 27](https://img.shields.io/badge/Skills-27-blue.svg)](docs/CATALOG_de.md)
[![Agents: 5](https://img.shields.io/badge/Agents-5-green.svg)](docs/CATALOG_de.md)
[![Maintained: yes](https://img.shields.io/badge/Maintained-yes-brightgreen.svg)](https://github.com/101mare/skill-library)

> **Docs:** [CATALOG_de.md](docs/CATALOG_de.md) | [ARTICLE_de.md](docs/ARTICLE_de.md)
>
> English version: [README.md](README.md) | [CATALOG.md](docs/CATALOG.md) | [ARTICLE.md](docs/ARTICLE.md)

## Das Problem

CLAUDE.md-Dateien wachsen zu 500-Zeilen-Monstern. Dieselben Regeln werden in jedes Projekt kopiert. Agents mit dem Label "You are an expert" zeigen [keine messbare Verbesserung](https://arxiv.org/abs/2308.07702) gegenüber gar keinem Label.

Diese Library löst das mit drei Schichten — **Rules** (immer geladen) → **Skills** (on demand) → **Agents** (isolierte Subprozesse) — jede mit klarer Aufgabe, nichts vermischt sich. Die vollständige Herleitung steht in [ARTICLE_de.md](docs/ARTICLE_de.md).

## Hier starten — Die fünf Kern-Skills

Wenn du nur fünf Skills installierst, decken diese den gesamten Entwicklungszyklus ab:

1. **prompt-builder** — Stellt klärende Fragen und formt vage Anfragen in strukturierte Prompts.
2. **plan-review** — Vier parallele Agents prüfen Architektur, Conventions, Risiken und Requirements. Ampel-Verdict *vor* dem Code.
3. **tdd** — Echtes RED-GREEN-REFACTOR mit Agent-Orchestrierung. Tests definieren Verhalten, nicht bestätigen Code.
4. **systematic-debugging** — Reproduzieren → Isolieren → Root-Cause → Fix+Absichern.
5. **session-verify** — End-of-Session Review: Security, Code-Qualität, Architektur, saubere Imports, keine TODOs.

**Prompt** → **Plan** → **Bauen + Testen** → **Debuggen** → **Verifizieren** — der gesamte Zyklus.

> **Hinweis:** plan-review und session-verify sind tokenintensiv (jeweils mehrere Agents). Für Speed: tdd + systematic-debugging allein decken die Kernarbeit.

## Schnellstart

Schau in **[CATALOG_de.md](docs/CATALOG_de.md)**, such dir raus was du brauchst, sag Claude er soll es installieren:

**Von GitHub** (kein Clone nötig):
```
Kopiere den Skill aus https://github.com/101mare/skill-library/tree/main/skills/workflow/tdd in mein Projekt
```

**Aus einem lokalen Clone:**
```
Kopiere den Skill aus ~/skill-library/skills/workflow/tdd/SKILL.md in mein Projekt
```

**Global** (Symlink — überall verfügbar, Updates via `git pull`):
```bash
ln -s ~/skill-library/skills/workflow/tdd ~/.claude/skills/tdd
```

Claude liest die Datei, kopiert sie nach `.claude/skills/` (oder `.claude/agents/`) und aktiviert sie automatisch.

## Wie es funktioniert

```
skill-library/
├── docs/                       # CATALOG + ARTICLE (EN + DE)
├── templates/
│   └── CLAUDE.md.template      # Produktionsreife CLAUDE.md für neue Projekte
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

**Rules** setzen globales Verhalten — Coding Conventions, Scope-Disziplin, Security-Defaults. Immer geladen, prägen jede Interaktion.

**Skills** vermitteln Claude spezialisierte Workflows — TDD-Zyklen, Debugging-Methodik, API-Design. Header immer sichtbar; vollständiger Inhalt lädt on demand.

**Agents** sind isolierte Subprozesse für spezifische Aufgaben — Code Review, Dead-Code-Erkennung, Tests schreiben. Kein Parent-Kontext rein, Ergebnis raus.

Der zentrale Unterschied: Skills instruieren, Agents arbeiten. Ein Workflow-Skill wie `plan-review` startet 4 Agents parallel und aggregiert deren Verdicts.

## Design-Prinzipien

**Agent Soul** — Generische Labels ("You are an expert") haben keinen signifikanten Effekt ([NAACL 2024](https://arxiv.org/abs/2308.07702)). Was funktioniert: spezifische Identität, Anti-Patterns, produktive Schwächen. Jeder Agent in dieser Library baut auf dieser Forschung auf.

**Progressive Disclosure** — Skill-Header laden, damit Claude weiß was verfügbar ist. Vollständige `SKILL.md` lädt on demand. Detaillierte `reference.md`-Dateien laden nur bei Bedarf. Context-Budget bleibt knapp.

**Context-Kosten** — Jeder installierte Skill kostet Token durch seinen Header — bei jedem API-Call. 27 Skills ≈ 100 Zeilen permanenter System-Prompt. Selektiv installieren.

## Weiterführend

- **[CATALOG_de.md](docs/CATALOG_de.md)** — Vollständiger Katalog aller Skills und Agents
- **[ARTICLE_de.md](docs/ARTICLE_de.md)** — Deep Dive: Drei Schichten statt einer großen CLAUDE.md, Agent-"Soul"-Design, Context-Budgets und Lessons Learned beim Bau von 27 Skills
- **[templates/CLAUDE.md.template](templates/CLAUDE.md.template)** — Produktionsreife CLAUDE.md für neue Projekte

---

**English version:** [README.md](README.md) | [CATALOG.md](docs/CATALOG.md) | [ARTICLE.md](docs/ARTICLE.md)
