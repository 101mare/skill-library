# Privacy & Offline Compliance

### Severity Levels

- **CRITICAL**: Data sent to external servers, telemetry, analytics
- **HIGH**: External API calls, cloud storage access
- **MEDIUM**: External CDN/font references, optional external features
- **LOW**: Localhost calls that could be external in production

### External HTTP Calls (CRITICAL/HIGH)

```python
# FLAGGED: External API calls
import requests
requests.get("https://api.example.com/...")
requests.post("https://external-service.com/...")

import httpx
httpx.get("https://...")

import urllib.request
urllib.request.urlopen("https://...")

# SAFE: Local calls
requests.get("http://localhost:11434/...")  # Local LLM
requests.get("http://127.0.0.1:8000/...")
```

### Telemetry & Analytics (CRITICAL)

```python
# FLAGGED patterns
import sentry_sdk
import analytics
import posthog
import mixpanel
import segment
from opentelemetry import trace  # If exporting externally

# FLAGGED: Usage tracking
send_telemetry(...)
track_event(...)
log_usage(...)
```

### Cloud Storage (HIGH)

```python
# FLAGGED: Cloud SDK imports
import boto3  # AWS
from google.cloud import storage  # GCP
from azure.storage.blob import ...  # Azure
import s3fs
import gcsfs

# FLAGGED: Cloud URLs
"s3://bucket/..."
"gs://bucket/..."
"https://storage.googleapis.com/..."
"https://s3.amazonaws.com/..."
```

### External LLM APIs (CRITICAL for local-first projects)

```python
# FLAGGED: External LLM calls
import openai
from anthropic import Anthropic
import cohere
from langchain.llms import OpenAI

# SAFE: Local LLM
import ollama
requests.post("http://localhost:11434/api/generate")
```

### Frontend External Resources (MEDIUM)

```html
<!-- FLAGGED: External fonts -->
<link href="https://fonts.googleapis.com/..." />

<!-- FLAGGED: External CDN -->
<script src="https://cdn.jsdelivr.net/..."></script>
<script src="https://unpkg.com/..."></script>

<!-- FLAGGED: Analytics -->
<script src="https://www.googletagmanager.com/..."></script>
```

```css
/* FLAGGED: External fonts */
@import url('https://fonts.googleapis.com/...');
```

### WebSocket Connections (HIGH)

```python
# FLAGGED: External WebSocket
import websockets
await websockets.connect("wss://external.com/...")

# SAFE: Local WebSocket
await websockets.connect("ws://localhost:8080/...")
```

### DNS/Network Lookups (MEDIUM)

```python
# FLAGGED: DNS that implies external access
import socket
socket.gethostbyname("api.example.com")
```

### Full Audit Checklist

#### Python Files

| Check | Pattern to Search |
|-------|-------------------|
| HTTP libraries | `import requests`, `import httpx`, `import urllib` |
| Cloud SDKs | `import boto3`, `google.cloud`, `azure.` |
| External LLMs | `import openai`, `import anthropic`, `import cohere` |
| Telemetry | `sentry`, `analytics`, `posthog`, `mixpanel` |
| WebSockets | `websockets.connect`, external URLs |

#### Config Files

| Check | Pattern to Search |
|-------|-------------------|
| External URLs | `https://` (not localhost) |
| API keys for external services | `OPENAI_API_KEY`, `AWS_`, `AZURE_` |
| Webhook URLs | `webhook`, `callback_url` |

#### Frontend Files

| Check | Pattern to Search |
|-------|-------------------|
| External scripts | `<script src="https://` |
| External styles | `<link href="https://` |
| Font imports | `fonts.googleapis.com`, `fonts.gstatic.com` |
| Analytics | `googletagmanager`, `gtag`, `analytics` |

### Safe Patterns (Whitelist)

These are generally safe for offline operation:

```python
# Local services
"http://localhost"
"http://127.0.0.1"
"http://0.0.0.0"
"http://[::1]"

# Local databases
"postgresql://localhost"
"mongodb://localhost"
"redis://localhost"
```

### Audit Process

1. **Scan imports**: Search for network library imports
2. **Find URLs**: Grep for `https://`, `http://` (excluding localhost)
3. **Check configs**: Review .env, config.yaml, settings for external URLs
4. **Analyze frontend**: Check HTML/CSS/JS for external resources
5. **Review dependencies**: Check if any pip packages phone home

Report findings with exact file locations and remediation steps.
