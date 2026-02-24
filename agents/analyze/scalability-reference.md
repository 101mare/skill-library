# Scalability

### Connection & Resource Pooling (CRITICAL)

#### Database Connections

```python
# BAD: New connection per request
def get_user(user_id):
    conn = psycopg2.connect(DATABASE_URL)  # New connection every time!
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    return cursor.fetchone()

# GOOD: Connection pool
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,  # Verify connections are alive
)

def get_user(user_id):
    with engine.connect() as conn:
        return conn.execute(
            "SELECT * FROM users WHERE id = %s", (user_id,)
        ).fetchone()
```

#### HTTP Client Connections

```python
# BAD: New client per request
async def fetch_data(url):
    async with aiohttp.ClientSession() as session:  # New session each time!
        async with session.get(url) as response:
            return await response.json()

# GOOD: Reuse session
class ApiClient:
    def __init__(self):
        self._session: aiohttp.ClientSession | None = None

    async def get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            connector = aiohttp.TCPConnector(limit=100, limit_per_host=30)
            self._session = aiohttp.ClientSession(connector=connector)
        return self._session

    async def fetch(self, url: str):
        session = await self.get_session()
        async with session.get(url) as response:
            return await response.json()

    async def close(self):
        if self._session:
            await self._session.close()
```

#### Redis Connections

```python
# BAD: New connection per operation
def get_cached(key):
    r = redis.Redis(host='localhost')  # New connection!
    return r.get(key)

# GOOD: Connection pool
pool = redis.ConnectionPool(
    host='localhost',
    port=6379,
    max_connections=50,
    decode_responses=True,
)

def get_redis():
    return redis.Redis(connection_pool=pool)
```

### Caching Strategies (HIGH)

#### Missing Application Cache

```python
# BAD: No caching of expensive operations
def get_user_permissions(user_id):
    user = db.get_user(user_id)          # DB call
    roles = db.get_roles(user.role_ids)  # Another DB call
    return compute_permissions(roles)     # CPU-intensive

# GOOD: Multi-layer caching
from functools import lru_cache
from cachetools import TTLCache

# In-memory cache with TTL
_permission_cache = TTLCache(maxsize=10000, ttl=300)

def get_user_permissions(user_id):
    if user_id in _permission_cache:
        return _permission_cache[user_id]

    user = db.get_user(user_id)
    roles = db.get_roles(user.role_ids)
    permissions = compute_permissions(roles)

    _permission_cache[user_id] = permissions
    return permissions
```

#### Missing Distributed Cache

```python
# BAD: Local cache only - doesn't work with multiple instances
_cache = {}  # Each instance has its own cache!

# GOOD: Redis for distributed caching
import redis
import json

redis_client = redis.Redis(connection_pool=pool)

def get_user_permissions(user_id: str) -> dict:
    cache_key = f"permissions:{user_id}"

    # Try cache first
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)

    # Compute and cache
    permissions = compute_permissions(user_id)
    redis_client.setex(cache_key, 300, json.dumps(permissions))
    return permissions
```

#### Missing Cache Invalidation

```python
# BAD: Cache never invalidated
@lru_cache(maxsize=1000)
def get_user(user_id):
    return db.get_user(user_id)

def update_user(user_id, data):
    db.update_user(user_id, data)
    # Cache still has stale data!

# GOOD: Explicit invalidation
def update_user(user_id, data):
    db.update_user(user_id, data)
    get_user.cache_clear()  # Or more granular invalidation
    redis_client.delete(f"user:{user_id}")
```

### Stateless Design (CRITICAL)

#### Session State in Memory

```python
# BAD: In-memory sessions - doesn't scale horizontally
sessions = {}  # Lost on restart, not shared between instances!

@app.route("/login")
def login():
    session_id = create_session_id()
    sessions[session_id] = {"user_id": user.id}
    return session_id

# GOOD: External session store
from redis import Redis

redis = Redis(connection_pool=pool)

@app.route("/login")
def login():
    session_id = create_session_id()
    redis.setex(
        f"session:{session_id}",
        3600,
        json.dumps({"user_id": user.id})
    )
    return session_id
```

#### Local File Storage

```python
# BAD: Local filesystem - not shared across instances
def save_upload(file):
    path = f"/uploads/{file.filename}"
    file.save(path)
    return path

# GOOD: Object storage (S3, MinIO, etc.)
import boto3

s3 = boto3.client('s3')

def save_upload(file):
    key = f"uploads/{uuid4()}/{file.filename}"
    s3.upload_fileobj(file, BUCKET_NAME, key)
    return f"s3://{BUCKET_NAME}/{key}"
```

#### Instance-Specific State

```python
# BAD: Background tasks tied to instance
scheduled_jobs = []  # Dies with instance!

def schedule_job(job):
    scheduled_jobs.append(job)

# GOOD: Distributed task queue
from celery import Celery

celery = Celery('tasks', broker='redis://localhost')

@celery.task
def process_job(job_data):
    # Runs on any worker
    return do_work(job_data)

def schedule_job(job):
    process_job.delay(job)
```

### Rate Limiting (HIGH)

#### Missing Rate Limiting

