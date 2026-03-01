# Global vs. Lokal: Wo deine Konfiguration lebt

> [README](../README_de.md) | [KATALOG](CATALOG.md) | [SKILLS-EXPLAINED](SKILLS-EXPLAINED_de.md) | [ARTICLE](ARTICLE_de.md) | **GLOBAL-VS-LOCAL**

### TL;DR

- **Drei Orte, drei Zwecke** — Global (`~/.claude/`) gilt für jedes Projekt auf deiner Maschine, Lokal (`.claude/`) ist projektspezifisch, dieses Repository ist die versionierte Quelle, die beide per Copy oder Symlink füttert
- **Ehrliche Antwort:** Ein Solo-Entwickler auf einer Maschine mit zwei Projekten braucht dieses Repo wahrscheinlich nicht. Ein Team, mehrere Maschinen, oder jeder der Configs teilt — schon
- **Global ≠ "alles überall"** — jeder installierte Skill-Header kostet Token bei jedem API-Call. Installiere selektiv

---

## Wo was lebt

| Was | Global `~/.claude/` | Lokal `.claude/` | Dieses Repo |
|-----|---------------------|------------------|-------------|
| Rules | `rules/*.md` — immer geladen | `rules/*.md` — erweitert oder überschreibt global | `rules/` — in eins von beiden kopieren |
| Skills | `skills/[name]/SKILL.md` — Header immer geladen, vollständiger Inhalt bei Bedarf | gleich — überschattet global | `skills/` — symlinken oder kopieren |
| Agents | `agents/[name].md` — geladen bei Referenz | gleich — überschattet global | `agents/` — bei Bedarf kopieren |
| Settings | `settings.json` — zusammengeführt mit lokal | `settings.local.json` — überschreibt gleiche Schlüssel | n/a |
| Projektkontext | n/a | `CLAUDE.md`, `memory.md` — immer geladen | `templates/` — kopieren & anpassen |

Dieses Repo ist **kein** Runtime-Ort. Claude Code liest niemals direkt aus `~/skill-library/`.

**Symlinke** Skills die du aktuell halten willst, **kopiere** Content den du besitzen willst. Siehe [README Quickstart](../README_de.md#quickstart) für Commands.

> [!TIP]
> **Der Lackmustest:** Wenn du es unverändert in ein neues Projekt kopieren würdest, gehört es nach global. Wenn du es anpassen würdest, gehört es nach lokal. Wenn du es versionieren und teilen willst, gehört es in dieses Repo.

---

## Wie sie zusammenspielen

### Auflösungsregeln

Wenn derselbe Name an beiden Orten existiert, **gewinnt lokal**:

```
Claude Code liest:
  1. ~/.claude/rules/security.md          (global)
  2. .claude/rules/security.md            (lokal — ersetzt global bei gleichem Dateinamen)

  1. ~/.claude/skills/tdd/SKILL.md        (global)
  2. .claude/skills/tdd/SKILL.md          (lokal — überschattet global bei gleichem Namen)
```

- **Rules:** Global wird zuerst geladen, lokal danach. Gleicher Dateiname → lokal ersetzt global. Verschiedene Dateinamen koexistieren.
- **Skills:** Lokal wird zuerst geprüft, dann global. Erster Treffer gewinnt — sie verschmelzen nicht.
- **CLAUDE.md:** Wird geladen, indem der Verzeichnisbaum nach oben durchlaufen wird — wenn du Claude in `foo/bar/` startest, lädt es sowohl `foo/bar/CLAUDE.md` als auch `foo/CLAUDE.md`. CLAUDE.md-Dateien in Unterverzeichnissen werden bei Bedarf geladen, wenn Claude dort Dateien liest. ([Docs](https://code.claude.com/docs/en/memory#how-claudemd-files-load))

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

## Brauchst du dieses Repo?

| Szenario | Repo nötig? | Empfohlenes Setup |
|----------|------------|-------------------|
| Solo-Dev, eine Maschine, ein Projekt | Nein | Rules nach global kopieren, Skills manuell schreiben |
| Solo-Dev, eine Maschine, 5+ Projekte | Vielleicht | Kern-Skills symlinken für Konsistenz |
| Solo-Dev, mehrere Maschinen | Ja | Repo klonen, nach `~/.claude/` symlinken |
| Kleines Team (2-5 Leute) | Ja | Geteiltes Repo, jedes Mitglied klont |
| Team + Open-Source-Projekte | Ja | Repo forken, in `custom/` hinzufügen, mit Team teilen |
| Organisation mit Standards | Ja | Repo forken, Rules via CI durchsetzen |

Für Installations-Commands, siehe [README Quickstart](../README_de.md#quickstart).

---

**English version:** [GLOBAL-VS-LOCAL.md](GLOBAL-VS-LOCAL.md)
