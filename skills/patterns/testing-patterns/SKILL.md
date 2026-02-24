---
name: testing-patterns
description: |
  pytest patterns, fixtures, mocking, parametrize, and property-based testing.
  Use when writing tests, improving coverage, or setting up test infrastructure.
  Recognizes: "testing-patterns", "write tests", "pytest patterns", "how to mock",
  "test fixtures", "parametrize", "property-based testing", "test organization",
  "improve coverage", "hypothesis tests"
---

# Testing Patterns

pytest conventions, mocking strategies, and property-based testing for Python.

## Test File Organization

```
tests/
├── conftest.py              # Shared fixtures (project-wide)
├── test_pipeline.py         # Integration tests
├── test_services/
│   ├── conftest.py          # Service-specific fixtures
│   ├── test_classifier.py
│   └── test_validators.py
├── test_providers/
│   ├── conftest.py
│   └── test_ollama.py
└── test_extractors/
    └── test_pdf.py
```

Rules:
- One test file per module (test_classifier.py tests classifier.py)
- Shared fixtures in conftest.py at the appropriate scope level
- conftest.py is auto-discovered — no imports needed

## Naming Conventions

```python
# Test functions: test_<what>_<condition>_<expected>
def test_classify_valid_input_returns_case_type():
def test_classify_empty_text_returns_unknown():
def test_validate_iban_invalid_checksum_returns_none():

# Fixture functions: descriptive nouns
@pytest.fixture
def sample_config():
@pytest.fixture
def mock_llm_client():
```

## Fixtures

### Basic Fixtures

```python
import pytest

@pytest.fixture
def config():
    """Fresh config for each test."""
    return PipelineConfig(provider=ProviderConfig(type="ollama"))

@pytest.fixture
def mock_client():
    """Mock LLM client with default response."""
    client = MagicMock(spec=LlmClient)
    client.complete.return_value = LlmResult(text='{"ca_type": "KVW"}')
    return client

@pytest.fixture
def classifier(config, mock_client):
    """Classifier wired with mock dependencies."""
    return CaseClassifier(config, mock_client)
```

### Fixture Scopes

```python
# Default: function (new instance per test)
@pytest.fixture
def fresh_data():
    return {"key": "value"}

# session: one instance for entire test run (expensive setup)
@pytest.fixture(scope="session")
def database_schema():
    return create_schema()

# module: one instance per test file
@pytest.fixture(scope="module")
def loaded_model():
    return load_model()
```

Rule: Only use broader scopes for genuinely expensive, read-only resources. Mutable fixtures must be function-scoped.

### Factory Fixtures

```python
@pytest.fixture
def make_config():
    """Factory: create configs with custom overrides."""
    def _make(**overrides):
        defaults = {
            "provider": ProviderConfig(type="ollama"),
            "llm": LlmConfig(temperature=0.1),
        }
        defaults.update(overrides)
        return PipelineConfig(**defaults)
    return _make

def test_high_temperature(make_config):
    config = make_config(llm=LlmConfig(temperature=0.9))
    assert config.llm.temperature == 0.9
```

### tmp_path (built-in)

```python
def test_file_processing(tmp_path):
    """tmp_path gives a unique temporary directory per test."""
    test_file = tmp_path / "document.txt"
    test_file.write_text("Hello World")

    result = process_file(test_file)
    assert result.text == "Hello World"

def test_case_directory(tmp_path):
    case_dir = tmp_path / "case_001"
    case_dir.mkdir()
    (case_dir / "doc.pdf").write_bytes(b"%PDF-fake")

    files = list_input_files(case_dir)
    assert len(files) == 1
```

## Mocking with unittest.mock

### MagicMock with spec

```python
from unittest.mock import MagicMock, patch, call

# spec= enforces the interface — typos raise AttributeError
mock_client = MagicMock(spec=LlmClient)
mock_client.complete.return_value = LlmResult(text='{"ca_type": "KVW"}')

# This would raise: mock_client.nonexistent_method()
```

