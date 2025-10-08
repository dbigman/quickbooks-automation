---
inclusion: fileMatch
fileMatchPattern: ['src/yourapp/**']
---

# Core (src/yourapp)

## Structure

- `domain/`: entities/value objects; no IO.
- `services/`: use-cases; orchestrate adapters; pure where possible.
- `adapters/`: boundaries to DB/files/HTTP; side-effects live here.

## Rules

- No UI imports in core.
- Accept dependencies via constructor (DI); no singletons.
- Validate external data at adapter boundaries.
- Raise explicit domain errors; UIs translate to messages.

## Testing

- Service tests mock/fake adapters.
- Keep logic deterministic and fast.

## Naming

- Files & symbols are descriptive: `planning.py` → `Planner`, `Task`, etc.
