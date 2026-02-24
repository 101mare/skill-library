---
name: deep-research
description: |
  Structured research workflow: Question → Sources (web + codebase) → Analyze → Synthesize → Document.
  Use before technical decisions, when evaluating libraries/tools, or investigating unknowns.
  Recognizes: "deep-research", "research this", "evaluate options", "which library",
  "compare approaches", "investigate", "technical decision", "what are the trade-offs",
  "recherchiere", "welche Library", "Optionen vergleichen", "pros and cons"
---

# Deep Research

Structured workflow for technical decisions. Prevents "20 tabs open, no conclusions" syndrome.

## When to Use

- **Before technical decisions** — "Should we use Redis or memcached?"
- **Evaluating libraries/tools** — "Which OCR library is best for our use case?"
- **Investigating unknowns** — "How does vLLM handle multi-GPU?"
- **Architecture exploration** — "What's the best pattern for event sourcing in Python?"
- **Debugging unfamiliar territory** — "Why does Docker networking behave differently on macOS?"

## The Workflow

```
1. FRAME          2. GATHER           3. ANALYZE         4. SYNTHESIZE      5. DOCUMENT
"What exactly?"   "Find sources"      "Evaluate"         "Decide"           "Write it down"

Define the        Web search +        Compare against    Pick winner +      Decision record
question +        Codebase search +   criteria           justify            in memory/docs
criteria          Read docs

Exit: Clear       Exit: 3+ relevant   Exit: Criteria     Exit: Clear        Exit: Decision
question +        sources found       scored             recommendation     recorded
success criteria                                         with trade-offs
```

---

## Phase 1: FRAME — Define the Question

**Goal:** Turn a vague question into a specific, answerable research question with success criteria.

### Steps

1. **State the question precisely**
2. **Define evaluation criteria** (weighted by importance)
3. **Identify constraints** (budget, timeline, existing stack, offline requirement)
4. **Define "good enough"** — what would a successful answer look like?

### Template

```markdown
## Research Question
[Precise question]

## Context
- Project: [what project, what stage]
- Constraints: [offline? specific Python version? existing dependencies?]
- Timeline: [when do we need the answer?]

## Evaluation Criteria
1. [Criterion A] — weight: HIGH/MEDIUM/LOW
2. [Criterion B] — weight: HIGH/MEDIUM/LOW
3. [Criterion C] — weight: HIGH/MEDIUM/LOW

## Success Criteria
The research is complete when: [specific condition]
```

### Example

```markdown
## Research Question
Which Python library should we use for PDF text extraction in an offline,
Docker-deployed pipeline?

## Context
- Project: Document classification pipeline (100 cases/day)
- Constraints: Must run 100% offline, Linux Docker container, no cloud APIs
- Existing: Currently using PyMuPDF for page-to-image, then OCR

## Evaluation Criteria
1. Text extraction quality (native + scanned PDFs) — HIGH
2. No external dependencies / cloud calls — HIGH
3. Performance (< 5s per page) — MEDIUM
4. Maintenance / community activity — MEDIUM
5. License compatibility (MIT/Apache preferred) — LOW

## Success Criteria
Recommendation with benchmark data from at least 2 libraries,
tested against our sample PDFs.
```

### Exit Criterion

Clear question, weighted criteria, known constraints.

---

## Phase 2: GATHER — Find Sources

**Goal:** Collect relevant information from multiple source types.

### Source Types

| Source | Tool | Best For |
|--------|------|----------|
| Web search | `WebSearch` | Current state of art, comparisons, benchmarks |
| Documentation | `WebFetch` | Official docs, API references, changelogs |
| Codebase | `Grep`, `Read` | Current implementation, existing patterns |
| Project docs | `Read` | CLAUDE.md, ARCHITECTURE.md, memory.md |
| GitHub repos | `WebFetch` / `gh` | Issues, discussions, release notes |

### Web Research Strategy

```
# Start broad, narrow down
WebSearch("Python PDF text extraction library 2026 comparison")
WebSearch("PyMuPDF vs pdfplumber vs pypdf benchmark")
WebSearch("offline PDF OCR Python Docker")

# Then go deep on candidates
WebFetch("https://pymupdf.readthedocs.io/en/latest/", "extraction capabilities and limitations")
WebFetch("https://github.com/jsvine/pdfplumber", "features, performance, recent activity")
```

### Codebase Research Strategy

```
# Understand current implementation
Grep("import.*pdf\|from.*pdf\|PyMuPDF\|fitz", type="py")
Read("src/extractors/pdf.py")
Read("CLAUDE.md")  # architecture constraints

# Check for related patterns
Grep("extract.*text\|text.*extract", type="py")
```

### Source Quality Checklist

- [ ] At least 3 independent sources per candidate
- [ ] Official documentation consulted (not just blog posts)
- [ ] Recent sources (within last 12 months for fast-moving topics)
- [ ] Codebase context understood (what we currently use and why)
- [ ] Constraints verified against each candidate

### Exit Criterion

3+ relevant sources per candidate. Enough data to evaluate against all criteria.

---

## Phase 3: ANALYZE — Evaluate Against Criteria

**Goal:** Systematically compare options against your defined criteria.

### Comparison Matrix

