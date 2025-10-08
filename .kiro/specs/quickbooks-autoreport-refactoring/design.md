# Design Document: QuickBooks Autoreport Refactoring

## Overview

This document describes the architectural design for refactoring the monolithic `quickbooks_autoreport.py` (1400+ lines) into a modular, maintainable codebase following hexagonal architecture principles. The refactoring will preserve all existing functionality while improving code quality, testability, and maintainability.

### Design Principles

1. **Hexagonal Architecture**: Core business logic isolated from external dependencies
2. **Dependency Inversion**: High-level modules don't depend on low-level modules
3. **Single Responsibility**: Each module has one clear purpose
4. **Explicit Dependencies**: All dependencies injected via constructors
5. **Type Safety**: Comprehensive type hints throughout
6. **Testability**: Pure functions and mockable interfaces

## Architecture

### High-Level Structure

```
quickbooks_autoreport/
├── apps/                           # Application entry points
│   ├── cli/                        # Command-line interface
│   │   └── __main__.py            # CLI entry point
│   └── gui/                        # Graphical user interface
│       ├── __main__.py            # GUI entry point
│       ├── main_window.py         # Main window implementation
│       └── widgets/               # Custom widgets
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
│   ├── unit/                      # Unit tests
│   │   ├── test_domain/
│   │   ├── test_services/
│   │   └── test_adapters/
│   ├── integration/               # Integration tests
│   │   └── test_report_flow.py
│   └── fixtures/                  # Test fixtures
│       └── sample_responses.xml
├── pyproject.toml                 # Project configuration
├── README.md                      # Project documentation
└── .env.example                   # Environment variable template
```

### Dependency Flow

```
┌─────────────────────────────────────────────────┐
│                  Apps Layer                      │
│  ┌──────────┐              ┌──────────┐        │
│  │   CLI    │              │   GUI    │        │
│  └────┬─────┘              └────┬─────┘        │
│       │                         │               │
└───────┼─────────────────────────┼───────────────┘
        │                         │
        ▼                         ▼
┌─────────────────────────────────────────────────┐
│               Services Layer                     │
│  ┌──────────────┐  ┌──────────────┐            │
│  │   Report     │  │  Scheduler   │            │
│  │  Generator   │  │              │            │
│  └──────┬───────┘  └──────┬───────┘            │
│         │                 │                     │
│  ┌──────┴───────┐  ┌──────┴───────┐            │
│  │    Excel     │  │ Diagnostics  │            │
│  │   Creator    │  │              │            │
│  └──────────────┘  └──────────────┘            │
└───────────┬─────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────┐
│              Adapters Layer                      │
│  ┌──────────────┐  ┌──────────────┐            │
│  │  QuickBooks  │  │     File     │            │
│  │   Adapter    │  │   Adapter    │            │
│  └──────────────┘  └──────────────┘            │
│  ┌──────────────┐  ┌──────────────┐            │
│  │   Settings   │  │    Logger    │            │
│  │   Adapter    │  │   Adapter    │            │
│  └──────────────┘  └──────────────┘            │
└─────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────┐
│           External Systems                       │
│  • QuickBooks Desktop (COM)                     │
│  • File System                                  │
│  • JSON Settings Files                          │
└─────────────────────────────────────────────────┘
```

## Components and Interfaces

### Domain Layer

#### 1. ReportConfig (domain/report_config.py)

```python
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class ReportConfig:
    """Configuration for a QuickBooks report."""
    key: str
    name: str
    qbxml_type: str
    query_type: str  # "GeneralDetail", "GeneralSummary", "Aging"
    csv_filename: str
    excel_filename: str
    hash_filename: str
    request_log: str
    response_log: str
    uses_date_range: bool
    
    def get_file_paths(self, output_dir: str) -> dict[str, str]:
        """Get all file paths for this report."""
        ...
```

**Responsibilities:**
- Immutable report configuration
- File path generation
- Report metadata

#### 2. ReportResult (domain/report_result.py)

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class ReportResult:
    """Result of a report execution."""
    report_key: str
    report_name: str
    rows: int
    changed: bool
    timestamp: datetime
    excel_created: bool
    insights: Optional[dict]
    connect_info: dict
    error: Optional[str] = None
    
    @property
    def success(self) -> bool:
        """Whether the report executed successfully."""
        return self.error is None
```

**Responsibilities:**
- Report execution results
- Success/failure status
- Metadata about execution

#### 3. Settings (domain/settings.py)

```python
from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class Settings:
    """Application settings."""
    output_dir: str
    interval: str
    report_date_from: str
    report_date_to: str
    company_file: Optional[str] = None
    
    def validate(self) -> None:
        """Validate settings values."""
        ...
