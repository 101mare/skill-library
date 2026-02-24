---
name: logging-builder
description: |
  Implements Python logging infrastructure following best practices.
  Creates logger configurations, adds logging to functions, sets up file rotation.
  Use when adding logging to code, setting up logging configuration, or improving
  existing logging. Triggers: "add logging", "setup logging", "configure logger",
  "logging infrastructure", "structured logging", "log rotation"
allowed-tools: Read, Grep, Glob, Edit, Write
---

# Logging Builder

Implements production-ready Python logging. For detailed patterns, see [reference.md](reference.md).

## Quick Setup

### 1. Module Logger (Always Use This)

```python
import logging

logger = logging.getLogger(__name__)
```

### 2. Entry Point Configuration

Add to `main.py` or entry point:

```python
import logging

def setup_logging(level: int = logging.INFO) -> None:
    """Configure logging for the application."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    # Silence noisy libraries
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
```

## Log Level Guide

| Level | When to Use | Example |
|-------|-------------|---------|
| `DEBUG` | Variable values, flow details | `logger.debug("Chunk %d/%d", i, total)` |
| `INFO` | Key operations, milestones | `logger.info("Processing started")` |
| `WARNING` | Handled issues, retries | `logger.warning("Retry %d/%d", n, max)` |
| `ERROR` | Operation failures | `logger.error("Parse failed: %s", path)` |
| `CRITICAL` | System failures | `logger.critical("DB connection lost")` |

## Exception Logging

```python
# CORRECT: Full traceback
try:
    result = process(data)
except ProcessingError:
    logger.exception("Processing failed for %s", doc_id)
    raise

# WRONG: Loses traceback
except Exception as e:
    logger.error(f"Error: {e}")  # No stack trace!
```

## Structured Logging

```python
# Use extra dict for machine-parseable data
logger.info(
    "Document processed",
    extra={"doc_id": doc.id, "pages": doc.pages, "ms": int(duration * 1000)}
)

# Use %-formatting (lazy evaluation)
logger.debug("Items: %d, batch: %s", len(items), batch_id)
```

## Security Rules

**Never log:**
- Passwords, API keys, tokens
- Personal data (PII)
- Full request/response bodies with sensitive fields
- **LLM responses in local/offline projects** (may contain extracted sensitive data)

```python
# GOOD
logger.info("User authenticated", extra={"user_id": user.id})

# BAD - exposes credentials
logger.debug(f"Token: {api_token}")
```

### LLM Logging (Local/Offline Projects)

When using local LLMs (Ollama, llama.cpp, etc.), **never log the actual response content**. LLM responses may contain sensitive data extracted from user documents.

```python
# GOOD - Log metadata only
logger.info(
    "LLM response received",
    extra={"model": model, "tokens": token_count, "duration_ms": duration}
)
logger.debug("LLM prompt category: %s", category)

# BAD - Exposes extracted document content
logger.debug(f"LLM response: {response}")
logger.info("Extracted terms: %s", llm_output)
```

This applies to prompts too if they contain document content.

## Log File Location (Privacy Projects)

For projects processing sensitive documents, store logs **outside the repository** in a configurable directory:

```python
# Read from config (e.g., config.yaml)
log_dir = Path(config["contracts"]["base_path"]) / "output" / "logs"
log_dir.mkdir(parents=True, exist_ok=True)
```

This keeps logs with the data they describe, not in the code repo.

### Log Viewer Script

Create a `view_logs.py` for convenient log access:

```bash
python view_logs.py                  # Last 300 lines
python view_logs.py -n 100           # Last 100 lines
python view_logs.py --errors         # Only ERROR/CRITICAL
python view_logs.py --warnings       # WARNING and above
python view_logs.py -f               # Real-time tail
python view_logs.py --list           # List all log files
```

See [reference.md](reference.md) for full implementation.

## Implementation Checklist

When adding logging to a module:

1. [ ] Add `logger = logging.getLogger(__name__)` at module top
2. [ ] Log entry points: `logger.info("Starting X")`
3. [ ] Log completions: `logger.info("Completed X")`
4. [ ] Log errors with `logger.exception()` in except blocks
5. [ ] Use DEBUG for variable values, INFO for operations
6. [ ] No f-strings in debug logs (use % formatting)
7. [ ] No sensitive data in any log level
8. [ ] Logs go to separate directory (not in repo) for privacy projects
