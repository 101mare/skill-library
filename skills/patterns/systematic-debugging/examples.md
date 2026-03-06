# Systematic Debugging — Examples

The 4-phase methodology applied to real bugs. See [SKILL.md](SKILL.md) for the framework reference.

## Table of Contents

- [Silent Classification Bug](#silent-classification-bug)
- [Flaky Test](#flaky-test)
- [Docker-Only Failure](#docker-only-failure)

---

## Silent Classification Bug

A text classifier returns `"general"` for inputs that should be `"urgent"`. No errors — just wrong answers.

**Reproduce:** Some urgent inputs work, others don't. The bug is input-dependent.

```python
clf = TextClassifier.load("models/v2")
clf.predict("CRITICAL: server CPU at 99%, requests timing out")  # "general" — wrong
clf.predict("disk full, writes failing")                         # "urgent" — correct
```

**Isolate:** Test systematically to find the pattern.

```python
test_cases = [
    ("disk full, writes failing", "urgent"),           # PASS
    ("CPU at 99%, requests timing out", "urgent"),     # FAIL → "general"
    ("memory usage 98.7% and climbing", "urgent"),     # FAIL → "general"
]
for text, expected in test_cases:
    actual = clf.predict(text)
    print(f"{'PASS' if actual == expected else 'FAIL'}: '{text[:40]}'")
```

Pattern: inputs containing **numbers** (99%, 98.7%) get misclassified.

**Root-Cause — 5 Whys:**

```
Why 1: predict() returns "general" for "CPU at 99%"
Why 2: The feature vector has near-zero values for numeric tokens
Why 3: normalize_token() clips all numbers to 1.0
Why 5: min(max(float("99"), 0.0), 1.0) → 1.0, same as float("1")
       ← ROOT CAUSE: clipping destroys numeric magnitude
```

**Fix + Defend:**

```python
import math

def normalize_token(token: str) -> float:
    try:
        value = float(token)
        return 1 / (1 + math.exp(-value / 20))  # sigmoid preserves magnitude
    except ValueError:
        return hash(token) % 1000 / 1000

def test_normalize_token_preserves_numeric_magnitude():
    assert normalize_token("1") != normalize_token("99")
    assert 0.0 <= normalize_token("99") <= 1.0

def test_regression_numeric_inputs_classified_correctly():
    clf = TextClassifier.load("models/v2")
    assert clf.predict("CPU at 99%, requests timing out") == "urgent"
```

---

## Flaky Test

A test passes locally but fails in CI ~30% of the time.

**Reproduce:**

```python
import asyncio
from event_bus import EventBus

async def test_event_delivery():
    bus = EventBus()
    received = []
    async def handler(event):
        await asyncio.sleep(0.01)
        received.append(event)
    bus.subscribe("alert", handler)
    await bus.publish("alert", {"msg": "test"})
    assert len(received) == 1  # FAILS intermittently
```

**Isolate:** Exaggerate the delay to reproduce locally.

```python
async def handler(event):
    await asyncio.sleep(0.5)  # now fails locally too — confirmed timing issue
    received.append(event)
```

**Root-Cause:** `publish()` fires handlers as background tasks and returns immediately.

```python
class EventBus:
    async def publish(self, channel: str, event: dict):
        for handler in self._subscribers.get(channel, []):
            asyncio.create_task(handler(event))  # fire-and-forget!
```

**Fix + Defend:** Wait for handler completion with a timeout.

```python
async def test_event_delivery():
    bus = EventBus()
    received = []
    done = asyncio.Event()
    async def handler(event):
        await asyncio.sleep(0.01)
        received.append(event)
        done.set()
    bus.subscribe("alert", handler)
    await bus.publish("alert", {"msg": "test"})
    await asyncio.wait_for(done.wait(), timeout=2.0)
    assert len(received) == 1
```

---

## Docker-Only Failure

App works locally, crashes in Docker: `FileNotFoundError: config/defaults.yaml`.

**Reproduce:**

```bash
python -m myapp serve                              # OK locally
docker build -t myapp . && docker run myapp        # FileNotFoundError
```

**Isolate:** The crash comes from a relative path in `load_config()`.

```python
def load_config():
    config_path = Path("config/defaults.yaml")  # relative to cwd
    with open(config_path) as f:
        return yaml.safe_load(f)
```

**Root-Cause:** The entry point calls `os.chdir()`, shifting the working directory.

```python
# src/__main__.py
os.chdir(os.path.dirname(__file__))  # cwd becomes /app/src/
# "config/defaults.yaml" now resolves to /app/src/config/defaults.yaml — doesn't exist
```

Locally, `os.chdir` stays within the project tree so relative paths still work. In Docker with a different directory layout, they break.

**Fix + Defend:** Anchor paths to the package location.

```python
_PACKAGE_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _PACKAGE_DIR.parent

def load_config():
    config_path = _PROJECT_ROOT / "config" / "defaults.yaml"
    with open(config_path) as f:
        return yaml.safe_load(f)

def test_load_config_independent_of_cwd(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)  # simulate different cwd
    config = load_config()
    assert "database" in config
```
