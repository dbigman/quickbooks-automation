---
inclusion: always
---

# Project Overview

**Product**: One product with two UIs (CLI + Streamlit). Keep UIs thin; put business logic in `src/yourapp/`.

**Monorepo Layout**
```
yourapp/
├─ pyproject.toml
├─ .pre-commit-config.yaml
├─ apps/
│  ├─ cli/                 # CLI entry
│  │  └─ __main__.py
│  └─ dashboard/           # Streamlit multipage app
│     ├─ Home.py
│     └─ pages/
│        └─ 1_Planning.py
├─ src/
│  └─ yourapp/
│     ├─ domain/
│     ├─ services/
│     └─ adapters/
└─ tests/
```

**Principles**
- Single source of truth: all business logic lives in `services/` (side-effects in `adapters/`).
- Dependency direction: UIs → core; **core never imports UI**.
- Explicit DI: pass adapters (file/db/http) into services.
- 12-factor: config via env; logs to stdout; no secrets in code.
- Strong typing; validate IO at adapter boundaries (e.g., `pydantic`).

**Run Commands**
- CLI: `python -m apps.cli ...`
- Dashboard: `streamlit run apps/dashboard/Home.py`

**Quality Bar**
- Pre-commit: `ruff`, `black`, `isort`, `mypy`.
- Tests: `pytest` for core/adapters; fast & deterministic.
- CI on push/PR: lint → typecheck → tests.
