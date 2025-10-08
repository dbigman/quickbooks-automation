---
inclusion: always
---

# Task Execution & Workflow

1. **Planning & Design:**

   * For non-trivial changes, create a design document with:
     - Problem statement, scope, and measurable success criteria
     - High-level architecture, data model, interfaces, and integration points
     - Non-functional requirements (reliability, performance, cost, security, privacy, compliance)
     - Risks, alternatives considered, and trade-offs
     - Rollout plan (gating, migration, feature flags) and rollback strategy
   * Capture key decisions as Architecture Decision Records (ADRs)
   * Define clear Definition of Done (DoD) for each task

2. **Task Definition:**

   * Clearly understand the task requirements, acceptance criteria, and any dependencies from `tasks/tasks.md` and the PRD
   * Break design into small, testable increments

3. **Systematic Change Protocol:**

   * **Identify Impact:** Determine affected components, dependencies, and potential side effects
   * **Plan:** Outline the steps. Tackle one logical change or file at a time
   * **Verify Testing:** Confirm how the change will be tested. Add tests if necessary *before* implementing (see TDD)
   * **Keep PRs Small:** Aim for < 400 lines diff net; use feature flags for incomplete work

4. **Progress Tracking:**

   * Keep `docs/status.md` updated with task progress (in-progress, completed, blocked), issues encountered, and completed items
   * Update `tasks/tasks.md` upon task completion or if requirements change during implementation
   * Track DORA metrics: deployment frequency, lead time for changes, change failure rate, MTTR
