# Skills, erklärt: Warum Ordner mit Markdown-Dateien so effektiv sind

> [README](../README_de.md) | [KATALOG](CATALOG_de.md) | **SKILLS-EXPLAINED** | [ARTICLE](ARTICLE_de.md)

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

### Inhalt

1. [Die Gewohnheit](#die-gewohnheit) — Wie sich Prompts natürlich zu Skills entwickeln
2. [Warum Prompting weiterhin zählt](#warum-prompting-weiterhin-zählt) — Klare Anweisungen verbessern jedes Modell
3. [Was sich tatsächlich ändert](#was-sich-tatsächlich-ändert-wenn-du-einen-skill-nutzt) — Progressive Disclosure, Struktur, Ressourcen
4. [Warum das für Teams wichtig ist](#warum-das-für-teams-wichtig-ist) — Implizites Wissen codifizieren
5. [In der Praxis](#in-der-praxis) — Wann ein Prozess zum Skill werden sollte

---

## Die Gewohnheit

Die meisten Nutzer von KI-Werkzeugen haben irgendwann einen Prompt, der "größtenteils funktioniert". Eine Checkliste, ein Workflow, ein Regelwerk wie "mach das nicht" und "prüf immer das". Du passt ihn ein paarmal an, bis das Ergebnis stimmt, und speicherst ihn zur Wiederverwendung.

Mit der Zeit verändert sich dieser Prompt schleichend. Du fügst eine neue Regel hinzu, nachdem etwas schiefgeht. Du löschst eine Zeile, die nicht mehr nötig scheint. Jemand anderes kopiert ihn in ein anderes Projekt und passt ihn leicht an.

Irgendwann existieren drei oder vier Versionen desselben Prozesses, und niemand weiß mehr genau, welche das Ergebnis liefert, das du tatsächlich willst. Das ist der natürliche Lebenszyklus eines Prompts — und genau das Problem, das Skills lösen.

**Ein Skill ist eine Formalisierung dieser Gewohnheit.** Im Kern ist ein Skill eine Sammlung von Prompts, niedergeschrieben in einer Markdown-Datei, manchmal mit zusätzlichen Referenzdateien oder Scripts, die das Modell nutzen kann. Es ist nicht grundlegend anders als Prompting. Es *ist* Prompting, wiederverwendbar gemacht.

Statt Anweisungen in einem Dokument oder einer Notiz-App aufzubewahren, legst du sie in einen Ordner — üblicherweise als `SKILL.md`-Datei — zusammen mit Beispielen, Templates oder Scripts, die den Workflow tatsächlich Ende-zu-Ende funktionieren lassen. Der Ordner wird zu etwas, das der Agent als wiederholbaren Prozess nutzen kann statt als einmaliger Versuch.

In dieser Library ist derselbe Instinkt der Grund, warum aus 500 Zeilen langen CLAUDE.md-Dateien getrennte Rules, Skills und Agents wurden. Der Prozess, der in [ARTICLE_de.md](ARTICLE_de.md) beschrieben wird — wo fünf Projekte fünf auseinandergelaufene Configs hatten — ist genau diese Gewohnheit im großen Maßstab.

> [!IMPORTANT]
> **Kernaussage:** Skills sind organisierte Prompts mit Ressourcen. Sie fangen die Prompt-Arbeit ein, die du sonst jedes Mal neu machen würdest.

---

## Warum Prompting weiterhin zählt

Man hört manchmal, dass Prompting weniger wichtig wird, weil Modelle besser werden. Das stimmt insofern, als man keine magische Formulierung oder Formatierungstricks mehr braucht, um das Modell zum Funktionieren zu bringen.

Aber wie im Gespräch mit jedem Menschen helfen klare und eindeutige Anweisungen. Das Modell kann nicht Gedanken lesen. Es kann eine Aufgabe nur anhand der Anweisungen und des Kontexts ausführen, die es erhält.

Die Forschung bestätigt das. Das NAACL 2024 Paper ["Better Zero-Shot Reasoning with Role-Play Prompting"](https://arxiv.org/abs/2308.07702) fand heraus, dass generische Labels wie "You are an expert in X" keinerlei statistisch signifikante Verbesserung gegenüber gar keinem Label zeigten. Aber spezifische, erfahrungsbasierte Anweisungen verbesserten die Genauigkeit um 10–60%. Der Unterschied liegt nicht darin, *ob* man promptet, sondern *wie spezifisch*.

Ein Skill ist einfach eine Möglichkeit, die Prompt-Arbeit einmal zu erledigen. Statt dass jeder Nutzer die richtigen Anweisungen jedes Mal neu entdecken muss, wird der Workflow einmal niedergeschrieben — so, wie die Aufgabe tatsächlich gemeint ist.

Mit einem gut gestalteten Skill kann der Nutzer viel einfachere Anweisungen geben und trotzdem konsistente Ergebnisse erhalten. "Nutze den tdd-Skill um einen User-Registration-Endpoint hinzuzufügen" ersetzt einen ganzen Absatz manueller Anweisungen über Tests-zuerst-schreiben, ausführen, implementieren, refactoren.

> [!IMPORTANT]
> **Kernaussage:** Bessere Modelle bedeuten nicht, dass Anweisungen weniger wichtig sind. Ein Skill fängt spezifische, getestete Anweisungen ein — keine generischen Labels.

---

## Was sich tatsächlich ändert, wenn du einen Skill nutzt

Es gibt drei konzeptionelle Unterschiede zwischen einem gespeicherten Prompt und einem Skill. Jeder adressiert eine andere Schwäche des Copy-Paste-Ansatzes.

### Progressive Disclosure

Ein gespeicherter Prompt lädt alles auf einmal in den Kontext. Jede Regel, jeden Sonderfall, jedes Beispiel — ob relevant für die aktuelle Aufgabe oder nicht.

Ein Skill funktioniert anders. Er enthüllt Informationen progressiv, von einfach zu komplex. Jeder Skill hat eine kurze Beschreibung, die erklärt, wofür er da ist. Der Agent liest diese Beschreibung und entscheidet, ob der Skill relevant ist. Erst wenn er feststellt, dass der Skill zutrifft, lädt er die vollständigen Anweisungen.

Es ist wie in einer Bibliothek. Du startest mit dem Katalog, um zu sehen, welche Bücher es zu einem Thema gibt. Wenn du das passende Buch gefunden hast, liest du nicht das ganze Ding — du blätterst zum Index, um das richtige Kapitel zu finden. Die detaillierten Anweisungen bleiben geschlossen, bis sie tatsächlich relevant sind.

In dieser Library funktionieren die drei Ebenen wie verschachtelte Container:

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

Das ist wichtig, weil Context Windows endlich sind — und [Forschung zeigt](https://arxiv.org/abs/2510.05381), dass die Performance mit der Kontextlänge abnimmt, selbst wenn relevante Informationen perfekt abrufbar sind. Nur laden, was gebraucht wird, wenn es gebraucht wird, ist die Antwort.

### Struktur

Ein gespeicherter Prompt ist ein flacher Text. Es gibt keine inhärente Organisation jenseits dessen, was du selbst in den Text einbaust.

Ein Skill lebt in einem Ordner innerhalb eines Dateisystems. Moderne Modelle sind ziemlich gut darin, Dateisysteme zu navigieren. Die Tatsache, dass etwas in einem bestimmten Pfad liegt, vermittelt bereits Information darüber, wie es verwendet werden soll.

Genauso wie du deinen eigenen Desktop nach Projekt oder Zweck organisierst, gibt die Struktur eines Skills-Verzeichnisses dem Modell Kontext:

```
skills/
├── build/
│   ├── backend/                 # Scaffolding & Infrastruktur
│   │   ├── ci-cd-builder/
│   │   ├── config-builder/
│   │   ├── docker-builder/
│   │   ├── exception-builder/
│   │   ├── logging-builder/
│   │   ├── project-scaffold/
│   │   └── prompt-builder/
│   └── frontend/                # Design & Komponenten
│       ├── frontend-design/
│       └── warmgold-frontend/
├── meta/                        # Skills, Agents & Teams bauen
│   ├── agent-builder/
│   ├── skill-builder/
│   └── team-builder/
├── patterns/                    # Wiederverwendbare Architektur-Patterns
│   ├── api-design/
│   ├── di-container/
│   ├── error-handling/
│   ├── protocol-design/
│   ├── resilience-patterns/
│   ├── strategy-registry/
│   ├── systematic-debugging/
│   └── testing-patterns/
└── workflow/                    # Multi-Agent-Workflows
    ├── deep-research/
    ├── plan-review/
    ├── pr-review/
    ├── ralph-loop/
    ├── ralph-loop-prompt-builder/
    ├── session-verify/
    └── tdd/
```

Das bringt auch **Modularität** mit sich. Ein Skill wird zu einer verpackten Workflow-Einheit, die wiederverwendet, geteilt, versioniert oder mit anderen Skills kombiniert werden kann. Statt leicht verschiedene Versionen desselben Prompts in jedes Projekt zu kopieren, behandelst du Workflows als Module, die zwischen Projekten und Teammitgliedern wandern.

Für die praktischen Details des SKILL.md-Formats — YAML-Frontmatter, Trigger-Matching und wie du eigene Skills erstellst — siehe den Abschnitt [Das SKILL.md Format](ARTICLE_de.md#das-skillmd-format) in ARTICLE_de.md.

Der [Agent Skills Standard](https://agentskills.io) geht noch weiter — Skills in diesem Format funktionieren mit über 30 Tools, darunter Claude Code, OpenAI Codex, Cursor, Gemini CLI und VS Code. Alle 27 Skills in dieser Library folgen dem Standard.

### Zugang zu zusätzlichen Ressourcen

Ein wiederverwendbarer Prompt ist üblicherweise auf das beschränkt, was du dir zu kopieren gemerkt hast. Ein Skill kann Anhänge, Beispiele, Scripts, Bewertungskriterien oder sogar ausführbares Tooling bündeln, das das Modell bei der Aufgabe nutzen kann.

Nimm den `ralph-loop`-Skill in dieser Library. Er ist nicht nur ein Satz von Anweisungen — er bündelt:

| Datei | Zweck |
|-------|-------|
| `SKILL.md` | Kern-Anweisungen für den `/ralph-loop`-Befehl |
| `init.md` | Installationsscript zum Einrichten des Hooks |
| `prompt-template.md` | Template, das Claude für jede Aufgabe ausfüllt |
| `ralph-loop-stop.sh` | Bash-Hook-Script — die eigentliche Automatisierungs-Engine |

Der Workflow wird nicht nur durch Anweisungen fundiert, sondern durch Kontext und Werkzeuge. Der Unterschied zwischen "hier sind Anweisungen zum Ausführen von Tests" und "hier ist ein Test-Runner, der deine Arbeit validiert."

Das kann den Aufruf von MCP-Servern, das Ausführen eines CLI-Scripts oder das Referenzieren interner Richtlinien in einer `reference.md` umfassen. In diesem Sinne sagt ein Skill dem Modell nicht nur, *was* es tun soll, sondern gibt ihm auch Zugang zu den unterstützenden Materialien, die es braucht, um es *gut* zu tun.

> [!IMPORTANT]
> **Kernaussage:** Drei Dinge trennen Skills von gespeicherten Prompts — Progressive Disclosure hält den Kontext schlank, Dateisystem-Struktur vermittelt Bedeutung, und gebündelte Ressourcen machen Workflows ausführbar.

---

## Warum das für Teams wichtig ist

Für einzelne Entwickler sind Skills ein Produktivitätswerkzeug. Du fängst ein, was funktioniert, und verwendest es wieder. Der Nutzen ist persönlich: weniger Wiederholung, mehr Konsistenz.

Für Teams ist der Nutzen anders — und bedeutender. Vieles von dem, was in einer Organisation als Expertise gilt, ist kein Satz von Fakten, sondern eine Abfolge von Gewohnheiten und Prüfungen. Es ist das Wissen, was man vor einem Deployment verifizieren muss, welche Annahmen getestet werden sollten, und welche Art von Output als akzeptabel gilt.

Normalerweise wird dieses Wissen informell weitergegeben oder liegt in veralteter Dokumentation begraben. Mit Skills kann dieses prozedurale Wissen in etwas verpackt werden, dem der Agent direkt folgen kann.

Nimm den `reviewer.md`-Agent dieser Library. Seine Identität ist nicht "You are an expert security reviewer." Stattdessen trägt er spezifische Erfahrungen:

> *"…found SQL injection slip through three rounds of code review, watched silent `except: pass` blocks cause production incidents, traced GDPR violations to debug-level LLM response logs…"*

Das ist implizites Wissen — die Art, die normalerweise Jahre an Erfahrung oder Pairing mit einem Senior-Entwickler erfordert. Verpackt als Skill oder Agent wird es sofort für jedes Teammitglied verfügbar.

In der Praxis ermöglicht das Teams, Expertise zu codifizieren und zu verstärken, die sonst implizit oder inkonsistent angewendet bliebe. Alle führen dieselben Schritte aus. Neue Teammitglieder müssen den Prozess nicht von Grund auf rekonstruieren.

Wenn sich der Prozess ändert, aktualisierst du den Skill einmal statt jeden zu bitten, seine eigenen Prompts anzupassen. Das gilt ob großes Unternehmen oder kleines Team.

> [!IMPORTANT]
> **Kernaussage:** Skills codifizieren implizites Wissen — die Gewohnheiten, Prüfungen und Entscheidungen, die normalerweise nur in Köpfen existieren.

---

## In der Praxis

Skills erweitern nicht, was das Modell tun kann. Sie machen es nicht schlauer und geben ihm keine neuen Fähigkeiten. Was sie tun: Es wird einfacher, wiederholbare Aufgaben vorhersagbar auszuführen.

Sie erlauben es dir, Prozesse zu codifizieren und zu teilen statt dich auf Gedächtnis oder Copy-Paste zu verlassen. Gleicher Skill, gleiche Input-Muster, gleiche Output-Qualität — jedes Mal.

Wenn du dich dabei ertappst, denselben Prozess mehr als ein paarmal zu wiederholen, ist das in der Regel ein Zeichen, dass er zum Skill werden kann. Das Signal ist Wiederholung. Die Lösung ist Formalisierung.

Was Skills einführen, ist keine neue Fähigkeit, sondern ein Weg, implizite Prozesse in etwas Explizites, Teilbares und konsistent Ausführbares zu verwandeln.

> [!TIP]
> Willst du eigene Skills erstellen? Der `skill-builder` Meta-Skill in dieser Library bringt Claude das SKILL.md-Format, Frontmatter-Konventionen und Best Practices bei — du kannst einfach sagen "erstelle einen Skill für X" und erhältst ein gut strukturiertes Ergebnis.

---

*Dieser Artikel basiert auf ["Skills, Explained"](https://x.com/gabrielchua/status/1936752568665473300) von [Gabriel Chua](https://x.com/gabrielchua), mit Konzepten, die für den Kontext dieser Library umformuliert und mit Beispielen aus dem skill-library Repository angereichert wurden.*

---

**English version:** [SKILLS-EXPLAINED.md](SKILLS-EXPLAINED.md)
