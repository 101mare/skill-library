# Config Builder Reference

## Pydantic BaseSettings Integration

For projects that prefer env-var-first configuration:

```python
from pydantic_settings import BaseSettings

class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="MYAPP_",
        env_nested_delimiter="__",
    )

    database_host: str = "localhost"
    database_port: int = 5432
    debug: bool = False
```

## Secret Management

```python
# Secrets separate from config
class SecretsConfig(BaseModel):
    api_key: str | None = Field(default=None)
    db_password: str | None = Field(default=None)

    @classmethod
    def from_env(cls) -> "SecretsConfig":
        return cls(
            api_key=os.getenv("API_KEY"),
            db_password=os.getenv("DB_PASSWORD"),
        )
```

Rules:
- Secrets NEVER in config.yaml or committed files
- Always load from environment or secret stores
- Validate presence at startup if required

## Config Migration Patterns

### Adding a field (non-breaking)
```python
class NewConfig(BaseModel):
    existing_field: str
    new_field: int = Field(default=42)  # Default = backwards compatible
```

### Removing a field
```python
class Config(BaseModel):
    # 1. Deprecate: make optional with default
    old_field: str | None = Field(default=None, deprecated=True)
    # 2. Next release: remove entirely
```

### Renaming a field
```python
class Config(BaseModel):
    new_name: str = Field(default="value")

    @model_validator(mode="before")
    @classmethod
    def migrate_old_names(cls, data):
        if "old_name" in data and "new_name" not in data:
            data["new_name"] = data.pop("old_name")
        return data
```

## Multi-Environment Config

```yaml
# config.yaml (defaults/development)
database:
  host: localhost
  port: 5432

# Override in production via env vars:
# MYAPP_DATABASE__HOST=prod-db.internal
# MYAPP_DATABASE__PORT=5432
```

Or separate files:
```python
def load_config(env: str = "development") -> AppConfig:
    base = load_yaml("config.yaml")
    override = load_yaml(f"config.{env}.yaml")
    merged = deep_merge(base, override)
    return AppConfig.model_validate(merged)
```

## Testing Config

```python
@pytest.fixture
def test_config(tmp_path: Path) -> AppConfig:
    config_file = tmp_path / "config.yaml"
    config_file.write_text("database:\n  host: testdb\n  name: test")
    return load_config(config_file)

@pytest.fixture
def minimal_config() -> AppConfig:
    return AppConfig(database=DatabaseConfig(name="test"))

def test_env_override(monkeypatch):
    monkeypatch.setenv("MYAPP_DATABASE__HOST", "override-host")
    config = load_config()
    assert config.database.host == "override-host"
```

## Docker Compose Env Patterns

```yaml
# docker-compose.yml
services:
  app:
    environment:
      - MYAPP_DATABASE__HOST=postgres
      - MYAPP_DATABASE__PORT=5432
      - MYAPP_LOGGING__LEVEL=WARNING
    env_file:
      - .env  # For secrets only
```

```bash
# .env (not committed)
DB_PASSWORD=secret123
API_KEY=sk-...
```
