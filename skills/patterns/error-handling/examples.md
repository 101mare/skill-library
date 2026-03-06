# Error Handling — Examples

Runnable Python examples for error handling patterns. See [SKILL.md](SKILL.md) for layer strategy, retry logic, and anti-patterns.

## Table of Contents

- [3-Layer Exception Flow](#3-layer-exception-flow)
- [Custom Exception Hierarchy](#custom-exception-hierarchy)
- [Retry Safety](#retry-safety)

---

## 3-Layer Exception Flow

Each layer transforms errors into its own vocabulary so implementation details never leak through.

```python
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# --- Domain exceptions (shared vocabulary) ---
class AppError(Exception):
    def __init__(self, message: str, code: str = "UNKNOWN") -> None:
        super().__init__(message)
        self.code = code

class ResourceNotFound(AppError):
    def __init__(self, resource: str, identifier: str) -> None:
        super().__init__(f"{resource} '{identifier}' not found", code="NOT_FOUND")

class ServiceUnavailable(AppError):
    def __init__(self, service: str) -> None:
        super().__init__(f"{service} is unreachable", code="UNAVAILABLE")

# --- Infrastructure: catch external, translate to domain ---
class OrderRepository:
    _db: dict[str, dict] = {}

    def get(self, order_id: str) -> dict:
        try:
            return self._db[order_id]
        except ConnectionRefusedError as e:
            raise ServiceUnavailable("database") from e
        except KeyError:
            raise ResourceNotFound("order", order_id)

# --- Service: business rules, lets domain errors propagate ---
class OrderService:
    def __init__(self, repo: OrderRepository) -> None:
        self.repo = repo

    def get_order_summary(self, order_id: str) -> str:
        order = self.repo.get(order_id)  # ResourceNotFound propagates
        if order.get("cancelled"):
            raise AppError("Order was cancelled", code="ORDER_CANCELLED")
        return f"Order {order_id}: {order['total']}"

# --- API: catch all AppError, translate to response ---
ERROR_STATUS = {ResourceNotFound: 404, ServiceUnavailable: 503}

def handle_request(order_id: str) -> dict:
    try:
        service = OrderService(OrderRepository())
        return {"status": 200, "body": service.get_order_summary(order_id)}
    except AppError as e:
        status = ERROR_STATUS.get(type(e), 400)
        return {"status": status, "body": str(e), "code": e.code}
    except Exception:
        logger.exception("Unexpected error")
        return {"status": 500, "body": "Internal server error"}

print(handle_request("nonexistent"))
# {'status': 404, 'body': "order 'nonexistent' not found", 'code': 'NOT_FOUND'}
```

`ConnectionRefusedError` never reaches the service layer -- the repository translates it. The API layer maps `AppError` subtypes to HTTP status codes without knowing anything about databases.

---

## Custom Exception Hierarchy

Domain exceptions with error codes, context data, and user-facing messages. Separates what developers see (full details) from what users see (safe messages).

```python
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class ErrorContext:
    operation: str
    entity: str | None = None
    entity_id: str | None = None

class DomainError(Exception):
    code: str = "DOMAIN_ERROR"
    http_status: int = 400

    def __init__(self, message: str, ctx: ErrorContext | None = None) -> None:
        super().__init__(message)
        self.ctx = ctx or ErrorContext(operation="unknown")

    @property
    def user_message(self) -> str:
        return "Something went wrong. Please try again."

class NotFoundError(DomainError):
    code = "NOT_FOUND"
    http_status = 404

    @property
    def user_message(self) -> str:
        return f"{self.ctx.entity or 'Resource'} not found."

# --- Usage ---
def create_invoice(customer_id: str) -> None:
    ctx = ErrorContext("create_invoice", entity="Customer", entity_id=customer_id)
    raise NotFoundError(f"No customer row for id={customer_id}", ctx=ctx)

try:
    create_invoice("cust_42")
except DomainError as e:
    print(f"Developer: {e}")              # No customer row for id=cust_42
    print(f"User:      {e.user_message}") # Customer not found.
    print(f"Code:      {e.code}")         # NOT_FOUND
    print(f"HTTP:      {e.http_status}")  # 404
```

Error codes give clients a stable string to branch on; `user_message` is always safe for HTTP responses.

---

## Retry Safety

Retrying a non-idempotent operation can duplicate records or double-charge customers. This decorator enforces that only `@idempotent`-marked functions can be retried.

```python
from __future__ import annotations
import functools, time
from typing import Callable, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")

def idempotent(func: Callable[P, R]) -> Callable[P, R]:
    """Mark a function as safe to retry."""
    func._idempotent = True  # type: ignore[attr-defined]
    return func

def retry(
    max_attempts: int = 3,
    delay: float = 0.5,
    retryable: tuple[type[Exception], ...] = (ConnectionError, TimeoutError),
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        if not getattr(func, "_idempotent", False):
            raise TypeError(
                f"Cannot retry '{func.__name__}': not marked @idempotent."
            )
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            last_exc: Exception | None = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except retryable as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(delay * (2 ** (attempt - 1)))
            raise last_exc  # type: ignore[misc]
        return wrapper
    return decorator

# --- Safe: read is idempotent ---
_call_count = 0

@retry(max_attempts=3)
@idempotent
def fetch_user(user_id: str) -> dict:
    global _call_count
    _call_count += 1
    if _call_count < 2:
        raise ConnectionError("db timeout")
    return {"id": user_id, "name": "Alice"}

print(fetch_user("u_1"))  # Retries once, then succeeds

# --- Unsafe: payment is NOT idempotent ---
def charge_payment(amount: float) -> str:
    return f"charged ${amount}"

try:
    retry()(charge_payment)
except TypeError as e:
    print(f"Blocked: {e}")
    # Blocked: Cannot retry 'charge_payment': not marked @idempotent.
```

The `@retry` decorator enforces the safety contract at decoration time -- mistakes are caught before any code runs.
