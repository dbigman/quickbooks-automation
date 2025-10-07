---
inclusion: always
---

# Refactoring

1. **Purposeful Refactoring:** Refactor to improve clarity, reduce duplication, simplify complexity, or adhere to architectural goals.
2. **Holistic Check:** Look for duplicate code, similar components/files, and opportunities for consolidation across the affected area.
3. **Edit, Don't Copy:** Modify existing files directly. Do not duplicate files and rename them (e.g., `component-v2.tsx`).
4. **Verify Integrations:** After refactoring, ensure all callers, dependencies, and integration points function correctly. Run relevant tests.
