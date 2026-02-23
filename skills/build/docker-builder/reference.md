# Docker Builder Reference

## GPU/CUDA Setup

### NVIDIA GPU with Docker Compose

```yaml
services:
  model-server:
    image: vllm/vllm-openai:latest
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
    volumes:
      - model-cache:/root/.cache/huggingface
    shm_size: "4gb"
```

### CUDA Base Image

```dockerfile
FROM nvidia/cuda:12.1.0-runtime-ubuntu22.04

RUN apt-get update && apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
```

### Shared Memory for PyTorch

```yaml
services:
  ml-worker:
    shm_size: "4gb"  # Required for PyTorch DataLoader with num_workers > 0
```

## Model Server Patterns

### Wait-for-Model Pattern

```python
import time
import urllib.request
import urllib.error

def wait_for_model_server(url: str, timeout: int = 300) -> None:
    """Block until model server is healthy."""
    start = time.monotonic()
    while time.monotonic() - start < timeout:
        try:
            urllib.request.urlopen(f"{url}/health", timeout=5)
            return
        except (urllib.error.URLError, ConnectionError):
            time.sleep(2)
    raise RuntimeError(f"Model server at {url} not ready after {timeout}s")
```

### Compose with Model Server

```yaml
services:
  app:
    depends_on:
      model-server:
        condition: service_healthy
    environment:
      - MODEL_SERVER_URL=http://model-server:8000

  model-server:
    image: vllm/vllm-openai:latest
    command: ["--model", "Qwen/Qwen2.5-7B", "--max-model-len", "8192"]
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 10s
      timeout: 5s
      retries: 30
      start_period: 120s  # Models take time to load
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

## Production Hardening

### Read-Only Filesystem

```yaml
services:
  app:
    read_only: true
    tmpfs:
      - /tmp
      - /app/cache
    volumes:
      - app-data:/app/data  # Only writable mount
```

### Resource Limits

```yaml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: "2.0"
          memory: 2G
        reservations:
          cpus: "0.5"
          memory: 512M
```

### Logging Configuration

```yaml
services:
  app:
    logging:
      driver: "json-file"
      options:
        max-size: "50m"
        max-file: "5"
```

### Restart Policy

```yaml
services:
  app:
    restart: unless-stopped
    # Or for critical services:
    deploy:
      restart_policy:
        condition: on-failure
        max_attempts: 5
        delay: 5s
```

### Security Options

```yaml
services:
  app:
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE  # Only if binding to port < 1024
```

## Multi-Architecture Builds

```bash
# Build for multiple platforms
docker buildx build --platform linux/amd64,linux/arm64 -t myapp:latest .
```

```dockerfile
# Use platform-aware base
FROM --platform=$TARGETPLATFORM python:3.12-slim
```

## Compose Profiles

```yaml
services:
  app:
    profiles: ["default"]

  debug-tools:
    profiles: ["debug"]
    image: busybox
    command: sleep infinity

  monitoring:
    profiles: ["monitoring"]
    image: grafana/grafana
```

```bash
docker compose up                          # Only "default" profile
docker compose --profile debug up          # default + debug
docker compose --profile monitoring up     # default + monitoring
```
