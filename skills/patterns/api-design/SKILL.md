---
name: api-design
description: |
  REST API design with FastAPI: routing, response models, error handling, dependencies.
  Use when building APIs, designing endpoints, or setting up FastAPI projects.
  Recognizes: "api-design", "REST API", "FastAPI", "endpoint design", "response model",
  "API error handling", "OpenAPI", "build an API", "API patterns", "HTTP endpoints"
---

# API Design Patterns

REST API design with FastAPI, Pydantic response models, and structured error handling.

## Project Structure

```
src/
├── api/
│   ├── __init__.py
│   ├── app.py              # FastAPI app factory
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── cases.py        # /cases endpoints
│   │   └── health.py       # /health endpoint
│   ├── dependencies.py     # Shared DI (get_config, get_container)
│   ├── errors.py           # Exception handlers
│   └── models/
│       ├── requests.py     # Input models
│       └── responses.py    # Output models
```

## App Factory

```python
from fastapi import FastAPI

def create_app(config: PipelineConfig | None = None) -> FastAPI:
    app = FastAPI(
        title="Autocase Classifier",
        version="1.0.0",
        docs_url="/docs",
        redoc_url=None,
    )

    # Store config in app state
    if config:
        app.state.config = config

    # Register routes
    from api.routes import cases, health
    app.include_router(health.router, tags=["health"])
    app.include_router(cases.router, prefix="/api/v1", tags=["cases"])

    # Register error handlers
    from api.errors import register_handlers
    register_handlers(app)

    return app
```

## Response Models

Separate input (request) and output (response) models. Never expose internal DTOs directly.

```python
from pydantic import BaseModel, Field
from datetime import datetime

# --- Response Models ---

class CaseResultResponse(BaseModel):
    case_id: str
    ca_type: str
    confidence: float = Field(ge=0.0, le=1.0)
    needs_review: bool
    entities: dict[str, str | None]
    processed_at: datetime

    model_config = {"json_schema_extra": {
        "example": {
            "case_id": "case_001",
            "ca_type": "KVW-Steuer",
            "confidence": 0.92,
            "needs_review": False,
            "entities": {"iban": "DE89370400440532013000"},
            "processed_at": "2026-02-24T10:30:00Z",
        }
    }}

class ErrorResponse(BaseModel):
    error: str
    detail: str | None = None

class HealthResponse(BaseModel):
    status: str  # "healthy" | "degraded" | "unhealthy"
    provider: str
    model_loaded: bool

# --- Request Models ---

class ClassifyRequest(BaseModel):
    case_id: str = Field(min_length=1, max_length=200)
    text: str = Field(min_length=1, max_length=50_000)
```

## Routes

```python
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()

@router.post(
    "/cases/classify",
    response_model=CaseResultResponse,
    status_code=status.HTTP_200_OK,
    responses={
        422: {"model": ErrorResponse, "description": "Validation error"},
        503: {"model": ErrorResponse, "description": "Model unavailable"},
    },
)
async def classify_case(
    request: ClassifyRequest,
    container: Container = Depends(get_container),
) -> CaseResultResponse:
    result = container.classifier.classify(request.text)
    return CaseResultResponse(
        case_id=request.case_id,
        ca_type=result.ca_type,
        confidence=result.confidence,
        needs_review=result.needs_review,
        entities=result.entities,
        processed_at=datetime.now(UTC),
    )

@router.get("/cases/{case_id}", response_model=CaseResultResponse)
async def get_case(case_id: str):
    result = load_result(case_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Case not found: {case_id}",
        )
    return result
```

## Dependency Injection

```python
from fastapi import Depends, Request

def get_config(request: Request) -> PipelineConfig:
    return request.app.state.config

def get_container(config: PipelineConfig = Depends(get_config)) -> Container:
    return Container(config)
```

For expensive resources (DB connections, model containers), use lifespan:

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    container = Container(app.state.config)
    container.startup()
    app.state.container = container
    yield
    # Shutdown
    container.shutdown()

app = FastAPI(lifespan=lifespan)

def get_container(request: Request) -> Container:
    return request.app.state.container
```

## Error Handling

Map domain exceptions to HTTP responses. Never leak internal details.

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

def register_handlers(app: FastAPI) -> None:

    @app.exception_handler(ModelConnectionError)
    async def model_connection_handler(request: Request, exc: ModelConnectionError):
        return JSONResponse(
            status_code=503,
            content={"error": "Model service unavailable", "detail": None},
        )

    @app.exception_handler(ModelNotFoundError)
    async def model_not_found_handler(request: Request, exc: ModelNotFoundError):
        return JSONResponse(
            status_code=503,
            content={"error": "Model not loaded", "detail": None},
        )

    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        return JSONResponse(
            status_code=422,
            content={"error": "Invalid input", "detail": str(exc)},
        )
```

