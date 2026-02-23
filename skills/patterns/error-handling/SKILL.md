---
name: error-handling
description: |
  Patterns for exception handling across application layers: mapping, retry, severity, logging.
  Use when designing error strategies, implementing retry logic, or mapping exceptions between layers.
  Recognizes: "error-handling", "exception handling", "retry pattern", "error strategy",
  "exception mapping", "error boundaries", "backoff pattern", "error propagation"
---

# Error Handling Patterns

Exception handling strategies across application layers.

## Layer Strategy

Each layer has a specific error handling responsibility:

```
Infrastructure Layer    Service Layer          API/CLI Layer
(adapters, I/O)        (business logic)       (entry points)

Catch: external errors  Catch: infra errors    Catch: all AppError
Translate: to domain    Translate: to domain   Translate: to response
Propagate: domain exc   Propagate: up          Log: at boundary
Retry: transient        Retry: if idempotent   Return: status code
```

### Infrastructure: Catch and Translate

```python
class DatabaseAdapter:
    def get_user(self, user_id: str) -> User:
        try:
            row = self._conn.execute("SELECT ...", (user_id,))
        except psycopg2.OperationalError as e:
            raise ConnectionError("database", "unreachable") from e
        except psycopg2.IntegrityError as e:
            raise DataIntegrityError(str(e)) from e

        if row is None:
            raise ResourceNotFound("user", user_id)
        return User.from_row(row)
```

### Service: Business Logic Errors

```python
class UserService:
    def create_user(self, data: UserInput) -> User:
        if self.repo.exists(data.email):
            raise DuplicateError(f"User {data.email} already exists")

        try:
            user = User.from_input(data)
            self.repo.save(user)
            return user
        except ConnectionError:
            raise  # Let infra errors propagate
```

### CLI/API: Catch All, Log, Exit

```python
def main() -> int:
    try:
        config = load_config()
        run(config)
        return 0
    except ConfigError as e:
        logger.error("Configuration error: %s", e)
        return 2
    except AppError as e:
        logger.error("Error: %s", e)
        return 1
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        return 130
    except Exception:
        logger.exception("Unexpected error")
        return 3
```

## Exception Mapping at Boundaries

```python
# Map infrastructure exceptions to domain exceptions
EXCEPTION_MAP = {
    ConnectionRefusedError: lambda e: ConnectionError("service", str(e)),
    TimeoutError: lambda e: ServiceTimeoutError(str(e)),
    FileNotFoundError: lambda e: ResourceNotFound("file", str(e)),
}

def map_exception(exc: Exception) -> AppError:
    """Translate infrastructure exceptions to domain exceptions."""
    for exc_type, factory in EXCEPTION_MAP.items():
        if isinstance(exc, exc_type):
            return factory(exc)
    return AppError(f"Unexpected: {exc}")
```

## Retry with Exponential Backoff

```python
import time
import logging
from typing import TypeVar, Callable

logger = logging.getLogger(__name__)
T = TypeVar("T")

def retry_with_backoff(
    func: Callable[[], T],
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
    retryable: tuple[type[Exception], ...] = (ConnectionError, TimeoutError),
) -> T:
    """Retry with exponential backoff for transient failures."""
    for attempt in range(1, max_attempts + 1):
        try:
            return func()
        except retryable as e:
            if attempt == max_attempts:
                logger.error(
                    "All %d attempts failed: %s",
                    max_attempts, e,
                )
                raise
            delay = min(base_delay * (2 ** (attempt - 1)), max_delay)
            logger.warning(
                "Attempt %d/%d failed: %s. Retrying in %.1fs",
                attempt, max_attempts, e, delay,
            )
            time.sleep(delay)
    raise RuntimeError("Unreachable")  # Type checker satisfaction
```

Usage:
```python
result = retry_with_backoff(
    lambda: api_client.complete(prompt),
    max_attempts=4,
    retryable=(ConnectionError, TimeoutError),
)
```

## Severity Matrix

| Error Type | Retry? | Log Level | User Action |
|-----------|--------|-----------|-------------|
| Connection timeout | Yes | WARNING | Wait |
| Authentication failure | No | ERROR | Fix credentials |
| Invalid input | No | WARNING | Fix input |
| Resource not found | No | INFO | Check request |
| Rate limited | Yes (with backoff) | WARNING | Wait |
| Server error (500) | Yes | ERROR | Wait or escalate |
| Config invalid | No | CRITICAL | Fix config, restart |
| Out of memory | No | CRITICAL | Reduce load |

## Logging Exceptions Correctly

```python
# GOOD: logger.exception() includes full traceback
try:
    result = process(data)
except ProcessingError:
    logger.exception("Processing failed for item %s", item_id)
    raise

# GOOD: exc_info=True when not in except block
logger.error("Operation failed", exc_info=True)

# BAD: Loses traceback
except ProcessingError as e:
    logger.error(f"Failed: {e}")  # No traceback!

# BAD: Log then re-raise at same level (duplicate entries)
except ProcessingError:
    logger.error("Failed")  # Logged here...
    raise  # ...and logged again at the boundary
```

**Rule:** Log at the handling boundary only. If you re-raise, don't log (the catcher will log).

## Graceful Degradation

```python
def process_with_fallback(document: Document) -> Result:
    """Try primary method, fall back to simpler approach."""
    try:
        return full_processing(document)
    except ExternalServiceError:
        logger.warning("Full processing unavailable, using fallback")
        return basic_processing(document)
    except ProcessingError:
        logger.warning("Processing failed, returning partial result")
        return Result(status="partial", data=document.metadata)
```

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| `except Exception: pass` | Silent failures | Catch specific, log, handle |
| `except:` (bare) | Catches SystemExit, KeyboardInterrupt | Specify exception type |
| Exception as flow control | Slow, unclear intent | Use return values, Optional |
| Catch-log-reraise at every layer | Duplicate log entries | Log only at handling boundary |
| Retry non-idempotent operations | Data duplication | Only retry safe operations |
| Infinite retry | Hangs forever | Always set max_attempts |
| Generic error messages | Impossible to debug | Include context (IDs, types) |

## Checklist

- [ ] Each layer has clear error handling responsibility
- [ ] Infrastructure exceptions translated to domain exceptions
- [ ] `from e` on all exception chaining
- [ ] Retry only for transient, idempotent failures
- [ ] Exponential backoff with max delay
- [ ] Logging at handling boundary only (not at every re-raise)
- [ ] CLI/API catches AppError and translates to exit code/HTTP status
- [ ] No bare `except:` anywhere
