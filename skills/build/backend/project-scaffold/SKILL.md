---
name: project-scaffold
description: |
  Scaffolds production-ready Python project structure: directory layout, pyproject.toml, config,
  logging, exceptions, testing, and CI/CD basics.
  Use when creating new Python projects or restructuring existing ones to production patterns.
  Recognizes: "project-scaffold", "new Python project", "production-ready setup",
  "project structure", "scaffold project", "how should I structure this?", "pyproject.toml setup"
---

# Project Scaffold

Production-ready Python project scaffolding: typing, validated config, structured logging, testable architecture, clean separation of concerns.

## When to Use

- Scaffolding a **new** Python project from scratch
- User explicitly asks to "refactor to production patterns"
- User asks about Python project best practices

## When NOT to Use

- Project has established conventions -- **follow existing patterns first**
- Quick scripts or prototypes -- overkill
- User just wants a bug fix -- don't restructure

## Adaptation Rules

1. **Never restructure without asking** -- Propose changes, don't force them
2. **Work with existing layout** -- If project uses `app/` instead of `src/`, keep `app/`
3. **Incremental adoption** -- Apply one pattern at a time, not everything at once
4. **Patterns are suggestions** -- Adapt to project context, not vice versa

---

## Project Layout

```
repo/
  pyproject.toml
  config.yaml              # User-editable configuration
  README.md
  CLAUDE.md                # AI development context
  src/
    <package>/
      __init__.py
      __main__.py
      cli.py               # Thin entry point
      logging_config.py
      exceptions.py
      config/
        __init__.py
        models.py          # Pydantic config models
        loader.py          # YAML loading + validation
      models/
        __init__.py
        domain.py          # Internal dataclasses
        dto.py             # Boundary Pydantic models
      services/
        __init__.py        # Business logic
      adapters/
        __init__.py        # External integrations (DB, APIs)
  tests/
    conftest.py
    test_smoke.py
```

**Guidelines (adapt to project):**
- Business logic in `services/`, infrastructure in `adapters/`
- Import through package, avoid relative "walk up" imports
- CLI only parses args and calls services
- Config loaded once at startup, passed explicitly

## Configuration

### Philosophy
- **config.yaml** for all user-configurable settings
- **Environment variables** only for secrets and deployment overrides
- **Pydantic models** for validation and type safety
- Fail fast: invalid config crashes at startup, not runtime

### Config Models

```python
# config/models.py
from pydantic import BaseModel, Field

class ModelConfig(BaseModel):
    name: str = Field(min_length=1)
    temperature: float = Field(ge=0.0, le=2.0, default=0.0)
    max_tokens: int = Field(ge=1, le=32000, default=4096)

class AppConfig(BaseModel):
    """Root configuration - mirrors config.yaml structure."""
    model: ModelConfig = Field(default_factory=ModelConfig)
```

### Config Loader

```python
# config/loader.py
from pathlib import Path
import yaml
from .models import AppConfig

def load_config(path: Path = Path("config.yaml")) -> AppConfig:
    """Load and validate config. Crashes on invalid config."""
    if not path.exists():
        return AppConfig()
    with open(path) as f:
        raw = yaml.safe_load(f) or {}
    return AppConfig.model_validate(raw)
```

## Typing Standards

- Type all public functions and methods
- Use `T | None` instead of `Optional[T]`
- Parameterize collections: `list[str]`, `dict[str, int]`
- Use `typing.Protocol` for interfaces

```python
from typing import Protocol

class Embedder(Protocol):
    def embed(self, text: str) -> list[float]: ...
```

## Models

### Internal Domain: dataclasses

```python
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Document:
    id: str
    content: str
    metadata: dict[str, str]
```

### Boundaries: Pydantic

```python
from pydantic import BaseModel, ConfigDict

class DocumentDTO(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    id: str
    content: str
```

**Guideline:** Pydantic at boundaries (API, config, file parsing), dataclasses internally.

## Exceptions

```python
# exceptions.py
class AppError(Exception):
    """Base for all expected errors."""

class ConfigError(AppError):
    """Invalid configuration."""

class ProcessingError(AppError):
    """Processing failed."""

class ExternalServiceError(AppError):
    """External API/service failure."""
```

Always chain with `from e`:
```python
try:
    response = api.call()
except ConnectionError as e:
    raise ExternalServiceError(f"API unreachable") from e
```

## Logging

```python
# logging_config.py
import logging
import os

def configure_logging(level: str | None = None) -> None:
    lvl = (level or os.getenv("LOG_LEVEL") or "INFO").upper()
    logging.basicConfig(
        level=lvl,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

# Usage in modules:
logger = logging.getLogger(__name__)
logger.info("Processing started", extra={"doc_id": doc.id})
```

**Guidelines:**
- One logger per module via `__name__`
- Never log secrets or PII
- Use `extra={}` for structured context

## CLI Pattern

```python
# cli.py
import argparse
import logging
from pathlib import Path
from .config.loader import load_config
from .exceptions import AppError
from .logging_config import configure_logging

logger = logging.getLogger(__name__)

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config.yaml")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    configure_logging("DEBUG" if args.verbose else None)

    try:
        config = load_config(Path(args.config))
        return 0
    except AppError as e:
        logger.error("Error: %s", e)
        return 2
    except Exception:
        logger.exception("Unexpected error")
        return 1
```

## pyproject.toml

```toml
[project]
name = "mypackage"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = ["pydantic>=2.0", "pyyaml>=6.0"]

[project.scripts]
mypackage = "mypackage.cli:main"

[tool.ruff]
target-version = "py310"
line-length = 100
src = ["src", "tests"]

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "UP", "SIM", "RUF"]

[tool.pytest.ini_options]
testpaths = ["tests"]
```

## CLAUDE.md

Every project should have a CLAUDE.md for AI-assisted development. Use the comprehensive template from the skill library:

```bash
cp ~/skill-library/templates/CLAUDE.md.template ./CLAUDE.md
```

The template covers: Critical Constraints (positioned first for attention priority), Architecture, Commands, Coding Conventions (DRY, naming, error handling, testing), Agent Behavior (scope discipline, when to ask), Security & Privacy (PII, input validation, secrets), and Quick Reference.

Key design principles applied in the template:
- **U-shaped attention**: Non-negotiable rules go first (Critical Constraints) and last (Quick Reference)
- **DRY as knowledge rule**: "DRY applies to knowledge, not code" -- avoid premature abstraction
- **Anti-patterns as behaviors**: Specific things Claude must NOT do, not vague traits
- **Scope discipline**: Only change what was asked, no drive-by refactors

## Definition of Done

- [ ] `pip install -e .` succeeds
- [ ] `python -m <package>` runs with clean logs
- [ ] `config.yaml` is validated at startup
- [ ] All public APIs are typed
- [ ] No `print()` in library code
- [ ] Tests pass (`pytest`)
- [ ] Exceptions caught and logged at CLI boundary
- [ ] Secrets in env vars, not config.yaml
- [ ] CLAUDE.md written

For detailed patterns (repository pattern, testing, tooling), see [reference.md](reference.md).
