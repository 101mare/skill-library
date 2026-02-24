---
name: exception-builder
description: |
  Designs Python exception hierarchies for layered applications.
  Covers base exceptions, layer mapping, chaining, and handler patterns.
  Use when creating exception systems, adding error handling, or designing error boundaries.
  Recognizes: "exception-builder", "exception hierarchy", "custom exceptions",
  "error classes", "design exceptions", "exception mapping", "error types"
---

# Exception Builder

Designs production-ready Python exception hierarchies for layered applications.

## When to Use

- Starting a new project and designing error handling
- Adding a new module that needs its own exceptions
- Mapping external errors to domain errors
- Designing error boundaries between layers

## Base Exception Pattern

```python
# exceptions.py
class AppError(Exception):
    """Base for all expected application errors."""

class ConfigError(AppError):
    """Invalid configuration. Non-recoverable."""

class ProcessingError(AppError):
    """Processing failed. May be retryable."""

class ExternalServiceError(AppError):
    """External dependency failure. Usually retryable."""
    def __init__(self, service: str, message: str):
        super().__init__(f"{service}: {message}")
        self.service = service
```

## Layer-Specific Exception Design

```
Infrastructure Layer     Domain/Service Layer     API/CLI Layer
-------------------     --------------------     -------------
ConnectionError    -->  ExternalServiceError -->  HTTP 503
TimeoutError       -->  ExternalServiceError -->  HTTP 504
FileNotFoundError  -->  ResourceNotFound     -->  HTTP 404
json.JSONDecodeError -> ProcessingError      -->  HTTP 422
```

### Infrastructure -> Domain Mapping

```python
# adapters/database.py
from app.exceptions import ExternalServiceError

class DatabaseAdapter:
    def get_user(self, user_id: str) -> User:
        try:
            return self._connection.query(User, user_id)
        except psycopg2.OperationalError as e:
            raise ExternalServiceError("database", "connection failed") from e
        except psycopg2.IntegrityError as e:
            raise ProcessingError(f"data integrity violation: {e}") from e
```

### Domain -> API Mapping

```python
# api/handlers.py
from app.exceptions import AppError, ResourceNotFound, ProcessingError

@app.exception_handler(ResourceNotFound)
def handle_not_found(exc: ResourceNotFound):
    return JSONResponse(status_code=404, content={"error": str(exc)})

@app.exception_handler(ProcessingError)
def handle_processing(exc: ProcessingError):
    return JSONResponse(status_code=422, content={"error": str(exc)})

@app.exception_handler(AppError)
def handle_app_error(exc: AppError):
    return JSONResponse(status_code=500, content={"error": "Internal error"})
```

## Exception Chaining

Always use `from e` to preserve the cause chain:

```python
# GOOD: Preserves original traceback
try:
    response = api.call()
except ConnectionError as e:
    raise ExternalServiceError("api", "unreachable") from e

# BAD: Loses original cause
try:
    response = api.call()
except ConnectionError:
    raise ExternalServiceError("api", "unreachable")  # Original traceback lost
```

## When Custom vs Stdlib

| Use Custom When | Use Stdlib When |
|----------------|-----------------|
| Caller needs to distinguish error types | Error is truly generic (ValueError for bad input) |
| You need extra data on the exception | No additional context needed |
| Crossing a layer boundary | Within a single function |
| Error represents a domain concept | Error represents a programming mistake |

```python
# Custom: Domain concept
class ModelNotFoundError(AppError):
    """Requested model not available on server."""
    def __init__(self, model: str):
        super().__init__(f"Model '{model}' not found")
        self.model = model

# Stdlib: Programming mistake
raise ValueError("age must be positive")  # Caller bug, not domain error
```

## Handler Patterns per Layer

### Service Layer: Catch, translate, propagate

```python
class UserService:
    def create_user(self, data: UserInput) -> User:
        try:
            return self.repo.save(User.from_input(data))
        except IntegrityError as e:
            raise DuplicateUserError(data.email) from e
        # Let other exceptions propagate unchanged
```

### CLI Layer: Catch all AppError, log, exit code

```python
def main() -> int:
    try:
        config = load_config()
        run_pipeline(config)
        return 0
    except ConfigError as e:
        logger.error("Configuration error: %s", e)
        return 2
    except AppError as e:
        logger.error("Error: %s", e)
        return 1
    except Exception:
        logger.exception("Unexpected error")
        return 3
```

### API Layer: Exception handlers per type

```python
# Map exceptions to HTTP status codes
EXCEPTION_STATUS_MAP = {
    ConfigError: 500,
    ResourceNotFound: 404,
    ProcessingError: 422,
    ExternalServiceError: 503,
}
```

## Exception Hierarchy Template

For a new project, start with this hierarchy:

```python
class AppError(Exception):
    """Base. All expected errors inherit from this."""

# Configuration
class ConfigError(AppError):
    """Invalid config. Crash at startup."""

# Resources
class ResourceNotFound(AppError):
    """Requested resource doesn't exist."""

# Processing
class ProcessingError(AppError):
    """Processing logic failed."""

class ValidationError(ProcessingError):
    """Input validation failed."""

# External
class ExternalServiceError(AppError):
    """External dependency failure."""
    def __init__(self, service: str, message: str):
        super().__init__(f"{service}: {message}")
        self.service = service

class ConnectionError(ExternalServiceError):
    """Cannot connect to external service."""

class TimeoutError(ExternalServiceError):
    """External service timed out."""
```

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| `except Exception: pass` | Silent failures, impossible to debug | Catch specific, log, re-raise or handle |
| `except:` (bare) | Catches SystemExit, KeyboardInterrupt | Always specify exception type |
| Exception as flow control | Slow, unclear intent | Use return values or Optional |
| Too deep hierarchy | Hard to choose correct type | Keep flat, max 2 levels deep |
| String-only errors | Can't catch by type | Create custom exception class |
| Logging then re-raising same | Duplicate log entries | Log at the handling boundary only |

## Checklist

- [ ] Single base exception for the application
- [ ] Layer boundaries translate exceptions
- [ ] `from e` on all exception chaining
- [ ] CLI/API catches AppError, logs, returns code/status
- [ ] No bare `except:` anywhere
- [ ] Exception hierarchy max 2 levels deep
- [ ] Custom exceptions carry relevant data attributes
