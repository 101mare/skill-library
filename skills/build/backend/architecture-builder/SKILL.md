---
name: architecture-builder
description: |
  Interactive architecture design for Python projects. Asks discovery
  questions about purpose, scale, constraints, and security, then
  proposes a tailored architecture with folder structure, tech stack,
  and documented trade-offs. Iterates with the user until the design
  is solid. Covers architecture style decisions (monolith, modular
  monolith, microservices, serverless), Clean Architecture layers,
  scalability patterns, and maintainability principles.
  Recognizes: "architecture", "architect", "design the system",
  "project architecture", "system design", "how should I structure",
  "folder structure", "tech stack", "monolith or microservices",
  "scalability", "design decisions"
  Does NOT handle: individual patterns (use di-container, protocol-design,
  strategy-registry), project scaffolding (use project-scaffold),
  frontend architecture (use frontend-design), API design (use api-design).
---

# Architecture Builder — Python Projects

> Interactive architecture design through structured discovery, informed decisions, and iterative refinement. For deeper reference on patterns, trade-offs, and decision matrices, see [reference.md](reference.md).

## Critical Constraints

- **Ask before designing.** Never propose an architecture without completing the Discovery phase
- **Explain every decision.** Every architectural choice must include *why* and *what trade-off* was accepted
- **Start simple.** Default to the simplest architecture that can plausibly work. Add complexity only when a concrete requirement demands it
- **Python-first.** All examples, folder structures, and patterns target Python (FastAPI, Django, or plain Python)
- **Compose with existing skills.** Reference `project-scaffold`, `di-container`, `protocol-design`, `api-design`, `error-handling`, `resilience-patterns` — don't duplicate them

---

## Phase 1: Discovery

Ask these questions **before any design work**. Group them conversationally — don't dump all at once. Start with Purpose, then drill into what matters.

### 1.1 Purpose & Users

- What problem does this system solve, and for whom?
- What are the top 3 use cases that must work perfectly?
- What does success look like in 6 months? In 2 years?
- What happens if the system is down for 1 hour? (SLA expectation)

### 1.2 Scale & Data

- Expected users/requests at launch? At 10x growth?
- Read/write ratio? (Mostly reads → caching; mostly writes → write optimization)
- Data volume now and in 3 years?
- Real-time requirements? (WebSocket, SSE, polling)

### 1.3 Constraints & Integrations

- Existing systems to integrate with? (Legacy APIs, databases, third-party services)
- Non-negotiable tech constraints? (Existing stack, team skills, vendor contracts)
- Compliance requirements? (GDPR, HIPAA, SOC2, PCI-DSS)
- Team size and how many teams will work on this?
- Deployment target? (Cloud provider, on-premise, edge, hybrid)
- Budget constraints? (Self-hosted vs managed services)

### 1.4 Quality Attributes — Define With Numbers

Never leave NFRs vague. Use concrete definitions:

| Attribute | Example Definition |
|---|---|
| Performance | 95th percentile API response < 200ms at 1000 req/s |
| Availability | 99.9% uptime (max 8.7 hrs downtime/year) |
| Scalability | Handle 10x traffic spike without code changes |
| Maintainability | New developer productive within 2 days |
| Security | All PII encrypted at rest; zero plaintext credentials |

---

## Phase 2: Architecture Style Decision

Based on discovery answers, recommend one of these styles. **Default to modular monolith** unless a specific signal demands otherwise.

### Decision Matrix

| Signal | Monolith | Modular Monolith | Microservices | Serverless |
|---|---|---|---|---|
| Team size | 1–5 | 5–50 | 50+ | Any |
| Domain clarity | Exploring | Partially known | Well-understood | Event-driven |
| Scaling needs | Uniform | Uniform | Per-component | Spiky/unpredictable |
| Deployment | Single unit | Single unit | Independent | Per-function |
| Data consistency | ACID | ACID | Eventual | Eventual |
| Operational cost | Low | Low | High | Pay-per-use |
| Local dev experience | Great | Great | Poor | Poor |

### When to Extract Services

Only extract from monolith to service when **at least two** of these are true:
- Component has dramatically different scaling needs (100x other components)
- Component requires a different tech stack (ML in Python, main app in Go)
- Regulatory isolation required (PCI-DSS scope minimization)
- Teams are blocked by deployment coupling
- Component needs independent deployment frequency

### The 2025/2026 Consensus

42% of organizations are consolidating microservices back to larger units (CNCF 2025). Amazon Prime Video cut infra costs 90% by moving back to monolith for video analysis. **Start modular, extract selectively.**