```python
# BAD: No rate limiting - vulnerable to abuse
@app.route("/api/search")
def search():
    return db.search(request.args["q"])  # Can be hammered!

# GOOD: Rate limiting with Redis
from limits import parse
from limits.storage import RedisStorage
from limits.strategies import MovingWindowRateLimiter

storage = RedisStorage("redis://localhost")
limiter = MovingWindowRateLimiter(storage)
rate = parse("100/minute")

@app.route("/api/search")
def search():
    client_ip = request.remote_addr
    if not limiter.hit(rate, client_ip):
        abort(429, "Rate limit exceeded")
    return db.search(request.args["q"])
```

#### Missing Backpressure

```python
# BAD: Unbounded queue - can exhaust memory
work_queue = []

def add_work(item):
    work_queue.append(item)  # Grows forever if workers are slow!

# GOOD: Bounded queue with backpressure
from queue import Queue, Full

work_queue = Queue(maxsize=1000)

def add_work(item):
    try:
        work_queue.put(item, timeout=5)
    except Full:
        raise ServiceOverloaded("Queue is full, try again later")
```

### Pagination & Batching (MEDIUM)

#### Cursor-Based Pagination

```python
# BAD: Returns all records
@app.route("/users")
def list_users():
    return db.query(User).all()  # 1 million users = OOM!

# GOOD: Cursor-based pagination
@app.route("/users")
def list_users():
    cursor = request.args.get("cursor")
    limit = min(int(request.args.get("limit", 100)), 1000)

    query = db.query(User).order_by(User.id)
    if cursor:
        query = query.filter(User.id > cursor)

    users = query.limit(limit + 1).all()
    next_cursor = users[-1].id if len(users) > limit else None

    return {
        "users": users[:limit],
        "next_cursor": next_cursor,
    }
```

#### Batch Processing

```python
# BAD: Processing one at a time
def send_notifications(user_ids):
    for user_id in user_ids:
        user = db.get_user(user_id)      # N queries
        send_email(user.email)            # N API calls

# GOOD: Batch processing
def send_notifications(user_ids):
    # Batch fetch
    users = db.query(User).filter(User.id.in_(user_ids)).all()

    # Batch send
    emails = [{"to": u.email, "body": msg} for u in users]
    email_service.send_batch(emails)
```

### Horizontal Scaling Blockers (HIGH)

#### Hardcoded Single Instance Assumptions

```python
# BAD: Assumes single instance
class Counter:
    _count = 0  # Shared across requests in ONE instance only

    @classmethod
    def increment(cls):
        cls._count += 1
        return cls._count

# GOOD: Distributed counter
def increment_counter(name: str) -> int:
    return redis_client.incr(f"counter:{name}")
```

#### Cron Jobs Without Coordination

```python
# BAD: Cron runs on every instance
@scheduler.scheduled_job('interval', minutes=5)
def cleanup_job():
    delete_old_records()  # Runs 5 times if 5 instances!

# GOOD: Distributed lock
from redis.lock import Lock

@scheduler.scheduled_job('interval', minutes=5)
def cleanup_job():
    lock = Lock(redis_client, "cleanup_lock", timeout=300)
    if lock.acquire(blocking=False):
        try:
            delete_old_records()
        finally:
            lock.release()
```

#### Singleton Services

```python
# BAD: Only one instance can run
class PaymentProcessor:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

# GOOD: Stateless service
class PaymentProcessor:
    def __init__(self, config: PaymentConfig):
        self.config = config

    def process(self, payment: Payment) -> Result:
        # No instance state, can run anywhere
        return self._call_gateway(payment)
```

### External Service Resilience (HIGH)

#### Missing Circuit Breaker

```python
# BAD: Keeps hitting failing service
def call_payment_api(data):
    return requests.post(PAYMENT_URL, json=data)  # Cascading failures!

# GOOD: Circuit breaker pattern
from circuitbreaker import circuit

@circuit(failure_threshold=5, recovery_timeout=30)
def call_payment_api(data):
    response = requests.post(PAYMENT_URL, json=data, timeout=10)
    response.raise_for_status()
    return response.json()
```

#### Missing Timeouts

```python
# BAD: Can hang forever
response = requests.get(external_api)

# GOOD: Always set timeouts
response = requests.get(
    external_api,
    timeout=(3.05, 27),  # (connect, read)
)
```

#### Missing Retry with Backoff

```python
# BAD: No retry or immediate retry
def fetch_data():
    return requests.get(url)

# GOOD: Exponential backoff
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
)
def fetch_data():
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()
```

### Database Scaling Patterns (MEDIUM)

#### Read Replicas

```python
# BAD: All queries to primary
def get_user(user_id):
    return primary_db.query(User).get(user_id)

def list_users():
    return primary_db.query(User).all()  # Reads on primary!

# GOOD: Route reads to replicas
def get_user(user_id):
    return replica_db.query(User).get(user_id)

def update_user(user_id, data):
    primary_db.query(User).filter_by(id=user_id).update(data)
```

#### Missing Query Limits

```python
# BAD: Unbounded queries
def search(term):
    return db.query(Item).filter(Item.name.like(f"%{term}%")).all()

# GOOD: Always limit
def search(term, limit=100):
    return (
        db.query(Item)
        .filter(Item.name.like(f"%{term}%"))
        .limit(limit)
        .all()
    )
```

---
