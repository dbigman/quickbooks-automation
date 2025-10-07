---
inclusion: always
---

# Commit Message Guidelines

Follow [Conventional Commits 1.0.0](https://www.conventionalcommits.org/) specification for all commit messages in this MPS Calculator project.

## Format Structure

```text
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

## Required Types

- **feat**: New features (triggers MINOR version bump)
- **fix**: Bug fixes (triggers PATCH version bump)
- **docs**: Documentation changes
- **refactor**: Code refactoring without feature changes
- **perf**: Performance improvements
- **test**: Adding or updating tests
- **chore**: Maintenance tasks, dependency updates

## Project-Specific Scopes

Use these scopes to indicate which component is affected:

- **calculator**: MPS calculation engine (`calculator.py`)
- **connector**: Odoo API integration (`connector.py`)
- **exporter**: Excel report generation (`exporter.py`)
- **cli**: Command-line interface (`main.py`)
- **inventory**: Warehouse and inventory management
- **orders**: Sales order processing
- **bom**: Bill of Materials handling
- **scheduling**: Production scheduling algorithms
- **reports**: Excel reporting and formatting

## Breaking Changes

Indicate breaking changes with `!` after type/scope or use `BREAKING CHANGE:` footer:

```text
feat(calculator)!: change MPS algorithm interface

BREAKING CHANGE: MPSCalculator now requires algorithm parameter in constructor
```

## MPS Calculator Examples

```text
feat(calculator): add FIFO scheduling algorithm
fix(connector): handle missing BOM data gracefully
docs(readme): update installation instructions
refactor(exporter): optimize Excel formatting performance
perf(inventory): improve memory usage for large datasets
test(calculator): add unit tests for priority scoring
chore(deps): update pandas to v2.1.0
```

## Body Guidelines

Include context for complex changes:

- Why the change was made
- Impact on existing functionality
- Migration notes for breaking changes
- Performance implications

## Footer References

- `Fixes #123`: Links to GitHub issues
- `Refs #456`: References related issues
- `Co-authored-by: Name <email>`: Multiple authors
