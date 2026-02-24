# Ralph Loop — Prompt Template

Use this template to write effective prompts for `/ralph-loop`.

## Template

```
/ralph-loop max=<N> <AUFGABE>

Anforderungen:
1. <Konkretes Ergebnis 1>
2. <Konkretes Ergebnis 2>
3. <Konkretes Ergebnis 3>

Verifikation nach jeder Iteration:
- <Pruefbarer Befehl, z.B. pytest, ruff, etc.>

Fertig wenn:
- [ ] <Checklisten-Punkt 1>
- [ ] <Checklisten-Punkt 2>
- [ ] <Checklisten-Punkt 3>
```

## Die drei Pflicht-Bestandteile

### 1. Klare Aufgabe (Was genau?)

Konkret und pruefbar, nicht vage.

| Schlecht | Gut |
|----------|-----|
| "Verbessere die Tests" | "Schreibe Unit-Tests fuer validators.py. Jede public Funktion braucht min. 2 Tests." |
| "Mach den Code besser" | "Refactore extract_json_object() — extrahiere die Regex-Logik in eine eigene Funktion." |
| "Finde Bugs" | "Fuehre ruff check src/ aus und behebe alle gemeldeten Fehler." |

### 2. Verifikationsschritte (Woher weiss Claude ob es klappt?)

Claude muss in jeder Iteration selbst pruefen koennen ob es Fortschritt macht.

```
Verifikation nach jeder Iteration:
- pytest tests/test_validators.py -q --tb=short
- ruff check src/services/validators.py
```

Gute Verifikationen: `pytest`, `ruff check`, `mypy`, `bash script.sh`, Datei-Checks.
Schlechte Verifikationen: "schau ob es gut aussieht", "teste manuell".

### 3. Fertig-Kriterium (Wann ist Schluss?)

Explizite Checkliste damit Claude weiss wann `<promise>COMPLETE</promise>` angebracht ist.

```
Fertig wenn:
- [ ] Alle 5 Funktionen haben Tests
- [ ] pytest laeuft gruen (0 failures)
- [ ] Kein linting-Fehler
```

## Beispiele

### Beispiel 1: Tests schreiben

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

### Beispiel 2: Refactoring

```
/ralph-loop max=10 Refactore src/extractors/pdf.py — die extract() Methode ist zu lang.

Anforderungen:
1. extract() auf max 30 Zeilen reduzieren
2. Logik in private Helper-Methoden extrahieren
3. Keine Verhaltensaenderung (bestehende Tests muessen gruen bleiben)

Verifikation nach jeder Iteration:
- pytest tests/test_extractors/ -q --tb=short
- ruff check src/extractors/pdf.py

Fertig wenn:
- [ ] extract() <= 30 Zeilen
- [ ] Alle bestehenden Tests gruen
- [ ] Kein linting-Fehler
```

### Beispiel 3: Bug fixen

```
/ralph-loop max=8 Behebe den Bug: IBAN-Validierung akzeptiert IBANs mit falscher Pruefziffer.

Anforderungen:
1. Pruefziffer-Validierung in EntityValidator.validate_iban() implementieren
2. Test der den Bug reproduziert (falsche Pruefziffer → None)
3. Test mit gueltigern IBANs die weiterhin akzeptiert werden

Verifikation nach jeder Iteration:
- pytest tests/test_services/test_validators.py -q --tb=short

Fertig wenn:
- [ ] Falsche Pruefziffern werden rejected
- [ ] Gueltige IBANs werden weiterhin akzeptiert
- [ ] Alle Tests gruen
```

### Beispiel 4: Batch-Aufgabe

```
/ralph-loop max=20 Fuege type hints zu allen Funktionen in src/utils/ hinzu.

Anforderungen:
1. Alle public Funktionen in src/utils/*.py brauchen vollstaendige type hints
2. Parameter UND Return-Types annotieren
3. mypy src/utils/ muss ohne Fehler laufen

Verifikation nach jeder Iteration:
- mypy src/utils/ --ignore-missing-imports
- pytest -q --tb=short

Fertig wenn:
- [ ] Alle public Funktionen in utils/ annotiert
- [ ] mypy meldet keine Fehler
- [ ] Bestehende Tests weiterhin gruen
```

## Anti-Patterns

| Vermeiden | Warum | Besser |
|-----------|-------|--------|
| Vage Ziele | Claude weiss nicht wann fertig | Konkrete Checkliste |
| Kein Verifikationsschritt | Kein Fortschritts-Check moeglich | `pytest`, `ruff`, etc. einbauen |
| Zu grosser Scope | Drift, Kontext-Verlust nach vielen Iterationen | In Phasen aufteilen |
| Design-Entscheidungen offen | Claude raet, du willst was anderes | Entscheidungen im Prompt treffen |
| max zu hoch | Kosten explodieren | max=10-20 fuer die meisten Aufgaben |

## Faustregel

> Wenn du einem Junior-Entwickler die Aufgabe geben koenntest und er sie ohne Rueckfragen abarbeiten kann — dann ist der Prompt gut fuer Ralph.
