# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Sales Dashboard specification with comprehensive requirements, design, and implementation plan
- `.kiro/specs/sales-dashboard/requirements.md` - User stories and acceptance criteria for dashboard features
- `.kiro/specs/sales-dashboard/design.md` - Technical architecture and component design
- `.kiro/specs/sales-dashboard/tasks.md` - Detailed implementation task breakdown
- MCP configuration files (`mcp.json`) added to `.gitignore` to prevent committing sensitive settings

### Changed
- Updated `.gitignore` to exclude all `mcp.json` files throughout the repository

### Security
- Prevented accidental commit of MCP configuration files that may contain sensitive settings
