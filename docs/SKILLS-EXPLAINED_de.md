# Skills, erklärt: Warum Ordner mit Markdown-Dateien so effektiv sind

> [README](../README_de.md) | [KATALOG](CATALOG.md) | **SKILLS-EXPLAINED** | [ARTICLE](ARTICLE_de.md)

> [!NOTE]
> Dieser Artikel erklärt die konzeptionellen Grundlagen von Skills — warum
> das Format funktioniert und was es von gespeicherten Prompts unterscheidet.
> Für die Architektur der Library und wie man sie nutzt, siehe
> [ARTICLE_de.md](ARTICLE_de.md).

### TL;DR

- **Skills formalisieren, was du ohnehin schon tust** — Menschen entwickeln Prompts mit der Zeit weiter; Skills fangen diese Entwicklung in einem wiederverwendbaren Format ein
- **Klare Anweisungen zählen weiterhin** — Modelle werden besser, aber sie können nicht Gedanken lesen. Ein Skill erledigt die Prompt-Arbeit einmal statt sie jedes Mal neu zu entdecken
- **Drei Dinge trennen Skills von gespeicherten Prompts** — Progressive Disclosure (nur laden, was gebraucht wird), Dateisystem-Struktur (Organisation vermittelt Bedeutung) und Zugang zu zusätzlichen Ressourcen (Scripts, Beispiele, APIs)
- **Teams profitieren am meisten** — Skills codifizieren implizites Wissen und standardisieren Prozesse über Personen und Projekte hinweg
- **Skills erweitern keine Fähigkeiten** — sie machen wiederholbare Aufgaben vorhersagbar und konsistent

---

## Die Gewohnheit

Die meisten Nutzer von KI-Werkzeugen haben irgendwann einen Prompt, der "größtenteils funktioniert". Du passt ihn ein paarmal an, speicherst ihn und verwendest ihn wieder. Mit der Zeit kommen Regeln dazu, Zeilen verschwinden, jemand kopiert ihn in ein anderes Projekt — und bald existieren drei Versionen, keine davon kanonisch.

**Ein Skill formalisiert diese Gewohnheit.** Statt Anweisungen in einem Dokument oder einer Notiz-App aufzubewahren, legst du sie in einen Ordner — üblicherweise als `SKILL.md`-Datei — zusammen mit Beispielen, Templates oder Scripts, die den Workflow Ende-zu-Ende funktionieren lassen. Der Ordner wird zu einem wiederholbaren Prozess statt einem einmaligen Versuch.

---

## Warum Prompting weiterhin zählt

Man hört manchmal, dass Prompting weniger wichtig wird, weil Modelle besser werden. Aber wie im Gespräch mit jedem Menschen helfen klare und eindeutige Anweisungen. Das Modell kann nicht Gedanken lesen.

