---
name: strategy-registry
description: |
  Implements Strategy pattern with registry-based dispatch for extensible systems.
  Use when building plugin systems, file type handlers, or any dispatch-by-key pattern.
  Recognizes: "strategy-registry", "strategy pattern", "registry pattern", "dispatch",
  "plugin system", "handler registry", "extensible dispatch", "file type handler"
---

# Strategy + Registry Pattern

Extensible dispatch systems using Strategy pattern with registry-based lookup.

## When to Use

- Dispatch by key (file extension -> handler, event type -> processor)
- Plugin systems where new handlers can be added without modifying core code
- Format converters, file type processors, command handlers
- Any "switch on type" that should be open for extension

## Dict-Based Registry (Simplest)

```python
from typing import Protocol

class Extractor(Protocol):
    def extract(self, path: Path) -> str: ...

class PdfExtractor:
    def extract(self, path: Path) -> str:
        return extract_pdf_text(path)

class TextExtractor:
    def extract(self, path: Path) -> str:
        return path.read_text()

class ImageExtractor:
    def extract(self, path: Path) -> str:
        return run_ocr(path)

# Registry: maps keys to strategy instances
EXTRACTORS: dict[str, Extractor] = {
    ".pdf": PdfExtractor(),
    ".txt": TextExtractor(),
    ".md": TextExtractor(),
    ".png": ImageExtractor(),
    ".jpg": ImageExtractor(),
}

def extract(path: Path) -> str:
    ext = path.suffix.lower()
    extractor = EXTRACTORS.get(ext)
    if extractor is None:
        raise ValueError(f"Unsupported file type: {ext}")
    return extractor.extract(path)
```

## Decorator-Based Registry (Cleanest)

```python
from typing import Callable
from pathlib import Path

# Registry with decorator
_handlers: dict[str, Callable] = {}

def handles(*extensions: str):
    """Register a handler for file extensions."""
    def decorator(cls):
        for ext in extensions:
            _handlers[ext.lower()] = cls
        return cls
    return decorator

def get_handler(extension: str):
    cls = _handlers.get(extension.lower())
    if cls is None:
        raise ValueError(f"No handler for: {extension}")
    return cls()

# Registration via decorator
@handles(".pdf")
class PdfHandler:
    def process(self, path: Path) -> str:
        return extract_pdf(path)

@handles(".txt", ".md", ".csv")
class TextHandler:
    def process(self, path: Path) -> str:
        return path.read_text()

@handles(".png", ".jpg", ".jpeg")
class ImageHandler:
    def process(self, path: Path) -> str:
        return run_ocr(path)
```

## Protocol Interface for Strategies

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class FileHandler(Protocol):
    """All handlers must implement this interface."""
    def process(self, path: Path) -> str: ...
    def supports(self, path: Path) -> bool: ...

class Registry:
    def __init__(self):
        self._handlers: dict[str, FileHandler] = {}

    def register(self, extension: str, handler: FileHandler) -> None:
        if not isinstance(handler, FileHandler):
            raise TypeError(f"Handler must implement FileHandler protocol")
        self._handlers[extension.lower()] = handler

    def get(self, extension: str) -> FileHandler:
        handler = self._handlers.get(extension.lower())
        if handler is None:
            raise KeyError(f"No handler for: {extension}")
        return handler

    def extensions(self) -> list[str]:
        return list(self._handlers.keys())
```

## Auto-Discovery with __init_subclass__

```python
class BaseHandler:
    """Handlers auto-register when subclassed."""
    _registry: dict[str, type] = {}

    def __init_subclass__(cls, extensions: tuple[str, ...] = (), **kwargs):
        super().__init_subclass__(**kwargs)
        for ext in extensions:
            BaseHandler._registry[ext] = cls

    @classmethod
    def for_extension(cls, ext: str) -> "BaseHandler":
        handler_cls = cls._registry.get(ext)
        if handler_cls is None:
            raise ValueError(f"No handler for: {ext}")
        return handler_cls()

# Auto-registers on class definition
class PdfHandler(BaseHandler, extensions=(".pdf",)):
    def process(self, path: Path) -> str:
        return extract_pdf(path)

class TextHandler(BaseHandler, extensions=(".txt", ".md")):
    def process(self, path: Path) -> str:
        return path.read_text()

# Usage
handler = BaseHandler.for_extension(".pdf")
```

## Adding a Default/Fallback

```python
class Registry:
    def __init__(self, default: FileHandler | None = None):
        self._handlers: dict[str, FileHandler] = {}
        self._default = default

    def get(self, extension: str) -> FileHandler:
        handler = self._handlers.get(extension.lower())
        if handler is not None:
            return handler
        if self._default is not None:
            return self._default
        raise KeyError(f"No handler for: {extension}")
```

## Testing Strategies and Registries

```python
def test_registry_returns_correct_handler():
    registry = Registry()
    handler = MockHandler()
    registry.register(".pdf", handler)
    assert registry.get(".pdf") is handler

def test_registry_raises_for_unknown():
    registry = Registry()
    with pytest.raises(KeyError, match="No handler for"):
        registry.get(".xyz")

def test_handler_processes_file(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("hello")
    handler = TextHandler()
    assert handler.process(file) == "hello"

def test_decorator_registration():
    # Verify decorator registered the handler
    handler = get_handler(".pdf")
    assert isinstance(handler, PdfHandler)
```

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Giant if/elif chain | Hard to extend, violates OCP | Use registry dict |
| Missing default handler | Crashes on unknown input | Add fallback or raise clear error |
| Mutable global registry | Test pollution | Use instance-based registry or reset in tests |
| Handler with too many responsibilities | God handler | One handler per concern |
| Registering at import time with side effects | Import order matters | Use explicit registration or __init_subclass__ |

## Checklist

- [ ] Protocol defines the handler interface
- [ ] Registry maps keys to handlers
- [ ] Unknown keys raise clear error (or use default)
- [ ] New handlers can be added without modifying dispatch code
- [ ] Each handler has focused responsibility
- [ ] Tests cover: correct dispatch, unknown key, each handler