---

## Phase 3: System Design

### 3.1 Clean Architecture Layers (Python)

Dependencies always point inward. Inner layers never import from outer layers.

```
┌─────────────────────────────────────────┐
│  Infrastructure (DB, HTTP, external)    │  Frameworks & Drivers
│  ┌───────────────────────────────────┐  │
│  │  API / CLI (presentation layer)   │  │  Interface Adapters
│  │  ┌─────────────────────────────┐  │  │
│  │  │  Use Cases (app logic)      │  │  │  Application Rules
│  │  │  ┌───────────────────────┐  │  │  │
│  │  │  │  Domain (entities)    │  │  │  │  Business Rules
│  │  │  └───────────────────────┘  │  │  │
│  │  └─────────────────────────────┘  │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

**The Dependency Rule**: Use cases define interfaces (Protocols). Infrastructure implements them. Wired via dependency injection at startup.

### 3.2 Folder Structure — Modular Monolith (FastAPI)

```
project/
├── src/
│   ├── main.py                      # App entry point, DI wiring
│   ├── config/
│   │   ├── settings.py              # Pydantic Settings (env vars)
│   │   └── dependencies.py          # DI container / providers
│   │
│   ├── modules/                     # Business modules (bounded contexts)
│   │   ├── users/
│   │   │   ├── domain/
│   │   │   │   ├── entities.py      # User entity (dataclass/Pydantic)
│   │   │   │   ├── value_objects.py # Email, UserId, etc.
│   │   │   │   └── events.py        # UserRegistered, UserDeleted
│   │   │   ├── usecases/
│   │   │   │   ├── register.py      # RegisterUser use case
│   │   │   │   └── authenticate.py  # AuthenticateUser use case
│   │   │   ├── interfaces/
│   │   │   │   └── repository.py    # UserRepository Protocol
│   │   │   ├── infrastructure/
│   │   │   │   └── pg_repository.py # PostgreSQL implementation
│   │   │   └── api/
│   │   │       ├── routes.py        # FastAPI router
│   │   │       └── schemas.py       # Request/Response models
│   │   │
│   │   ├── billing/                 # Another bounded context
│   │   │   └── ...                  # Same internal structure
│   │   │
│   │   └── shared/                  # Cross-module shared kernel
│   │       ├── domain/
│   │       │   └── base.py          # Base entity, AggregateRoot
│   │       └── infrastructure/
│   │           └── database.py      # Engine, session factory
│   │
│   └── common/                      # Technical cross-cutting
│       ├── exceptions.py            # Exception hierarchy
│       ├── logging.py               # Structured logging setup
│       └── middleware.py            # Auth, CORS, error handling
│
├── tests/
│   ├── conftest.py
│   ├── unit/                        # Domain + use case tests (fast)
│   ├── integration/                 # DB + API tests (slower)
│   └── e2e/                         # Full flow tests (slowest)
│
├── docs/
│   └── decisions/                   # Architecture Decision Records
│       └── ADR-001-use-postgresql.md
│
├── alembic/                         # DB migrations
├── pyproject.toml
├── Dockerfile
└── docker-compose.yml
```

**Module rules:**
- Each module owns its domain, use cases, interfaces, infrastructure, and API
- Modules communicate via shared kernel or domain events — never direct imports between modules
- `shared/` contains only what genuinely belongs to multiple modules
- If a module grows beyond ~2000 LOC, evaluate splitting

### 3.3 Folder Structure — Simple Monolith (FastAPI)

For smaller projects where modules are overkill:

```
project/
├── src/
│   ├── main.py
│   ├── config.py                    # Settings
│   ├── domain/
│   │   ├── entities.py
│   │   └── interfaces.py           # Repository Protocols
│   ├── usecases/
│   │   └── user_usecases.py
│   ├── infrastructure/
│   │   ├── database.py
│   │   └── repositories.py         # Implementations
│   ├── api/
│   │   ├── routes.py
│   │   └── schemas.py
│   └── exceptions.py
├── tests/
├── pyproject.toml
└── Dockerfile
```

---

## Phase 4: Architecture Proposal

After discovery and style decision, present a structured proposal:

### Proposal Template

```markdown
# Architecture Proposal: [Project Name]

## 1. Architecture Style
[Modular Monolith / Monolith / Microservices + Justification]

## 2. Tech Stack
| Layer          | Technology        | Why                          |
|----------------|-------------------|------------------------------|
| Framework      | FastAPI / Django  | [reason]                     |
| Database       | PostgreSQL        | [reason]                     |
| Cache          | Redis             | [reason]                     |
| Message Broker | -                 | [not needed yet because...]  |
| Auth           | [approach]        | [reason]                     |

