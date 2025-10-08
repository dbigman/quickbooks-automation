---
inclusion: always
---

# Core Philosophy

1. **Design First:** Every non-trivial change starts with a written design document. Capture key decisions as Architecture Decision Records (ADRs).
2. **Build in Small, Safe Steps:** Prefer short-lived branches and frequent integration. Keep PRs small and focused (ideally < 400 lines diff net).
3. **Tests Before Code:** Practice TDD where practical; always maintain a healthy testing pyramid (many fast unit tests, fewer integration tests, minimal end-to-end tests).
4. **Two Sets of Eyes:** All changes require peer review before merge. Minimum two qualified reviewers for production-affecting changes.
5. **Security by Default:** Treat security and privacy as first-class requirements. Integrate security throughout planning, coding, testing, and release.
6. **Automate Quality:** Linters, formatters, pre-commit hooks, CI gates, and repeatable builds are mandatory.
7. **Evidence-Based Delivery:** Measure with DORA metrics and SLOs; use data (including error budgets) to guide pace.
8. **AI-Assisted, Human-Owned:** Use AI to accelerate, not replace, engineering judgment. Humans remain accountable.
9. **Simplicity:** Prioritize simple, clear, and maintainable solutions. Avoid unnecessary complexity or over-engineering.
10. **Focus:** Concentrate efforts on the specific task assigned. Avoid unrelated changes or scope creep.
