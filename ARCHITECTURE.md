# QuickBooks Auto Reporter - Architecture

## Overview

This document describes the architecture of the refactored QuickBooks Auto Reporter application, which follows hexagonal architecture principles for improved maintainability, testability, and modularity.

## Project Structure

```
quickbooks-auto-reporter/
├── apps/                           # Application entry points
│   ├── cli/                        # Command-line interface
│   │   ├── __init__.py
│   │   └── __main__.py            # CLI entry point
│   └── gui/                        # Graphical user interface
│       ├── __init__.py
│       ├── __main__.py            # GUI entry point
│       ├── main_window.py         # Main window implementation
│       └── widgets/               # Custom widgets
│           ├── __init__.py
│           ├── status_panel.py
│           ├── config_panel.py
│           └── report_grid.py
├── src/
│   └── quickbooks_autoreport/     # Core application
│       ├── __init__.py
│       ├── domain/                # Domain models (pure Python)
│       │   ├── __init__.py
│       │   ├── report_config.py   # Report configuration model
│       │   ├── report_result.py   # Report execution result
│       │   ├── settings.py        # Application settings model
│       │   ├── diagnostics.py     # Diagnostic result model
│       │   └── exceptions.py      # Custom exceptions
│       ├── services/              # Business logic
│       │   ├── __init__.py
│       │   ├── report_generator.py    # Report generation orchestration
│       │   ├── excel_creator.py       # Excel file creation
│       │   ├── csv_creator.py         # CSV file creation
│       │   ├── scheduler.py           # Scheduled execution
│       │   ├── diagnostics.py         # System diagnostics
│       │   └── insights_generator.py  # Business insights
│       ├── adapters/              # External integrations
│       │   ├── __init__.py
│       │   ├── quickbooks/        # QuickBooks integration
│       │   │   ├── __init__.py
│       │   │   ├── connection.py  # QB connection management
│       │   │   ├── xml_builder.py # qbXML request builder
│       │   │   └── xml_parser.py  # qbXML response parser
│       │   ├── file_adapter.py    # File system operations
│       │   ├── settings_adapter.py # Settings persistence
│       │   └── logger_adapter.py  # Logging configuration
│       └── utils/                 # Shared utilities
│           ├── __init__.py
│           ├── hashing.py         # File hashing utilities
│           └── validation.py      # Input validation
├── tests/                         # Test suite
│   ├── __init__.py
│   ├── unit/                      # Unit tests
│   │   ├── __init__.py
│   │   ├── test_domain/
│   │   ├── test_services/
│   │   └── test_adapters/
│   ├── integration/               # Integration tests
│   │   ├── __init__.py
│   │   └── test_report_flow.py
│   └── fixtures/                  # Test fixtures
│       ├── __init__.py
│       └── sample_responses.xml
├── .env.example                   # Environment variable template
├── .gitignore                     # Git ignore rules
├── .pre-commit-config.yaml        # Pre-commit hooks
├── pyproject.toml                 # Project configuration
├── README.md                      # User documentation
└── ARCHITECTURE.md                # This file
```

## Architectural Principles

### Hexagonal Architecture (Ports and Adapters)

The application follows hexagonal architecture to achieve:

1. **Separation of Concerns**: Business logic is isolated from external dependencies
2. **Testability**: Core logic can be tested without external systems
3. **Flexibility**: Easy to swap implementations (e.g., different storage backends)
4. **Maintainability**: Clear boundaries between layers

### Dependency Flow

```
Apps Layer (CLI/GUI)
        ↓
Services Layer (Business Logic)
        ↓
Adapters Layer (External Systems)
        ↓
External Systems (QuickBooks, File System, etc.)
```

**Key Rule**: Dependencies flow inward. Core domain never depends on external systems.

## Layer Descriptions

### Domain Layer (`src/quickbooks_autoreport/domain/`)

Pure Python models with no external dependencies. Contains:

- **Data Models**: Immutable data structures (dataclasses)
- **Business Rules**: Domain-specific validation logic
- **Exceptions**: Custom exception types for domain errors

**Characteristics**:
- No I/O operations
- No framework dependencies
- 100% testable with unit tests
- Immutable where appropriate

### Services Layer (`src/quickbooks_autoreport/services/`)

Business logic and orchestration. Contains:

- **Report Generator**: Coordinates report generation workflow
- **Excel/CSV Creators**: Format and create output files
- **Scheduler**: Manages scheduled execution
- **Diagnostics**: System health checks
- **Insights Generator**: Business analytics

**Characteristics**:
- Depends on domain models
- Receives adapters via dependency injection
- Contains no I/O code (delegates to adapters)
- Testable with mocked adapters

### Adapters Layer (`src/quickbooks_autoreport/adapters/`)

External system integrations. Contains:

- **QuickBooks Adapter**: COM integration with QuickBooks Desktop
- **File Adapter**: File system operations
- **Settings Adapter**: Configuration persistence
- **Logger Adapter**: Logging setup

**Characteristics**:
- Implements interfaces expected by services
- Handles all I/O operations
- Translates between external formats and domain models
- Can be mocked for testing

### Application Layer (`apps/`)

User interfaces and entry points. Contains:

- **CLI**: Command-line interface
- **GUI**: Tkinter graphical interface

**Characteristics**:
- Thin layer that wires up dependencies
- Handles user input/output
- Creates and configures services
- No business logic

## Dependency Injection

All dependencies are explicitly injected via constructors:

```python
# Service receives dependencies
class ReportGenerator:
    def __init__(
        self,
        qb_connection: QuickBooksConnection,
        file_adapter: FileAdapter,
        excel_creator: ExcelCreator,
        logger: logging.Logger
    ):
        self._qb = qb_connection
        self._file = file_adapter
        self._excel = excel_creator
        self._logger = logger
```

