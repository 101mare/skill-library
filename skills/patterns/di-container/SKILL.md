---
name: di-container
description: |
  Guides implementation of Dependency Injection containers using Python Protocols.
  Use when designing service wiring, managing component lifecycle, or decoupling modules.
  Recognizes: "di-container", "dependency injection", "container pattern", "service wiring",
  "inversion of control", "IoC container", "lazy initialization", "protocol-based DI"
---

# DI Container Pattern

Dependency Injection containers with Python Protocols for decoupled, testable applications.

## When to Use

- Application has 5+ services that depend on each other
- Services need lifecycle management (startup/shutdown)
- You want to swap implementations (e.g., different backends)
- Testing requires replacing real services with mocks

## When NOT to Use

- Small scripts or single-module apps
- Only 2-3 services with simple wiring
- No need for lifecycle management

## Container Skeleton

```python
from typing import Protocol

# 1. Define interfaces
class LlmClient(Protocol):
    def complete(self, prompt: str) -> str: ...

class Storage(Protocol):
    def save(self, key: str, data: bytes) -> None: ...
    def load(self, key: str) -> bytes | None: ...

# 2. Container with lazy properties
class Container:
    def __init__(self, config: AppConfig):
        self._config = config
        self._llm_client: LlmClient | None = None
        self._storage: Storage | None = None
        self._classifier: Classifier | None = None

    @property
    def llm_client(self) -> LlmClient:
        if self._llm_client is None:
            self._llm_client = self._create_llm_client()
        return self._llm_client

    @property
    def storage(self) -> Storage:
        if self._storage is None:
            self._storage = self._create_storage()
        return self._storage

    @property
    def classifier(self) -> Classifier:
        if self._classifier is None:
            self._classifier = Classifier(
                llm=self.llm_client,
                config=self._config,
            )
        return self._classifier

    def _create_llm_client(self) -> LlmClient:
        """Factory: select implementation based on config."""
        match self._config.provider.type:
            case "ollama":
                from .providers.ollama import OllamaClient
                return OllamaClient(self._config.provider.ollama)
            case "openai":
                from .providers.openai import OpenAIClient
                return OpenAIClient(self._config.provider.openai)
            case _:
                raise ConfigError(f"Unknown provider: {self._config.provider.type}")

    def _create_storage(self) -> Storage:
        from .storage.filesystem import FileStorage
        return FileStorage(self._config.storage.path)
```

## Provider Factory Pattern

```python
# providers/__init__.py
def create_provider(config: ProviderConfig) -> ModelProvider:
    """Factory function for provider selection."""
    match config.type:
        case "ollama":
            from .ollama.provider import OllamaProvider
            return OllamaProvider(config.ollama)
        case "vllm":
            from .vllm.provider import VllmProvider
            return VllmProvider(config.vllm)
        case _:
            raise ConfigError(f"Unknown provider: {config.type}")
```

Key principles:
- Import provider-specific code **inside** the match case (lazy import)
- Service code never imports provider implementations directly
- Only the container/factory knows about concrete types

## Lifecycle Management

```python
class Container:
    def startup(self) -> None:
        """Initialize services that need explicit startup."""
        logger.info("Container starting up")
        self._provider = create_provider(self._config.provider)
        self._provider.startup()
        logger.info("Container ready")

    def shutdown(self) -> None:
        """Clean up resources."""
        logger.info("Container shutting down")
        if self._provider:
            self._provider.shutdown()
        if self._storage:
            self._storage.close()
        logger.info("Container shutdown complete")

    def __enter__(self) -> "Container":
        self.startup()
        return self

    def __exit__(self, *exc) -> None:
        self.shutdown()
```

Usage:
```python
config = load_config()
with Container(config) as container:
    result = container.classifier.classify(document)
```

## Testing with DI

```python
from unittest.mock import Mock

def test_classifier_with_mock():
    # Create mock that satisfies Protocol
    mock_llm = Mock(spec=LlmClient)
    mock_llm.complete.return_value = '{"category": "invoice"}'

    # Inject directly -- no container needed for unit tests
    classifier = Classifier(llm=mock_llm, config=test_config)
    result = classifier.classify("some document")

    assert result.category == "invoice"
    mock_llm.complete.assert_called_once()

def test_with_container():
    # For integration tests, use the real container
    config = load_config("test_config.yaml")
    with Container(config) as container:
        result = container.classifier.classify("test doc")
        assert result is not None
```

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Service Locator | `container.get("service_name")` -- no type safety | Use typed properties |
| Global container | `global_container.service` -- hidden dependency | Pass container or services explicitly |
| Over-abstraction | Protocol for a single implementation | Only abstract when 2+ implementations exist |
| Eager initialization | All services created at startup | Use lazy properties |
| Circular dependencies | Service A needs B, B needs A | Extract shared logic to C |
| Container in business logic | `def process(container)` | Inject specific services, not the container |

## Checklist

- [ ] Interfaces defined as Protocols (not concrete classes)
- [ ] Container uses lazy properties
- [ ] Provider selection via factory (match/case or dict)
- [ ] Provider-specific imports only inside factory
- [ ] Lifecycle methods (startup/shutdown)
- [ ] Context manager support (__enter__/__exit__)
- [ ] Services accept Protocols, not concrete types
- [ ] Unit tests inject mocks directly (no container)
