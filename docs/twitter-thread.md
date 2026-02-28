# Twitter Thread: skill-library

## 1/6

Dein CLAUDE.md ist ein 500-Zeilen-Monster? Copy-paste von Regeln über 5 Projekte? skill-library löst das: Eine modulare Toolbox für Claude Code. 3 saubere Ebenen statt einer riesigen Config-Datei. Open Source, reines Markdown, MIT-Lizenz.

## 2/6

Die 3 Ebenen: Rules — immer geladen, nie dupliziert. Skills — on demand, 27 Workflows und Patterns. Agents — isolierte Subprozesse mit eigener Expertise. Jede Ebene hat einen klaren Job. Keine Vermischung.

## 3/6

27 Skills in 4 Kategorien: Meta (Skills bauen Skills), Backend (Docker, CI/CD, Logging), Frontend (Design Systems), Workflow (TDD, Code Review, Deep Research) und Patterns (DI Container, API Design, Error Handling). Alles per Skill-Aufruf aktivierbar.

## 4/6

5 spezialisierte Agents: Reviewer (Security, Type Safety), Analyzer (Architektur, Dead Code), Planner (Implementierung validieren), Code-Simplifier und Test-Architect. Jeder läuft isoliert — kein Parent-Kontext rein, nur Ergebnis raus.

## 5/6

Der Clou: Progressive Disclosure. 27 Skills kosten nur ~100 Zeilen im System Prompt. Details laden erst bei Bedarf. Plus: Agent-Identität schlägt generische Labels. "Du bist ein Experte" bringt laut Forschung exakt 0 Verbesserung.

## 6/6

Funktioniert nicht nur mit Claude Code — der Agent Skills Standard macht alles portabel über 30+ Tools (Cursor, Gemini CLI, etc.). Einfach Skill kopieren, fertig. github.com/101mare/skill-library
