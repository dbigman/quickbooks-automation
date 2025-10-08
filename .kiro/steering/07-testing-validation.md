---
inclusion: fileMatch
fileMatchPattern: ['tests/**']
---

# Testing & Validation

## Testing Pyramid

Maintain a healthy testing pyramid:

- **Many fast unit tests** (base of pyramid)
- **Fewer integration tests** (middle)
- **Minimal end-to-end tests** (top)

## Test-Driven Development (TDD)

1. **New Features:** Write a failing test, implement code to pass it, then refactor (red/green/refactor)
2. **Bug Fixes:** Write a test reproducing the bug *before* fixing it
3. **At Minimum:** Write tests alongside code changes

## Test Scope & Organization

### Unit Tests

- Test `services/` with adapter fakes/mocks
- Fast, deterministic, no external dependencies
- Mirror source paths: `tests/services/test_planning.py`

### Integration Tests

- Narrow IO tests for adapters (tmp dirs/files)
- Test component interactions
- Avoid sleeps and network calls where possible

### Non-Functional Tests

- Include performance, load, resiliency, and accessibility tests as appropriate

## Coverage Requirements

- **Core modules:** >90% coverage (calculator.py, connector.py, exporter.py)
- **Error scenarios:** Test network failures, malformed data, missing configurations
- **Business logic:** Validate manufacturing algorithms and inventory calculations

## Test Quality Standards

1. **Tests Must Pass:** All tests **must** pass before committing or considering a task complete
2. **Deterministic:** Avoid flaky tests; no random data or timing dependencies
3. **Fast:** Keep test suite under ~5 minutes; parallelize if needed
4. **Isolated:** Each test should be independent and not rely on test execution order
5. **Clear Assertions:** Use descriptive assertion messages

## Test Commands

- Run all tests: `pytest`
- Quick run: `pytest -q`
- With coverage: `pytest --cov=src`
- Specific test: `pytest tests/services/test_planning.py`

## Mock Data Guidelines

- Use mock data *only* within test environments
- Development and production should use real or realistic data sources
- Create reusable test fixtures for common scenarios

## Manual Verification

- Supplement automated tests with manual checks where appropriate
- Especially important for UI changes and user workflows
- Document manual test procedures for complex features
