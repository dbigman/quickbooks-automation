---
inclusion: always
---

# Version Control & Environment

## Branching & Integration

1. **Trunk-Based Development:**
   - Use trunk-based development where possible
   - Feature branches are short-lived; rebase/merge to main frequently (at least daily when active)
   - No direct commits to `main`. All changes via Pull Requests (PRs)

2. **Git Hygiene:**
   - Commit frequently with clear, atomic messages using Conventional Commits
   - Keep the working directory clean; ensure no unrelated or temporary files are staged or committed
   - Use `.gitignore` effectively

3. **Branch Protection:**
   - Required checks and branch protection rules enforced on `main`
   - All PRs require approval before merge
   - Configure CODEOWNERS so the right people are auto-requested

## Pull Request Standards

1. **Size & Focus:**
   - Keep PRs small and focused (ideally < 400 lines diff net)
   - One logical change per PR
   - Use feature flags for incomplete work

2. **PR Description Requirements:**
   - Provide context (problem, approach)
   - Link to design docs/ADRs
   - Include screenshots for UX changes
   - Provide test evidence
   - Summarize significant AI assistance when applicable

3. **Review Requirements:**
   - Minimum two qualified reviewers for production-affecting changes
   - At least one reviewer for low-risk docs/tests
   - Respond to reviews promptly; keep discussions constructive

## Semantic Versioning

- Use **semantic versioning** (SemVer) for public artifacts and APIs
- `MAJOR.MINOR.PATCH` where:
  - Breaking changes bump MAJOR
  - Backward-compatible features bump MINOR
  - Fixes bump PATCH

## Environment Management

1. **.env Files:**
   - **Never** commit `.env` files
   - Use `.env.example` as templates
   - Do not overwrite local `.env` files without confirmation

2. **Environment Awareness:**
   - Ensure code functions correctly across different environments (dev, test, prod)
   - Use environment variables for configuration
   - Maintain Dev → Staging → Production parity as much as practical

3. **Server Management:**
   - Kill related running servers before starting new ones
   - Restart servers after relevant configuration or backend changes
