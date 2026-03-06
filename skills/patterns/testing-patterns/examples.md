# Testing Patterns — Examples

Complete test suites showing pytest patterns in practice. See [SKILL.md](SKILL.md) for individual patterns reference.

## Table of Contents

- [Classifier Test Suite](#classifier-test-suite)
- [Property-Based JSON Tests](#property-based-json-tests)
- [Integration with tmp_path](#integration-with-tmp_path)

---

## Classifier Test Suite

A complete test suite for a `SentimentClassifier`: unit tests, integration, and parametrized edge cases.

### Shared Fixtures (conftest.py)

```python
import pytest
from unittest.mock import MagicMock
from classifier import SentimentClassifier, Tokenizer, ScoringEngine

@pytest.fixture
def tokenizer():
    return Tokenizer(language="en")

@pytest.fixture
def mock_scorer():
    scorer = MagicMock(spec=ScoringEngine)
    scorer.score.return_value = {"positive": 0.8, "negative": 0.1, "neutral": 0.1}
    return scorer

@pytest.fixture
def classifier(tokenizer, mock_scorer):
    return SentimentClassifier(tokenizer=tokenizer, scorer=mock_scorer)
```

### Unit Tests

```python
class TestTokenizer:
    def test_tokenize_splits_on_whitespace(self, tokenizer):
        assert tokenizer.tokenize("hello world") == ["hello", "world"]

    def test_tokenize_lowercases(self, tokenizer):
        assert tokenizer.tokenize("Hello WORLD") == ["hello", "world"]

    def test_tokenize_empty_string_returns_empty_list(self, tokenizer):
        assert tokenizer.tokenize("") == []
```

### Integration Test

```python
class TestClassifierPipeline:
    def test_end_to_end_positive(self, classifier, mock_scorer):
        result = classifier.classify("This product is excellent")
        assert result.label == "positive"
        assert result.confidence > 0.5
        mock_scorer.score.assert_called_once()

    def test_end_to_end_negative(self, classifier, mock_scorer):
        mock_scorer.score.return_value = {"positive": 0.05, "negative": 0.9, "neutral": 0.05}
        result = classifier.classify("Terrible, broken")
        assert result.label == "negative"
```

### Parametrized Edge Cases

```python
@pytest.mark.parametrize("text, expected_label", [
    pytest.param("great!", "positive", id="single-word-positive"),
    pytest.param("awful", "negative", id="single-word-negative"),
    pytest.param("meeting at 3pm", "neutral", id="factual-neutral"),
    pytest.param("   ", "neutral", id="whitespace-only"),
])
def test_classify_edge_cases(classifier, mock_scorer, text, expected_label):
    mock_scorer.score.return_value = {
        "positive": 0.5 if expected_label == "positive" else 0.1,
        "negative": 0.5 if expected_label == "negative" else 0.1,
        "neutral": 0.5 if expected_label == "neutral" else 0.1,
    }
    result = classifier.classify(text)
    assert result.label == expected_label
```

---

## Property-Based JSON Tests

Using hypothesis to verify a JSON serialization layer handles arbitrary data.

```python
import json
from hypothesis import given, settings, strategies as st

def serialize(obj: object) -> str:
    return json.dumps(obj, default=_default_handler)

def deserialize(text: str) -> object:
    return json.loads(text)
```

Build a recursive strategy that generates any valid JSON structure:

```python
json_primitives = st.one_of(
    st.none(), st.booleans(),
    st.integers(min_value=-(2**53), max_value=2**53),
    st.floats(allow_nan=False, allow_infinity=False),
    st.text(max_size=100),
)
json_values = st.recursive(
    json_primitives,
    lambda children: st.one_of(
        st.lists(children, max_size=5),
        st.dictionaries(st.text(max_size=10), children, max_size=5),
    ),
    max_leaves=15,
)
```

### Roundtrip and Idempotency Properties

```python
@given(data=json_values)
@settings(max_examples=200)
def test_roundtrip_preserves_data(data):
    assert deserialize(serialize(data)) == data

@given(data=json_values)
def test_serialize_always_returns_valid_json(data):
    json.loads(serialize(data))  # must not raise

@given(data=json_values)
def test_double_roundtrip_is_stable(data):
    first = serialize(data)
    second = serialize(deserialize(first))
    assert first == second
```

Hypothesis generates thousands of random JSON structures — nested dicts, unicode, empty containers — catching edge cases hand-written tests miss.

---

## Integration with tmp_path

File-based operations tested with `tmp_path` for full isolation. No test touches the real filesystem.

```python
import csv
from pathlib import Path

class ReportGenerator:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate(self, title: str, rows: list[dict]) -> Path:
        path = self.output_dir / f"{title}.csv"
        if not rows:
            path.write_text("")
            return path
        with open(path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        return path
```

### Tests

```python
class TestReportGenerator:
    @pytest.fixture
    def generator(self, tmp_path):
        return ReportGenerator(output_dir=tmp_path / "reports")

    def test_generate_creates_csv_with_headers(self, generator):
        path = generator.generate("grades", [{"name": "Alice", "score": "95"}])
        assert path.exists()
        assert "name,score" in path.read_text()

    def test_generate_empty_rows_creates_empty_file(self, generator):
        path = generator.generate("empty", [])
        assert path.read_text() == ""

    def test_multiple_reports_coexist(self, generator):
        generator.generate("first", [{"x": "1"}])
        generator.generate("second", [{"y": "2"}])
        assert len(list(generator.output_dir.glob("*.csv"))) == 2

    def test_content_readable_by_csv_module(self, generator):
        path = generator.generate("data", [{"id": "1", "val": "hello"}])
        with open(path) as f:
            rows = list(csv.DictReader(f))
        assert rows[0]["val"] == "hello"
```

Each test gets its own `tmp_path`, automatically cleaned up by pytest. No shared state, no cleanup code.