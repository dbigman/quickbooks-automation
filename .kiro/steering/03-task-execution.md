---
inclusion: always
---

# Task Execution & Workflow

1. **Task Definition:**

   * Clearly understand the task requirements, acceptance criteria, and any dependencies from `tasks/tasks.md` and the PRD.

2. **Systematic Change Protocol:**

   * **Identify Impact:** Determine affected components, dependencies, and potential side effects.
   * **Plan:** Outline the steps. Tackle one logical change or file at a time.
   * **Verify Testing:** Confirm how the change will be tested. Add tests if necessary *before* implementing (see TDD).

3. **Progress Tracking:**

   * Keep `docs/status.md` updated with task progress (in-progress, completed, blocked), issues encountered, and completed items.
   * Update `tasks/tasks.md` upon task completion or if requirements change during implementation.