Das [NAACL 2024 Paper](https://arxiv.org/abs/2308.07702) fand heraus, dass generische Labels wie "You are an expert in X" keinerlei statistisch signifikante Verbesserung zeigten. Aber spezifische, erfahrungsbasierte Anweisungen verbesserten die Genauigkeit um 10–60%. Der Unterschied liegt nicht darin, *ob* man promptet, sondern *wie spezifisch*.

Ein Skill erledigt die Prompt-Arbeit einmal. "Nutze den tdd-Skill um einen User-Registration-Endpoint hinzuzufügen" ersetzt einen ganzen Absatz manueller Anweisungen über Tests-zuerst-schreiben, ausführen, implementieren, refactoren.

---

## Was sich tatsächlich ändert, wenn du einen Skill nutzt

Drei konzeptionelle Unterschiede trennen einen Skill von einem gespeicherten Prompt.

### Progressive Disclosure

Ein gespeicherter Prompt lädt alles auf einmal — jede Regel, jeden Sonderfall — ob relevant oder nicht.

Ein Skill enthüllt Informationen progressiv. Jeder Skill hat eine kurze Header-Beschreibung. Der Agent liest sie und entscheidet, ob der Skill zutrifft. Erst dann lädt er die vollständigen Anweisungen. Detaillierte Referenzdateien bleiben geschlossen, bis sie tatsächlich gebraucht werden.

```
┌─────────────────────────────────────────────────────┐
│  Ebene 1: Skill-Header (immer geladen)               │
│  name + description → Agent weiß, was verfügbar ist  │
│                                                      │
│  ┌───────────────────────────────────────────────┐   │
│  │  Ebene 2: SKILL.md (bei Bedarf geladen)       │   │
│  │  Kern-Anweisungen, Trigger, Beispiele         │   │
│  │                                               │   │
│  │  ┌───────────────────────────────────────┐    │   │
│  │  │  Ebene 3+: Zusätzliche Dateien        │    │   │
│  │  │  reference.md, examples.md, forms.md  │    │   │
│  │  │  (nur gelesen wenn wirklich nötig)    │    │   │
│  │  └───────────────────────────────────────┘    │   │
│  └───────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

Das ist wichtig, weil Context Windows endlich sind — und [Forschung zeigt](https://arxiv.org/abs/2510.05381), dass die Performance mit der Kontextlänge abnimmt, selbst wenn relevante Informationen perfekt abrufbar sind.

### Struktur

Ein gespeicherter Prompt ist ein flacher Text. Ein Skill lebt in einem Ordner innerhalb eines Dateisystems. Der Pfad vermittelt bereits Information über die Verwendung — genauso wie du deinen Desktop nach Projekt oder Zweck organisierst. Siehe den vollständigen Verzeichnisbaum in [CATALOG.md](CATALOG.md).

Das bringt **Modularität** mit sich: ein Skill wird zu einer verpackten Workflow-Einheit, die wiederverwendet, geteilt, versioniert oder mit anderen Skills kombiniert werden kann. Für die praktischen Details des SKILL.md-Formats — YAML-Frontmatter, Trigger-Matching und wie du eigene Skills erstellst — siehe [ARTICLE_de.md](ARTICLE_de.md#das-skillmd-format).

Der [Agent Skills Standard](https://agentskills.io) geht noch weiter — Skills in diesem Format funktionieren mit über 30 Tools, darunter Claude Code, OpenAI Codex, Cursor, Gemini CLI und VS Code. Alle Skills in dieser Library folgen dem Standard.

### Zugang zu zusätzlichen Ressourcen

Ein gespeicherter Prompt ist auf das beschränkt, was du hineinkopiert hast. Ein Skill kann Anhänge, Beispiele, Scripts, Bewertungskriterien oder ausführbares Tooling bündeln.

Nimm den `ralph-loop`-Skill:

| Datei | Zweck |
|-------|-------|
| `SKILL.md` | Kern-Anweisungen für den `/ralph-loop`-Befehl |
| `init.md` | Installationsscript zum Einrichten des Hooks |
| `prompt-template.md` | Template, das Claude für jede Aufgabe ausfüllt |
| `ralph-loop-stop.sh` | Bash-Hook-Script — die eigentliche Automatisierungs-Engine |

Der Unterschied zwischen "hier sind Anweisungen zum Ausführen von Tests" und "hier ist ein Test-Runner, der deine Arbeit validiert." Ein Skill kann MCP-Server aufrufen, CLI-Scripts ausführen oder interne Richtlinien in einer `reference.md` referenzieren.

---

## Warum das für Teams wichtig ist

Für Einzelpersonen reduzieren Skills Wiederholung. Für Teams ist der Nutzen bedeutender: Vieles von dem, was als Expertise gilt, ist keine Sammlung von Fakten, sondern eine Abfolge von Gewohnheiten und Prüfungen — wissen was man vor einem Deployment verifiziert, welche Annahmen getestet werden, welcher Output akzeptabel ist.

Der `reviewer.md`-Agent dieser Library zeigt den Unterschied. Seine Identität ist nicht "You are an expert security reviewer." Stattdessen trägt er spezifische Erfahrungen:

> *"…found SQL injection slip through three rounds of code review, watched silent `except: pass` blocks cause production incidents, traced GDPR violations to debug-level LLM response logs…"*

Das ist implizites Wissen — die Art, die normalerweise Jahre an Erfahrung erfordert. Verpackt als Skill oder Agent wird es sofort für jedes Teammitglied verfügbar. Wenn sich der Prozess ändert, aktualisierst du den Skill einmal statt jeden zu bitten, seine eigenen Prompts anzupassen.

---

## In der Praxis

Skills erweitern nicht, was das Modell tun kann. Sie machen wiederholbare Aufgaben vorhersagbar. Wenn du dich dabei ertappst, denselben Prozess mehr als ein paarmal zu wiederholen — das ist das Signal, ihn zum Skill zu machen.

> [!TIP]
> Willst du eigene Skills erstellen? Der `skill-builder` Meta-Skill bringt Claude das SKILL.md-Format, Frontmatter-Konventionen und Best Practices bei — sag "erstelle einen Skill für X" und du erhältst ein gut strukturiertes Ergebnis.

---

*Dieser Artikel basiert auf ["Skills, Explained"](https://x.com/gabrielchua/status/1936752568665473300) von [Gabriel Chua](https://x.com/gabrielchua), mit Konzepten, die für den Kontext dieser Library umformuliert und mit Beispielen aus dem skill-library Repository angereichert wurden.*

---

**English version:** [SKILLS-EXPLAINED.md](SKILLS-EXPLAINED.md)
