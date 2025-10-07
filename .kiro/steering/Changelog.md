---
inclusion: always
---

# Changelog & Version Management Guidelines

## Changelog Format

Follow [Keep a Changelog](https://keepachangelog.com/) format with semantic versioning:

```markdown
# Changelog

## [Unreleased]

### Added

### Changed

### Deprecated

### Removed

### Fixed

### Security

## [1.2.0] - 2024-08-11

### Added

- New MPS calculation algorithm for priority-based scheduling
- Excel export functionality with multi-sheet reports
```

## Version Numbering

Use semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Breaking changes to API or core functionality
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

## Entry Categories

### Added

- New features, endpoints, or capabilities
- New configuration options or environment variables
- New dependencies or integrations

### Changed

- Modifications to existing functionality
- Performance improvements
- Updated dependencies
- Configuration changes

### Fixed

- Bug fixes and error corrections
- Memory leaks or performance issues
- Data accuracy improvements

### Removed

- Deprecated features or endpoints
- Unused dependencies
- Legacy code cleanup

### Security

- Security vulnerability fixes
- Authentication improvements
- Data protection enhancements

## Commit Message Format

Use conventional commits for automatic changelog generation:

```
feat: add priority-based order scheduling algorithm
fix: resolve inventory calculation memory leak
docs: update API documentation for new endpoints
refactor: optimize pandas data processing pipeline
```

## Documentation Updates

When making changes, always update:

- **README.md**: For user-facing changes
- **API_REFERENCE.md**: For API modifications
- **USAGE_EXAMPLES.md**: For new features or workflows
- **requirements.txt**: For dependency changes

## Release Process

1. Update version in `pyproject.toml`
2. Update changelog with release date
3. Run full test suite: `pytest -v --cov`
4. Generate new Excel exports for validation
5. Tag release: `git tag v1.2.0`

## Breaking Changes

Document breaking changes clearly:

- What changed and why
- Migration path for users
- Deprecation timeline if applicable
- Code examples showing before/after

## Integration Impact

Consider impact on:

- **Odoo Integration**: API changes or new endpoints
- **Excel Exports**: New sheets or format changes
- **CLI Interface**: New flags or changed behavior
- **Configuration**: New environment variables or settings

---

description: Enforce Keep a Changelog 1.1.0 format when writing CHANGELOG.md files.
globs:

- "CHANGELOG\*.md"

---

# Changelog Format (Keep a Changelog 1.1.0)

Changelogs **MUST** follow the [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) specification.

## Structure

Each `CHANGELOG.md` **MUST** include the following sections in this order:

1. **Header**

   ```markdown
   # Changelog

   All notable changes to this project will be documented in this file.
   ```

2. **Unreleased** (always present)

   ```markdown
   ## [Unreleased]
   ```

3. **Release entries**, one per version, sorted latest first:

   ```markdown
   ## [1.2.0] - 2025-05-15
   ```

## Categories

Under each release or Unreleased, group changes into these sections (only include those that apply):

- **Added**: for new features.
- **Changed**: for changes in existing functionality.
- **Deprecated**: for soon-to-be removed features.
- **Removed**: for now removed features.
- **Fixed**: for any bug fixes.
- **Security**: in case of vulnerability fixes.

### Example Entry

```markdown
## [Unreleased]

### Added

- new authentication endpoint for multi-factor login

### Fixed

- correct token expiration handling in API client

## [1.1.0] - 2025-04-10

### Changed

- updated dependency X to version Y

### Security

- patched XSS vulnerability in rendering module
```

## References

- Version links (optional) at the bottom:

  ```markdown
  [Unreleased]: https://github.com/your/repo/compare/v1.2.0...HEAD
  [1.2.0]: https://github.com/your/repo/releases/tag/v1.2.0
  ```

Ensure all contributors adhere to this format for consistency and automated tooling support.
