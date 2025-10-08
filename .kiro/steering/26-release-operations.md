---
inclusion: always
---

# Build, Release & Operations

## CI/CD Pipeline

**Build Requirements:**
- Reproducible builds
- Artifacts stored in a trusted registry
- Required checks enforced on `main`
- Branch protection rules active

**CI Pipeline (on push/PR):**
1. Linting: `ruff check .`
2. Formatting: `black --check .`
3. Import sorting: `isort --check-only .`
4. Type checking: `mypy src`
5. Unit tests: `pytest`
6. Security scans: SCA, SAST
7. License checks

**Pipeline Policies:**
- Fail on any violations
- Keep CI under ~5 minutes
- Parallelize tests if needed
- Pin exact tool versions in `pyproject.toml`

## Environments

**Environment Parity:**
- Dev → Staging → Production parity as much as practical
- Use ephemeral preview environments for PRs when possible
- Maintain consistent configuration across environments
- Use environment variables for environment-specific config

**Configuration Management:**
- 12-factor app principles: config via env
- No secrets in code
- Use `.env.example` as template
- Document all required environment variables

## Rollout Strategies

**Progressive Delivery:**
- Prefer feature flags, canary, and/or blue-green deployments
- Start with small percentage of traffic
- Monitor metrics and error rates
- Gradually increase rollout percentage

**Feature Flags:**
- Use for incomplete work on trunk
- Enable progressive rollouts
- Support A/B testing
- Allow quick rollback without deployment

**Deployment Checklist:**
- [ ] Version bumped (SemVer)
- [ ] Staging validated
- [ ] Canary/blue-green plan defined
- [ ] SLOs/alerts/runbooks in place
- [ ] Rollback plan verified
- [ ] Changelog and release notes published

## Observability

**Logging:**
- Emit structured logs to stdout
- Use centralized logger setup
- Include context (request ID, user ID, etc.)
- Follow emoji-based logging patterns (📥 📊 ✅)

**Metrics & Traces:**
- Define SLIs/SLOs before launch
- Create dashboards for key metrics
- Implement distributed tracing
- Track business and technical metrics

**Alerting:**
- Alerts should be actionable
- Tie alerts to user-impacting SLOs
- Avoid alert fatigue
- Keep on-call runbooks up to date

**SLIs/SLOs:**
- Define Service Level Indicators (measurements)
- Set Service Level Objectives (targets)
- Monitor error budgets
- Use data to guide pace and priorities

## Post-Release

**Monitoring:**
- Monitor error budgets and key metrics
- Track DORA metrics:
  - Deployment Frequency
  - Lead Time for Changes
  - Change Failure Rate
  - Mean Time to Restore (MTTR)

**Incident Response:**
- Conduct blameless postmortems for incidents
- Document root causes and contributing factors
- Track action items to closure
- Share learnings across team

**Continuous Improvement:**
- Review metrics regularly
- Identify bottlenecks and pain points
- Implement improvements iteratively
- Update processes based on learnings

## Rollback Procedures

**Rollback Plan:**
- Always include rollback plan before deployment
- Test rollback procedure in staging
- Document rollback steps clearly
- Ensure rollback can be executed quickly

**Automated Health Checks:**
- Implement health check endpoints
- Monitor critical functionality
- Automated rollback on health check failures
- Alert on degraded performance

## Performance & Reliability

**Performance Requirements:**
- Complete MPS runs within 2 minutes for 1000+ SKUs
- Process large datasets efficiently
- Achieve >20% memory reduction where applicable
- Optimize database queries and indexing

**Reliability:**
- Implement retry logic for external services
- Graceful degradation for non-critical features
- Circuit breakers for failing dependencies
- Proper error handling and recovery
