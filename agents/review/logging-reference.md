# Logging

### Severity Levels

- **CRITICAL**: Sensitive data logged (passwords, tokens, PII), secrets in log output
- **HIGH**: Missing error logging, wrong log levels, no exception context
- **MEDIUM**: Inconsistent formatting, missing structured data, verbose debug logs
- **LOW**: Style suggestions, performance optimizations

### Logger Setup

```python
# GOOD: Module-level logger with __name__
import logging
logger = logging.getLogger(__name__)

# BAD: Root logger or hardcoded name
logging.info("...")  # Uses root logger
logger = logging.getLogger("myapp")  # Hardcoded
```

### Log Levels

| Level | Use Case | Example |
|-------|----------|---------|
| `DEBUG` | Development details, variable values | `logger.debug(f"Processing chunk {i}/{total}")` |
| `INFO` | Normal operations, milestones | `logger.info("Pipeline started")` |
| `WARNING` | Unexpected but handled situations | `logger.warning("Retry attempt %d", attempt)` |
| `ERROR` | Failures that stop current operation | `logger.error("Failed to parse JSON")` |
| `CRITICAL` | System-wide failures | `logger.critical("Database connection lost")` |

### Exception Logging

```python
# GOOD: Use exception() for full traceback
try:
    result = process(data)
except ProcessingError as e:
    logger.exception("Processing failed for document %s", doc_id)
    raise

# GOOD: Use exc_info=True if not in except block
logger.error("Operation failed", exc_info=True)

# BAD: Loses traceback information
except Exception as e:
    logger.error(f"Error: {e}")  # No traceback!
```

### Structured Logging

```python
# GOOD: Use extra dict for structured data
logger.info(
    "Document processed successfully",
    extra={
        "doc_id": doc.id,
        "pages": doc.page_count,
        "duration_ms": int(duration * 1000),
    }
)

# GOOD: Use %-formatting for lazy evaluation
logger.debug("Processing %d items in batch %s", len(items), batch_id)

# BAD: f-strings always evaluated (even if log level disabled)
logger.debug(f"Large object: {expensive_repr(obj)}")  # Always computed!
```

### Sensitive Data Protection

```python
# CRITICAL: Never log these
- Passwords, API keys, tokens
- Personal identifiable information (PII)
- Credit card numbers, SSNs
- Full request/response bodies with sensitive fields
- LLM responses in local/offline projects (contain extracted document data)
- Prompts containing document content

# GOOD: Redact or mask sensitive data
logger.info("User authenticated", extra={"user_id": user.id})  # ID only

# BAD: Exposes credentials
logger.debug(f"Connecting with token {api_token}")
logger.info(f"User login: {username}:{password}")
```

### LLM Logging (Privacy-Critical)

For local LLM projects (Ollama, llama.cpp, etc.), responses may contain sensitive extracted data:

```python
# GOOD: Log metadata only
logger.info("LLM response received", extra={"model": model, "tokens": count, "duration_ms": ms})
logger.debug("Processing category: %s", category)

# BAD: Exposes document content via LLM output
logger.debug(f"LLM response: {response}")
logger.info("Extracted: %s", llm_output)
logger.warning(f"Parse failed. Response: {response}")  # Also bad!
```

Also check **exception messages** -- they may contain LLM responses:

```python
# BAD: Exception contains full response
raise ValueError(f"Invalid JSON in LLM response: {response}")

# GOOD: Exception without sensitive content
raise ValueError(f"Invalid JSON in LLM response ({len(response)} chars)")
```

### Performance Considerations

```python
# GOOD: Guard expensive log construction
if logger.isEnabledFor(logging.DEBUG):
    logger.debug("Data dump: %s", expensive_serialize(data))

# GOOD: Use lazy % formatting
logger.debug("Items: %r", items)  # Only formatted if DEBUG enabled

# BAD: Always computed
logger.debug(f"Complex: {json.dumps(large_dict, indent=2)}")
```

### Configuration Patterns

#### Basic Setup

```python
# GOOD: Configure once in main/entry point
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Adjust specific loggers
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("sentence_transformers").setLevel(logging.WARNING)
```

#### File + Console Logging with Rotation

```python
import logging
from logging.handlers import RotatingFileHandler

def setup_logging(log_file: str = "app.log", level: int = logging.INFO):
    """Configure logging with file rotation and console output."""
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Console handler
    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s"
    ))
    root_logger.addHandler(console)

    # File handler with rotation (10MB, keep 5 backups)
    file_handler = RotatingFileHandler(
        log_file, maxBytes=10_000_000, backupCount=5
    )
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s"
    ))
    root_logger.addHandler(file_handler)
```

#### JSON Formatter (Production)

```python
import json
import logging

class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        if hasattr(record, "extra"):
            log_data.update(record.extra)
        return json.dumps(log_data)
```

### Common Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| `print()` statements | Not configurable, no levels | Use `logger.info()` |
| `except: pass` | Silent failures | Log + re-raise or handle |
| `logger.error(str(e))` | Loses traceback | `logger.exception()` |
| Logging in tight loops | Performance + noise | Log aggregates or sample |
| `logging.debug(f"...")` | Always evaluated | Use % formatting |
| Root logger only | No granular control | `getLogger(__name__)` |

### Full Audit Checklist

1. **Setup**
   - [ ] Each module uses `logger = logging.getLogger(__name__)`
   - [ ] Logging configured once in entry point
   - [ ] Third-party loggers silenced appropriately

2. **Levels**
   - [ ] DEBUG: Variable values, detailed flow
   - [ ] INFO: Key operations, milestones
   - [ ] WARNING: Handled issues, retries
   - [ ] ERROR: Failures with context
   - [ ] CRITICAL: System failures only

3. **Exceptions**
   - [ ] All except blocks log the error
   - [ ] `logger.exception()` used for tracebacks
   - [ ] Error context includes relevant IDs

4. **Security**
   - [ ] No secrets/tokens in logs
   - [ ] No PII without redaction
   - [ ] Request/response bodies sanitized
   - [ ] **No LLM responses logged** (local projects)
   - [ ] **No prompts with document content logged**
   - [ ] Exception messages don't contain LLM responses

5. **Performance**
   - [ ] No expensive operations in log statements
   - [ ] Debug logs guarded if expensive
   - [ ] No logging in tight loops

6. **Log Location (Privacy Projects)**
   - [ ] Logs stored outside repository (e.g., `{data_path}/output/logs/`)
   - [ ] Log directory created automatically if missing
   - [ ] `view_logs.py` provided for easy access

---
