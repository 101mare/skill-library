# Project Scaffold Reference

## Repository Pattern

Abstract data access for testability:

```python
from typing import Protocol

class DocumentRepository(Protocol):
    def get(self, id: str) -> Document | None: ...
    def save(self, doc: Document) -> None: ...
    def list_all(self) -> list[Document]: ...

# Concrete implementation
class FileDocumentRepository:
    def __init__(self, base_path: Path):
        self.base_path = base_path

    def get(self, id: str) -> Document | None:
        path = self.base_path / f"{id}.json"
        if not path.exists():
            return None
        return Document(**json.loads(path.read_text()))
```

Benefits:
- Swap implementations (file -> database) without changing services
- Easy mocking in tests

## Testing Patterns

### conftest.py

```python
import pytest
from pathlib import Path
from unittest.mock import Mock

@pytest.fixture
def temp_config(tmp_path: Path) -> Path:
    config = tmp_path / "config.yaml"
    config.write_text("model:\n  name: test-model")
    return config

@pytest.fixture
def mock_repository() -> Mock:
    repo = Mock(spec=DocumentRepository)
    repo.get.return_value = Document(id="1", content="test", metadata={})
    return repo
```

### Test Structure

```python
def test_process_document_success(mock_repository):
    service = DocumentService(repository=mock_repository)
    result = service.process("doc-1")
    assert result.status == "completed"
    mock_repository.get.assert_called_once_with("doc-1")

def test_process_document_not_found(mock_repository):
    mock_repository.get.return_value = None
    service = DocumentService(repository=mock_repository)
    with pytest.raises(ProcessingError, match="not found"):
        service.process("missing")
```

### Smoke Test

```python
def test_app_starts():
    """Verify basic startup without errors."""
    from mypackage.config.loader import load_config
    config = load_config()
    assert config is not None
```

## Tooling

### Pre-commit (optional)

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

### Makefile (optional)

```makefile
.PHONY: test lint format

test:
    pytest -q --tb=line

lint:
    ruff check src/ tests/

format:
    ruff format src/ tests/

check: lint test
```

## Environment Variable Pattern for Secrets

```python
import os

class SecretsConfig(BaseModel):
    api_key: str | None = Field(default=None)

    @classmethod
    def from_env(cls) -> "SecretsConfig":
        return cls(api_key=os.getenv("API_KEY"))
```

## .gitignore Template

```
# Python
__pycache__/
*.pyc
*.pyo
*.egg-info/
dist/
build/
.venv/

# IDE
.idea/
.vscode/
*.swp

# Config
.env
*.local.yaml

# Output
logs/
output/

# OS
.DS_Store
Thumbs.db
```
