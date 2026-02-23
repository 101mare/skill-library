# Logging Reference

Detailed patterns for production logging.

## Contents

- [Configuration Patterns](#configuration-patterns)
- [File Rotation](#file-rotation)
- [JSON Logging](#json-logging)
- [Context Managers](#context-managers)
- [Performance Patterns](#performance-patterns)
- [Testing with Logs](#testing-with-logs)

---

## Configuration Patterns

### Basic Console Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
```

### Dict-Based Configuration

```python
import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "detailed": {
            "format": "%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "standard",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "detailed",
            "filename": "app.log",
            "maxBytes": 10_000_000,
            "backupCount": 5,
        },
    },
    "loggers": {
        "": {  # Root logger
            "level": "DEBUG",
            "handlers": ["console", "file"],
        },
        "urllib3": {"level": "WARNING"},
        "httpx": {"level": "WARNING"},
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
```

### Config from YAML

```python
import logging.config
import yaml

with open("logging.yaml") as f:
    config = yaml.safe_load(f)
logging.config.dictConfig(config)
```

---

## File Rotation

### Size-Based Rotation

```python
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    "app.log",
    maxBytes=10_000_000,  # 10 MB
    backupCount=5,        # Keep 5 old files
    encoding="utf-8",
)
```

### Time-Based Rotation

```python
from logging.handlers import TimedRotatingFileHandler

handler = TimedRotatingFileHandler(
    "app.log",
    when="midnight",      # Rotate daily
    interval=1,
    backupCount=30,       # Keep 30 days
    encoding="utf-8",
)
```

### Complete Setup Function

```python
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logging(
    log_file: str | Path | None = None,
    level: int = logging.INFO,
    max_bytes: int = 10_000_000,
    backup_count: int = 5,
) -> None:
    """
    Configure application logging with optional file output.

    Args:
        log_file: Path to log file. If None, console only.
        level: Minimum log level.
        max_bytes: Max file size before rotation.
        backup_count: Number of backup files to keep.
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Clear existing handlers
    root_logger.handlers.clear()

    # Console handler
    console_fmt = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%H:%M:%S",
    )
    console = logging.StreamHandler()
    console.setFormatter(console_fmt)
    console.setLevel(level)
    root_logger.addHandler(console)

    # File handler (optional)
    if log_file:
        file_fmt = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )
        file_handler.setFormatter(file_fmt)
        file_handler.setLevel(logging.DEBUG)  # Capture all to file
        root_logger.addHandler(file_handler)

    # Silence noisy libraries
    for lib in ["urllib3", "httpx", "sentence_transformers", "httpcore"]:
        logging.getLogger(lib).setLevel(logging.WARNING)
```

---

## JSON Logging

For production/log aggregation systems (ELK, Datadog, etc.):

```python
import json
import logging
from datetime import datetime, timezone


class JSONFormatter(logging.Formatter):
    """Format log records as JSON for structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "line": record.lineno,
        }

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        # Add extra fields
        if hasattr(record, "__dict__"):
            for key, value in record.__dict__.items():
                if key not in {
                    "name", "msg", "args", "created", "filename",
                    "funcName", "levelname", "levelno", "lineno",
                    "module", "msecs", "pathname", "process",
                    "processName", "relativeCreated", "stack_info",
                    "exc_info", "exc_text", "thread", "threadName",
                    "taskName", "message",
                }:
                    log_data[key] = value

        return json.dumps(log_data, default=str)


# Usage
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logging.getLogger().addHandler(handler)

# Log with extra fields
logger.info("Request processed", extra={"user_id": 123, "duration_ms": 45})
# Output: {"timestamp": "...", "level": "INFO", "message": "Request processed", "user_id": 123, "duration_ms": 45}
```

---

## Context Managers

### Timed Operations

```python
import logging
import time
from contextlib import contextmanager
from typing import Iterator

logger = logging.getLogger(__name__)


@contextmanager
def log_duration(operation: str, level: int = logging.INFO) -> Iterator[None]:
    """Log the duration of an operation."""
    start = time.perf_counter()
    logger.log(level, "Starting: %s", operation)
    try:
        yield
    finally:
        duration = time.perf_counter() - start
        logger.log(level, "Completed: %s (%.2fs)", operation, duration)


# Usage
with log_duration("PDF processing"):
    process_pdf(file_path)
# Output:
# Starting: PDF processing
# Completed: PDF processing (2.34s)
```

### Operation Context

```python
import logging
from contextlib import contextmanager
from typing import Any, Iterator

logger = logging.getLogger(__name__)


@contextmanager
def log_context(
    operation: str,
    **context: Any,
) -> Iterator[None]:
    """Log operation with context, including any errors."""
    logger.info("Starting %s", operation, extra=context)
    try:
        yield
    except Exception:
        logger.exception("Failed: %s", operation, extra=context)
        raise
    else:
        logger.info("Completed %s", operation, extra=context)


# Usage
with log_context("document processing", doc_id=doc.id, pages=doc.pages):
    result = process_document(doc)
```

---

## Performance Patterns

### Guard Expensive Debug Logs

```python
# BAD: Always computed even if DEBUG disabled
logger.debug(f"Large data: {json.dumps(huge_dict, indent=2)}")

# GOOD: Only computed if DEBUG enabled
if logger.isEnabledFor(logging.DEBUG):
    logger.debug("Large data: %s", json.dumps(huge_dict, indent=2))

# GOOD: Lazy formatting (built-in)
logger.debug("Items count: %d", len(items))  # len() called only if DEBUG
```

### Sampling High-Volume Logs

```python
import random

# Log only 1% of high-volume events
if random.random() < 0.01:
    logger.debug("Processing item %s", item_id)
```

### Batch Logging

```python
# BAD: Log every item
for item in items:
    logger.debug("Processing: %s", item)

# GOOD: Log aggregates
logger.info("Processing %d items", len(items))
# ... process ...
logger.info("Processed %d items, %d failed", success, failed)
```

---

## Testing with Logs

### Capture Logs in Tests

```python
import logging
import pytest


def test_logs_warning_on_retry(caplog: pytest.LogCaptureFixture) -> None:
    """Test that retry attempts are logged."""
    with caplog.at_level(logging.WARNING):
        service.call_with_retry()

    assert "Retry attempt" in caplog.text
    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == "WARNING"


def test_logs_error_with_context(caplog: pytest.LogCaptureFixture) -> None:
    """Test error logging includes context."""
    with caplog.at_level(logging.ERROR):
        with pytest.raises(ProcessingError):
            process_document(invalid_doc)

    assert "doc_id" in caplog.text
```

### Assert Specific Log Records

```python
def test_structured_logging(caplog: pytest.LogCaptureFixture) -> None:
    """Test that structured data is logged."""
    with caplog.at_level(logging.INFO):
        process(doc_id=123)

    # Check extra fields
    record = caplog.records[0]
    assert record.doc_id == 123  # type: ignore
```

---

## LLM Logging (Privacy-Critical)

For local/offline LLM projects (Ollama, llama.cpp, vLLM, etc.), LLM responses may contain sensitive data extracted from user documents. **Never log the actual content.**

### What to Log

```python
# Metadata only - safe for logs
logger.info(
    "LLM call completed",
    extra={
        "model": model_name,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "duration_ms": int(duration * 1000),
        "category": extraction_category,
    }
)

# Status and flow
logger.debug("Sending prompt to LLM for category: %s", category)
logger.info("LLM extraction complete for %d categories", len(categories))
logger.warning("LLM retry %d/%d for category %s", attempt, max_retries, category)
```

### What NOT to Log

```python
# BAD - Response contains extracted document data
logger.debug(f"LLM response: {response}")
logger.info("Extracted: %s", llm_output)

# BAD - Prompt contains document content
logger.debug(f"Sending prompt: {prompt}")

# BAD - Even partial content is problematic
logger.debug("First 100 chars: %s", response[:100])
```

### Safe Pattern for LLM Modules

```python
import logging

logger = logging.getLogger(__name__)


def call_llm(prompt: str, model: str) -> str:
    """Call LLM - logs metadata only, never content."""
    logger.debug("LLM call starting", extra={"model": model})

    start = time.perf_counter()
    response = ollama.generate(model=model, prompt=prompt)
    duration = time.perf_counter() - start

    # Log metadata only
    logger.info(
        "LLM response received",
        extra={
            "model": model,
            "duration_ms": int(duration * 1000),
            "response_length": len(response),  # Length is OK, content is not
        }
    )

    return response
```

### Debugging Without Logging Content

Use a separate debug file system instead of logs:

```python
from pathlib import Path

DEBUG_DIR = Path("output/debug")

def save_debug_output(name: str, content: str) -> None:
    """Save content to debug file (not logs) for development only."""
    if not DEBUG_DIR.exists():
        return  # Only save if debug dir explicitly created
    (DEBUG_DIR / name).write_text(content)
```

---

## Log Viewer Script (view_logs.py)

For projects with logs outside the repo, provide a `view_logs.py`:

```python
#!/usr/bin/env python3
"""Simple log viewer for application logs.

Usage:
    python view_logs.py                  # Show last 300 lines
    python view_logs.py -n 100           # Show last 100 lines
    python view_logs.py --errors         # Show only errors
    python view_logs.py --warnings       # Show warnings and errors
    python view_logs.py --follow         # Tail logs in real-time
    python view_logs.py --list           # List all log files
"""

import argparse
import subprocess
import sys
from pathlib import Path

import yaml


def get_log_dir() -> Path:
    """Get log directory from config."""
    config_path = Path("config.yaml")
    if config_path.exists():
        with open(config_path) as f:
            config = yaml.safe_load(f)
            base_path = Path(config.get("contracts", {}).get("base_path", "data"))
            return base_path / "output" / "logs"
    return Path("data/output/logs")


def main():
    parser = argparse.ArgumentParser(description="View application logs")
    parser.add_argument("-n", "--lines", type=int, default=300, help="Number of lines")
    parser.add_argument("--errors", action="store_true", help="Show only ERROR/CRITICAL")
    parser.add_argument("--warnings", action="store_true", help="Show WARNING and above")
    parser.add_argument("--follow", "-f", action="store_true", help="Tail in real-time")
    parser.add_argument("--list", action="store_true", help="List all log files")

    args = parser.parse_args()
    log_dir = get_log_dir()

    if args.list:
        if log_dir.exists():
            print(f"Log directory: {log_dir}\n")
            for f in sorted(log_dir.glob("*")):
                size = f.stat().st_size
                size_str = f"{size / 1024:.1f} KB" if size > 1024 else f"{size} B"
                print(f"  {f.name:<30} {size_str:>10}")
        else:
            print(f"Log directory not found: {log_dir}")
        return

    log_file = log_dir / "app.log"  # Adjust filename as needed

    if not log_file.exists():
        print(f"Log file not found: {log_file}")
        print("Run the application first to generate logs.")
        sys.exit(1)

    if args.follow:
        try:
            subprocess.run(["tail", "-f", str(log_file)])
        except KeyboardInterrupt:
            print("\nStopped.")
        return

    with open(log_file, encoding="utf-8") as f:
        lines = f.readlines()

    if args.errors:
        lines = [l for l in lines if "| ERROR" in l or "| CRITICAL" in l]
    elif args.warnings:
        lines = [l for l in lines if any(lvl in l for lvl in ["| WARNING", "| ERROR", "| CRITICAL"])]

    lines = lines[-args.lines:]

    if not lines:
        print("No matching log entries found.")
        return

    print(f"--- Last {len(lines)} entries from {log_file.name} ---\n")
    for line in lines:
        print(line.rstrip())


if __name__ == "__main__":
    main()
```

---

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| `print()` | Not configurable | `logger.info()` |
| `logging.info()` | Uses root logger | `logger = getLogger(__name__)` |
| `logger.error(str(e))` | Loses traceback | `logger.exception()` |
| `f"Data: {big_obj}"` | Always evaluated | `"Data: %s", big_obj` |
| Log in tight loop | Performance, noise | Log aggregates |
| `except: pass` | Silent failures | Log + handle/raise |
| Hardcoded logger name | Wrong module shown | `getLogger(__name__)` |
| Log LLM responses | Privacy violation | Log metadata only |
