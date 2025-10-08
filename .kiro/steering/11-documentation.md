---
inclusion: always
---

# Documentation Maintenance

## Documentation Requirements

1. **Keep Docs Current:**
   - Update documentation as part of the PR, not after
   - Keep design docs and ADRs current with what shipped
   - Update `README.md`, API references (e.g., OpenAPI), and `CHANGELOG.md`
   - For user-facing changes, provide release notes and migration guides

2. **Required Documentation:**
   - `README.md` - project overview, setup, patterns, technology stack
   - `docs/architecture.md` - system architecture, component relationships
   - `docs/technical.md` - technical specifications, established patterns
   - `tasks/tasks.md` - current development tasks, requirements
   - `docs/status.md` - task progress and completion status
   - `CHANGELOG.md` - version history following Keep a Changelog format
   - ADRs (Architecture Decision Records) - significant architectural decisions

3. **Architecture Decision Records (ADRs):**
   - Create ADRs for significant architectural decisions
   - Include: context, decision, alternatives considered, consequences
   - Link to design docs/PRs where applicable
   - Store in `docs/adr/` directory

4. **API Documentation:**
   - Maintain OpenAPI specs for REST APIs
   - Document all public functions with type hints and docstrings
   - Include usage examples and error scenarios
   - Keep API references synchronized with code

5. **Keep Rules Updated:**
   - Review and update steering documents periodically
   - Reflect learned best practices and project evolution
   - Update when workflows or standards change

## Documentation Standards

- Use clear, descriptive language
- Provide practical usage examples
- Include troubleshooting guidance
- Maintain consistent formatting and structure
- Use UTC timestamps for all documentation metadata
