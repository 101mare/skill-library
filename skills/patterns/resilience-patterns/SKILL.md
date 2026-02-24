---
name: resilience-patterns
description: |
  Resilience patterns for Python: Retry with Backoff, Circuit Breaker, Timeout, Graceful Degradation.
  Use when building code that depends on external services (APIs, databases, model servers).
  Recognizes: "resilience-patterns", "retry", "backoff", "circuit breaker", "timeout",
  "graceful degradation", "fault tolerance", "service unavailable", "connection error",
  "handle failures", "make it resilient", "retry logic"
---

# Resilience Patterns

Patterns for building Python code that handles failures from external dependencies gracefully.

## When You Need Resilience

Any time your code depends on something that can fail independently:
- Model servers (Ollama, vLLM, external APIs)
- Databases
- File systems (network drives, Docker volumes)
- External services (HTTP APIs, message queues)

The question isn't IF these will fail, but WHEN and HOW your code handles it.

---

## Pattern 1: Retry with Exponential Backoff

The most common pattern. Retry a failing operation with increasing delays.

### Implementation

```python
import time
import logging
from functools import wraps
from typing import TypeVar, Callable

logger = logging.getLogger(__name__)
T = TypeVar("T")

def retry_with_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
    retryable_exceptions: tuple[type[Exception], ...] = (ConnectionError, TimeoutError),
) -> Callable:
    """Retry with exponential backoff. Only retries specified exceptions."""

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            last_exception: Exception | None = None

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except retryable_exceptions as e:
                    last_exception = e
                    if attempt == max_retries:
                        break

                    delay = min(base_delay * (2 ** attempt), max_delay)
                    logger.warning(
                        "Retry %d/%d after %.1fs",
                        attempt + 1,
                        max_retries,
                        delay,
                        extra={
                            "event": "retry",
                            "attempt": attempt + 1,
                            "delay_s": delay,
                            "error": str(e),
                        },
                    )
                    time.sleep(delay)

            raise last_exception  # type: ignore[misc]

        return wrapper
    return decorator
```

### Usage

```python
from interfaces.exceptions import ModelConnectionError, ModelTimeoutError

@retry_with_backoff(
    max_retries=3,
    base_delay=2.0,
    retryable_exceptions=(ModelConnectionError, ModelTimeoutError),
)
def call_llm(client: LlmClient, prompt: str) -> LlmResult:
    return client.complete(prompt)
```

### Key Rules

- **Only retry retryable errors** — ConnectionError yes, ValueError no
- **Exponential backoff** — don't hammer a struggling service
- **Cap the delay** — `max_delay` prevents absurd waits
- **Log every retry** — you need to know it's happening
- **Finite retries** — always give up eventually

---

## Pattern 2: Circuit Breaker

Stop calling a service that's clearly down. Fail fast instead of waiting for timeouts.

### States

```
     ┌──────────┐
     │  CLOSED  │──── failure_count >= threshold ────→ ┌──────┐
     │ (normal) │                                      │ OPEN │
     │          │←── success ─────────────────────────│      │
     └──────────┘                                      └──┬───┘
          ↑                                                │
          │                          timeout expired       │
          │                                                ▼
          │                                          ┌───────────┐
          └────────── success ──────────────────────│ HALF-OPEN │
                                                     │ (1 probe) │
                                                     └───────────┘
```

### Implementation