```

**Responsibilities:**
- Application configuration
- Settings validation
- Default values

#### 4. DiagnosticResult (domain/diagnostics.py)

```python
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class DiagnosticResult:
    """Result of system diagnostics."""
    timestamp: str
    system_info: Dict[str, Any]
    quickbooks_installation: Dict[str, Any]
    sdk_installation: Dict[str, Any]
    connectivity_test: Dict[str, Any]
    recommendations: List[str]
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        ...
```

**Responsibilities:**
- Diagnostic information
- System status
- Recommendations

#### 5. Exceptions (domain/exceptions.py)

```python
class QuickBooksError(Exception):
    """Base exception for QuickBooks-related errors."""
    pass

class QuickBooksConnectionError(QuickBooksError):
    """QuickBooks connection failed."""
    def __init__(self, message: str, error_type: str, solutions: List[str]):
        self.error_type = error_type
        self.solutions = solutions
        super().__init__(message)

class ReportGenerationError(QuickBooksError):
    """Report generation failed."""
    pass

class FileOperationError(Exception):
    """File operation failed."""
    pass

class SettingsError(Exception):
    """Settings validation or loading failed."""
    pass
```

**Responsibilities:**
- Custom exception types
- Error context and solutions
- Type-safe error handling

### Services Layer

#### 1. ReportGenerator (services/report_generator.py)

```python
from typing import List, Dict, Optional
from ..domain.report_config import ReportConfig
from ..domain.report_result import ReportResult
from ..adapters.quickbooks.connection import QuickBooksConnection
from ..adapters.file_adapter import FileAdapter
import logging

class ReportGenerator:
    """Orchestrates report generation process."""
    
    def __init__(
        self,
        qb_connection: QuickBooksConnection,
        file_adapter: FileAdapter,
        excel_creator: 'ExcelCreator',
        csv_creator: 'CSVCreator',
        logger: logging.Logger
    ):
        self._qb = qb_connection
        self._file = file_adapter
        self._excel = excel_creator
        self._csv = csv_creator
        self._logger = logger
    
    def generate_report(
        self,
        config: ReportConfig,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None
    ) -> ReportResult:
        """Generate a single report."""
        ...
    
    def generate_all_reports(
        self,
        configs: List[ReportConfig],
        date_from: Optional[str] = None,
        date_to: Optional[str] = None
    ) -> tuple[Dict[str, ReportResult], Dict[str, str]]:
        """Generate all configured reports."""
        ...
```

**Responsibilities:**
- Report generation orchestration
- Error handling and retry logic
- Coordination between adapters and creators

#### 2. ExcelCreator (services/excel_creator.py)

```python
from typing import List
import logging

class ExcelCreator:
    """Creates Excel reports with formatting."""
    
    def __init__(self, logger: logging.Logger):
        self._logger = logger
    
    def create_excel(
        self,
        headers: List[str],
        rows: List[List[str]],
        output_path: str,
        sheet_name: str
    ) -> bool:
        """Create formatted Excel file."""
        ...
    
    def create_enhanced_excel(
        self,
        headers: List[str],
        rows: List[List[str]],
        output_path: str,
        insights: dict
    ) -> bool:
        """Create Excel with charts and analytics."""
        ...
```

**Responsibilities:**
- Excel file creation
- Formatting and styling
- Chart generation

#### 3. CSVCreator (services/csv_creator.py)

```python
from typing import List
import logging

class CSVCreator:
    """Creates CSV reports."""
    
    def __init__(self, logger: logging.Logger):
        self._logger = logger
    
    def create_csv(
        self,
        headers: List[str],
        rows: List[List[str]]
    ) -> str:
        """Create CSV content as string."""
        ...
```

**Responsibilities:**
- CSV generation
- Proper escaping and formatting

#### 4. Scheduler (services/scheduler.py)

```python
from typing import Callable, Optional
from datetime import datetime, timedelta
import threading
import logging

class Scheduler:
    """Manages scheduled report execution."""
    
    def __init__(self, logger: logging.Logger):
        self._logger = logger
        self._running = False
        self._timer: Optional[threading.Timer] = None
    
    def start(
        self,
        callback: Callable[[], None],
        interval_seconds: int
    ) -> None:
        """Start scheduled execution."""
        ...
    
    def stop(self) -> None:
        """Stop scheduled execution."""
        ...
    
    def get_next_run_time(self, interval_seconds: int) -> datetime:
        """Calculate next run time."""
        ...
