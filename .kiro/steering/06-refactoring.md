---
inclusion: always
---

# Refactoring Guidelines

## Core Principles

**Purposeful Refactoring Only**: Refactor to improve clarity, reduce duplication, simplify complexity, or align with architectural goals. Avoid refactoring for its own sake.

**Edit, Don't Duplicate**: Modify existing files directly. Never create duplicate files with version suffixes (e.g., `component-v2.tsx`, `utils_old.py`).

## Pre-Refactoring Checklist

- Identify the specific problem being solved
- Ensure adequate test coverage exists before changes
- Document the current behavior if tests are insufficient
- Check for all usage locations using search tools

## Refactoring Process

1. **Scope Analysis**: Use `grepSearch` to find all references and dependencies
2. **Impact Assessment**: Identify affected modules, imports, and integration points
3. **Incremental Changes**: Make small, atomic changes that can be easily verified
4. **Validation**: Run tests and check diagnostics after each logical change

## Python-Specific Patterns

**Module Consolidation**: Look for similar functionality across `quickbooks/` modules that can be unified
**Type Safety**: Maintain or improve type hints during refactoring
**Import Cleanup**: Remove unused imports and organize according to project standards
**Error Handling**: Preserve or improve existing error handling patterns

## Manufacturing Domain Considerations

**Data Processing**: Maintain pandas DataFrame operations and column naming conventions
**Business Logic**: Preserve manufacturing algorithms (FIFO, LIFO, EDD scheduling)
**Configuration**: Keep environment variable patterns and `.env` usage intact
**Logging**: Maintain emoji-based logging patterns (📥 📊 ✅) for consistency

## Post-Refactoring Verification

- Run `getDiagnostics` on all modified files
- Execute relevant tests to ensure functionality is preserved
- Verify imports and dependencies are correctly updated
- Check that configuration and environment handling still works
