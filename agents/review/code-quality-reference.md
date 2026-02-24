# Code Quality & Type Safety

### Type Hints

```python
# GOOD: Fully typed
def process_items(
    items: list[dict[str, Any]],
    limit: int | None = None
) -> tuple[list[str], int]:
    ...

# BAD: No types
def process_items(items, limit=None):
    ...
```

### Modern Type Patterns (Python 3.10+)

```python
# Union syntax
def get_value(key: str) -> str | None: ...

# Match statement type narrowing
match value:
    case str() as s:
        return s.upper()
    case int() as n:
        return str(n)
    case _:
        raise TypeError("Invalid type")
```

### Pydantic vs Dataclass

**Pydantic** -- External input validation:

```python
from pydantic import BaseModel, field_validator

class UserInput(BaseModel):
    email: str
    age: int

    @field_validator("age")
    @classmethod
    def validate_age(cls, v: int) -> int:
        if v < 0:
            raise ValueError("Age must be positive")
        return v
```

**Dataclass** -- Internal data structures:

```python
from dataclasses import dataclass, field

@dataclass(frozen=True, slots=True)
class Config:
    host: str
    port: int = 8080
    tags: list[str] = field(default_factory=list)
```

### Protocol (Structural Subtyping)

```python
from typing import Protocol

class Repository(Protocol):
    def get(self, id: int) -> Model | None: ...
    def save(self, item: Model) -> None: ...

# Any class with get/save methods satisfies Repository
# No inheritance required
```

### Error Handling Patterns

#### Specific Exceptions

```python
# GOOD: Specific, logged, cleaned up
try:
    with open(path) as f:
        data = json.load(f)
except FileNotFoundError:
    logger.warning(f"Config not found: {path}")
    data = default_config
except json.JSONDecodeError as e:
    logger.exception(f"Invalid JSON in {path}")
    raise ConfigError(f"Invalid config: {e}") from e

# BAD: Catches everything, silent
try:
    data = json.load(open(path))
except:
    data = {}
```

#### Custom Exception Hierarchy

```python
class ProcessingError(Exception):
    """Base exception for processing failures."""

class ValidationError(ProcessingError):
    """Input validation failed."""

class TimeoutError(ProcessingError):
    """Operation timed out."""
    def __init__(self, operation: str, timeout: float):
        super().__init__(f"{operation} timed out after {timeout}s")
        self.operation = operation
        self.timeout = timeout
```

### Pythonic Patterns

| Pattern | Good | Bad |
|---------|------|-----|
| Truthiness | `if items:` | `if len(items) > 0:` |
| Iteration | `for item in items:` | `for i in range(len(items)):` |
| Dict access | `d.get("key", default)` | `d["key"] if "key" in d` |
| Comprehension | `[x*2 for x in items]` | Loop + append |
| Context manager | `with open() as f:` | `f.close()` manual |
| Walrus operator | `if (n := len(x)) > 10:` | `n = len(x); if n > 10:` |

### Match Statements (Python 3.10+)

```python
# GOOD: Pattern matching
def process(value: str | int | list) -> str:
    match value:
        case str() as s:
            return s.upper()
        case int() as n if n > 0:
            return f"positive: {n}"
        case [first, *rest]:
            return f"list starting with {first}"
        case _:
            return "unknown"

# BAD: if/elif chains
def process(value):
    if isinstance(value, str):
        return value.upper()
    elif isinstance(value, int) and value > 0:
        return f"positive: {value}"
    ...
```

### Function Design

```python
# GOOD: Early return, clear flow
def process_user(user_id: int) -> User | None:
    if not user_id:
        return None

    user = db.get_user(user_id)
    if not user or not user.is_active:
        return None

    return user

# BAD: Deep nesting
def process_user(user_id):
    if user_id:
        user = db.get_user(user_id)
        if user:
            if user.is_active:
                return user
    return None
```

### Module Interface (__all__)

```python
# GOOD: Explicit public API
__all__ = ["UserService", "create_user", "UserError"]

class UserService: ...
class _InternalHelper: ...  # Private by convention

def create_user(): ...
def _validate(): ...  # Private
```

### Async Patterns

#### Concurrent vs Sequential

```python
# GOOD: Concurrent execution
async def fetch_all(urls: list[str]) -> list[Response]:
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_one(session, url) for url in urls]
        return await asyncio.gather(*tasks)

# BAD: Sequential in async (defeats purpose)
async def fetch_all(urls: list[str]) -> list[Response]:
    results = []
    for url in urls:
        results.append(await fetch_one(url))
    return results
```

#### Async Context Managers

```python
# GOOD: Proper cleanup
async with asyncio.timeout(30):
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)

# BAD: No cleanup, no timeout
session = aiohttp.ClientSession()
response = await session.get(url)
```

### Architecture

#### Module Organization

| Check | Good | Bad |
|-------|------|-----|
| Clear boundaries | Separate concerns | God modules |
| Dependency direction | Core <- adapters | Circular imports |
| Configuration | Centralized, validated | Scattered magic values |

#### Dependency Injection

```python
# GOOD: Injectable
class ReportGenerator:
    def __init__(self, llm_client: LLMClient, storage: Storage):
        self.llm = llm_client
        self.storage = storage

# BAD: Hard-coupled
class ReportGenerator:
    def __init__(self):
        self.llm = OllamaClient()  # Can't test/swap
```

### Performance

| Check | Good | Bad |
|-------|------|-----|
| Generator for large data | `yield item` | Return huge list |
| Avoid N+1 queries | Batch/join | Loop with query |
| Cache expensive ops | `@lru_cache` | Recompute |
| Use __slots__ | Memory optimization | Many instances |

```python
# GOOD: Memory-efficient with __slots__
@dataclass(slots=True)
class Point:
    x: float
    y: float

# Without slots: each instance has __dict__ overhead
```

---
