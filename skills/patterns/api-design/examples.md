# API Design — Examples

Runnable FastAPI examples covering patterns not in [SKILL.md](SKILL.md): file uploads, background tasks, and request correlation.

## Table of Contents

- [File Upload Endpoint](#file-upload-endpoint)
- [Async Background Task](#async-background-task)
- [Request Correlation Middleware](#request-correlation-middleware)

---

## File Upload Endpoint

Streaming upload with chunked validation -- rejects oversized files _during_ the read, not after loading everything into memory.

```python
from fastapi import APIRouter, UploadFile, HTTPException, Depends, status
from pydantic import BaseModel
from datetime import datetime, UTC
import hashlib

ALLOWED_TYPES = {"application/pdf", "image/png", "image/jpeg"}
MAX_SIZE = 10 * 1024 * 1024  # 10 MB
router = APIRouter()

class UploadResponse(BaseModel):
    file_id: str
    filename: str
    size_bytes: int
    content_type: str
    uploaded_at: datetime

class StorageBackend:
    async def write(self, file_id: str, data: bytes) -> None: ...

@router.post("/files", response_model=UploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile,
    storage: StorageBackend = Depends(),
) -> UploadResponse:
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="Unsupported file type")

    chunks: list[bytes] = []
    total = 0
    while chunk := await file.read(64 * 1024):
        total += len(chunk)
        if total > MAX_SIZE:
            raise HTTPException(status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="File too large")
        chunks.append(chunk)

    data = b"".join(chunks)
    file_id = hashlib.sha256(data).hexdigest()[:16]
    await storage.write(file_id, data)
    return UploadResponse(
        file_id=file_id, filename=file.filename or "unnamed",
        size_bytes=total, content_type=file.content_type, uploaded_at=datetime.now(UTC),
    )
```

---

## Async Background Task

Kicks off a long-running job, returns a task ID immediately (202 Accepted), and provides a polling endpoint. Avoids HTTP timeouts for operations that take minutes.

```python
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from enum import Enum
import asyncio, uuid

router = APIRouter()

class TaskStatus(str, Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"

class TaskResponse(BaseModel):
    task_id: str
    status: TaskStatus
    result: dict | None = None
    error: str | None = None

class CreateReportRequest(BaseModel):
    dataset_id: str
    format: str = "pdf"

_tasks: dict[str, TaskResponse] = {}  # Use Redis/DB in production

async def _generate_report(task_id: str, dataset_id: str, fmt: str) -> None:
    _tasks[task_id] = TaskResponse(task_id=task_id, status=TaskStatus.running)
    try:
        await asyncio.sleep(5)  # Simulate expensive work
        _tasks[task_id] = TaskResponse(
            task_id=task_id, status=TaskStatus.completed,
            result={"url": f"/files/report-{dataset_id}.{fmt}"},
        )
    except Exception as exc:
        _tasks[task_id] = TaskResponse(task_id=task_id, status=TaskStatus.failed, error=str(exc))

@router.post("/reports", response_model=TaskResponse, status_code=status.HTTP_202_ACCEPTED)
async def create_report(request: CreateReportRequest) -> TaskResponse:
    task_id = str(uuid.uuid4())
    task = TaskResponse(task_id=task_id, status=TaskStatus.pending)
    _tasks[task_id] = task
    asyncio.create_task(_generate_report(task_id, request.dataset_id, request.format))
    return task

@router.get("/reports/{task_id}", response_model=TaskResponse)
async def get_report_status(task_id: str) -> TaskResponse:
    if task_id not in _tasks:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Task {task_id} not found")
    return _tasks[task_id]
```

Clients poll `GET /reports/{task_id}` until status is `completed` or `failed`. The `result` field holds the output location; `error` holds the failure reason.

---

## Request Correlation Middleware

Generates or propagates a correlation ID through the request lifecycle using `ContextVar`. Essential for tracing requests across logs and downstream services.

```python
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from contextvars import ContextVar
import uuid, logging, time

correlation_id: ContextVar[str] = ContextVar("correlation_id", default="")
HEADER = "X-Correlation-ID"
logger = logging.getLogger("api")

class CorrelationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        cid = request.headers.get(HEADER) or str(uuid.uuid4())
        correlation_id.set(cid)
        start = time.perf_counter()
        logger.info("request_start", extra={"cid": cid, "path": request.url.path})

        response = await call_next(request)
        ms = (time.perf_counter() - start) * 1000
        response.headers[HEADER] = cid
        logger.info("request_end", extra={"cid": cid, "status": response.status_code, "ms": f"{ms:.1f}"})
        return response

def create_app() -> FastAPI:
    app = FastAPI()
    app.add_middleware(CorrelationMiddleware)

    @app.get("/items/{item_id}")
    async def get_item(item_id: str) -> dict:
        cid = correlation_id.get()
        logger.info("fetching_item", extra={"cid": cid, "item_id": item_id})
        return {"item_id": item_id, "correlation_id": cid}

    return app
```

The `ContextVar` makes the correlation ID available anywhere in the call stack without threading it through function signatures. The middleware propagates the ID back in the response header so clients can reference it in support requests.
