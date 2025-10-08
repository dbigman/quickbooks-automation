---
inclusion: fileMatch
fileMatchPattern: ['CHANGELOG.md', 'CHANGELOG.*', '**/CHANGELOG.*']
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

* **Added**: for new features.
* **Changed**: for changes in existing functionality.
* **Deprecated**: for soon-to-be removed features.
* **Removed**: for now removed features.
* **Fixed**: for any bug fixes.
* **Security**: in case of vulnerability fixes.

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

* Version links (optional) at the bottom:

  ```markdown
  [Unreleased]: https://github.com/your/repo/compare/v1.2.0...HEAD
  [1.2.0]: https://github.com/your/repo/releases/tag/v1.2.0
  ```

Ensure all contributors adhere to this format for consistency and automated tooling support.
