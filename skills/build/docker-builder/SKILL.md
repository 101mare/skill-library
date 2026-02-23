---
name: docker-builder
description: |
  Scaffolds Dockerfile and docker-compose.yml for Python projects.
  Covers multi-stage builds, health checks, env vars, network isolation, and GPU setup.
  Use when containerizing Python apps, setting up Docker Compose, or optimizing Docker builds.
  Recognizes: "docker-builder", "Dockerfile", "docker-compose", "containerize",
  "Docker setup", "multi-stage build", "Docker health check", "GPU Docker"
---

# Docker Builder

Scaffolds production-ready Dockerfile and docker-compose.yml for Python projects.

## When to Use

- Containerizing a Python application
- Setting up multi-service Docker Compose
- Adding health checks, env vars, or GPU support
- Optimizing Docker image size

## Multi-Stage Dockerfile

```dockerfile
# Stage 1: Build dependencies
FROM python:3.12-slim AS builder

WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Runtime
FROM python:3.12-slim AS runtime

# Security: non-root user
RUN groupadd -r app && useradd -r -g app -d /app -s /sbin/nologin app

WORKDIR /app

# Copy only installed packages from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY src/ ./src/
COPY config.yaml .
COPY pyproject.toml .

# Install app itself (editable not needed in container)
RUN pip install --no-cache-dir --no-deps .

USER app

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

ENTRYPOINT ["python", "-m", "myapp"]
```

## Docker Compose

```yaml
version: "3.8"

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    environment:
      - MYAPP_DATABASE__HOST=postgres
      - MYAPP_LOGGING__LEVEL=INFO
    env_file:
      - .env  # Secrets only
    volumes:
      - app-data:/app/data
    depends_on:
      postgres:
        condition: service_healthy
    networks:
      - internal
    restart: unless-stopped

  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: myapp
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    volumes:
      - pg-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U myapp"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - internal

volumes:
  app-data:
  pg-data:

networks:
  internal:
    driver: bridge
```

## Health Check Patterns

```yaml
# Python HTTP service
healthcheck:
  test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]
  interval: 30s
  timeout: 5s
  retries: 3
  start_period: 10s

# Simple process check
healthcheck:
  test: ["CMD", "python", "-c", "import sys; sys.exit(0)"]
  interval: 30s
  timeout: 5s

# Script-based
healthcheck:
  test: ["CMD", "/app/scripts/health_check.sh"]
  interval: 30s
```

## Environment Variable Patterns

```yaml
services:
  app:
    environment:
      # Inline (non-secret)
      - MYAPP_LOGGING__LEVEL=WARNING
      - MYAPP_DATABASE__HOST=postgres
    env_file:
      # File-based (secrets)
      - .env
```

```bash
# .env (never committed)
DB_PASSWORD=secret123
API_KEY=sk-...
```

## Network Isolation

```yaml
networks:
  # Internal: services communicate
  internal:
    driver: bridge

  # External: only exposed services
  external:
    driver: bridge

services:
  app:
    networks:
      - internal      # Talks to DB
      - external      # Receives requests

  postgres:
    networks:
      - internal      # Only reachable by app
    # No 'ports:' = not exposed to host
```

## Volume Patterns

```yaml
volumes:
  # Named volume (managed by Docker)
  pg-data:

  # Bind mount (host directory)
  # Good for: config files, development
  # Bad for: production data

services:
  app:
    volumes:
      # Named volume for persistent data
      - app-data:/app/data

      # Read-only config mount
      - ./config.yaml:/app/config.yaml:ro

      # Temp directory (not persisted)
      - type: tmpfs
        target: /app/tmp
```

## Python-Specific Best Practices

| Practice | Why |
|----------|-----|
| `python:3.12-slim` base | Smaller image (~120MB vs ~900MB) |
| `--no-cache-dir` on pip | Reduces image size |
| Multi-stage build | Dev deps not in final image |
| Non-root user | Security best practice |
| `.dockerignore` | Exclude tests, docs, .git |
| `COPY requirements.txt` first | Caches dependency layer |
| `pip install --no-deps .` | Avoids re-downloading deps |

### .dockerignore

```
.git
.venv
__pycache__
*.pyc
tests/
docs/
*.md
.env
.claude/
```

## GPU/CUDA Setup

See [reference.md](reference.md) for GPU patterns.

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| `COPY . .` before pip install | Busts cache on every code change | Copy requirements.txt first |
| Running as root | Security risk | Add USER directive |
| No .dockerignore | Large context, slow builds | Add .dockerignore |
| No health check | Compose can't detect failures | Add HEALTHCHECK |
| Hardcoded secrets in Dockerfile | Exposed in image layers | Use env vars or secrets |
| `latest` tag | Non-reproducible builds | Pin exact versions |

## Checklist

- [ ] Multi-stage build (build deps separate from runtime)
- [ ] Non-root user
- [ ] .dockerignore excludes unnecessary files
- [ ] Health check defined
- [ ] Environment variables for config overrides
- [ ] Secrets via env_file or Docker secrets (never inline)
- [ ] Named volumes for persistent data
- [ ] Network isolation between services
- [ ] depends_on with condition: service_healthy
