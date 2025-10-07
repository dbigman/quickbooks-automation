---
inclusion: always
---

# Conventional Commits for Git

Commits **MUST** follow the [Conventional Commits 1.0.0](https://www.conventionalcommits.org/) specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

## Types (correlate with SemVer)

* **feat:** Introduces a new feature (MINOR release)
* **fix:** Patches a bug (PATCH release)
* **build, chore, ci, docs, style, refactor, perf, test, etc.:** Other commit types (no SemVer impact unless BREAKING CHANGE)

## Scopes

* A scope **MAY** be provided in parentheses after the type, e.g.,:

  ```
  feat(api): add new authentication endpoint
  ```

## Breaking Changes

* Indicate breaking changes by either:

  * Appending `!` after type or scope:

    ```
    feat!: overhaul authentication flow
    ```
  * Or adding a footer:

    ```
    BREAKING CHANGE: authentication now requires two-factor verification
    ```

## Message Structure Rules

1. **Prefix (REQUIRED):** `<type>[optional scope][!]: `
2. **Description (REQUIRED):** Brief summary after the colon.
3. **Body (OPTIONAL):** Detailed explanation separated by a blank line.
4. **Footers (OPTIONAL):** Metadata or references, one per line, separated by a blank line from the body.

## Examples

```
fix(parser): handle empty input correctly

Introduce fallback behavior when no input is provided.

Reviewed-by: Jane Doe
Refs: #123
```

```
feat(ui)!: redesign header component

BREAKING CHANGE: header now requires user authentication state to render.
```

Use this format for all commit messages to maintain consistency and enable automated tooling.