## 3. Module Boundaries
[List of modules with responsibilities]

## 4. Key Decisions (ADRs)
- ADR-001: [Decision + trade-off summary]
- ADR-002: ...

## 5. Scalability Path
[Current → 10x growth → 100x growth — what changes at each stage]

## 6. Security Architecture
[Auth approach, data flow, encryption, compliance]

## 7. Folder Structure
[The full tree]

## 8. Open Questions
[What needs more discussion]
```

### Iterate

After presenting the proposal:
1. Ask the user for feedback on each section
2. Challenge your own decisions — "I proposed X, but Y would work if [condition]"
3. Refine until the user confirms the architecture
4. Generate ADRs for all significant decisions

---

## Principles Checklist

Every proposed architecture must satisfy:

### Clean Code & Design
- [ ] Single Responsibility: each module/service has one business capability
- [ ] Dependency Inversion: inner layers define Protocols, outer layers implement
- [ ] Separation of Concerns: business logic free from framework code
- [ ] KISS: no technology added without a concrete justification
- [ ] YAGNI: no speculative abstractions — build for current + 1 step ahead
- [ ] DRY applied to knowledge, not code — duplicate across modules if it avoids coupling

### Scalability
- [ ] Stateless services (session state externalized)
- [ ] Scaling path documented (vertical → horizontal → selective extraction)
- [ ] Caching strategy defined (L1 in-process, L2 Redis, L3 CDN)
- [ ] Database scaling plan (connection pooling → read replicas → sharding)

### Maintainability
- [ ] New developer productive within 2 days
- [ ] Acyclic dependency graph between modules
- [ ] Module boundaries enforced (no cross-module direct imports)
- [ ] Consistent naming conventions documented
- [ ] Each file < 300 lines, each function < 30 lines target

### Security
- [ ] Auth architecture defined (identity provider, token strategy)
- [ ] Input validation at every system boundary
- [ ] Secrets in environment variables / secret manager
- [ ] PII handling documented (encryption, logging exclusion)
- [ ] Compliance requirements addressed

### Observability
- [ ] Structured logging with correlation IDs
- [ ] Health endpoint with dependency checks
- [ ] Key metrics defined (RED: Rate, Errors, Duration)

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|---|---|---|
| Big Ball of Mud | No boundaries, everything imports everything | Define modules with explicit interfaces |
| Premature Microservices | Operational cost explodes for < 5 devs | Start as modular monolith |
| Shared Database | Modules coupled at data layer | Each module owns its tables |
| God Module | One module does everything | Split by business capability |
| Framework Married | Business logic depends on FastAPI/Django | Dependency inversion via Protocols |
| Golden Hammer | Same pattern for every problem | Match pattern to problem |
| Speculative Generality | Building for hypothetical scale | YAGNI — solve current problems |
| Distributed Monolith | Microservices that must deploy together | If they can't deploy independently, merge them |

---

## Composing With Other Skills

This skill designs the architecture. Other skills implement the details:

| Decision Area | Delegate To |
|---|---|
| Initial file structure | `project-scaffold` |
| Dependency injection setup | `di-container` |
| Interface design (Protocols) | `protocol-design` |
| API endpoints | `api-design` |
| Exception hierarchy | `error-handling` / `exception-builder` |
| Retry, Circuit Breaker, Timeout | `resilience-patterns` |
| Extensible dispatch | `strategy-registry` |
| Test structure | `testing-patterns` |
| Config management | `config-builder` |
| Logging setup | `logging-builder` |
| Docker & CI/CD | `docker-builder` / `ci-cd-builder` |

---

## Verification

Before delivering the architecture proposal, check:

1. **Discovery complete**: Were all four question groups (Purpose, Scale, Constraints, Quality Attributes) addressed? If the user skipped any, flag it as an open risk.
2. **Every decision justified**: Can you point to a concrete discovery answer that drove each architectural choice? If a decision is based on assumption, state it explicitly.
3. **KISS check**: Is there any component in the proposal that could be removed without violating a stated requirement? If yes, remove it.
4. **Baseline test**: Would a generic "FastAPI + PostgreSQL + Docker" template cover this project equally well? If yes, the discovery didn't surface enough constraints — ask more questions.
5. **Scalability path exists**: Does the proposal include what changes at 10x and 100x growth? If not, add it.
6. **Anti-pattern scan**: Does the proposal contain any pattern from the Anti-Patterns table above? If yes, fix before delivering.
