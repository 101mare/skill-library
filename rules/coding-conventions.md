# Coding Conventions

## DRY (Don't Repeat Yourself)

- **Extract, don't copy**: If logic appears twice, extract into a function. Three similar blocks are always one abstraction with parameters.
- **Single Source of Truth**: Constants, config values, validation rules — defined in ONE place, imported everywhere else.
- **But: avoid premature abstraction**: Two similar-looking blocks that serve different purposes are NOT duplication. Only extract when the shared logic is the SAME concept, not just the same syntax.
- **DRY applies to knowledge, not code**: If two functions have identical lines but represent different domain concepts, they are NOT duplicates. Forcing them into one abstraction creates coupling that makes future changes harder.
- **Config over code**: If a value could change, put it in config. If a pattern repeats with different parameters, make it data-driven.

## Naming & Imports

- Package-qualified imports from project root
- Relative imports within a package
- No circular imports — if A needs B and B needs A, extract the shared type into a third module

## Error Handling

- Specific exceptions only — never bare `except:` or `except Exception:`
- Chain with `from e`: `raise AppError("message") from e`
- Handle at boundaries (CLI, API endpoints), propagate in business logic
- No error swallowing: if you catch it, log it or re-raise it

## Functions & Methods

- Max ~30 lines per function. If longer, extract sub-steps.
- One responsibility per function — if the name has "and", split it
- Return early to avoid deep nesting
- No mutable default arguments — use `None` sentinel

## Types

- Type hints mandatory on all function signatures
- Use `T | None` instead of `Optional[T]`
- Parameterize collections: `list[str]`, `dict[str, int]`
- Use `typing.Protocol` for interfaces

## Testing

- Mock at Protocol/interface boundaries, not internals
- Test behavior, not implementation: assert outcomes, not call counts
- One assertion focus per test (multiple asserts OK if they test one concept)
- Use `pytest` fixtures for shared setup, `tmp_path` for file operations
- New logic must have tests
