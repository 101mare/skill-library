# Security (OWASP-Aligned)

### Severity Levels

- **CRITICAL**: Exploitable vulnerability, data exposure, RCE potential
- **HIGH**: Missing validation on external input, weak auth, secret exposure
- **MEDIUM**: Incomplete sanitization, missing security headers, weak defaults
- **LOW**: Hardening suggestions, defense-in-depth recommendations

### A01: Broken Access Control

```python
# CHECK: Authorization on every endpoint
# CHECK: Path traversal in file operations
# CHECK: IDOR (insecure direct object references)

# BAD: No authorization check
@app.route("/admin/users")
def list_users():
    return db.get_all_users()

# GOOD: Authorization verified
@app.route("/admin/users")
@require_role("admin")
def list_users():
    return db.get_all_users()
```

### A02: Cryptographic Failures

```python
# CHECK: No hardcoded secrets
# CHECK: Proper hashing for passwords (bcrypt, argon2)
# CHECK: Secure random generation

# BAD: MD5 for passwords
import hashlib
password_hash = hashlib.md5(password.encode()).hexdigest()

# GOOD: bcrypt
import bcrypt
password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
```

### A03: Injection

```python
# SQL Injection
# BAD
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")

# GOOD
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))

# Command Injection
# BAD
os.system(f"convert {user_file} output.png")
subprocess.run(f"ls {directory}", shell=True)

# GOOD
subprocess.run(["convert", user_file, "output.png"], check=True)
subprocess.run(["ls", directory], check=True)

# Template Injection
# BAD
template = Template(user_input)

# GOOD: Use autoescape, don't construct templates from user input
```

### A04: Insecure Design

```python
# CHECK: Rate limiting on auth endpoints
# CHECK: Account lockout after failed attempts
# CHECK: Input size limits before processing
```

### A05: Security Misconfiguration

```python
# CHECK: Debug mode disabled in production
# CHECK: Default credentials changed
# CHECK: Unnecessary features disabled
# CHECK: Error messages don't leak internal details

# BAD: Stack trace to user
except Exception as e:
    return {"error": str(e)}  # Leaks internals

# GOOD: Generic message
except Exception:
    logger.exception("Request failed")
    return {"error": "Internal server error"}
```

### A07: Identification and Authentication Failures

```python
# CHECK: Passwords not logged
# CHECK: Session tokens have expiration
# CHECK: Credentials not in source code
```

### A08: Software and Data Integrity Failures

```python
# CHECK: Deserialization of untrusted data
# BAD
import pickle
data = pickle.loads(user_data)  # RCE risk!

# GOOD: Use safe formats
import json
data = json.loads(user_data)

# BAD: yaml.load (allows code execution)
data = yaml.load(content)

# GOOD: yaml.safe_load
data = yaml.safe_load(content)
```

### Path Traversal

```python
from pathlib import Path

# BAD: User controls path
file_path = base_dir / user_input
content = file_path.read_text()

# GOOD: Validate path stays within bounds
def safe_path(base: Path, user_path: str) -> Path:
    resolved = (base / user_path).resolve()
    base_resolved = base.resolve()
    if not resolved.is_relative_to(base_resolved):
        raise ValueError("Path traversal detected")
    if resolved.is_symlink():
        raise ValueError("Symlinks not allowed")
    return resolved
```

### Secrets Management

```python
# FLAGGED: Hardcoded secrets
API_KEY = "sk-abc123..."
PASSWORD = "admin123"
token = "ghp_xxxxxxxxxxxx"

# FLAGGED: Secrets in logs
logger.info(f"Connecting with token {token}")
logger.debug(f"Auth header: {auth_header}")

# GOOD: From environment
api_key = os.getenv("API_KEY")
if not api_key:
    raise ConfigError("API_KEY environment variable required")
```

### Resource Limits

```python
# CHECK: File size limits before processing
# CHECK: Request body size limits
# CHECK: Recursion depth limits
# CHECK: Timeout on external calls

# BAD: No size check
def process_upload(file):
    content = file.read()  # Could be 10GB

# GOOD: Check first
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

def process_upload(file):
    file.seek(0, 2)
    size = file.tell()
    file.seek(0)
    if size > MAX_FILE_SIZE:
        raise ValueError(f"File too large: {size} bytes")
    content = file.read()
```

### Input Validation