```

**Responsibilities:**
- Scheduled execution
- Timer management
- Thread safety

#### 5. DiagnosticsService (services/diagnostics.py)

```python
from ..domain.diagnostics import DiagnosticResult
from ..adapters.quickbooks.connection import QuickBooksConnection
import logging

class DiagnosticsService:
    """Performs system diagnostics."""
    
    def __init__(
        self,
        qb_connection: QuickBooksConnection,
        logger: logging.Logger
    ):
        self._qb = qb_connection
        self._logger = logger
    
    def run_diagnostics(self) -> DiagnosticResult:
        """Run comprehensive system diagnostics."""
        ...
    
    def check_quickbooks_installation(self) -> tuple[bool, List[str]]:
        """Check if QuickBooks is installed."""
        ...
    
    def check_sdk_installation(self) -> tuple[bool, str]:
        """Check if SDK is properly installed."""
        ...
```

**Responsibilities:**
- System diagnostics
- Installation checks
- Connectivity testing

#### 6. InsightsGenerator (services/insights_generator.py)

```python
from typing import List, Dict, Any
import logging

class InsightsGenerator:
    """Generates business insights from report data."""
    
    def __init__(self, logger: logging.Logger):
        self._logger = logger
    
    def generate_insights(
        self,
        headers: List[str],
        rows: List[List[str]],
        report_key: str
    ) -> Dict[str, Any]:
        """Generate insights for a report."""
        ...
```

**Responsibilities:**
- Data analysis
- Business metrics calculation
- Insight generation

### Adapters Layer

#### 1. QuickBooks Connection (adapters/quickbooks/connection.py)

```python
from typing import Optional, Tuple, Dict, Any
import logging

class QuickBooksConnection:
    """Manages QuickBooks Desktop COM connection."""
    
    def __init__(
        self,
        app_name: str,
        company_file: Optional[str],
        logger: logging.Logger
    ):
        self._app_name = app_name
        self._company_file = company_file
        self._logger = logger
        self._rp = None
        self._ticket = None
    
    def connect(self) -> None:
        """Establish connection to QuickBooks."""
        ...
    
    def disconnect(self) -> None:
        """Close connection to QuickBooks."""
        ...
    
    def execute_request(self, xml_request: str) -> Tuple[str, Dict[str, Any]]:
        """Execute qbXML request and return response."""
        ...
    
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()
```

**Responsibilities:**
- COM object management
- Connection lifecycle
- Request execution
- Error translation

#### 2. XML Builder (adapters/quickbooks/xml_builder.py)

```python
from typing import Optional
from ...domain.report_config import ReportConfig

class XMLBuilder:
    """Builds qbXML requests."""
    
    def build_report_request(
        self,
        config: ReportConfig,
        version: str,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None
    ) -> str:
        """Build qbXML request for a report."""
        ...
    
    def normalize_xml(self, xml: str) -> str:
        """Normalize XML to avoid parser errors."""
        ...
```

**Responsibilities:**
- qbXML generation
- XML normalization
- Version handling

#### 3. XML Parser (adapters/quickbooks/xml_parser.py)

```python
from typing import List, Tuple

class XMLParser:
    """Parses qbXML responses."""
    
    def parse_report_response(self, xml: str) -> Tuple[List[str], List[List[str]]]:
        """Parse report response into headers and rows."""
        ...
    
    def extract_error_info(self, xml: str) -> Optional[dict]:
        """Extract error information from response."""
        ...
```

**Responsibilities:**
- XML parsing
- Data extraction
- Error detection

#### 4. File Adapter (adapters/file_adapter.py)

```python
from typing import Optional
import logging

class FileAdapter:
    """Handles file system operations."""
    
    def __init__(self, logger: logging.Logger):
        self._logger = logger
    
    def write_file(self, path: str, content: str) -> None:
        """Write content to file."""
        ...
    
    def read_file(self, path: str) -> str:
        """Read content from file."""
        ...
    
    def file_exists(self, path: str) -> bool:
        """Check if file exists."""
        ...
    
    def ensure_directory(self, path: str) -> None:
        """Ensure directory exists."""
        ...
    
    def compute_hash(self, content: str) -> str:
        """Compute SHA256 hash of content."""
        ...
    
    def read_hash(self, path: str) -> Optional[str]:
        """Read hash from file."""
        ...
    
    def write_hash(self, path: str, hash_value: str) -> None:
        """Write hash to file."""
        ...
```

**Responsibilities:**
- File I/O operations
- Directory management
- Hash computation
- Error handling

#### 5. Settings Adapter (adapters/settings_adapter.py)

```python
from ..domain.settings import Settings
import logging

