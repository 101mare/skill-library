# Strategy Registry — Examples

Real dispatch scenarios showing registry patterns in context. See [SKILL.md](SKILL.md) for core implementations (dict-based, decorator-based, auto-discovery).

## Table of Contents

- [Document Extractor Registry](#document-extractor-registry)
- [Auto-Discovery Commands](#auto-discovery-commands)
- [Config-Driven Strategy](#config-driven-strategy)

---

## Document Extractor Registry

A file processor that auto-detects extractors by extension, falling back to MIME type when extensions are unreliable.

```python
import mimetypes
from pathlib import Path
from typing import Protocol

class Extractor(Protocol):
    def extract(self, path: Path) -> str: ...
    def supported_mimes(self) -> set[str]: ...

_ext_registry: dict[str, type] = {}
_mime_registry: dict[str, type] = {}

def extractor(*extensions: str):
    """Register extractor by file extension and MIME type."""
    def decorator(cls):
        for ext in extensions:
            _ext_registry[ext.lower()] = cls
        for mime in cls().supported_mimes():
            _mime_registry[mime] = cls
        return cls
    return decorator

@extractor(".pdf")
class PdfExtractor:
    def extract(self, path: Path) -> str:
        import subprocess
        return subprocess.run(
            ["pdftotext", str(path), "-"], capture_output=True, text=True, check=True,
        ).stdout

    def supported_mimes(self) -> set[str]:
        return {"application/pdf"}

@extractor(".csv")
class CsvExtractor:
    def extract(self, path: Path) -> str:
        import csv
        with open(path, newline="") as f:
            return "\n".join(",".join(row) for row in csv.reader(f))

    def supported_mimes(self) -> set[str]:
        return {"text/csv"}

@extractor(".json")
class JsonExtractor:
    def extract(self, path: Path) -> str:
        import json
        return path.read_text()

    def supported_mimes(self) -> set[str]:
        return {"application/json"}

def extract_file(path: Path) -> str:
    """Dispatch: try extension first, then MIME type."""
    ext = path.suffix.lower()
    cls = _ext_registry.get(ext)
    if cls is not None:
        return cls().extract(path)
    mime, _ = mimetypes.guess_type(str(path))
    if mime and mime in _mime_registry:
        return _mime_registry[mime]().extract(path)
    raise ValueError(f"No extractor for {path.name} (ext={ext}, mime={mime})")
```

The two-tier lookup handles files without extensions or with wrong extensions. Each extractor self-declares its MIME types, so adding a new format means adding one decorated class.

---

## Auto-Discovery Commands

A CLI framework where command classes are auto-discovered from a package directory. Drop a module into `commands/` and it becomes available — no manual registration.

```python
import importlib
import pkgutil
from abc import ABC, abstractmethod
from pathlib import Path

class Command(ABC):
    """Base command. Subclasses auto-register via __init_subclass__."""
    _registry: dict[str, type["Command"]] = {}

    def __init_subclass__(cls, name: str = "", **kwargs):
        super().__init_subclass__(**kwargs)
        cmd_name = name or cls.__name__.lower().removesuffix("command")
        if cmd_name:
            Command._registry[cmd_name] = cls

    @abstractmethod
    def execute(self, args: list[str]) -> int: ...

    @classmethod
    def discover(cls, package_name: str) -> None:
        """Import all modules in a package to trigger registration."""
        pkg = importlib.import_module(package_name)
        pkg_path = Path(pkg.__file__).parent
        for info in pkgutil.iter_modules([str(pkg_path)]):
            importlib.import_module(f"{package_name}.{info.name}")

    @classmethod
    def run(cls, argv: list[str]) -> int:
        if not argv:
            print("Available:", ", ".join(sorted(cls._registry)))
            return 1
        name, *args = argv
        cmd_cls = cls._registry.get(name)
        if cmd_cls is None:
            print(f"Unknown command: {name}")
            return 1
        return cmd_cls().execute(args)

# --- In commands/export.py ---
class ExportCommand(Command, name="export"):
    """Export data to a file."""
    def execute(self, args: list[str]) -> int:
        print(f"Exporting as {args[0] if args else 'json'}...")
        return 0

# --- In commands/validate.py ---
class ValidateCommand(Command, name="validate"):
    """Validate input files."""
    def execute(self, args: list[str]) -> int:
        for p in args:
            print(f"Validating {p}...")
        return 0

# --- main.py ---
# Command.discover("myapp.commands")
# sys.exit(Command.run(sys.argv[1:]))
```

`discover()` walks the package and imports each module, triggering `__init_subclass__`. To add a command, create a file in `commands/` with a `Command` subclass — nothing else changes.

---

## Config-Driven Strategy

Strategy selection driven by environment variables instead of hardcoded conditionals.

```python
import os
from typing import Protocol

class Sender(Protocol):
    def send(self, recipient: str, message: str) -> bool: ...

class EmailSender:
    def __init__(self, host: str): self.host = host
    def send(self, recipient: str, message: str) -> bool:
        print(f"Email to {recipient} via {self.host}: {message}")
        return True

class SlackSender:
    def __init__(self, url: str): self.url = url
    def send(self, recipient: str, message: str) -> bool:
        print(f"Slack to {recipient}: {message}")
        return True

class ConsoleSender:
    def send(self, recipient: str, message: str) -> bool:
        print(f"[CONSOLE] {recipient}: {message}")
        return True

FACTORIES = {
    "email": lambda: EmailSender(os.environ.get("SMTP_HOST", "localhost")),
    "slack": lambda: SlackSender(os.environ.get("SLACK_WEBHOOK", "")),
    "console": lambda: ConsoleSender(),
}

def create_sender() -> Sender:
    """Build sender from NOTIFY_METHOD env var."""
    method = os.environ.get("NOTIFY_METHOD", "console")
    factory = FACTORIES.get(method)
    if factory is None:
        raise ValueError(f"Unknown: '{method}'. Available: {', '.join(FACTORIES)}")
    return factory()

# export NOTIFY_METHOD=slack SLACK_WEBHOOK=https://hooks.slack.com/...
# sender = create_sender()
# sender.send("ops-team", "Deployment complete")
```

Application code depends only on the `Sender` protocol. Switching from email to Slack means changing one env var, not modifying code.