```python
import time
import threading
from enum import Enum

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    """Fail fast when a service is down."""

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 30.0,
        name: str = "default",
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.name = name
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._last_failure_time: float = 0
        self._lock = threading.Lock()

    @property
    def state(self) -> CircuitState:
        with self._lock:
            if self._state == CircuitState.OPEN:
                if time.monotonic() - self._last_failure_time >= self.recovery_timeout:
                    self._state = CircuitState.HALF_OPEN
            return self._state

    def call(self, func, *args, **kwargs):
        """Execute function through circuit breaker."""
        current_state = self.state

        if current_state == CircuitState.OPEN:
            raise CircuitOpenError(
                f"Circuit '{self.name}' is open. Service unavailable."
            )

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise

    def _on_success(self) -> None:
        with self._lock:
            self._failure_count = 0
            self._state = CircuitState.CLOSED

    def _on_failure(self) -> None:
        with self._lock:
            self._failure_count += 1
            self._last_failure_time = time.monotonic()
            if self._failure_count >= self.failure_threshold:
                self._state = CircuitState.OPEN
                logger.warning(
                    "Circuit '%s' opened after %d failures",
                    self.name,
                    self._failure_count,
                    extra={"event": "circuit_open", "circuit": self.name},
                )

class CircuitOpenError(Exception):
    """Raised when circuit breaker is open."""
```

### Usage

```python
llm_circuit = CircuitBreaker(
    failure_threshold=3,
    recovery_timeout=60.0,
    name="llm-provider",
)

def classify(text: str) -> CaseResult:
    result = llm_circuit.call(client.complete, prompt)
    return parse_result(result)
```

### When to Use

