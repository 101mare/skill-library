---
name: protocol-design
description: |
  Guides proper use of Python typing.Protocol for structural subtyping and interface design.
  Use when defining contracts between modules, creating testable interfaces, or choosing between Protocol and ABC.
  Recognizes: "protocol-design", "typing.Protocol", "structural subtyping", "interface design",
  "Protocol vs ABC", "duck typing", "mock with spec", "protocol pattern"
---

# Protocol Design

Python `typing.Protocol` for structural subtyping -- interfaces without inheritance.

## Protocol vs ABC

| Aspect | Protocol | ABC |
|--------|----------|-----|
| Inheritance required | No | Yes (`class Foo(MyABC)`) |
| Structural subtyping | Yes (duck typing) | No |
| Runtime checking | Optional (`@runtime_checkable`) | Always (`isinstance()`) |
| Best for | Interfaces between modules | Shared implementation |
| Testing | `Mock(spec=Protocol)` | Must subclass |

**Rule of thumb:** Use Protocol when you care about *what methods exist*. Use ABC when you want to *share implementation*.

## Defining Protocols

### Basic Protocol

```python
from typing import Protocol

class Repository(Protocol):
    def get(self, id: str) -> Model | None: ...
    def save(self, item: Model) -> None: ...
```

Any class with matching `get` and `save` methods satisfies this -- no inheritance needed.

### Protocol with Properties

```python
class Configurable(Protocol):
    @property
    def name(self) -> str: ...

    @property
    def is_ready(self) -> bool: ...
```

### Protocol with Class Methods

```python
class Factory(Protocol):
    @classmethod
    def create(cls, config: dict) -> "Factory": ...
```

### Protocol with Default Implementation

```python
class Logger(Protocol):
    def log(self, message: str) -> None: ...

    def log_error(self, message: str) -> None:
        """Default implementation -- can be overridden."""
        self.log(f"ERROR: {message}")
```

## runtime_checkable

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Closeable(Protocol):
    def close(self) -> None: ...

# Now isinstance() works:
if isinstance(resource, Closeable):
    resource.close()
```

**Limitations of runtime_checkable:**
- Only checks method **names**, not signatures
- Cannot check return types at runtime
- Use sparingly -- type checkers are more reliable

## Using Mock(spec=Protocol)

```python
from unittest.mock import Mock

class LlmClient(Protocol):
    def complete(self, prompt: str) -> str: ...
    def embed(self, text: str) -> list[float]: ...

# Mock respects the Protocol interface
mock_client = Mock(spec=LlmClient)
mock_client.complete.return_value = "response"

# This would raise AttributeError (not in Protocol):
# mock_client.nonexistent_method()
```

## Protocol Composition

```python
class Readable(Protocol):
    def read(self, n: int = -1) -> bytes: ...

class Writable(Protocol):
    def write(self, data: bytes) -> int: ...

class ReadWrite(Readable, Writable, Protocol):
    """Combines both protocols."""
    ...

# Or use Union for "one of":
def process(source: Readable | Writable) -> None: ...
```

## Generic Protocols

```python
from typing import Protocol, TypeVar

T = TypeVar("T")

class Repository(Protocol[T]):
    def get(self, id: str) -> T | None: ...
    def save(self, item: T) -> None: ...
    def list_all(self) -> list[T]: ...

# Usage in type hints:
def process_users(repo: Repository[User]) -> None:
    users = repo.list_all()
    ...
```

## Practical Patterns

### Provider Abstraction

```python
class ModelProvider(Protocol):
    """Abstract over different ML model backends."""
    def startup(self) -> None: ...
    def shutdown(self) -> None: ...
    @property
    def llm_client(self) -> LlmClient: ...
    @property
    def vision_engine(self) -> VisionEngine | None: ...
```

### Service Interface

```python
class NotificationService(Protocol):
    def send(self, recipient: str, message: str) -> bool: ...

# Implementations satisfy without inheriting:
class EmailNotifier:
    def send(self, recipient: str, message: str) -> bool:
        return send_email(recipient, message)

class SlackNotifier:
    def send(self, recipient: str, message: str) -> bool:
        return post_to_slack(recipient, message)
```

### Callback Protocol

```python
from typing import Protocol

class ProgressCallback(Protocol):
    def __call__(self, current: int, total: int) -> None: ...

def process(data: list, on_progress: ProgressCallback | None = None) -> None:
    for i, item in enumerate(data):
        handle(item)
        if on_progress:
            on_progress(i + 1, len(data))
```

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Protocol for 1 implementation | Over-abstraction | Just use the class directly |
| Too many methods in Protocol | God interface | Split into focused Protocols |
| runtime_checkable everywhere | Performance cost, false confidence | Use type checker instead |
| Protocol with state | Protocols define behavior, not state | Use ABC if shared state needed |
| Importing concrete types | Defeats the purpose | Import only the Protocol |

## Checklist

- [ ] Protocol defined for each cross-module interface
- [ ] Methods have complete type hints
- [ ] `runtime_checkable` only where `isinstance` is truly needed
- [ ] Tests use `Mock(spec=Protocol)` for type safety
- [ ] Services accept Protocols in __init__, not concrete types
- [ ] No Protocol with only 1 method (consider Callable)
- [ ] Protocols live in an `interfaces/` module or alongside consumers
