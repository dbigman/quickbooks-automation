---
inclusion: always
---

# Security & Compliance

## Secure SDL (Software Development Lifecycle)

Integrate security throughout planning, coding, testing, and release:

1. **Threat Modeling:**
   - Conduct threat modeling for new features and high-risk changes
   - Document mitigations and security controls
   - Review attack surfaces and trust boundaries

2. **Secrets & Data Management:**
   - **Never hardcode secrets** or credentials in the codebase
   - Use secret managers (environment variables, vault services)
   - Minimize PII; apply least privilege and proper data retention
   - Validate external data at adapter boundaries

3. **Dependency Hygiene:**
   - Run Software Composition Analysis (SCA) on every PR and nightly
   - Maintain an SBOM (Software Bill of Materials) using CycloneDX or SPDX
   - Triage vulnerabilities within SLA; fix or mitigate
   - Document vulnerability management in changelog

4. **Supply Chain Security:**
   - Aim for SLSA-aligned build provenance and signed artifacts
   - Use trusted registries for artifacts
   - Verify dependency integrity

5. **AppSec Checks:**
   - Static analysis (SAST) in CI pipeline
   - Dynamic analysis (DAST) for web applications
   - Container scans for Docker images
   - Infrastructure as Code (IaC) scans

6. **Input Validation:**
   - Always sanitize and validate user input on the server-side
   - Use type validation (pydantic, TypeScript types)
   - Implement rate limiting and input size restrictions

7. **Server-Side Authority:**
   - Keep sensitive logic, validation, and data manipulation strictly on the server-side
   - Use secure API endpoints with proper authentication
   - Implement authorization checks at every access point

## Security Review Checklist

- [ ] Threat model completed for high-risk changes
- [ ] No secrets in code; using secret manager
- [ ] Input validation implemented
- [ ] SCA scan passed
- [ ] Static analysis passed
- [ ] Least privilege applied
- [ ] Security testing included