Benefits:
- Easy to test (inject mocks)
- Clear dependencies
- Flexible configuration
- No hidden dependencies

## Configuration Management

### Environment Variables

Configuration via `.env` file (never committed):

```bash
QB_COMPANY_FILE=C:\Path\To\Company.QBW
OUTPUT_DIR=C:\Reports
LOG_LEVEL=INFO
```

### User Settings

Persistent user preferences in JSON:

```json
{
  "output_dir": "C:\\Reports",
  "interval": "15 minutes",
  "report_date_from": "2024-01-01",
  "report_date_to": "2024-01-31"
}
```

## Error Handling

### Exception Hierarchy

```
Exception
├── QuickBooksError (base for QB errors)
│   ├── QuickBooksConnectionError
│   └── ReportGenerationError
├── FileOperationError
└── SettingsError
```

### Error Translation

Adapters translate external errors to domain exceptions:

```python
try:
    # External system call
    result = external_system.call()
except ExternalError as e:
    # Translate to domain exception
    raise QuickBooksConnectionError(
        message="User-friendly message",
        error_type="SDK_NOT_INSTALLED",
        solutions=["Install SDK", "Run as admin"]
    )
```

## Testing Strategy

### Testing Pyramid

```
        /\
       /  \      E2E Tests (few)
      /____\
     /      \    Integration Tests (some)
    /________\
   /          \  Unit Tests (many)
  /____________\
```

### Test Organization

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test component interactions
- **Fixtures**: Shared test data and mocks

### Coverage Goals

- Domain models: 100%
- Services: >95%
- Adapters: >85%
- Overall: >90%

## Code Quality Tools

### Linting and Formatting

- **ruff**: Fast Python linter
- **black**: Code formatter
- **isort**: Import sorter
- **mypy**: Static type checker

### Pre-commit Hooks

Automatically run before each commit:
- Trailing whitespace removal
- YAML/JSON validation
- Code formatting
- Type checking

### CI/CD Pipeline

1. Linting (`ruff check .`)
2. Formatting (`black --check .`)
3. Import sorting (`isort --check-only .`)
4. Type checking (`mypy src`)
5. Unit tests (`pytest tests/unit`)
6. Integration tests (`pytest tests/integration`)
7. Coverage report

## Development Workflow

### Setting Up Development Environment

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Copy environment template
copy .env.example .env
```

### Running Tests

```bash
# All tests
pytest

# Unit tests only
pytest tests/unit

# With coverage
pytest --cov=src/quickbooks_autoreport --cov-report=html

# Specific test file
pytest tests/unit/test_domain/test_report_config.py
```

### Code Quality Checks

```bash
# Run all checks
ruff check .
black --check .
isort --check-only .
mypy src

# Auto-fix issues
ruff check --fix .
black .
isort .
```

### Running the Application

```bash
# CLI mode
python -m apps.cli

# GUI mode
python -m apps.gui

# With diagnostics
python -m apps.cli --diagnose
```

## Migration from Monolithic Version

The refactoring maintains backward compatibility:

1. **Same Functionality**: All 9 report types work identically
2. **Same Output**: CSV and Excel formats unchanged
3. **Same Settings**: Settings file format compatible
4. **Same Performance**: Equivalent or better performance

### Migration Path

1. Keep old `quickbooks_autoreport.py` as backup
2. Install refactored version
3. Test with existing settings
4. Verify output matches
5. Remove old version when confident

## Extensibility

### Adding New Report Types

1. Add configuration to domain models
2. Update XML builder for new report structure
3. Add parser logic if needed
4. Update services to handle new type
5. Add tests

### Adding New Output Formats

1. Create new creator service (e.g., `PDFCreator`)
2. Inject into `ReportGenerator`
3. Add format selection to UI
4. Add tests

### Adding New Data Sources

1. Create new adapter (e.g., `QuickBooksOnlineAdapter`)
2. Implement same interface as desktop adapter
3. Inject appropriate adapter based on configuration
4. Add tests

## Performance Considerations

### Optimization Strategies

1. **Lazy Loading**: Load dependencies only when needed
2. **Connection Pooling**: Reuse QuickBooks connections
3. **Caching**: Cache report configurations
4. **Async I/O**: Use threading for file operations in GUI
5. **Memory Management**: Stream large XML responses

### Performance Targets

- Report generation: ≤ current performance
- Excel creation: ≤ current performance
- GUI startup: ≤ 2 seconds
- Memory usage: ≤ current usage

## Security Considerations

### Secure Practices

1. **No Secrets in Code**: All credentials via environment variables
2. **Input Validation**: Validate at adapter boundaries
3. **File Permissions**: Proper permissions for output files
4. **Logging**: Never log sensitive information
5. **Error Messages**: Don't expose internal details

### Security Checklist

- [ ] No hardcoded credentials
- [ ] Environment variables for sensitive data
- [ ] Input validation at boundaries
- [ ] Secure file operations
- [ ] Safe XML parsing (prevent XXE)
- [ ] Proper error handling (no info leakage)

## Future Enhancements

### Planned Improvements

1. **Async/Await**: Use asyncio for better concurrency
2. **Plugin System**: Allow custom report types
3. **Web UI**: Add web-based interface
4. **REST API**: Expose API for integrations
5. **Cloud Storage**: Support cloud storage backends
6. **Multi-Company**: Support multiple QuickBooks companies
7. **Notifications**: Email/Slack notifications
8. **Advanced Scheduling**: Cron-like scheduling

## References

- [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Dependency Injection](https://en.wikipedia.org/wiki/Dependency_injection)
- [QuickBooks SDK Documentation](https://developer.intuit.com/app/developer/qbdesktop/docs/get-started)