| Check | Pass | Fail |
|-------|------|------|
| User input validated | Pydantic/dataclass | Trust raw input |
| File paths sanitized | `pathlib`, bounded | `os.path.join(user_input)` |
| SQL parameterized | `cursor.execute(sql, params)` | f-strings in SQL |

```python
# GOOD: Parameterized
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))

# BAD: SQL injection
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
```

### Command Injection

```python
# GOOD: List args, no shell
subprocess.run(["ls", "-la", directory], check=True)

# BAD: Shell injection
os.system(f"ls -la {user_directory}")
```

### Secrets & Credentials

| Check | Pass | Fail |
|-------|------|------|
| No hardcoded secrets | Env vars, config files | `password = "secret"` |
| Secrets not logged | Redact sensitive | `logger.info(f"Token: {t}")` |
| .env in .gitignore | Excluded | Committed credentials |

### Async Security

```python
# GOOD: Timeout on async operations
async with asyncio.timeout(30):
    result = await client.fetch(url)

# BAD: No timeout (can hang forever)
result = await client.fetch(url)
```

### A06: Vulnerable and Outdated Components

```python
# CHECK: Dependencies scanned for known vulnerabilities
# CHECK: Lock files with hashes (pip-compile, poetry.lock)
# CHECK: No typosquatted package names (e.g. "requets" instead of "requests")

# Audit commands:
# pip audit
# safety check
# pip-compile --generate-hashes
```

### A10: Server-Side Request Forgery (SSRF)

```python
import urllib.parse
import ipaddress
import socket

# BAD: User controls URL directly
url = request.args.get("url")
response = requests.get(url)  # SSRF!

# GOOD: Whitelist + private IP blocking
ALLOWED_HOSTS = {"api.internal.com", "cdn.example.com"}

def safe_request(url: str) -> requests.Response:
    parsed = urllib.parse.urlparse(url)
    if parsed.hostname not in ALLOWED_HOSTS:
        raise ValueError(f"Host not allowed: {parsed.hostname}")
    ip = socket.gethostbyname(parsed.hostname)
    if ipaddress.ip_address(ip).is_private:
        raise ValueError("Private IP not allowed")
    return requests.get(url, allow_redirects=False)
```

### Dangerous Builtins

```python
# BAD: RCE via eval/exec with external input
result = eval(user_input)
exec(user_code)
compile(user_input, "<string>", "exec")

# BAD: assert stripped in production (python -O)
assert user.is_admin, "Unauthorized"  # Bypassed with -O!

# GOOD: Explicit check
if not user.is_admin:
    raise PermissionError("Unauthorized")

# BAD: Predictable tokens
import random
token = random.randint(0, 999999)

# GOOD: Cryptographically secure
import secrets
token = secrets.token_urlsafe(32)
```

### Timing-Safe Comparison

```python
import hmac

# BAD: Timing side-channel leaks token length/content
if token == expected_token:
    grant_access()

# GOOD: Constant-time comparison
if hmac.compare_digest(token.encode(), expected_token.encode()):
    grant_access()
```

### Archive/Decompression Safety

```python
import zipfile

# BAD: Zip bomb + path traversal
with zipfile.ZipFile(user_file) as zf:
    zf.extractall(target)  # Unchecked!

# GOOD: Validate sizes and paths before extraction
MAX_EXTRACT_SIZE = 100 * 1024 * 1024  # 100MB

def safe_extract(archive_path: Path, target: Path) -> None:
    with zipfile.ZipFile(archive_path) as zf:
        total = sum(f.file_size for f in zf.infolist())
        if total > MAX_EXTRACT_SIZE:
            raise ValueError(f"Archive too large: {total} bytes")
        for info in zf.infolist():
            extracted = (target / info.filename).resolve()
            if not extracted.is_relative_to(target.resolve()):
                raise ValueError(f"Path traversal: {info.filename}")
        zf.extractall(target)
```

### XML External Entity (XXE)

```python
# BAD: xml.etree allows XXE with external input
import xml.etree.ElementTree as ET
tree = ET.parse(user_uploaded_file)  # XXE risk!

# GOOD: defusedxml blocks XXE
import defusedxml.ElementTree as ET
tree = ET.parse(user_uploaded_file)
```

### Temporary File Safety

```python
import tempfile

# BAD: Manual tmp path — race condition + symlink attack
tmp_path = "/tmp/myapp_" + filename
with open(tmp_path, "w") as f:
    f.write(data)

# GOOD: Atomic creation, unique name, auto-cleanup
with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=True) as f:
    f.write(data)
    f.flush()
    process(f.name)
```

---
