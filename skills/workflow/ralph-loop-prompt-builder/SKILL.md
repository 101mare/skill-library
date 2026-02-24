---
name: ralph-loop-prompt-builder
description: |
  Helps build effective prompts for the Ralph Loop autonomous work system.
  Asks clarifying questions about the task, then generates a structured prompt
  with clear requirements, verification steps, and completion criteria.
  Usage: /ralph-loop-prompt-builder
  Triggers: "ralph prompt", "build ralph prompt", "help me write a ralph loop prompt"
---

# Ralph Loop Prompt Builder

Help the user create an effective prompt for `/ralph-loop`. A good Ralph prompt has three mandatory parts: clear task, verification steps, and completion criteria.

## Step 1: Gather Information

Ask the user up to 4 questions using AskUserQuestion. Choose the most relevant questions from this list:

### Question 1: Task Type (always ask)
"Was fuer eine Aufgabe soll der Ralph Loop erledigen?"
Options:
- Tests schreiben
- Bug fixen
- Refactoring
- Neues Feature implementieren

### Question 2: Scope (always ask)
"Welche Dateien/Module sind betroffen?"
Options:
- Einzelne Datei (z.B. validators.py)
- Ein Modul (z.B. src/services/)
- Mehrere Module
- Ganzes Projekt

### Question 3: Verification (ask if not obvious)
"Wie soll Claude pruefen ob der Fortschritt stimmt?"
Options:
- pytest (Unit Tests)
- ruff check (Linting)
- Beides (pytest + ruff)
- Anderes (bitte beschreiben)

### Question 4: Iteration Limit (ask if user didn't specify)
"Wie viele Iterationen maximal?"
Options:
- 5 (kleiner Fix)
- 10 (mittlere Aufgabe)
- 20 (groessere Aufgabe)
- 50 (Default, grosse Aufgabe)

## Step 2: Build the Prompt

Based on the answers, construct a Ralph Loop prompt with this structure:

```
/ralph-loop max=<N> <TASK_SUMMARY>

Anforderungen:
1. <Requirement 1>
2. <Requirement 2>
3. <Requirement 3>

Verifikation nach jeder Iteration:
- <verification command 1>
- <verification command 2>

Fertig wenn:
- [ ] <Completion criterion 1>
- [ ] <Completion criterion 2>
- [ ] <Completion criterion 3>
```

### Rules for Building the Prompt

**Anforderungen:**
- Be specific and measurable, never vague
- Include file paths where relevant
- State what should NOT change (preserve existing behavior)

**Verifikation:**
- Must be automated commands Claude can run (pytest, ruff, mypy, etc.)
- Never "check manually" or "make sure it looks good"
- Include both correctness (tests) and quality (linting) checks if applicable

**Fertig-Kriterien:**
- Checkboxes that Claude can verify programmatically
- Each criterion maps to a verification command
- Include "all existing tests still pass" for refactoring tasks

**Max Iterations:**
- 5 for small, focused fixes
- 10-15 for medium tasks (tests, single-module refactoring)
- 20 for larger tasks (multi-file, new features)
- 50 only for batch operations across many files

## Step 3: Present and Refine

Present the generated prompt to the user. Ask if they want to adjust anything:
- Add or remove requirements
- Change iteration limit
- Modify verification steps

Once confirmed, the user can copy-paste the prompt directly.

## Examples of Good Output

### For "Tests schreiben" + "Einzelne Datei"

```
/ralph-loop max=15 Schreibe Unit-Tests fuer src/services/confidence.py.

Anforderungen:
1. Jede public Methode von ConfidenceScorer braucht min. 2 Tests
2. Edge Cases testen: Score 0.0, Score 1.0, None-Werte
3. Tests in tests/test_services/test_confidence.py

Verifikation nach jeder Iteration:
- pytest tests/test_services/test_confidence.py -q --tb=short

Fertig wenn:
- [ ] Min. 10 Tests geschrieben
- [ ] Alle Tests gruen
- [ ] Edge Cases abgedeckt
```

### For "Bug fixen" + "Einzelne Datei"

```
/ralph-loop max=8 Behebe den Bug: <BUG_DESCRIPTION>.

Anforderungen:
1. Reproduziere den Bug mit einem fehlschlagenden Test
2. Implementiere den Fix in <FILE>
3. Stelle sicher dass bestehende Tests weiterhin gruen sind

Verifikation nach jeder Iteration:
- pytest <TEST_FILE> -q --tb=short

Fertig wenn:
- [ ] Bug-reproduzierender Test existiert und ist gruen
- [ ] Bestehende Tests weiterhin gruen
- [ ] Kein linting-Fehler
```
