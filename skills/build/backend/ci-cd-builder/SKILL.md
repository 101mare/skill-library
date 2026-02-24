---
name: ci-cd-builder
description: |
  GitHub Actions CI/CD pipeline scaffolding: pytest, linting, Docker build, release.
  Use when setting up CI/CD for Python projects, adding pipelines, or configuring GitHub Actions.
  Recognizes: "ci-cd-builder", "CI/CD", "GitHub Actions", "pipeline", "add CI",
  "setup CI/CD", "continuous integration", "automate tests", "build pipeline",
  "release workflow", "deploy pipeline"
---

# CI/CD Builder

GitHub Actions pipeline scaffolding for Python projects. From basic test pipeline to full release workflow.

## File Structure

```
.github/
├── workflows/
│   ├── ci.yml              # Main CI: test + lint on every push/PR
│   ├── release.yml         # Release: build + publish on tag
│   └── docker.yml          # Docker: build + push image (optional)
└── dependabot.yml          # Dependency updates (optional)
```

---

## Core Pipeline: CI

The foundation. Runs on every push and PR.

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Cache pip
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements*.txt') }}
          restore-keys: ${{ runner.os }}-pip-

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e ".[dev]"

      - name: Lint with ruff
        run: |
          ruff check .
          ruff format --check .

      - name: Run tests
        run: pytest -q --tb=line

  type-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -e ".[dev]"
      - name: Type check with mypy
        run: mypy src/ --ignore-missing-imports
```

### Adapting the CI Pipeline

| Project uses... | Change |
|---|---|
| `requirements.txt` instead of `pyproject.toml` | Replace `pip install -e ".[dev]"` with `pip install -r requirements.txt -r requirements-dev.txt` |
| Single Python version | Remove `strategy.matrix`, hardcode version |
| No type checking | Remove `type-check` job |
| System dependencies (LibreOffice, etc.) | Add `apt-get install` step before pip |
| Private packages | Add `pip install --extra-index-url` with secrets |

---

## Lint Job: Ruff

Ruff replaces flake8, isort, black, and pylint in one tool.

```yaml
# Standalone lint job (alternative to inline step)
lint:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: astral-sh/ruff-action@v3
      with:
        args: "check"
    - uses: astral-sh/ruff-action@v3
      with:
        args: "format --check"
```

### Ruff Config (pyproject.toml)

```toml
[tool.ruff]
target-version = "py311"
line-length = 120

[tool.ruff.lint]
select = ["E", "F", "W", "I", "UP", "B", "SIM"]
ignore = ["E501"]  # line length handled by formatter

[tool.ruff.format]
quote-style = "double"
```

---

## Docker Build Pipeline

For projects with Docker deployment.

```yaml
# .github/workflows/docker.yml
name: Docker

on:
  push:
    tags: ["v*"]
  workflow_dispatch:

permissions:
  contents: read
  packages: write

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Log in to Container registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

---

## Release Pipeline

Triggered on version tags. Runs tests first, then builds.

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags: ["v*"]

permissions:
  contents: write

jobs:
  test:
    uses: ./.github/workflows/ci.yml

  release:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v2
        with:
          generate_release_notes: true
```

### For PyPI Publishing

```yaml
  publish:
    needs: test
    runs-on: ubuntu-latest
    environment: release
    permissions:
      id-token: write  # trusted publishing
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install build
      - run: python -m build
      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
```

---

## Dependabot

Automated dependency updates.

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: pip
    directory: "/"
    schedule:
      interval: weekly
    open-pull-requests-limit: 5

  - package-ecosystem: github-actions
    directory: "/"
    schedule:
      interval: weekly
```

---

## Secrets Management

```yaml
# Reference secrets in workflows
env:
  API_KEY: ${{ secrets.API_KEY }}

# Set secrets via CLI
# gh secret set API_KEY --body "your-key"

# Environment-specific secrets (for production deploys)
jobs:
  deploy:
    environment: production  # requires approval
    steps:
      - run: echo "Using ${{ secrets.PROD_DB_URL }}"
```

### Never Do

- Never hardcode secrets in workflow files
- Never echo secrets in logs (`run: echo $SECRET`)
- Never use `${{ secrets.GITHUB_TOKEN }}` in PR jobs from forks (use `pull_request_target` carefully)

---

## Common Patterns

### Run CI Only on Relevant Changes

```yaml
on:
  push:
    paths:
      - "src/**"
      - "tests/**"
      - "pyproject.toml"
      - ".github/workflows/ci.yml"
```

### Conditional Jobs

```yaml
jobs:
  docker:
    if: github.ref == 'refs/heads/main'
    # Only build Docker on main, not on PRs
```

### Job Dependencies

```yaml
jobs:
  test:
    # runs first
  lint:
    # runs in parallel with test
  deploy:
    needs: [test, lint]
    # runs only after both pass
```

### Artifacts

```yaml
- name: Upload test results
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: test-results
    path: reports/
    retention-days: 7
```

---

## Offline / Air-Gapped Projects

For projects that run without internet (like local-only tools):

```yaml
# CI still runs on GitHub, but tests must not call external services
- name: Run tests (offline mode)
  env:
    AUTOCASE_PROVIDER_TYPE: mock  # or use fixtures
    NO_EXTERNAL_CALLS: "1"
  run: pytest -q --tb=line -m "not integration"
```

Mark integration tests that need external services:

```python
@pytest.mark.integration
def test_ollama_connection():
    """Requires running Ollama server."""
    ...
```

---

## Starter Templates

### Minimal (test + lint)

```yaml
name: CI
on: [push, pull_request]
permissions: { contents: read }
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install -e ".[dev]"
      - run: ruff check . && ruff format --check .
      - run: pytest -q --tb=line
```

### Full (test + lint + type check + Docker + release)

Combine the `ci.yml`, `docker.yml`, and `release.yml` files above.

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|---|---|---|
| No caching | Slow builds, wasted compute | Cache pip, Docker layers |
| `pip install` without pinned versions | Non-reproducible builds | Use lockfile or pinned requirements |
| Running all tests on every file change | Slow feedback | Use `paths` filter |
| Secrets in workflow files | Leaked credentials | Use `${{ secrets.NAME }}` |
| No matrix for Python versions | Works on 3.12, breaks on 3.11 | Test multiple versions |
| Deploying without test gate | Broken releases | `needs: [test]` on deploy jobs |
| `continue-on-error: true` everywhere | Hiding failures | Only use for non-critical steps |

## Checklist

- [ ] CI runs on push + PR to main
- [ ] Tests pass before merge (branch protection)
- [ ] Linting enforced (ruff check + format)
- [ ] Dependencies cached
- [ ] Secrets stored in GitHub Secrets, not in code
- [ ] Docker build uses layer caching
- [ ] Release pipeline gated on CI passing
- [ ] Dependabot configured for pip + actions