class SettingsAdapter:
    """Manages settings persistence."""
    
    def __init__(self, settings_file: str, logger: logging.Logger):
        self._settings_file = settings_file
        self._logger = logger
    
    def load_settings(self) -> Settings:
        """Load settings from file."""
        ...
    
    def save_settings(self, settings: Settings) -> None:
        """Save settings to file."""
        ...
    
    def get_default_settings(self) -> Settings:
        """Get default settings."""
        ...
```

**Responsibilities:**
- Settings serialization
- JSON file management
- Default values

#### 6. Logger Adapter (adapters/logger_adapter.py)

```python
import logging
from typing import Optional

class LoggerAdapter:
    """Configures and provides loggers."""
    
    @staticmethod
    def setup_logger(
        name: str,
        log_file: Optional[str] = None,
        level: int = logging.INFO
    ) -> logging.Logger:
        """Setup and return a configured logger."""
        ...
    
    @staticmethod
    def log_with_emoji(
        logger: logging.Logger,
        level: int,
        emoji: str,
        message: str
    ) -> None:
        """Log message with emoji prefix."""
        ...
```

**Responsibilities:**
- Logger configuration
- Emoji logging support
- Centralized setup

### Application Layer

#### 1. CLI Application (apps/cli/__main__.py)

```python
import sys
import argparse
from quickbooks_autoreport.services.report_generator import ReportGenerator
from quickbooks_autoreport.services.diagnostics import DiagnosticsService
from quickbooks_autoreport.adapters.settings_adapter import SettingsAdapter
# ... other imports

