---
name: security
description: Input validation, PII protection in logs, secrets management, and dependency policies.
---

# Security & Privacy

## Input Validation

- Validate all external input at system boundaries (user input, file uploads, API responses)
- Trust internal code and framework guarantees — don't re-validate inside business logic
- Path traversal: always use `Path.resolve()` + `is_relative_to()` for user-controlled paths
- No `shell=True` in subprocess calls
- File size limits before processing, not after
- No mutable defaults in function signatures

## Logging & PII

- **Never log PII**: No names, emails, IBANs, phone numbers, document content in logs
- Log process metadata only: file counts, durations, status codes, error types
- Use `extra={}` for structured logging context
- Error messages to users: generic. Error messages to logs: specific (but no PII).

## Secrets

- Secrets in environment variables, NEVER in source code or config files
- No credentials in log output
- No secrets in error messages or stack traces
- `.env` files must be in `.gitignore`

## Dependencies

- No new dependencies without asking first
- Pin versions in requirements
- Prefer stdlib over third-party when the stdlib solution is reasonable
