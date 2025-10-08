# Design Document

## Overview

This document describes the architectural design for refactoring the monolithic `quickbooks_autoreport.py` into a modular, maintainable codebase following hexagonal architecture principles.
The refactoring preserves all existing functionality while improving code quality, testability, and maintainability.
Core business logic is isolated from external dependencies; adapters handle I/O; services orchestrate workflows; domain models represent data.

## Steering Document Alignment

### Technical Standards (tech.md)
This design follows documented technical patterns including type safety, explicit dependency injection, and layered architecture.
Logging, validation, and error handling conform to standards defined in [tech.md](.spec-workflow/steering/tech.md:1).
Configuration is environment-driven with secure handling of sensitive data.

### Project Structure (structure.md)
Implementation will follow the project organization conventions described in [structure.md](.spec-workflow/steering/structure.md:1).
Applications (CLI/GUI) are entry points; services orchestrate business logic; adapters provide external integrations; domain models remain pure.
Data flow adheres to clear boundaries to maintain separation of concerns.

## Code Reuse Analysis

### Existing Components to Leverage
- [report_service.py](src/quickbooks_autoreport/services/report_service.py:1) — report orchestration
- [diagnostics_service.py](src/quickbooks_autoreport/services/diagnostics_service.py:1) — system diagnostics
- [export_service.py](src/quickbooks_autoreport/services/export_service.py:1) — CSV/Excel export helpers
- [qbxml_generator.py](src/quickbooks_autoreport/services/qbxml_generator.py:1) — qbXML request builder
- [report_parser.py](src/quickbooks_autoreport/services/report_parser.py:1) — QuickBooks response parsing
- [scheduler.py](src/quickbooks_autoreport/services/scheduler.py:1) — scheduled execution
- [connection.py](src/quickbooks_autoreport/adapters/quickbooks/connection.py:1) — QuickBooks COM connection
- [request_handler.py](src/quickbooks_autoreport/adapters/quickbooks/request_handler.py:1) — qbXML request execution
- [error_handler.py](src/quickbooks_autoreport/adapters/quickbooks/error_handler.py:1) — error translation
- [file_utils.py](src/quickbooks_autoreport/utils/file_utils.py:1) — file system operations
- [logging_utils.py](src/quickbooks_autoreport/utils/logging_utils.py:1) — centralized logging
- [exceptions.py](src/quickbooks_autoreport/domain/exceptions.py:1) — structured exceptions
- [report_config.py](src/quickbooks_autoreport/domain/report_config.py:1) — report configuration model
- [report_result.py](src/quickbooks_autoreport/domain/report_result.py:1) — report result model
- [settings.py](src/quickbooks_autoreport/domain/settings.py:1) — application settings model
- [diagnostics.py](src/quickbooks_autoreport/domain/diagnostics.py:1) — diagnostics data model
- [cli.py](src/quickbooks_autoreport/cli.py:1) — command-line application
- [gui.py](src/quickbooks_autoreport/gui.py:1) — graphical user interface

### Integration Points
- QuickBooks Desktop COM via qbXML requests and responses
- File system for outputs, logs, and hashes
- JSON settings persistence with validation on load

## Architecture

Refactoring follows hexagonal architecture:
- Domain models are pure and immutable where appropriate
- Services encapsulate business workflows without direct I/O
- Adapters translate between external systems and domain models
- Applications (CLI/GUI) compose services and adapters

### Modular Design Principles
- Single File Responsibility: each file handles one concern
- Component Isolation: small, focused components
- Service Layer Separation: data access, business logic, and presentation
- Utility Modularity: focused, single-purpose utilities

```mermaid
graph TD
    A[Apps: CLI/GUI] --> B[Services]
    B --> C[Adapters]
    B --> D[Domain Models]
    C --> E[External Systems (QuickBooks, FS)]
```

## Components and Interfaces

### Domain Layer
- ReportConfig — configuration and file path derivation
- ReportResult — execution metadata and success status
- Settings — app configuration and validation
- DiagnosticResult — system diagnostics representation
- Exceptions — QuickBooksConnectionError, ReportGenerationError, FileOperationError, SettingsError

### Services Layer
- Report Service — orchestrates report generation across types
- Export Service — creates CSV and Excel outputs with professional formatting
- QBXML Generator — builds qbXML requests and normalizes XML
- Report Parser — extracts headers and rows and detects errors
- Scheduler — manages timers and threading safely
- Diagnostics Service — runs installation and connectivity checks

### Adapters Layer
- QuickBooks Connection — COM lifecycle and request execution
- Request Handler — batch execution and version fallbacks
- Error Handler — mapping low-level errors to domain exceptions
- Settings Adapter — load/save JSON settings, defaults, validation
- File Adapter — read/write files, ensure directories, compute hashes

### Utilities
- Logging Utilities — structured logging with emoji indicators
- File Utilities — safe I/O, hashing, and path helpers

### Application Layer
- CLI — argument parsing, mode selection, orchestrates services
- GUI — Tkinter-based interface, status updates, user actions

## Data Models

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any, List

@dataclass(frozen=True)
class ReportConfig:
    key: str
    name: str
    qbxml_type: str
    query_type: str
    csv_filename: str
    excel_filename: str
    hash_filename: str
    request_log: str
    response_log: str
    uses_date_range: bool

@dataclass
class ReportResult:
    report_key: str
    report_name: str
    rows: int
    changed: bool
    timestamp: datetime
    excel_created: bool
    insights: Optional[dict]
    connect_info: Dict[str, Any]
    error: Optional[str] = None

@dataclass
class Settings:
    output_dir: str
    interval: str
    report_date_from: str
    report_date_to: str
    company_file: Optional[str] = None
```

## Error Handling

- Translate COM errors to specific domain exceptions with actionable solutions
- Maintain structured logging with emoji indicators for clarity (📥 📊 ✅ ❌)
- Avoid leaking sensitive information in user-facing messages

## Testing Strategy

### Unit Testing
- Domain models: 100% coverage (pure, deterministic)
- Services: high coverage with mocked adapters
- Adapters: interface-focused tests; simulate COM and file operations

### Integration Testing
- End-to-end report generation with sample responses and temporary directories
- Settings persistence across runs
- Error recovery scenarios

### End-to-End Testing
- CLI workflows: diagnostics and report generation
- GUI workflows: initialization, actions, status updates
- Build validation and runtime diagnostics

## Implementation Notes

- Maintain backward compatibility with current outputs and settings
- Migrate application entry points to apps/ structure when feasible
- Incremental refactoring to avoid breaking working code

## Conclusion

This design provides a solid blueprint for aligning the QuickBooks Auto Reporter with hexagonal architecture, maximizing reuse of existing modules while improving testability and maintainability.