### Exception → HTTP Mapping

| Domain Exception | HTTP Status | Response |
|-----------------|-------------|----------|
| `ModelConnectionError` | 503 Service Unavailable | `{"error": "Model service unavailable"}` |
| `ModelNotFoundError` | 503 Service Unavailable | `{"error": "Model not loaded"}` |
| `ModelTimeoutError` | 504 Gateway Timeout | `{"error": "Model timeout"}` |
| `ConfigError` | 500 Internal Server Error | `{"error": "Configuration error"}` |
| `ValueError` | 422 Unprocessable Entity | `{"error": "Invalid input"}` |
| Not found | 404 Not Found | `{"error": "Resource not found"}` |

## Health Endpoint

```python
@router.get("/health", response_model=HealthResponse)
async def health_check(container: Container = Depends(get_container)):
    try:
        is_ready = container.provider.is_available()
        return HealthResponse(
            status="healthy" if is_ready else "degraded",
            provider=container.config.provider.type,
            model_loaded=is_ready,
        )
    except Exception:
        return HealthResponse(
            status="unhealthy",
            provider=container.config.provider.type,
            model_loaded=False,
        )
```

## Versioning

Prefix routes with `/api/v1/`. When breaking changes are needed, add `/api/v2/` alongside.

```python
app.include_router(cases_v1.router, prefix="/api/v1", tags=["cases-v1"])
app.include_router(cases_v2.router, prefix="/api/v2", tags=["cases-v2"])
```

## Pagination

```python
class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    page_size: int
    has_next: bool

@router.get("/cases", response_model=PaginatedResponse[CaseResultResponse])
async def list_cases(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
):
    total, items = get_cases(offset=(page - 1) * page_size, limit=page_size)
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        has_next=(page * page_size) < total,
    )
```

## Testing FastAPI

```python
from fastapi.testclient import TestClient

@pytest.fixture
def app(mock_container):
    app = create_app(config)
    app.state.container = mock_container
    return app

@pytest.fixture
def client(app):
    return TestClient(app)

def test_classify_returns_result(client, mock_container):
    mock_container.classifier.classify.return_value = CaseResult(
        ca_type="KVW-Steuer", confidence=0.9
    )

    response = client.post("/api/v1/cases/classify", json={
        "case_id": "test_001",
        "text": "Steuererklärung 2024",
    })

    assert response.status_code == 200
    data = response.json()
    assert data["ca_type"] == "KVW-Steuer"
    assert data["confidence"] == 0.9

def test_classify_empty_text_returns_422(client):
    response = client.post("/api/v1/cases/classify", json={
        "case_id": "test",
        "text": "",
    })
    assert response.status_code == 422

def test_health_healthy(client, mock_container):
    mock_container.provider.is_available.return_value = True
    response = client.get("/health")
    assert response.json()["status"] == "healthy"

def test_health_degraded(client, mock_container):
    mock_container.provider.is_available.return_value = False
    response = client.get("/health")
    assert response.json()["status"] == "degraded"
```

## Security

- **Input validation**: Pydantic does this automatically. Add `Field(max_length=)` to prevent oversized payloads.
- **No PII in logs**: Log request IDs, not request bodies.
- **CORS**: Only configure if serving a frontend from a different origin.
- **Rate limiting**: Not needed for local/offline deployments. Add when exposed to networks.

```python
# CORS (only if frontend runs on different port)
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Returning internal DTOs directly | Leaks implementation details | Use dedicated response models |
| Catching all exceptions silently | Hides bugs | Catch specific exceptions, re-raise unknown |
| Business logic in route functions | Untestable, fat controllers | Delegate to services, routes are thin |
| Nested `if` chains for validation | Complex, error-prone | Use Pydantic validators |
| Hardcoded status codes | Magic numbers | Use `fastapi.status` constants |
| No response model declaration | Missing OpenAPI docs | Always declare `response_model=` |
| Sync blocking calls in async routes | Blocks event loop | Use `def` (not `async def`) for sync code, or run in executor |

## Checklist

- [ ] App factory pattern (testable, configurable)
- [ ] Separate request and response models
- [ ] Exception handlers map domain errors to HTTP status codes
- [ ] Health endpoint returns provider status
- [ ] Routes are thin — business logic in services
- [ ] Dependencies via `Depends()` (not global state)
- [ ] Lifespan for expensive resource management
- [ ] Input validation via Pydantic `Field` constraints
- [ ] Tests use `TestClient` with mocked dependencies
- [ ] No PII in API logs
