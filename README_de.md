# Skill Library

Bringe Claude Code bei, wie ein Senior Engineer zu arbeiten. Eine Sammlung aus 27 Skills, 16 Agents und praxiserprobten Rules, die Claude wiederverwendbares Wissen ueber Architektur-Patterns, Entwicklungs-Workflows und Code-Qualitaet geben.

**[CATALOG_de.md](CATALOG_de.md)** — Alle 27 Skills und 16 Agents mit Beschreibungen und Dateipfaden. Dein Einstiegspunkt zum Auswaehlen und Installieren.

**[ARTICLE_de.md](ARTICLE_de.md)** — Der ausfuehrliche Deep Dive: Warum diese Library existiert, wie Rules/Skills/Agents zusammenspielen, wie man Agents eine "Seele" gibt, und Lessons Learned beim Aufbau.

> English version: [README.md](README.md) | [CATALOG.md](CATALOG.md) | [ARTICLE.md](ARTICLE.md)

## Schnellstart

Sag Claude, welchen Skill oder Agent du willst. Das war's.

```
Kopiere den Skill aus ~/skill-library/skills/workflow/tdd/SKILL.md in mein Projekt
```

Claude liest die Datei, kopiert sie in dein Projekt unter `.claude/skills/` (oder `.claude/agents/`) und aktiviert sie automatisch. Die vollstaendige Liste findest du in [CATALOG_de.md](CATALOG_de.md).

## Was drin steckt

```
skill-library/
├── templates/
│   └── CLAUDE.md.template      # Generische CLAUDE.md fuer neue Projekte
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

**Skills** vermitteln Claude spezialisiertes Wissen und Workflows — von TDD-Zyklen und systematischem Debugging bis hin zu DI-Containern und API-Design. Sie aktivieren sich automatisch, wenn Claude den richtigen Kontext erkennt.

**Agents** sind fokussierte Subagenten, die Claude fuer bestimmte Aufgaben startet — Code auf Sicherheitsluecken pruefen, toten Code erkennen, Tests schreiben oder Implementierungsrisiken bewerten.

**Rules** setzen globales Verhalten: Coding Conventions, Scope-Disziplin, Security-Defaults und Selbstverbesserung durch Korrekturen.

## Wie es funktioniert

Skills und Agents nutzen das native Erweiterungssystem von Claude Code. Ein Skill ist eine `SKILL.md`-Datei mit strukturiertem Wissen. Ein Agent ist eine `.md`-Datei mit YAML-Frontmatter, die einen spezialisierten Subagenten definiert. Rules sind immer geladene `.md`-Dateien, die Claudes Verhalten ueber alle Aufgaben hinweg praegen.

Kopiere was du brauchst in das `.claude/`-Verzeichnis deines Projekts — oder verlinke per Symlink aus diesem Repo nach `~/.claude/` fuer globale Verfuegbarkeit. Passe Trigger an, ergaenze projektspezifische Regeln oder kombiniere Teile aus mehreren Skills zu deinem eigenen.

## CLAUDE.md Template

Ein produktionsreifes CLAUDE.md-Template findest du unter `templates/CLAUDE.md.template`:

```bash
cp ~/skill-library/templates/CLAUDE.md.template my-project/CLAUDE.md
```

Deckt Architektur, Commands, Import-Konventionen, Key Patterns und Konfiguration ab. Generische Regeln (DRY, Agent-Verhalten, Security) leben in `rules/` und muessen hier nicht wiederholt werden.

## Weiterfuehrend

- **[CATALOG_de.md](CATALOG_de.md)** — Vollstaendiger Katalog aller Skills und Agents
- **[ARTICLE_de.md](ARTICLE_de.md)** — Architektur, Design-Entscheidungen und Nutzungsmuster
