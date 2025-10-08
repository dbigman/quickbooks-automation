# Coding Guidelines

_Last updated: 2025-10-07_

These guidelines describe how we design, build, review, test, secure, and ship production-quality software. They incorporate our team’s workflow (design-first, test-first, review-gated, staged deploys) plus industry best practices.

---

## 1) Principles
- **Design first.** Every non-trivial change starts with a written design document.
- **Build in small, safe steps.** Prefer short-lived branches and frequent integration.
- **Tests before code.** Practice TDD where practical; always maintain a healthy testing pyramid.
- **Two sets of eyes.** All changes require peer review before merge.
- **Security by default.** Treat security and privacy as first-class requirements.
- **Automate quality.** Linters, formatters, pre-commit hooks, CI gates, and repeatable builds are mandatory.
- **Evidence-based delivery.** Measure with DORA metrics and SLOs; use data (including error budgets) to guide pace.
- **AI-assisted, human-owned.** Use AI to accelerate, not replace, engineering judgment. Humans remain accountable.

---

## 2) Planning & Design
1. **Proposal → Design Doc**
   - Problem statement, scope, and measurable success criteria.
   - High-level architecture, data model, interfaces, and integration points.
   - Non-functional requirements (reliability, performance, cost, security, privacy, compliance).
   - Risks, alternatives considered, and trade-offs.
   - Rollout plan (gating, migration, data backfill, config/feature flags) and rollback strategy.
2. **Design Review**
   - Share the design widely; expect it to be challenged. Incorporate feedback and record decisions.
   - Capture key decisions as **Architecture Decision Records (ADRs)**.
3. **Backlog & Sprint Planning**
   - Break the design into small, testable increments. Define a clear **Definition of Done (DoD)** for each item.

---

## 3) Development Workflow
1. **Branching & Integration**
   - Use trunk-based development where possible.
   - Feature branches are short-lived; rebase/merge to main frequently (at least daily when active).
   - No direct commits to `main`. All changes via Pull Requests (PRs).
2. **Commits & Change Size**
   - Keep PRs small and focused (ideally < 400 lines diff net). Write meaningful commit messages using **Conventional Commits**.
   - Use **semantic versioning** for public artifacts and APIs.
3. **Style & Quality Gates**
   - Enforce a single code style via `.editorconfig` and language-appropriate linters/formatters.
   - Enable **pre-commit hooks** for formatting, linting, basic security checks, and unit tests when feasible.
   - CI must run: build, static analysis, unit tests, security/SCA scans, and license checks. All required checks must pass before merge.
4. **Testing**
   - **TDD** encouraged. At a minimum, write tests alongside code changes.
   - Maintain a **testing pyramid**: many fast unit tests, fewer integration tests, and minimal end-to-end tests.
   - Include non-functional tests as appropriate (performance, load, resiliency, accessibility).
5. **AI-Assisted Development**
   - Use AI to draft tests, scaffolding, boilerplate, and refactors; validate outputs with reviews and tests.
   - Never paste secrets, live customer data, or proprietary unredacted content into external tools.
   - Prefer enterprise-approved AI tools with org policies enforced. Log noteworthy AI-generated code decisions in the PR description or ADR.

---

## 4) Code Review
- **Approvals**: Minimum two qualified reviewers for changes that affect production paths; at least one for low-risk docs/tests.
- **Ownership**: Configure CODEOWNERS so the right people are auto-requested.
- **Reviewer checklist** (apply what’s relevant):
  - Correctness, clarity, test coverage, and maintainability.
  - Adherence to design/ADRs, style, and security guidelines.
  - Reasonable change size and clean commit history.
  - Appropriate telemetry, metrics, and feature flags.
- **Author responsibilities**: Provide context (problem, approach), links to design/ADRs, screenshots for UX, and test evidence.
- **Speed & respect**: Respond to reviews promptly; keep discussions constructive. Prefer follow-up PRs for nits.

---

## 5) Security & Compliance
- **Secure SDL**: Integrate security throughout planning, coding, testing, and release.
- **Threat modeling** for new features and high-risk changes; document mitigations.
- **Secrets & data**: No secrets in code; use secret managers. Minimize PII; apply least privilege and proper data retention.
- **Dependency hygiene**: Run Software Composition Analysis (SCA) on every PR and nightly; maintain an SBOM (CycloneDX or SPDX).
- **Supply chain**: Aim for SLSA-aligned build provenance and signed artifacts.
- **AppSec checks**: Static/dynamic analysis, container scans, Infrastructure as Code scans in CI.
- **Vuln management**: Triage within SLA; fix or mitigate; document in the change log.

---

## 6) Build, Release & Operations
1. **CI/CD**
   - Reproducible builds; artifacts stored in a trusted registry.
   - Required checks and branch protection rules enforced on `main`.
2. **Environments**
   - Dev → Staging → Production parity as much as practical. Use ephemeral preview environments for PRs when possible.
3. **Rollout Strategies**
   - Prefer progressive delivery: feature flags, canary, and/or blue–green deployments.
   - Always include a rollback plan and automated health checks.
4. **Observability**
   - Emit structured logs, metrics, traces. Define SLIs/SLOs and dashboards before launch.
   - Alerts should be actionable and tied to user-impacting SLOs. Keep on-call runbooks up to date.