### Patching

```python
# Patch where the name is USED, not where it's defined
@patch("core.pipeline.Container")
def test_pipeline_creates_container(MockContainer):
    mock_instance = MockContainer.return_value
    mock_instance.classifier = MagicMock()
    mock_instance.vision_engine = None

    run_all_cases(config)

    MockContainer.assert_called_once_with(config)
    mock_instance.startup.assert_called_once()
    mock_instance.shutdown.assert_called_once()

# Context manager form
def test_with_patched_module():
    with patch("services.classifier.build_case_prompt") as mock_prompt:
        mock_prompt.return_value = "test prompt"
        result = classifier.classify(text)
        mock_prompt.assert_called_once()
```

### Side Effects

```python
# Raise exception
mock_client.complete.side_effect = ModelConnectionError("offline")

# Return different values on successive calls
mock_client.complete.side_effect = [
    LlmResult(text="first"),
    LlmResult(text="second"),
    ModelTimeoutError("timeout"),
]

# Custom function
mock_client.complete.side_effect = lambda prompt, **kw: LlmResult(text=prompt[:10])
```

### Asserting Calls

```python
# Called at all
mock.assert_called()
mock.assert_called_once()

# Called with specific args
mock.assert_called_with("expected_arg", key="value")
mock.assert_called_once_with("expected_arg")

# Multiple calls in order
mock.assert_has_calls([
    call("first"),
    call("second"),
], any_order=False)

# Not called
mock.assert_not_called()

# Check call count
assert mock.call_count == 3
```

## Parametrize

```python
@pytest.mark.parametrize("input_text, expected_type", [
    ("Steuererklärung 2024", "KVW-Steuer"),
    ("IBAN DE89 3704", "KVW-Bank"),
    ("", "UNKNOWN"),
])
def test_classify_returns_correct_type(classifier, input_text, expected_type):
    result = classifier.classify(input_text)
    assert result.ca_type == expected_type

# IDs for readable test output
@pytest.mark.parametrize("iban, valid", [
    pytest.param("DE89370400440532013000", True, id="valid-german"),
    pytest.param("DE00000000000000000000", False, id="invalid-checksum"),
    pytest.param("XX12345", False, id="wrong-country"),
    pytest.param("", False, id="empty"),
])
def test_iban_validation(iban, valid):
    result = validate_iban(iban)
    assert result.is_valid == valid
```

### Parametrize + Fixtures

```python
@pytest.mark.parametrize("provider_type", ["ollama", "vllm"])
def test_provider_creation(provider_type, make_config):
    config = make_config(provider=ProviderConfig(type=provider_type))
    provider = create_provider(config)
    assert provider is not None
```

## Exception Testing

```python
def test_unknown_extension_raises():
    with pytest.raises(ValueError, match="Unsupported file type"):
        extract(Path("file.xyz"))

def test_connection_error_contains_host():
    with pytest.raises(ModelConnectionError) as exc_info:
        client.complete("test")
    assert "localhost" in str(exc_info.value)
```

## Property-Based Testing (Hypothesis)

Test properties that should hold for ALL valid inputs, not just hand-picked examples.

```python
from hypothesis import given, strategies as st, assume, settings

# Text truncation never exceeds max length
@given(text=st.text(min_size=0, max_size=10000), max_len=st.integers(1, 5000))
def test_truncate_never_exceeds_max(text, max_len):
    result = truncate_text(text, max_len)
    assert len(result) <= max_len

# IBAN validator never crashes on arbitrary input
@given(text=st.text(max_size=100))
def test_iban_validator_handles_any_input(text):
    result = validate_iban(text)
    assert result is None or isinstance(result, str)

# JSON repair always returns valid JSON or raises
@given(text=st.text(max_size=500))
def test_json_repair_returns_valid_or_raises(text):
    try:
        result = repair_json(text)
        json.loads(result)  # Must be valid if returned
    except JsonRepairError:
        pass  # Expected for unrepairable input

# Confidence scorer output is always in [0.0, 1.0]
@given(
    llm_conf=st.floats(0.0, 1.0),
    ext_conf=st.floats(0.0, 1.0),
    val_score=st.floats(0.0, 1.0),
)
def test_confidence_always_in_range(llm_conf, ext_conf, val_score):
    result = compute_confidence(llm_conf, ext_conf, val_score)
    assert 0.0 <= result <= 1.0
```

