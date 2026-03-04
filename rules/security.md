---
name: security
description: Input validation, authentication & sessions, PII protection in logs, secrets management, and dependency policies.
---

# Security & Privacy

## Input Validation

- Validate all external input at system boundaries (user input, file uploads, API responses)
- Trust internal code and framework guarantees — don't re-validate inside business logic
- Path traversal: always use `Path.resolve()` + `is_relative_to()` for user-controlled paths
- No `shell=True` in subprocess calls
- File size limits before processing, not after
- No mutable defaults in function signatures

## Dangerous Patterns

- No `eval()`, `exec()`, `compile()` with any external input — no sanitizing makes this safe
- No `assert` for security/validation checks — stripped by `python -O` in production
- `secrets` module for tokens/passwords/nonces — `random` is NOT cryptographically secure
- `hmac.compare_digest()` for secret/token comparison — never `==` (timing attack)
- `tempfile.NamedTemporaryFile`/`TemporaryDirectory` for temp files — never construct tmp paths manually
- `defusedxml` for untrusted XML — `xml.etree.ElementTree` allows XXE
- Validate/whitelist URLs before HTTP requests with user-controlled input (SSRF)
- No unbounded regex repetition (`(a+)+`) with user input (ReDoS)
- No `extractall()` on untrusted archives without size/path checks (zip bombs, path traversal)

## Authentication & Sessions

- Hash passwords with `bcrypt` (rounds=12+) or `argon2id` — NEVER `hashlib.md5()`, `hashlib.sha1()`, or unsalted `hashlib.sha256()`
- Generic auth errors only: "Invalid credentials" — never reveal whether username or password was wrong (user enumeration)
- Session cookies: always set `HttpOnly`, `Secure`, and `SameSite=Strict`
- Invalidate sessions on logout, idle timeout, and absolute timeout — regenerate session ID after login
- Rate-limit authentication endpoints (e.g. 5 attempts/min per IP) — progressive backoff or lockout after repeated failures
- No default credentials in shipped code — force password change on first login for seeded accounts
- Password reset tokens: `secrets.token_urlsafe()`, expire after max 1 hour, single-use

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
- Run `pip audit` or `safety check` before releases to detect known vulnerabilities
- Verify package names carefully — typosquatting is a real supply chain attack vector

## Quick Reference — Critical Patterns

```python
# PATH TRAVERSAL
resolved = (base / user_input).resolve()
if not resolved.is_relative_to(base.resolve()):
    raise ValueError("Path traversal")

# SQL INJECTION — always parameterize
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))

# COMMAND INJECTION — list args, no shell
subprocess.run(["convert", user_file, "out.png"], check=True)

# SECRETS — cryptographically secure
token = secrets.token_urlsafe(32)                  # NOT random.randint()
if hmac.compare_digest(token, expected):            # NOT ==

# DESERIALIZATION — safe formats only
data = json.loads(user_data)                        # NOT pickle.loads()
data = yaml.safe_load(content)                      # NOT yaml.load()

# PASSWORD HASHING — adaptive, salted
import bcrypt
hashed = bcrypt.hashpw(pw.encode(), bcrypt.gensalt(rounds=12))  # NOT hashlib.md5()
bcrypt.checkpw(pw.encode(), hashed)                              # NOT ==
```