5. **Post-release**
   - Monitor error budgets and key metrics. Conduct blameless postmortems for incidents; track action items to closure.

---

## 7) Documentation
- Keep design docs and ADRs current with what shipped.
- Update READMEs, API references (e.g., OpenAPI), and CHANGELOGs as part of the PR.
- For user-facing changes, provide release notes and migration guides.

---

## 8) Governance & Exceptions
- Exceptions to these guidelines require explicit approval from an engineering lead and security.
- Record exceptions in the design doc or ADR with scope, duration, and risk acceptance.

---

## 9) Checklists (copy into PR templates)
**Design Doc**
- [ ] Problem, scope, success metrics
- [ ] Architecture + data model
- [ ] Integrations & contracts
- [ ] NFRs (perf, reliability, cost, security, privacy)
- [ ] Risks & alternatives
- [ ] Rollout & rollback

**PR / Change**
- [ ] Small, focused diffs and meaningful commit messages (Conventional Commits)
- [ ] Tests added/updated; coverage acceptable
- [ ] Lint/format, build, SCA, license, and security checks pass
- [ ] Telemetry & docs updated; feature flags gated
- [ ] Reviewers/owners assigned; ADRs linked

**Release**
- [ ] Version bumped (SemVer)
- [ ] Staging validated; canary/blue–green plan
- [ ] SLOs/alerts/runbooks in place
- [ ] Rollback verified; changelog and release notes published

---

## 10) Glossary
**ADR (Architecture Decision Record)** — Short document capturing a significant architectural decision, context, alternatives, and consequences. Links to design doc/PR where applicable.

**ASVS (Application Security Verification Standard)** — OWASP framework of security requirements for web apps/APIs; used as a reference checklist for AppSec reviews.

**Blue–Green Deployment** — Two production‑like environments (blue and green); traffic switches between them to enable zero/low‑downtime releases and quick rollback.

**Canary Release** — Progressive rollout of a change to a small cohort to reduce risk before full release.

**CI/CD (Continuous Integration / Continuous Delivery or Deployment)** — Practices and tooling to integrate work frequently and deliver changes safely and continuously.

**CODEOWNERS** — GitHub mechanism that auto‑assigns reviewers/owners for paths in a repo to route PRs to the right people.

**Conventional Commits** — Commit message convention (e.g., `feat:`, `fix:`) that encodes intent and supports automation (changelogs, SemVer bumps).

**DORA Metrics (Four Keys)** — Deployment Frequency, Lead Time for Changes, Change Failure Rate, and Mean Time to Restore (MTTR): outcome metrics for delivery performance.

**DoD (Definition of Done)** — Team‑agreed checklist of criteria that must be met before a backlog item is considered complete.

**Feature Flag / Toggle** — Runtime or build‑time switch controlling feature exposure; enables trunk‑based development, canaries, A/B tests, and safe rollbacks.

**NFR (Non‑Functional Requirements)** — Qualities such as reliability, performance, cost, security, privacy, and compliance that constrain design/implementation.

**Observability** — Telemetry to understand system state and user impact; typically logs, metrics, and traces with dashboards/alerts tied to SLOs.

**SBOM (Software Bill of Materials)** — Machine‑readable inventory of components and dependencies (e.g., CycloneDX, SPDX) to support security, license, and supply‑chain risk management.

**SCA (Software Composition Analysis)** — Scanning dependencies to identify known vulnerabilities, license issues, and outdated components.

**SDL/SSDLC (Secure Software Development Lifecycle)** — Security activities integrated into the SDLC (threat modeling, secure coding, scanning, review, pen testing, hardening).

**SLA / SLO / SLI** — Service Level Agreement (external commitment), Service Level Objective (target reliability), and Service Level Indicator (measurement used to assess SLO conformance).

**SLSA (Supply‑chain Levels for Software Artifacts)** — Framework and levels for build provenance and supply‑chain integrity (attestations, verified builds, hardened workflows).

**TDD (Test‑Driven Development)** — Write a failing test, implement code to pass it, then refactor (red/green/refactor).

**Testing Pyramid** — Emphasize many fast unit tests, fewer integration tests, and minimal end‑to‑end UI tests.

**Trunk‑Based Development** — Short‑lived branches (or direct-to‑trunk) with frequent integration; feature flags for incomplete work.

**Progressive Delivery** — Gradual rollouts (canary, blue–green, feature gating) with automated analysis and guardrails.

**SemVer (Semantic Versioning)** — `MAJOR.MINOR.PATCH` where breaking changes bump MAJOR, backward‑compatible features bump MINOR, and fixes bump PATCH.

---

### Appendix: AI Usage Guardrails
- Prefer approved enterprise AI tools with enforced retention and model policies.
- Summarize significant AI assistance in PR descriptions when it affects design or implementation.
- Do not use AI to generate cryptography, auth logic, or code that must meet strict compliance without expert review.
- Validate AI-generated code with tests and reviews; never bypass review gates.

---

> TL;DR: Start with a solid design, build in small reviewed increments, write tests first, automate quality and security, ship safely with progressive delivery, and measure outcomes.