```markdown
## Comparison: PDF Text Extraction

| Criterion (Weight) | PyMuPDF | pdfplumber | pypdf |
|---|---|---|---|
| Text quality (HIGH) | Excellent native, no OCR | Good native, table-aware | Basic, struggles with layout |
| Offline (HIGH) | Yes, C library | Yes, pure Python | Yes, pure Python |
| Performance (MEDIUM) | ~0.5s/page | ~2s/page | ~1s/page |
| Maintenance (MEDIUM) | Active, monthly releases | Active, slower releases | Active, PSF-maintained |
| License (LOW) | AGPL-3.0 | MIT | BSD |
```

### Scoring

Rate each cell: Strong (++), Good (+), Neutral (0), Weak (-), Disqualifier (X)

```markdown
| Criterion (Weight) | PyMuPDF | pdfplumber | pypdf |
|---|---|---|---|
| Text quality (HIGH) | ++ | + | - |
| Offline (HIGH) | ++ | ++ | ++ |
| Performance (MEDIUM) | ++ | 0 | + |
| Maintenance (MEDIUM) | ++ | + | + |
| License (LOW) | - (AGPL) | ++ | ++ |
```

### Identify Deal-Breakers

Before detailed scoring, check for disqualifiers:
- Does it violate a HIGH-weight constraint?
- Is it unmaintained / archived?
- Does it have known security issues?
- Is the license incompatible?

### Exit Criterion

All candidates scored against all criteria. Deal-breakers identified.

---

## Phase 4: SYNTHESIZE — Make a Decision

**Goal:** Pick a winner and articulate WHY, including trade-offs.

### Decision Template

```markdown
## Decision

**Winner: [Option]**

### Why
[2-3 sentences explaining the primary reasons]

### Trade-offs Accepted
- [What you're giving up by choosing this]
- [Risk you're accepting]

### Alternatives Considered
- **[Option B]**: [Why not chosen — specific reason]
- **[Option C]**: [Why not chosen — specific reason]

### Migration Path (if replacing something)
1. [Step 1]
2. [Step 2]
3. [Step 3]
```

### Example

```markdown
## Decision

**Winner: PyMuPDF**

### Why
Best text extraction quality and performance by a wide margin. The AGPL license
is acceptable because our pipeline is internal-only and not distributed.

### Trade-offs Accepted
- AGPL license restricts distribution (acceptable for internal tool)
- C dependency makes pure-Python environments harder (we use Docker, so fine)

### Alternatives Considered
- **pdfplumber**: Good table extraction but 4x slower per page. Worth considering
  if we need structured table data in the future.
- **pypdf**: Too basic for scanned documents. No OCR pathway.
```

### Exit Criterion

Clear recommendation with justified trade-offs.

---

## Phase 5: DOCUMENT — Record the Decision

**Goal:** Write it down so you don't research the same thing again.

### Where to Document

| Scope | Location | Example |
|-------|----------|---------|
| Project-specific decision | `.claude/memory.md` | "Using PyMuPDF for PDF extraction because..." |
| Architecture decision | `ARCHITECTURE.md` or ADR | Formal decision record |
| Library choice | `CLAUDE.md` (Key Patterns) | "PDF: PyMuPDF (AGPL, best quality)" |
| General learning | Skill library memory | Reusable insight for future projects |

### ADR Format (Architecture Decision Record)

```markdown
# ADR-001: PDF Text Extraction Library

## Status: Accepted

## Context
We need to extract text from PDFs (native and scanned) in an offline Docker pipeline.

## Decision
Use PyMuPDF (fitz) for PDF text extraction.

## Consequences
- AGPL license — cannot distribute as part of a proprietary product
- C dependency — requires system-level installation in Docker
- Excellent performance and quality for our use case
```

### Exit Criterion

Decision recorded in the appropriate location. Future you (or Claude) can find it.

---

## Research for Existing Skills

When deep-research reveals insights relevant to existing skills, update them:

- **New pattern discovered** → Update the relevant pattern skill
- **Library comparison done** → Note the winner in the relevant builder skill
- **Anti-pattern found** → Add to the relevant skill's anti-patterns table
- **Best practice confirmed** → Strengthen the relevant skill's guidance

---

## Quick Research (< 5 minutes)

For simple questions that don't need the full workflow:

1. **WebSearch** with specific query
2. **Skim 2-3 results** with WebFetch
3. **State conclusion** in one paragraph
4. **Note source** for reference

Use full workflow only when: multiple viable options exist, the decision has significant impact, or the topic is unfamiliar.

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|---|---|---|
| No clear question | Research goes in circles | FRAME phase: precise question + criteria |
| Only one source | Confirmation bias | Minimum 3 independent sources |
| Blog posts only | Outdated, biased, incomplete | Always check official docs |
| No criteria defined upfront | Decision becomes subjective | Define and weight criteria before gathering |
| Analysis paralysis | Never decides | Set a timebox, "good enough" beats perfect |
| No documentation | Research repeated next month | Always write down the decision |
| Researching what you already know | Wasted time | Check codebase + memory first |
| Ignoring existing implementation | Solution doesn't fit project | Read CLAUDE.md + current code first |

## Checklist

- [ ] Question precisely defined with criteria
- [ ] Constraints identified (offline, license, performance)
- [ ] Web + codebase + docs sources gathered
- [ ] At least 3 sources per candidate
- [ ] Comparison matrix with weighted scoring
- [ ] Deal-breakers checked first
- [ ] Clear recommendation with trade-offs
- [ ] Decision documented in appropriate location