### Hypothesis Strategies

```python
# Primitives
st.integers(min_value=0, max_value=100)
st.floats(min_value=0.0, max_value=1.0, allow_nan=False)
st.text(min_size=1, max_size=200, alphabet=st.characters(whitelist_categories=("L", "N")))
st.booleans()
st.none()

# Collections
st.lists(st.integers(), min_size=1, max_size=50)
st.dictionaries(st.text(min_size=1), st.integers())

# Composite (custom data)
@st.composite
def case_results(draw):
    return CaseResult(
        ca_type=draw(st.sampled_from(["KVW-Steuer", "KVW-Bank", "UNKNOWN"])),
        confidence=draw(st.floats(0.0, 1.0)),
        entities=draw(st.dictionaries(st.text(min_size=1), st.text())),
    )

@given(result=case_results())
def test_result_serialization_roundtrip(result):
    json_str = result.to_json()
    restored = CaseResult.from_json(json_str)
    assert restored == result
```

### When to Use Hypothesis

- Functions that transform arbitrary input (parsers, validators, formatters)
- Mathematical properties (idempotency, commutativity, roundtrips)
- "Should never crash" guarantees
- Edge case discovery (empty strings, unicode, huge numbers)

NOT for: Testing specific business rules with exact inputs → use parametrize.

## Integration Test Pattern

```python
class TestPipelineIntegration(unittest.TestCase):
    """Test the full pipeline with mocked provider."""

    def setUp(self):
        self.config = _build_config()
        self.mock_provider = MagicMock(spec=ModelProvider)
        self.mock_client = MagicMock(spec=LlmClient)
        self.mock_provider.create_client.return_value = self.mock_client

    @patch("core.pipeline.Container")
    def test_full_case_processing(self, MockContainer):
        container = MockContainer.return_value
        container.classifier = CaseClassifier(self.config, self.mock_client)
        container.vision_engine = None

        self.mock_client.complete.return_value = LlmResult(
            text='{"ca_type": "KVW-Steuer", "confidence": 0.9}'
        )

        result = run_case(self.config, case_dir, container)
        assert result.ca_type == "KVW-Steuer"
```

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Testing implementation, not behavior | Brittle tests break on refactor | Assert outputs and side effects, not internals |
| Mock without `spec=` | Mocks accept any attribute silently | Always use `spec=InterfaceName` |
| Patching where defined, not where used | Patch has no effect | Patch the import path in the consuming module |
| Shared mutable state between tests | Tests pollute each other | Function-scoped fixtures, fresh instances |
| `time.sleep()` in tests | Slow tests | Mock time or use deterministic waits |
| Giant test functions | Hard to diagnose failures | One assertion focus per test |
| No parametrize for similar cases | Duplicated test code | Use `@pytest.mark.parametrize` |
| Testing third-party library behavior | Not your responsibility | Mock at the boundary |

## Checklist

- [ ] Tests named `test_<what>_<condition>_<expected>`
- [ ] Mocks use `spec=` for type safety
- [ ] Fixtures in conftest.py at appropriate scope
- [ ] `@pytest.mark.parametrize` for similar test cases
- [ ] `pytest.raises` for expected exceptions (with `match=`)
- [ ] `tmp_path` for file system tests (no hardcoded paths)
- [ ] Factory fixtures for configurable test data
- [ ] No `time.sleep()` or network calls in unit tests
- [ ] Integration tests clearly separated from unit tests