- Services with known downtime patterns (model servers restarting)
- High-latency failures (60s timeouts you'd rather skip)
- Cascading failure prevention (one service down shouldn't block everything)

---

## Pattern 3: Timeout Wrapper

Enforce maximum execution time for operations.

### Implementation

```python
import signal
from contextlib import contextmanager

class OperationTimeoutError(Exception):
    """Operation exceeded time limit."""

@contextmanager
def timeout(seconds: float, operation: str = "operation"):
    """Context manager that raises after `seconds`."""

    def _handler(signum, frame):
        raise OperationTimeoutError(
            f"{operation} timed out after {seconds}s"
        )

    old_handler = signal.signal(signal.SIGALRM, _handler)
    signal.alarm(int(seconds))
    try:
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old_handler)
```

### Usage

```python
with timeout(120, operation="LLM classification"):
    result = client.complete(prompt)
```

### Thread-Safe Alternative

`signal.alarm` only works in the main thread. For threaded code:

```python
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeout

def with_timeout(func, args=(), kwargs=None, timeout_s: float = 30.0):
    """Run function with timeout, thread-safe."""
    kwargs = kwargs or {}
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(func, *args, **kwargs)
        try:
            return future.result(timeout=timeout_s)
        except FuturesTimeout:
            raise OperationTimeoutError(
                f"Operation timed out after {timeout_s}s"
            )
```

---

## Pattern 4: Graceful Degradation

When a non-critical service fails, continue with reduced functionality instead of crashing.

### Implementation

```python
def process_case(case_dir: Path, container: Container) -> CaseResult:
    """Process a case. Degrades gracefully if OCR is unavailable."""
    text_files = extract_text_files(case_dir)

    # OCR is optional — degrade if unavailable
    ocr_files = []
    if container.vision_engine is not None:
        try:
            ocr_files = extract_with_ocr(case_dir, container.vision_engine)
        except VisionConnectionError:
            logger.warning(
                "OCR unavailable, continuing with text-only extraction",
                extra={"event": "ocr_degraded", "case": case_dir.name},
            )

    all_text = combine_extractions(text_files + ocr_files)

    result = container.classifier.classify(all_text)

    # Flag reduced confidence when degraded
    if not ocr_files and has_image_files(case_dir):
        result = result.with_reduced_confidence(
            reason="OCR unavailable, image files skipped"
        )

    return result
```

### Degradation Hierarchy

```
Full Service  ──→  Degraded Service  ──→  Cached Response  ──→  Default Value  ──→  Error
(preferred)        (partial results)      (stale data OK)      (safe fallback)     (last resort)
```

### Key Rules

- **Only degrade non-critical paths** — if classification fails, that IS the critical path
- **Log the degradation** — you need to know it happened
- **Flag degraded results** — `needs_review = True`, reduced confidence
- **Never silently degrade** — that's just a hidden bug

---

## Combining Patterns

Real-world code combines multiple patterns:

```python
# Circuit breaker around the LLM provider
llm_circuit = CircuitBreaker(failure_threshold=3, recovery_timeout=60.0, name="llm")

# Retry with backoff for transient failures
@retry_with_backoff(
    max_retries=2,
    base_delay=2.0,
    retryable_exceptions=(ModelConnectionError,),
)
def classify_with_resilience(client: LlmClient, prompt: str) -> LlmResult:
    """Classify with circuit breaker + retry."""
    return llm_circuit.call(client.complete, prompt)

# Graceful degradation at the pipeline level
def run_case(case_dir: Path, container: Container) -> CaseResult:
    try:
        return classify_with_resilience(container.llm_client, prompt)
    except CircuitOpenError:
        logger.error("LLM circuit open, cannot classify", extra={"case": case_dir.name})
        return CaseResult.unknown(case_dir.name, reason="LLM unavailable")
```

### Pattern Composition Order

```
Caller → Graceful Degradation → Circuit Breaker → Retry → Timeout → Actual Call
                                                                        ↓
                                                                   External Service
```

Timeout wraps the actual call. Retry wraps timeout. Circuit breaker wraps retry. Graceful degradation wraps circuit breaker.

---

## Testing Resilience

```python
def test_retry_succeeds_on_second_attempt(mock_client):
    """Should retry once and succeed."""
    mock_client.complete.side_effect = [
        ModelConnectionError("down"),
        LlmResult(text='{"ca_type": "KVW"}'),
    ]

    result = classify_with_retry(mock_client, "test prompt")

    assert result.text == '{"ca_type": "KVW"}'
    assert mock_client.complete.call_count == 2

def test_retry_gives_up_after_max_retries(mock_client):
    """Should raise after exhausting retries."""
    mock_client.complete.side_effect = ModelConnectionError("down")

    with pytest.raises(ModelConnectionError):
        classify_with_retry(mock_client, "test prompt")

    assert mock_client.complete.call_count == 4  # initial + 3 retries

def test_circuit_breaker_opens_after_threshold():
    """Circuit should open after N failures."""
    breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=60.0)
    failing_func = MagicMock(side_effect=ConnectionError("down"))

    for _ in range(3):
        with pytest.raises(ConnectionError):
            breaker.call(failing_func)

    assert breaker.state == CircuitState.OPEN

    with pytest.raises(CircuitOpenError):
        breaker.call(failing_func)  # fast fail, doesn't call func

def test_graceful_degradation_without_ocr(mock_container):
    """Should continue with text-only when OCR fails."""
    mock_container.vision_engine.extract.side_effect = VisionConnectionError("down")

    result = process_case(case_dir, mock_container)

    assert result.ca_type != ""  # still classified
    assert result.needs_review is True  # flagged for review
```

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|---|---|---|
| Retry all exceptions | Retries ValueErrors, logic bugs | Only retry transient/connection errors |
| No backoff (immediate retry) | Hammers struggling service | Exponential backoff with cap |
| Infinite retries | Never fails, hangs forever | Always set `max_retries` |
| Silent degradation | Bugs hidden as "degraded" mode | Log + flag degraded results |
| No circuit breaker on critical path | Every request waits for timeout | Add circuit breaker for known-flaky services |
| Retry inside retry | Exponential explosion of attempts | Retry at one layer only |
| Timeout longer than user patience | User gives up, retry continues | Timeout < user-facing SLA |

## Checklist

- [ ] Retry only transient errors (connection, timeout)
- [ ] Exponential backoff with max delay cap
- [ ] Finite retry count
- [ ] Every retry logged with attempt number and delay
- [ ] Circuit breaker on services with known downtime
- [ ] Timeouts on all external calls
- [ ] Graceful degradation for non-critical paths
- [ ] Degraded results flagged (needs_review, reduced confidence)
- [ ] Resilience patterns tested (success, failure, exhaustion)
- [ ] Patterns composed in correct order (timeout → retry → circuit → degradation)
