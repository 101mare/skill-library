<p align="center"><img src="docs/images/skill-library.png" width="80%" alt="Skill Library"></p>

# Skill Library

27 Skills, 5 Agents, 4 Rules — in Claude Code einstecken, Prompt-Engineering überspringen.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Skills: 27](https://img.shields.io/badge/Skills-27-blue.svg)](docs/CATALOG.md)
[![Agents: 5](https://img.shields.io/badge/Agents-5-green.svg)](docs/CATALOG.md)
[![Maintained: yes](https://img.shields.io/badge/Maintained-yes-brightgreen.svg)](https://github.com/101mare/skill-library)

> **Docs:** [CATALOG.md](docs/CATALOG.md) | [SKILLS-EXPLAINED_de.md](docs/SKILLS-EXPLAINED_de.md) | [ARTICLE_de.md](docs/ARTICLE_de.md)
>
> English version: [README.md](README.md) | [CATALOG.md](docs/CATALOG.md) | [SKILLS-EXPLAINED.md](docs/SKILLS-EXPLAINED.md) | [ARTICLE.md](docs/ARTICLE.md)

## Das Problem

CLAUDE.md-Dateien wachsen zu 500-Zeilen-Monstern. Dieselben Regeln werden in jedes Projekt kopiert. Agents mit dem Label "You are an expert" performen kaum besser als ohne Label — aber [spezifische Experiential Identities verbessern die Accuracy um 10-60%](https://arxiv.org/abs/2308.07702).

Diese Library löst das mit drei Schichten — **Rules** (immer geladen) → **Skills** (on demand) → **Agents** (isolierte Subprozesse) — jede mit klarer Aufgabe, nichts vermischt sich. Die vollständige Herleitung steht in [ARTICLE_de.md](docs/ARTICLE_de.md).

## Schnellstart

Schau in **[CATALOG.md](docs/CATALOG.md)**, such dir raus was du brauchst, sag Claude er soll es installieren:

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

Dann sag Claude:

> Nutze den tdd Skill um einen User-Registration-Endpoint hinzuzufügen

Claude liest den Skill, führt RED-GREEN-REFACTOR durch und liefert getesteten Code — kein manuelles Prompting nötig.

## Hier starten — Die fünf Kern-Skills

Wenn du nur fünf Skills installierst, decken diese den gesamten Entwicklungszyklus ab:

| Skill | Was er tut | Phase |
|-------|-----------|-------|
| **prompt-builder** | Formt vage Anfragen in strukturierte Prompts | Prompt |
| **plan-review** | 4 parallele Agents prüfen Arch, Conventions, Risiken, Reqs | Plan |
| **tdd** | RED-GREEN-REFACTOR mit Agent-Orchestrierung | Bauen + Testen |
| **systematic-debugging** | Reproduzieren → Isolieren → Root-Cause → Fix | Debug |
| **session-verify** | End-of-Session Security- + Qualitäts-Review | Verify |

**Prompt** → **Plan** → **Bauen + Testen** → **Debuggen** → **Verifizieren** — der gesamte Zyklus.

> [!TIP]
> plan-review und session-verify sind tokenintensiv (jeweils mehrere Agents). Für Speed: tdd + systematic-debugging allein decken die Kernarbeit.

## Wie es funktioniert

```
skill-library/
├── custom/                     # Deine projektspezifischen Skills & Agents
│   ├── skills/                 #   Fork it, füg deine hier hinzu
│   └── agents/                 #   Upstream-Updates fassen das nicht an
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

<details>
<summary><strong>Design-Prinzipien</strong></summary>

**Agent Soul** — Generische Labels ("You are an expert") bewegen kaum etwas, aber spezifische Experiential Identities verbessern die Accuracy um 10-60% ([NAACL 2024](https://arxiv.org/abs/2308.07702)). Was funktioniert: eine "Seele" mit konkreten Erfahrungen, Anti-Patterns und produktiven Schwächen. Jeder Agent in dieser Library baut auf dieser Forschung auf.

**Progressive Disclosure** — Skill-Header laden, damit Claude weiß was verfügbar ist. Vollständige `SKILL.md` lädt on demand. Detaillierte `reference.md`-Dateien laden nur bei Bedarf. Context-Budget bleibt knapp.

**Context-Kosten** — Jeder installierte Skill kostet Token durch seinen Header — bei jedem API-Call. Selektiv installieren.

</details>

## Eigene Skills & Agents

Fork dieses Repo und füge deine eigenen Skills in `custom/skills/` und Agents in `custom/agents/` hinzu. Dieser Ordner gehört dir — Upstream-Updates fassen ihn nicht an, `git pull` läuft ohne Merge-Konflikte.

```
Kopiere den Skill aus ~/skill-library/custom/skills/mein-skill/SKILL.md in mein Projekt
```

Die Meta-Skills ([skill-builder](skills/meta/skill-builder), [agent-builder](skills/meta/agent-builder)) können gut strukturierte Custom-Skills für dich generieren. Details in [custom/README.md](custom/README.md).

## Mitwirken

Bug gefunden? Idee für einen neuen Skill? [Issue öffnen](https://github.com/101mare/skill-library/issues) oder PR einreichen.

Die Meta-Skills ([skill-builder](skills/meta/skill-builder), [agent-builder](skills/meta/agent-builder), [team-builder](skills/meta/team-builder)) zeigen wie man Skills und Agents baut, die den Patterns der Library folgen.

## Weiterführend

- **[CATALOG.md](docs/CATALOG.md)** — Vollständiger Katalog aller Skills und Agents
- **[SKILLS-EXPLAINED_de.md](docs/SKILLS-EXPLAINED_de.md)** — Warum Skills funktionieren: Progressive Disclosure, Dateisystem-Struktur und gebündelte Ressourcen
- **[ARTICLE_de.md](docs/ARTICLE_de.md)** — Deep Dive: Drei Schichten statt einer großen CLAUDE.md, Agent-"Soul"-Design, Context-Budgets und Lessons Learned
- **[templates/CLAUDE.md.template](templates/CLAUDE.md.template)** — Produktionsreife CLAUDE.md für neue Projekte

---

**English version:** [README.md](README.md) | [CATALOG.md](docs/CATALOG.md) | [SKILLS-EXPLAINED.md](docs/SKILLS-EXPLAINED.md) | [ARTICLE.md](docs/ARTICLE.md)
