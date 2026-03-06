# Resilience Patterns — Examples

Composing resilience patterns into real systems. See [SKILL.md](SKILL.md) for individual pattern implementations.

## Table of Contents

- [Resilient LLM Client](#resilient-llm-client)
- [Degrading Pipeline](#degrading-pipeline)
- [Resilience Testing](#resilience-testing)

---

## Resilient LLM Client

Individual patterns are building blocks. Real code composes them in layers: timeout wraps the call, retry wraps timeout, circuit breaker wraps retry, and fallback wraps everything.

```python
import time
import logging
from dataclasses import dataclass
from typing import Callable
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeout

logger = logging.getLogger(__name__)

@dataclass
class LlmResponse:
    text: str
    model: str
    degraded: bool = False

class ResilientLlmClient:
    """LLM client composing timeout + retry + circuit breaker + fallback."""

    def __init__(self, primary: Callable, fallback: Callable | None = None,
                 timeout_s: float = 30.0, max_retries: int = 2,
                 circuit_threshold: int = 3, circuit_recovery_s: float = 60.0):
        self.primary = primary
        self.fallback = fallback
        self.timeout_s = timeout_s
        self.max_retries = max_retries
        self._fail_count = 0
        self._threshold = circuit_threshold
        self._recovery_s = circuit_recovery_s
        self._opened_at: float | None = None

    def complete(self, prompt: str) -> LlmResponse:
        if self._circuit_open():
            return self._use_fallback(prompt)

        last_err: Exception | None = None
        for attempt in range(self.max_retries + 1):
            try:
                with ThreadPoolExecutor(1) as pool:
                    result = pool.submit(self.primary, prompt).result(timeout=self.timeout_s)
                self._fail_count = 0
                self._opened_at = None
                return LlmResponse(text=result, model="primary")
            except (ConnectionError, TimeoutError, FuturesTimeout) as e:
                last_err = e
                self._fail_count += 1
                if self._fail_count >= self._threshold:
                    self._opened_at = time.monotonic()
                if attempt < self.max_retries:
                    time.sleep(min(2.0 * (2 ** attempt), 16.0))

        logger.error("Primary exhausted: %s", last_err)
        return self._use_fallback(prompt)

    def _circuit_open(self) -> bool:
        if self._opened_at is None:
            return False
        if time.monotonic() - self._opened_at >= self._recovery_s:
            self._opened_at = None
            return False
        return True

    def _use_fallback(self, prompt: str) -> LlmResponse:
        if self.fallback is None:
            raise ConnectionError("Primary failed, no fallback configured")
        return LlmResponse(text=self.fallback(prompt), model="fallback", degraded=True)
```

Composition order matters: timeout is innermost (bounds each attempt), retry wraps timeout, circuit breaker short-circuits when the service is down, and fallback is the last resort.

---

## Degrading Pipeline

A data pipeline that continues with partial data when non-critical enrichment stages fail.

```python
import logging
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

@dataclass
class Record:
    id: str
    raw_text: str
    language: str | None = None
    sentiment: float | None = None
    entities: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

def run_pipeline(record: Record, lang_api, ner_api, sentiment_api) -> Record:
    """Process record with graceful degradation on non-critical stages."""
    optional_stages = [
        ("language", lambda r: setattr(r, "language", lang_api.detect(r.raw_text)), "en"),
        ("entities", lambda r: setattr(r, "entities", ner_api.extract(r.raw_text)), []),
    ]
    for name, stage_fn, default in optional_stages:
        try:
            stage_fn(record)
        except Exception as e:
            logger.warning("Stage '%s' degraded: %s", name, e)
            setattr(record, name, default)
            record.warnings.append(f"{name} unavailable")

    # Critical stage — must succeed
    record.sentiment = sentiment_api.predict(record.raw_text)
    return record
```

The design separates critical from non-critical stages explicitly. Each optional stage declares its own default, and the `warnings` list lets downstream consumers know which enrichments are missing.

---

## Resilience Testing

Test resilience by injecting failures at each layer and verifying correct responses.

```python
from unittest.mock import MagicMock
import pytest

def test_fallback_after_retries_exhausted():
    primary = MagicMock(side_effect=ConnectionError("down"))
    fallback = MagicMock(return_value="cached answer")
    client = ResilientLlmClient(primary=primary, fallback=fallback, max_retries=1)

    result = client.complete("prompt")

    assert result.model == "fallback"
    assert result.degraded is True
    assert primary.call_count == 2  # initial + 1 retry

def test_circuit_skips_primary():
    primary = MagicMock(side_effect=ConnectionError("down"))
    fallback = MagicMock(return_value="safe")
    client = ResilientLlmClient(primary=primary, fallback=fallback,
                                max_retries=0, circuit_threshold=2)
    client.complete("a")
    client.complete("b")  # trips circuit
    primary.reset_mock()

    result = client.complete("c")  # should skip primary
    primary.assert_not_called()
    assert result.degraded is True

def test_pipeline_applies_defaults_on_failure():
    record = Record(id="1", raw_text="Hello world")
    lang_api = MagicMock()
    lang_api.detect.side_effect = ConnectionError("down")
    ner_api = MagicMock()
    ner_api.extract.return_value = ["World"]
    sentiment_api = MagicMock()
    sentiment_api.predict.return_value = 0.9

    result = run_pipeline(record, lang_api, ner_api, sentiment_api)

    assert result.language == "en"  # default applied
    assert result.entities == ["World"]  # succeeded
    assert result.sentiment == 0.9
    assert "language unavailable" in result.warnings
```

Each test targets one resilience boundary. Mock at the boundary and verify each layer independently — avoid testing resilience logic through integration tests.
