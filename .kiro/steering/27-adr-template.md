---
inclusion: manual
---

# Architecture Decision Record (ADR) Template

## What is an ADR?

An Architecture Decision Record (ADR) captures a significant architectural decision, its context, alternatives considered, and consequences. ADRs provide a historical record of why decisions were made and help future developers understand the reasoning behind architectural choices.

## When to Create an ADR

Create an ADR for decisions that:
- Affect system architecture or structure
- Have long-term implications
- Are difficult or expensive to reverse
- Impact multiple components or teams
- Involve significant trade-offs
- Set precedents for future work

## ADR Template

```markdown
# ADR-[NUMBER]: [Title]

**Status:** [Proposed | Accepted | Deprecated | Superseded by ADR-XXX]
**Date:** YYYY-MM-DD
**Deciders:** [List of people involved in the decision]
**Technical Story:** [Link to issue/PR/design doc]

## Context

[Describe the context and problem statement. What forces are at play? What are the constraints? What is the current situation that requires a decision?]

## Decision

[Describe the decision that was made. Be specific and clear about what will be done.]

## Alternatives Considered

### Option 1: [Name]
**Pros:**
- [Advantage 1]
- [Advantage 2]

**Cons:**
- [Disadvantage 1]
- [Disadvantage 2]

### Option 2: [Name]
**Pros:**
- [Advantage 1]

**Cons:**
- [Disadvantage 1]

[Repeat for each alternative]

## Consequences

### Positive
- [Positive consequence 1]
- [Positive consequence 2]

### Negative
- [Negative consequence 1]
- [Negative consequence 2]

### Neutral
- [Neutral consequence 1]

## Implementation Notes

[Optional: Specific guidance for implementing this decision]

## References

- [Link to design doc]
- [Link to related ADRs]
- [Link to external resources]
```

## ADR Numbering

- Use sequential numbering: ADR-001, ADR-002, etc.
- Store in `docs/adr/` directory
- File naming: `ADR-XXX-short-title.md`

## ADR Lifecycle

1. **Proposed:** Decision is under discussion
2. **Accepted:** Decision has been approved and should be implemented
3. **Deprecated:** Decision is no longer relevant but kept for historical context
4. **Superseded:** Decision has been replaced by a newer ADR (reference the new ADR)

## Example ADR

```markdown
# ADR-001: Use PostgreSQL for Primary Database

**Status:** Accepted
**Date:** 2025-01-15
**Deciders:** Engineering Team, CTO
**Technical Story:** #123

## Context

We need to select a primary database for our manufacturing order management system. The system requires:
- ACID compliance for financial transactions
- Complex relational queries for BOM explosion
- Support for JSON data for flexible product attributes
- Strong ecosystem and tooling support
- Ability to scale to 10,000+ SKUs

## Decision

We will use PostgreSQL 15+ as our primary database.

## Alternatives Considered

### Option 1: PostgreSQL
**Pros:**
- Excellent ACID compliance
- Native JSON support (JSONB)
- Strong query optimizer
- Mature ecosystem
- Free and open source
- Great Python support (psycopg3)

**Cons:**
- Requires more operational expertise than managed services
- Vertical scaling limits

### Option 2: MySQL
**Pros:**
- Widely used and understood
- Good performance for simple queries
- Many hosting options

**Cons:**
- Weaker JSON support
- Less sophisticated query optimizer
- InnoDB limitations for complex queries

### Option 3: MongoDB
**Pros:**
- Flexible schema
- Horizontal scaling

**Cons:**
- No ACID transactions across documents (at the time)
- Not ideal for complex relational queries
- BOM explosion would be complex

## Consequences

### Positive
- Strong data integrity guarantees
- Excellent support for complex manufacturing queries
- JSON support allows flexible product attributes
- Large community and ecosystem

### Negative
- Team needs PostgreSQL expertise
- Requires careful index management for performance
- Vertical scaling may require sharding in future

### Neutral
- Will use SQLAlchemy ORM for Python integration
- Need to establish backup and recovery procedures

## Implementation Notes

- Use PostgreSQL 15+ for JSONB improvements
- Set up connection pooling (pgbouncer)
- Implement proper indexing strategy
- Use migrations (Alembic) for schema changes

## References

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- Design Doc: Manufacturing Data Model v2
```

## Best Practices

1. **Be Concise:** ADRs should be readable in 5-10 minutes
2. **Be Specific:** Avoid vague language; be clear about what was decided
3. **Show Your Work:** Document alternatives and why they weren't chosen
4. **Link Context:** Reference related issues, PRs, and design docs
5. **Update Status:** Mark ADRs as deprecated or superseded when appropriate
6. **Review Regularly:** Revisit ADRs during architecture reviews
7. **Make Them Discoverable:** Keep an index of ADRs in `docs/adr/README.md`
