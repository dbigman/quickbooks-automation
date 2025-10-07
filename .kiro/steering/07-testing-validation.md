---
inclusion: fileMatch
fileMatchPattern: ['tests/**']
---

<!-- BEGIN merged content from testing.mdc -->
# Tests

**Scope**
- Unit tests for `services/` with adapter fakes/mocks.
- Narrow IO tests for adapters (tmp dirs/files).

**Conventions**
- Mirror source paths: `tests/services/test_planning.py`.
- Deterministic assertions; avoid sleeps and network.

**Commands**
- `pytest -q`
<!-- END merged content from testing.mdc -->

---

<!-- BEGIN merged content from 07-testing-validation.mdc -->
---

description: Testing strategies & TDD guidelines for robust code validation.
globs:

* "tests/\*\*/\*"
* "src/\*\*/\*.{js,jsx,ts,tsx}"

---

# Testing & Validation

1. **Test-Driven Development (TDD):**

   * **New Features:** Outline tests, write failing tests, implement code, refactor.
   * **Bug Fixes:** Write a test reproducing the bug *before* fixing it.
2. **Comprehensive Tests:** Write thorough unit, integration, and end-to-end tests covering critical paths, edge cases, and major functionality.
3. **Tests Must Pass:** All tests **must** pass before committing or considering a task complete. Notify immediately if tests fail and cannot be easily fixed.
4. **No Mock Data (Except Tests):** Use mock data *only* within test environments. Development and production should use real or realistic data sources.
5. **Manual Verification:** Supplement automated tests with manual checks where appropriate, especially for UI changes.
<!-- END merged content from 07-testing-validation.mdc -->
