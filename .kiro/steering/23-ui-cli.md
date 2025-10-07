---
inclusion: fileMatch
fileMatchPattern: ['apps/cli/**']
---

# CLI (apps/cli)

**Patterns**
- Use Typer for commands; functions do: parse args → call service → print stable output.
- Instantiate services via a factory (inject adapters once).
- Avoid business logic; push it into `services/`.

**UX**
- Be concise; exit codes > interactive prompts.
- Safe defaults; dry runs where destructive.

**Run**
- `python -m apps.cli`
