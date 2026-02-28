# Global vs. Lokal: Wo deine Konfiguration lebt

> [README](../README_de.md) | [KATALOG](CATALOG.md) | [SKILLS-EXPLAINED](SKILLS-EXPLAINED_de.md) | [ARTICLE](ARTICLE_de.md) | **GLOBAL-VS-LOCAL**

### TL;DR

- **Drei Orte, drei Zwecke** — Global (`~/.claude/`) ist die Runtime-Config deiner Maschine, Lokal (`.claude/`) ist die Runtime-Config eines Projekts, dieses Repository ist die Source of Truth, in der Content gepflegt, versioniert und geteilt wird
- **Das Repo konkurriert nicht mit global/lokal** — es ist die Quelle, die beide füttert. Die Beziehung: Repo → (copy/symlink) → Global oder Lokal → Claude Code liest es
- **Ehrliche Antwort:** Ein Solo-Entwickler auf einer Maschine mit zwei Projekten braucht dieses Repo wahrscheinlich nicht. Ein Team, mehrere Maschinen, oder jeder der Configs teilt — schon
- **Global ≠ "alles überall"** — installiere was du brauchst, nicht was du irgendwann brauchen könntest. Jeder Skill-Header kostet Token bei jedem API-Call

### Inhalt

1. [Die drei Orte](#die-drei-orte) — Global, Lokal und dieses Repository
2. [Was gehört wohin](#was-gehört-wohin) — Empfehlungen für jeden Content-Typ
3. [Wie sie zusammenspielen](#wie-sie-zusammenspielen) — Override-, Shadow- und Merge-Verhalten
4. [Wo dieses Repository hingehört](#wo-dieses-repository-hingehört) — Source of Truth, nicht Runtime-Ziel
5. [Ehrliche Einschätzung](#ehrliche-einschätzung-wann-du-dieses-repo-brauchst-und-wann-nicht) — Wann du dieses Repo brauchst und wann nicht
6. [Empfohlenes Setup](#empfohlenes-setup) — Drei Stufen von minimal bis voll

---

## Die drei Orte

Claude Code liest Konfiguration zur Laufzeit von zwei Orten. Dieses Repository ist ein dritter Ort, der außerhalb von Claude Codes Runtime existiert — hier wird der Content erstellt und gepflegt.

### Global: `~/.claude/`

Deine maschinenweite Konfiguration. Alles hier gilt für **jedes Projekt**, das du mit Claude Code öffnest.

| Verzeichnis | Was es enthält | Ladeverhalten |
|-------------|---------------|---------------|
| `~/.claude/rules/*.md` | Verhaltensregeln | Immer in jeden Prompt geladen |
| `~/.claude/skills/[name]/SKILL.md` | Skill-Definitionen | Header immer geladen; vollständiger Inhalt bei Bedarf |
| `~/.claude/agents/[name].md` | Agent-Definitionen | Geladen wenn explizit referenziert |
| `~/.claude/settings.json` | Tool-Berechtigungen, Modell-Präferenzen | Zusammengeführt mit lokalen Einstellungen |

**Nutze global für:** Standards, die für all deine Arbeit gelten — Coding-Konventionen, Sicherheits-Defaults, Agent-Verhalten, Kern-Workflow-Skills.

### Lokal: `.claude/`

Projektspezifische Konfiguration. Lebt im Projektverzeichnis und wird typischerweise in das Git-Repository des Projekts committet.

| Datei / Verzeichnis | Was es enthält | Ladeverhalten |
|---------------------|---------------|---------------|
| `.claude/CLAUDE.md` | Projektkontext, Constraints, Architektur | Immer geladen |
| `.claude/rules/*.md` | Projektspezifische Regeln | Immer geladen; erweitert oder überschreibt global |
| `.claude/skills/[name]/SKILL.md` | Projektspezifische Skills | Header immer geladen; vollständiger Inhalt bei Bedarf |
| `.claude/agents/[name].md` | Projektspezifische Agents | Geladen wenn explizit referenziert |
| `.claude/memory.md` | Gelernte Lektionen in diesem Projekt | Beim Session-Start geladen |
| `.claude/settings.local.json` | Projekteinstellungen, Hooks | Zusammengeführt mit globalen Einstellungen |

**Nutze lokal für:** Was dieses Projekt einzigartig macht — seine Architektur, seine Commands, seine domänenspezifischen Skills, seine gelernten Lektionen.

### Dieses Repository: `~/skill-library/`

Ein Git-Repository mit kuratiertem, dokumentiertem, versioniertem Content, den du in globale oder lokale Orte kopierst oder verlinkst.

| Verzeichnis | Was es enthält | Wie es zu Claude Code kommt |
|-------------|---------------|---------------------------|
| `rules/` | 4 universelle Verhaltensregeln | Kopieren nach `~/.claude/rules/` oder `.claude/rules/` |
| `skills/` | 27 wiederverwendbare Skills | Symlink nach `~/.claude/skills/` oder kopieren nach `.claude/skills/` |
| `agents/` | 5 spezialisierte Agents | Bei Bedarf nach `.claude/agents/` kopieren |
| `templates/` | CLAUDE.md-Template | Pro Projekt kopieren und anpassen |
| `custom/` | Deine eigenen Erweiterungen | Fork-Bereich, Upstream fasst ihn nicht an |
| `docs/` | Katalog, Artikel, Erklärungen | Nur Referenz, wird nicht installiert |

**Das ist kein Runtime-Ort.** Claude Code liest niemals direkt aus `~/skill-library/`. Das Repo ist, wo du Content pflegst; Global und Lokal sind, wo Claude Code ihn liest.

---

## Was gehört wohin

| Content | Wohin | Warum |
|---------|-------|-------|
| Coding-Konventionen (DRY, Types, Error Handling) | **Globale Rules** | Überall dieselben Standards |
| Agent-Verhalten (read-first, Scope-Disziplin) | **Globale Rules** | Überall derselbe Arbeitsstil |
| Sicherheits-Defaults (Input-Validierung, PII, Secrets) | **Globale Rules** | Nicht verhandelbar, überall |
| Self-Improvement (Lektionen erfassen, beim Start reviewen) | **Globale Rules** | Überall derselbe Lernzyklus |
| Kern-Workflow-Skills (tdd, Debugging, plan-review) | **Globale Skills** | In den meisten Projekten genutzt |
| Architekturmuster-Skills (DI, API-Design) | **Globale Skills** | Projektübergreifend wiederverwendbar |
| Meta-Skills (skill-builder, agent-builder) | **Globale Skills** | Projektunabhängig |
| Frontend-Design-Skills | **Globale Skills** (falls du Frontend machst) | Wiederverwendbare Design-Prinzipien |
| Scaffold-, Docker-, CI/CD-Skills | **Globale Skills** oder **nicht installieren** | Einmal pro Projekt genutzt; bei Bedarf installieren |
| Projektarchitektur, Constraints, Commands | **Lokale CLAUDE.md** | Einzigartig für dieses Projekt |
| Domänenspezifische Skills (dein DB-Schema, deine API-Eigenheiten) | **Lokale Skills** | Einzigartig für dieses Projekt |
| Gelernte Lektionen, entdeckte Workarounds | **Lokale memory.md** | Projektwissen |
| Hook-Konfiguration (Ralph Loop, Custom Hooks) | **Lokale Settings** | Projektspezifische Automatisierung |

> [!TIP]
> **Der Lackmustest:** Wenn du es unverändert in ein neues Projekt kopieren würdest, gehört es nach global. Wenn du es für das neue Projekt anpassen würdest, gehört es nach lokal. Wenn du es versionieren und teilen willst, gehört es in dieses Repo.

---

## Wie sie zusammenspielen

### Priorität: Lokal überschattet Global

Wenn derselbe Name an beiden Orten existiert, gewinnt lokal:

```
Claude Code liest:
  1. ~/.claude/rules/security.md          (global)
  2. .claude/rules/security.md            (lokal — überschattet global bei gleichem Dateinamen)

  1. ~/.claude/skills/tdd/SKILL.md        (global)
  2. .claude/skills/tdd/SKILL.md          (lokal — überschattet global bei gleichem Namen)
```

### Rules: Koexistieren, Lokal kann überschreiben

Globale Rules werden zuerst geladen. Lokale Rules danach. Hat eine lokale Rule denselben Dateinamen wie eine globale, ersetzt die lokale Version sie. Unterschiedliche Dateinamen koexistieren — du bekommst beide.

### Skills: Erster Treffer gewinnt

Claude prüft zuerst lokal, dann global. Existiert `.claude/skills/tdd/`, wird das verwendet. Wenn nicht, Fallback auf `~/.claude/skills/tdd/`. Sie verschmelzen nicht — es ist das eine oder das andere.

### Settings: Zusammengeführt, Lokal überschreibt Schlüssel

```json
// ~/.claude/settings.json
{ "autoCompact": true }

// .claude/settings.local.json
{ "hooks": { "Stop": [...] } }

// Effektiv:
{ "autoCompact": true, "hooks": { "Stop": [...] } }
```

Gleiche Schlüssel in lokal überschreiben global. Verschiedene Schlüssel koexistieren.

### Der Fluss

```
┌─────────────────────┐
│  skill-library/     │  Source of Truth
│  (dieses Repo)      │  Versioniert, dokumentiert, geteilt
└────────┬────────────┘
         │
         │  copy / symlink
         │
    ┌────▼──────────┐        ┌──────────────────┐
    │  ~/.claude/   │        │  .claude/        │
    │  (global)     │        │  (lokal/Projekt) │
    │               │        │                  │
    │  rules/       │───────▶│  rules/          │  lokal überschattet global
    │  skills/      │───────▶│  skills/         │  lokal überschattet global
    │  agents/      │───────▶│  agents/         │  lokal überschattet global
    │  settings     │───────▶│  settings.local  │  zusammengeführt, lokal überschreibt
    └───────────────┘        └──────────────────┘
              │                       │
              └───────────┬───────────┘
                          │
                          ▼
                  ┌───────────────┐
                  │  Claude Code  │  Runtime liest von beiden
                  └───────────────┘
```

---

## Wo dieses Repository hingehört

Dieses Repository ist **kein** globales oder lokales Konfigurationsverzeichnis. Es ist eine **Quelle**, die beide füttert.

### Was das Repo IST

- **Eine versionierte Sammlung** — Git-History verfolgt jede Änderung. `~/.claude/` hat keine History; Bearbeitungen sind endgültig.
- **Ein Distributionskanal** — Andere können forken, klonen, browsen, beitragen. `~/.claude/` sind private Dateien auf deiner Maschine.
- **Ein Dokumentations-Hub** — Katalog, Artikel, Erklärungen. Globale/lokale Configs sind nur Dateien in einem Ordner.
- **Ein Sync-Mechanismus** — Einmal symlinken, `git pull` um überall zu aktualisieren. Ohne das Repo kopierst du manuell und driftest auseinander.
- **Ein Fork-Punkt** — Der `custom/`-Ordner gibt dir einen dedizierten Platz für eigene Skills, den Upstream-Updates nicht anfassen.

### Was das Repo NICHT IST

- **Keine Runtime-Abhängigkeit** — Claude Code liest niemals direkt aus `~/skill-library/`.
- **Kein Framework** — Keine Install-Scripts, keine Build-Steps, keine Lock-Files. Es sind nur Markdown-Dateien.
- **Nicht erforderlich, damit Claude Code funktioniert** — Du kannst Rules, Skills und Agents von Grund auf neu schreiben.

### Zwei Installationsmuster

**Symlink** (empfohlen für Skills, die du aktuell halten willst):
```bash
ln -s ~/skill-library/skills/workflow/tdd ~/.claude/skills/tdd
```
- Änderungen im Repo wirken sofort
- `git pull` aktualisiert alle verlinkten Skills auf einmal
- Ideal für: Globale Skills, die du aktuell halten willst

**Kopie** (für Content, den du besitzen und anpassen willst):
```bash
cp ~/skill-library/rules/*.md ~/.claude/rules/
cp -r ~/skill-library/skills/workflow/tdd .claude/skills/tdd
```
- Deine Kopie entwickelt sich unabhängig
- Manueller Sync nötig
- Ideal für: Rules (ändern sich selten) und projektlokale Skills (pro Projekt angepasst)

---

## Ehrliche Einschätzung: Wann du dieses Repo brauchst und wann nicht

### Wann du dieses Repo wahrscheinlich NICHT brauchst

**Solo-Entwickler, eine Maschine, 1-2 Projekte mit ähnlichem Stack:**

Kopiere die vier Rule-Dateien nach `~/.claude/rules/`. Schreib deine Skills direkt in `~/.claude/skills/`. Fertig. Du bekommst dasselbe Runtime-Verhalten, ohne ein separates Repository zu pflegen. Die Rules in diesem Repo sind gute Ausgangspunkte, aber sobald sie in `~/.claude/rules/` liegen, hat das Repo seinen Zweck erfüllt.

**Du brauchst nur 2-3 Skills:**

Erstelle sie direkt in `~/.claude/skills/`. Kein Repo nötig. Der Overhead aus Klonen, Symlinken und Pull-Updates lohnt sich nicht für eine Handvoll Dateien, die du selbst schreiben könntest.

**Du teilst deine Konfiguration mit niemandem:**

Globale Configs auf deiner Maschine funktionieren prima für den Eigengebrauch. Der Hauptvorteil des Repos — Teilen, Zusammenarbeit, Distribution — ist irrelevant, wenn niemand anders deine Configs je sieht.

### Wann du dieses Repo BRAUCHST

**Mehrere Maschinen:**

Klone das Repo auf jeder Maschine, symlinke nach `~/.claude/`. Ein `git pull` aktualisiert alles überall. Ohne das Repo synchronisierst du Dateien manuell zwischen Maschinen — und sie werden auseinanderdriften.

**Team oder Organisation:**

Alle klonen dasselbe Repo. Neue Teammitglieder haben sofort Zugriff auf 27 getestete Skills, 5 spezialisierte Agents und 4 Rule-Dateien. Ohne das Repo baut jeder sein eigenes Setup von Grund auf und man landet genau bei dem Problem, das diese Library lösen soll: fünf Leute, fünf divergierende Configs.

**Du willst Versionshistorie:**

`~/.claude/rules/security.md` hat keine History. Du bearbeitest sie, die alte Version ist weg. Das Repo gibt dir Git-History, Blame, Diff und die Möglichkeit, zurückzurollen.

**Du willst beitragen oder Updates erhalten:**

Das Repo wird gepflegt und aktualisiert. Skills werden verfeinert, neue kommen dazu, Bugs werden gefixt. `git pull` bringt dir all das. Ohne das Repo bist du bei der Version eingefroren, die du kopiert hast.

**Du baust Custom Skills und willst eine saubere Trennung:**

Der `custom/`-Ordner gibt dir einen dedizierten Platz für eigene Skills, den Upstream-Updates nicht anfassen. Ohne die Repo-Struktur vermischst du eigene Arbeit mit geborgtem Content und verlierst den Überblick, was woher kam.

### Entscheidungsmatrix

| Szenario | Repo nötig? | Empfohlenes Setup |
|----------|------------|-------------------|
| Solo-Dev, eine Maschine, ein Projekt | Nein | Rules nach global kopieren, Skills manuell schreiben |
| Solo-Dev, eine Maschine, 5+ Projekte | Vielleicht | Kern-Skills symlinken für Konsistenz |
| Solo-Dev, mehrere Maschinen | Ja | Repo klonen, nach `~/.claude/` symlinken |
| Kleines Team (2-5 Leute) | Ja | Geteiltes Repo, jedes Mitglied klont |
| Team + Open-Source-Projekte | Ja | Repo forken, in `custom/` hinzufügen, mit Team teilen |
| Organisation mit Standards | Ja | Repo forken, Rules via CI durchsetzen |

---

## Empfohlenes Setup

### Minimal: Nur Rules

Kopiere die vier Rule-Dateien und nutze Claude Codes eingebaute Fähigkeiten für alles andere.

```bash
cp ~/skill-library/rules/*.md ~/.claude/rules/
```

**Was du bekommst:** Konsistente Coding-Konventionen, Sicherheits-Defaults und Agent-Verhalten in allen Projekten. Kein Skill-Overhead.

**Ideal für:** Entwickler, die eine solide Grundlage wollen, ohne sich auf die volle Library einzulassen.

### Standard: Rules + Core Five Skills

Die Rules plus die fünf Skills, die den gesamten Entwicklungszyklus abdecken.

```bash
# Rules
cp ~/skill-library/rules/*.md ~/.claude/rules/

# Kern-Workflow-Skills (gelinkt für Updates)
ln -s ~/skill-library/skills/build/backend/prompt-builder ~/.claude/skills/prompt-builder
ln -s ~/skill-library/skills/workflow/plan-review ~/.claude/skills/plan-review
ln -s ~/skill-library/skills/workflow/tdd ~/.claude/skills/tdd
ln -s ~/skill-library/skills/patterns/systematic-debugging ~/.claude/skills/systematic-debugging
ln -s ~/skill-library/skills/workflow/session-verify ~/.claude/skills/session-verify
```

**Was du bekommst:** Prompt → Plan → Build+Test → Debug → Verify — der gesamte Zyklus.

**Ideal für:** Die meisten Entwickler, die einen strukturierten Workflow wollen, ohne alles zu installieren.

### Voll: Gelinkte Skill-Kategorien

Symlinke ganze Skill-Kategorien basierend auf deiner Arbeit.

```bash
# Rules (immer)
cp ~/skill-library/rules/*.md ~/.claude/rules/

# Alle Workflow-Skills
for skill in ~/skill-library/skills/workflow/*/; do
  ln -s "$skill" ~/.claude/skills/$(basename "$skill")
done

# Alle Pattern-Skills
for skill in ~/skill-library/skills/patterns/*/; do
  ln -s "$skill" ~/.claude/skills/$(basename "$skill")
done

# Backend-Build-Skills (falls du Backend machst)
for skill in ~/skill-library/skills/build/backend/*/; do
  ln -s "$skill" ~/.claude/skills/$(basename "$skill")
done

# Meta-Skills (falls du Custom Skills baust)
for skill in ~/skill-library/skills/meta/*/; do
  ln -s "$skill" ~/.claude/skills/$(basename "$skill")
done
```

**Was du bekommst:** Den vollen Werkzeugkasten. Jeder Skill bei Bedarf verfügbar.

**Trade-off:** Mehr Skill-Header in jedem Prompt = höhere Token-Kosten pro API-Call. Installiere nur Kategorien, die du tatsächlich nutzt.

> [!WARNING]
> Jeder installierte Skill kostet Token durch seinen Header bei jedem API-Call. Das volle Setup fügt ~27 Header hinzu. Wenn du kostensensitiv bist oder an kurzen Tasks arbeitest, bleib beim Standard-Setup.

---

**English version:** [GLOBAL-VS-LOCAL.md](GLOBAL-VS-LOCAL.md)
