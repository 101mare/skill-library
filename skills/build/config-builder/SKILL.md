---
name: config-builder
description: |
  Scaffolds Python configuration infrastructure: Pydantic models, YAML loading, environment variable overrides.
  Use when creating config systems, adding config fields, or migrating from hardcoded values to validated config.
  Recognizes: "config-builder", "add config", "pydantic config", "yaml config", "env vars",
  "configuration management", "validated settings", "config infrastructure"
---

# Config Builder

Scaffolds production-ready Python configuration with Pydantic validation, YAML files, and environment variable overrides.

## When to Use

- Setting up configuration for a new project
- Migrating hardcoded values to validated config
- Adding new config sections or fields
- Implementing environment variable overrides for Docker/CI

## Config Architecture

```
config.yaml          # User-editable defaults
  |
  v
YAML Loader          # yaml.safe_load()
  |
  v
Pydantic Models      # Validation, type coercion, defaults
  |
  v
Env Override          # MYAPP_SECTION__KEY=value
  |
  v
AppConfig            # Validated, typed, immutable config object
```

## Core Pattern: Pydantic Config Models

```python
# config/models.py
from pydantic import BaseModel, Field, field_validator
from pathlib import Path

class DatabaseConfig(BaseModel):
    host: str = Field(default="localhost")
    port: int = Field(ge=1, le=65535, default=5432)
    name: str = Field(min_length=1)
    pool_size: int = Field(ge=1, le=100, default=10)

class LoggingConfig(BaseModel):
    level: str = Field(default="INFO", pattern="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$")
    file: Path | None = Field(default=None)
    json_format: bool = Field(default=False)

class AppConfig(BaseModel):
    """Root config - mirrors config.yaml structure."""
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)

    @field_validator("database", mode="before")
    @classmethod
    def ensure_database(cls, v):
        return v or {}
```

## YAML Loader

```python
# config/loader.py
from pathlib import Path
import yaml
from .models import AppConfig

def load_config(path: Path = Path("config.yaml")) -> AppConfig:
    """Load config from YAML. Returns defaults if file missing."""
    if not path.exists():
        return AppConfig()

    with open(path) as f:
        raw = yaml.safe_load(f) or {}

    return AppConfig.model_validate(raw)
```

## Environment Variable Overrides

```python
# config/loader.py (extended)
import os

def apply_env_overrides(config: dict, prefix: str = "MYAPP") -> dict:
    """Override config values from environment variables.

    Convention: MYAPP_SECTION__KEY=value
    Example: MYAPP_DATABASE__HOST=postgres -> config["database"]["host"] = "postgres"
    """
    for key, value in os.environ.items():
        if not key.startswith(f"{prefix}_"):
            continue
        parts = key[len(prefix) + 1:].lower().split("__")
        target = config
        for part in parts[:-1]:
            target = target.setdefault(part, {})
        target[parts[-1]] = value
    return config

def load_config(path: Path = Path("config.yaml"), env_prefix: str = "MYAPP") -> AppConfig:
    if not path.exists():
        raw = {}
    else:
        with open(path) as f:
            raw = yaml.safe_load(f) or {}

    raw = apply_env_overrides(raw, env_prefix)
    return AppConfig.model_validate(raw)
```

## Nested Config with Discriminated Unions

```python
from pydantic import BaseModel, Field
from typing import Literal

class PostgresConfig(BaseModel):
    type: Literal["postgres"] = "postgres"
    host: str = "localhost"
    port: int = 5432

class SqliteConfig(BaseModel):
    type: Literal["sqlite"] = "sqlite"
    path: str = "app.db"

class AppConfig(BaseModel):
    database: PostgresConfig | SqliteConfig = Field(discriminator="type")
```

## Field Patterns

```python
class Config(BaseModel):
    # String with validation
    name: str = Field(min_length=1, max_length=100)

    # Enum-like string
    mode: str = Field(default="production", pattern="^(development|staging|production)$")

    # Numeric range
    timeout: int = Field(ge=1, le=3600, default=300)
    temperature: float = Field(ge=0.0, le=2.0, default=0.0)

    # Path (auto-converted from string)
    output_dir: Path = Field(default=Path("./output"))

    # Optional with default
    api_key: str | None = Field(default=None)

    # List with default factory
    tags: list[str] = Field(default_factory=list)
```

## Config Hierarchy

Priority (highest to lowest):
1. **CLI arguments** -- Explicit user override
2. **Environment variables** -- Deployment/Docker override
3. **config.yaml** -- User-editable defaults
4. **Pydantic defaults** -- Code-level fallbacks

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Hardcoded values | Can't change without code change | Add to config.yaml + Pydantic model |
| `os.getenv()` scattered | No validation, no defaults | Centralize in Pydantic model |
| Dict-based config | No type safety, no validation | Use Pydantic BaseModel |
| Config without validation | Runtime errors from typos | Pydantic validates at startup |
| Mutable config object | State bugs | Use `ConfigDict(frozen=True)` |

## Checklist

- [ ] All user-configurable values in config.yaml
- [ ] Pydantic model mirrors YAML structure
- [ ] Field validators for complex constraints
- [ ] Environment variable override support
- [ ] Config loaded once at startup, passed explicitly
- [ ] Invalid config crashes at startup, not runtime
- [ ] Secrets in env vars, never in config.yaml
- [ ] Default values for all optional fields

For detailed patterns (BaseSettings, secrets, migrations, testing), see [reference.md](reference.md).
