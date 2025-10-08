---
inclusion: always
---

# Code Review

## Review Requirements

**Approvals:**
- Minimum two qualified reviewers for changes that affect production paths
- At least one reviewer for low-risk docs/tests
- Configure CODEOWNERS so the right people are auto-requested

**Ownership:**
- Use CODEOWNERS file to define code ownership
- Auto-request appropriate reviewers based on file paths
- Ensure domain experts review relevant changes

## Reviewer Checklist

Apply what's relevant to the change:

**Correctness & Quality:**
- [ ] Code is correct and implements requirements
- [ ] Logic is clear and maintainable
- [ ] Test coverage is adequate
- [ ] No obvious bugs or edge cases missed

**Design & Architecture:**
- [ ] Adheres to design docs and ADRs
- [ ] Follows established patterns and conventions
- [ ] Respects module boundaries and dependencies
- [ ] No architectural violations

**Code Style:**
- [ ] Follows project style guidelines
- [ ] Linting and formatting checks pass
- [ ] Type hints are complete and accurate
- [ ] Naming is clear and consistent

**Testing & Validation:**
- [ ] Tests are included and pass
- [ ] Test coverage meets requirements
- [ ] Edge cases are tested
- [ ] Non-functional requirements addressed (performance, security)

**Security:**
- [ ] No secrets or credentials in code
- [ ] Input validation implemented
- [ ] Security best practices followed
- [ ] Threat model considerations addressed

**Documentation:**
- [ ] Code is well-documented
- [ ] API changes documented
- [ ] README/docs updated if needed
- [ ] CHANGELOG updated

**Change Management:**
- [ ] PR size is reasonable (< 400 lines preferred)
- [ ] Commit history is clean
- [ ] Feature flags used for incomplete work
- [ ] Rollback plan considered

**Observability:**
- [ ] Appropriate logging added
- [ ] Metrics/telemetry included
- [ ] Error handling is comprehensive
- [ ] Monitoring considerations addressed

## Author Responsibilities

**PR Description:**
- Provide clear context (problem, approach)
- Link to design docs/ADRs
- Include screenshots for UX changes
- Provide test evidence
- Summarize significant AI assistance

**Communication:**
- Respond to review comments promptly
- Keep discussions constructive and professional
- Explain reasoning for decisions
- Be open to feedback and suggestions

**Quality:**
- Ensure all CI checks pass before requesting review
- Self-review code before submitting
- Keep PRs focused and atomic
- Address review feedback thoroughly

## Review Process

1. **Initial Review:**
   - Check PR description and context
   - Verify CI checks pass
   - Review overall approach and design

2. **Detailed Review:**
   - Review code changes line by line
   - Check tests and coverage
   - Verify documentation updates
   - Consider security and performance

3. **Feedback:**
   - Provide constructive, specific feedback
   - Distinguish between blocking issues and suggestions
   - Explain reasoning for requested changes
   - Suggest alternatives when appropriate

4. **Approval:**
   - Approve when all concerns addressed
   - Verify all required checks pass
   - Ensure minimum reviewer count met

## Review Best Practices

**Speed & Respect:**
- Respond to review requests within 24 hours
- Keep discussions constructive and professional
- Prefer follow-up PRs for minor nits
- Focus on important issues first

**Effective Feedback:**
- Be specific and actionable
- Explain the "why" behind suggestions
- Distinguish between must-fix and nice-to-have
- Acknowledge good work and improvements

**Continuous Improvement:**
- Learn from reviews (both giving and receiving)
- Update guidelines based on common issues
- Share knowledge and best practices
- Foster a culture of quality and collaboration
