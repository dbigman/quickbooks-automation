---
inclusion: fileMatch
fileMatchPattern: ['src/yourapp/adapters/**']
---

# Adapters

**Contract**
- Provide a minimal repository interface consumed by services: `all()`, `get(id)`, `save(entity)`, `next_id()`.

**IO Practices**
- No business rules in adapters.
- Read paths/URLs/creds from env (e.g., `TASKS_PATH`), not hardcoded.
- Use `pydantic-settings` or dotenv to load config.
- Log side-effects; return typed objects.

**Testing**
- Exercise real IO in narrow tests (e.g., tmp files), not in service tests.
