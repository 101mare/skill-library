# Protocol Design — Examples

Runnable Python examples showing `typing.Protocol` in real-world scenarios. See [SKILL.md](SKILL.md) for basics of defining protocols, composition, generics, and anti-patterns.

## Table of Contents

- [Notification Backends](#notification-backends)
- [Generic Repository](#generic-repository)
- [Protocol Composition](#protocol-composition)

---

## Notification Backends

A `Notifier` protocol with concrete backends. No class inherits from the protocol -- they satisfy it through structural subtyping alone.

```python
from __future__ import annotations
from typing import Protocol
from dataclasses import dataclass

@dataclass
class Message:
    recipient: str
    subject: str
    body: str

class Notifier(Protocol):
    """Any class with a matching send() is a valid Notifier."""
    def send(self, msg: Message) -> bool: ...

# --- Backends don't import or inherit Notifier ---
class EmailBackend:
    def __init__(self, smtp_host: str) -> None:
        self.smtp_host = smtp_host

    def send(self, msg: Message) -> bool:
        print(f"[EMAIL via {self.smtp_host}] To: {msg.recipient} | {msg.subject}")
        return True

class SlackBackend:
    def __init__(self, webhook_url: str) -> None:
        self.webhook_url = webhook_url

    def send(self, msg: Message) -> bool:
        print(f"[SLACK] #{msg.recipient} | {msg.subject}: {msg.body[:50]}")
        return True

# --- Dispatch uses only the Protocol type ---
def broadcast(notifiers: list[Notifier], msg: Message) -> dict[str, bool]:
    return {type(n).__name__: n.send(msg) for n in notifiers}

backends: list[Notifier] = [
    EmailBackend("smtp.example.com"),
    SlackBackend("https://hooks.slack.com/xxx"),
]
results = broadcast(backends, Message("team", "Deploy v2.1", "Deployed to prod."))
print(results)  # {'EmailBackend': True, 'SlackBackend': True}
```

Adding a new backend requires zero changes to existing code -- it just needs a matching `send` method.

---

## Generic Repository

A typed repository protocol with CRUD operations. The generic parameter ensures `Repository[User]` cannot accidentally return `Product` objects.

```python
from __future__ import annotations
from typing import Protocol, TypeVar
from dataclasses import dataclass

T = TypeVar("T")

class Repository(Protocol[T]):
    def get(self, id: str) -> T | None: ...
    def save(self, item: T) -> None: ...
    def delete(self, id: str) -> bool: ...
    def list_all(self) -> list[T]: ...

@dataclass
class User:
    id: str
    name: str
    email: str

class InMemoryUserRepo:
    """Satisfies Repository[User] without inheriting it."""
    def __init__(self) -> None:
        self._store: dict[str, User] = {}

    def get(self, id: str) -> User | None:
        return self._store.get(id)

    def save(self, item: User) -> None:
        self._store[item.id] = item

    def delete(self, id: str) -> bool:
        return self._store.pop(id, None) is not None

    def list_all(self) -> list[User]:
        return list(self._store.values())

# --- Service depends on the protocol, not the implementation ---
def export_users(repo: Repository[User]) -> list[str]:
    return [f"{u.name} <{u.email}>" for u in repo.list_all()]

repo = InMemoryUserRepo()
repo.save(User("1", "Alice", "alice@example.com"))
repo.save(User("2", "Bob", "bob@example.com"))
print(export_users(repo))  # ['Alice <alice@example.com>', 'Bob <bob@example.com>']
print(repo.delete("1"))    # True
print(repo.delete("999"))  # False
```

`export_users` works with any `Repository[User]` -- in-memory, SQL-backed, or a test mock. The generic parameter gives type checkers enough information to catch misuse.

---

## Protocol Composition

Small, focused protocols combine into richer contracts. Each function requests only the capability it needs.

```python
from __future__ import annotations
from typing import Protocol, runtime_checkable

@runtime_checkable
class Readable(Protocol):
    def read(self) -> str: ...

@runtime_checkable
class Writable(Protocol):
    def write(self, data: str) -> None: ...

class Closeable(Protocol):
    def close(self) -> None: ...

# --- Composed protocols ---
class ReadWritable(Readable, Writable, Protocol):
    ...

class ManagedStream(ReadWritable, Closeable, Protocol):
    """Full stream: read + write + lifecycle."""
    ...

# --- StringBuffer satisfies ManagedStream without knowing it ---
class StringBuffer:
    def __init__(self) -> None:
        self._buf: list[str] = []
        self._closed = False

    def read(self) -> str:
        return "".join(self._buf)

    def write(self, data: str) -> None:
        if self._closed:
            raise RuntimeError("write to closed buffer")
        self._buf.append(data)

    def close(self) -> None:
        self._closed = True

# --- Functions accept the narrowest protocol they need ---
def dump_contents(source: Readable) -> None:
    print(f"Contents: {source.read()}")

def process_stream(stream: ManagedStream) -> str:
    stream.write("hello ")
    stream.write("world")
    result = stream.read()
    stream.close()
    return result

buf = StringBuffer()
print(process_stream(buf))  # hello world

# runtime_checkable lets us verify capabilities dynamically
print(isinstance(buf, Readable))          # True
print(isinstance(buf, Writable))          # True
print(isinstance("plain str", Readable))  # False
```

`dump_contents` accepts anything `Readable`, while `process_stream` requires the full `ManagedStream`. Functions that don't need `close()` should not demand it.