def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="QuickBooks Auto Reporter")
    parser.add_argument("--gui", action="store_true", help="Launch GUI")
    parser.add_argument("--diagnose", action="store_true", help="Run diagnostics")
    parser.add_argument("--output-dir", help="Output directory")
    parser.add_argument("--date-from", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--date-to", help="End date (YYYY-MM-DD)")
    
    args = parser.parse_args()
    
    # Setup dependencies
    logger = LoggerAdapter.setup_logger("quickbooks_autoreport")
    settings_adapter = SettingsAdapter(SETTINGS_FILE, logger)
    settings = settings_adapter.load_settings()
    
    # ... dependency injection and execution
    
if __name__ == "__main__":
    main()
```

**Responsibilities:**
- Command-line argument parsing
- Dependency injection setup
- CLI workflow orchestration

#### 2. GUI Application (apps/gui/__main__.py)

```python
import tkinter as tk
from .main_window import MainWindow
from quickbooks_autoreport.adapters.logger_adapter import LoggerAdapter
# ... other imports

def main():
    """GUI entry point."""
    # Setup dependencies
    logger = LoggerAdapter.setup_logger("quickbooks_autoreport_gui")
    
    # Create and run GUI
    root = tk.Tk()
    app = MainWindow(root, logger)
    root.mainloop()

if __name__ == "__main__":
    main()
```

**Responsibilities:**
- GUI initialization
- Dependency injection
- Event loop management

## Data Models

### Report Configuration

```python
REPORT_CONFIGS = {
    "open_sales_orders": ReportConfig(
        key="open_sales_orders",
        name="Open Sales Orders by Item",
        qbxml_type="OpenSalesOrderByItem",
        query_type="GeneralDetail",
        csv_filename="Open_Sales_Orders_By_Item.csv",
        excel_filename="Open_Sales_Orders_By_Item.xlsx",
        hash_filename="Open_Sales_Orders_By_Item.hash",
        request_log="open_so_request.xml",
        response_log="open_so_response.xml",
        uses_date_range=False
    ),
    # ... other reports
}
```

### Settings Model

```python
@dataclass
class Settings:
    output_dir: str = DEFAULT_OUT_DIR
    interval: str = "15 minutes"
    report_date_from: str = field(default_factory=lambda: date.today().replace(day=1).isoformat())
    report_date_to: str = field(default_factory=lambda: date.today().isoformat())
    company_file: Optional[str] = None
```

## Error Handling

### Error Translation Strategy

```python
def translate_com_error(error: Exception) -> QuickBooksConnectionError:
    """Translate COM errors to user-friendly messages."""
    error_str = str(error)
    
    if "-2147221005" in error_str:
        return QuickBooksConnectionError(
            message="Cannot connect to QuickBooks Desktop",
            error_type="SDK_NOT_INSTALLED",
            solutions=[
                "Install QuickBooks Desktop",
                "Download and install QuickBooks SDK",
                "Run as Administrator",
                "Restart computer after SDK installation"
            ]
        )
    # ... other error translations
```

### Error Handling Flow

```
┌─────────────────┐
│  User Action    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Service       │──┐
│   Layer         │  │ Try/Catch
└────────┬────────┘  │
         │           │
         ▼           │
┌─────────────────┐  │
│   Adapter       │  │
│   Layer         │  │
└────────┬────────┘  │
         │           │
         ▼           │
┌─────────────────┐  │
│  External       │  │
│  System         │  │
└────────┬────────┘  │
         │           │
         ▼           │
    [Error]◄─────────┘
         │
         ▼
┌─────────────────┐
│  Translate to   │
│  Domain Error   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Log Error      │
│  with Context   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Return User-   │
│  Friendly Msg   │
└─────────────────┘
```

## Testing Strategy

### Unit Tests

```python
# tests/unit/test_services/test_report_generator.py
def test_generate_report_success(mock_qb_connection, mock_file_adapter):
    """Test successful report generation."""
    generator = ReportGenerator(
        qb_connection=mock_qb_connection,
        file_adapter=mock_file_adapter,
        excel_creator=mock_excel_creator,
        csv_creator=mock_csv_creator,
        logger=mock_logger
    )
    
    result = generator.generate_report(test_config)
    
    assert result.success
    assert result.rows > 0
```

### Integration Tests

```python
# tests/integration/test_report_flow.py
def test_full_report_generation_flow():
    """Test complete report generation flow."""
    # Setup real adapters with test data
    # Execute full flow
    # Verify outputs
```

### Test Coverage Goals

- Domain models: 100% (pure Python, easy to test)
- Services: >95% (business logic)
- Adapters: >85% (external dependencies)
- Overall: >90%

## Migration Strategy

### Phase 1: Setup Structure
1. Create new directory structure
2. Setup pyproject.toml with dependencies
3. Create empty module files with interfaces

### Phase 2: Domain Layer
1. Extract domain models from existing code
2. Create exception classes
3. Add comprehensive type hints
4. Write unit tests for domain models

### Phase 3: Adapters Layer
1. Extract QuickBooks COM logic
2. Extract file operations
3. Extract settings management
4. Create adapter interfaces
5. Write unit tests for adapters

### Phase 4: Services Layer
1. Extract report generation logic
2. Extract Excel/CSV creation
3. Extract scheduler logic
4. Extract diagnostics
5. Wire up dependency injection
6. Write unit tests for services

### Phase 5: Application Layer
1. Create CLI entry point
2. Create GUI entry point
3. Wire up all dependencies
4. Test end-to-end flows

### Phase 6: Testing & Validation
1. Run integration tests
2. Verify all functionality works
3. Performance testing
4. User acceptance testing

### Phase 7: Documentation & Cleanup
1. Update README
2. Create architecture docs
3. Create migration guide
4. Remove old monolithic file

## Performance Considerations

### Optimization Strategies

1. **Lazy Loading**: Load heavy dependencies only when needed
2. **Connection Pooling**: Reuse QuickBooks connections where possible
3. **Caching**: Cache report configurations and settings
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
2. **Input Validation**: Validate all external inputs at adapter boundaries
3. **File Permissions**: Proper file permissions for output files
4. **Logging**: Never log sensitive information
5. **Error Messages**: Don't expose internal details in user-facing errors

### Security Checklist

- [ ] No hardcoded credentials
- [ ] Environment variables for sensitive data
- [ ] Input validation at boundaries
- [ ] Secure file operations
- [ ] Safe XML parsing (prevent XXE)
- [ ] Proper error handling (no info leakage)

## Rollout Plan

### Deployment Strategy

1. **Feature Flag**: Add flag to use new or old implementation
2. **Parallel Running**: Run both implementations side-by-side
3. **Gradual Migration**: Migrate one report type at a time
4. **Monitoring**: Monitor for errors and performance issues
5. **Rollback Plan**: Keep old implementation available

### Success Metrics

- All tests passing
- No performance regression
- No functionality regression
- Code coverage >90%
- All linting checks passing
- Successful user acceptance testing

## Future Enhancements

### Potential Improvements

1. **Async/Await**: Use asyncio for better concurrency
2. **Plugin System**: Allow custom report types
3. **Web UI**: Add web-based interface
4. **API**: Expose REST API for integrations
5. **Cloud Storage**: Support cloud storage backends
6. **Multi-Company**: Support multiple QuickBooks companies
7. **Notifications**: Email/Slack notifications for reports
8. **Scheduling**: More advanced scheduling options

## Conclusion

This design provides a solid foundation for refactoring the monolithic `quickbooks_autoreport.py` into a maintainable, testable, and extensible codebase. The hexagonal architecture ensures clear separation of concerns, while dependency injection enables easy testing and flexibility. The phased migration approach minimizes risk and allows for incremental validation of the refactoring.
