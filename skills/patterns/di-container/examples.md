# DI Container — Examples

Runnable Python examples beyond the basics in [SKILL.md](SKILL.md): multi-provider pipelines, CLI applications, and testing without a container.

## Table of Contents

- [Multi-Provider Pipeline](#multi-provider-pipeline)
- [CLI Container](#cli-container)
- [Testing Without Container](#testing-without-container)

---

## Multi-Provider Pipeline

Container wiring Fetcher, Transformer, and Loader behind Protocol interfaces. Changing a data source means changing one config field.

```python
from typing import Protocol
from dataclasses import dataclass

class Fetcher(Protocol):
    def fetch(self, source: str) -> list[dict]: ...

class Transformer(Protocol):
    def transform(self, records: list[dict]) -> list[dict]: ...

class Loader(Protocol):
    def load(self, records: list[dict]) -> int: ...

@dataclass
class PipelineConfig:
    source_type: str  # "api" or "csv"
    dest_type: str    # "jsonl"
    filter_nulls: bool = True

class ApiFetcher:
    def __init__(self, base_url: str) -> None:
        self._url = base_url
    def fetch(self, source: str) -> list[dict]:
        import urllib.request, json
        with urllib.request.urlopen(f"{self._url}/{source}") as r:
            return json.loads(r.read())

class CsvFetcher:
    def fetch(self, source: str) -> list[dict]:
        import csv
        with open(source) as f: return list(csv.DictReader(f))

class NullFilter:
    def transform(self, records: list[dict]) -> list[dict]:
        return [r for r in records if all(v is not None for v in r.values())]

class JsonlLoader:
    def __init__(self, path: str) -> None:
        self._path = path
    def load(self, records: list[dict]) -> int:
        import json
        with open(self._path, "w") as f:
            for r in records: f.write(json.dumps(r) + "\n")
        return len(records)

class PipelineContainer:
    def __init__(self, config: PipelineConfig) -> None:
        self._config = config

    @property
    def fetcher(self) -> Fetcher:
        match self._config.source_type:
            case "api":  return ApiFetcher("https://data.example.com")
            case "csv":  return CsvFetcher()
            case other:  raise ValueError(f"Unknown source: {other}")

    @property
    def transformer(self) -> Transformer:
        return NullFilter() if self._config.filter_nulls else (lambda r: r)  # type: ignore

    @property
    def loader(self) -> Loader:
        match self._config.dest_type:
            case "jsonl": return JsonlLoader("output.jsonl")
            case other:   raise ValueError(f"Unknown dest: {other}")

    def run(self, source: str) -> int:
        raw = self.fetcher.fetch(source)
        cleaned = self.transformer.transform(raw)
        return self.loader.load(cleaned)
```

---

## CLI Container

DI containers work outside web apps. Here a CLI tool uses a container for output formatting and reporting.

```python
from typing import Protocol
import sys

class Formatter(Protocol):
    def format(self, data: dict) -> str: ...

class Reporter(Protocol):
    def send(self, message: str) -> None: ...

class JsonFormatter:
    def format(self, data: dict) -> str:
        import json
        return json.dumps(data, indent=2)

class TableFormatter:
    def format(self, data: dict) -> str:
        return "\n".join(f"{k:<20} {v}" for k, v in data.items())

class StdoutReporter:
    def send(self, message: str) -> None: sys.stdout.write(message + "\n")

class FileReporter:
    def __init__(self, path: str) -> None:
        self._path = path
    def send(self, message: str) -> None:
        with open(self._path, "a") as f: f.write(message + "\n")

class CliContainer:
    def __init__(self, output_format: str = "table", report_to: str = "stdout") -> None:
        self._fmt = output_format
        self._dest = report_to

    @property
    def formatter(self) -> Formatter:
        match self._fmt:
            case "json":  return JsonFormatter()
            case "table": return TableFormatter()
            case other:   raise ValueError(f"Unknown format: {other}")

    @property
    def reporter(self) -> Reporter:
        if self._dest == "stdout":
            return StdoutReporter()
        return FileReporter(self._dest)

def main(argv: list[str] | None = None) -> None:
    import argparse
    parser = argparse.ArgumentParser(description="Status reporter")
    parser.add_argument("--format", choices=["json", "table"], default="table")
    parser.add_argument("--output", default="stdout")
    args = parser.parse_args(argv)

    container = CliContainer(output_format=args.format, report_to=args.output)
    data = {"service": "api-gateway", "status": "healthy", "uptime": "14d 3h"}
    container.reporter.send(container.formatter.format(data))
```

Protocols define interfaces, the container selects implementations from config, `main` is a thin orchestrator.

---

## Testing Without Container

Unit tests inject dependencies directly, bypassing the container entirely.

```python
from typing import Protocol

class Cache(Protocol):
    def get(self, key: str) -> str | None: ...
    def set(self, key: str, value: str) -> None: ...

class UserService:
    def __init__(self, cache: Cache) -> None:
        self._cache = cache

    def get_greeting(self, user_id: str) -> str:
        cached = self._cache.get(f"greeting:{user_id}")
        if cached:
            return cached
        greeting = f"Hello, {user_id}"
        self._cache.set(f"greeting:{user_id}", greeting)
        return greeting

# --- Tests: no container, no mocking library ---

class FakeCache:
    def __init__(self) -> None:
        self._store: dict[str, str] = {}
    def get(self, key: str) -> str | None: return self._store.get(key)
    def set(self, key: str, value: str) -> None: self._store[key] = value

def test_greeting_is_cached() -> None:
    cache = FakeCache()
    svc = UserService(cache=cache)
    assert svc.get_greeting("alice") == "Hello, alice"
    assert cache.get("greeting:alice") == "Hello, alice"

def test_cached_greeting_is_returned() -> None:
    cache = FakeCache()
    cache.set("greeting:bob", "Welcome back, bob")
    assert UserService(cache=cache).get_greeting("bob") == "Welcome back, bob"
```

`FakeCache` satisfies the `Cache` protocol without inheriting from it -- structural subtyping at work. Tests construct the service directly with the fake: no container, no mock library, no patching.
