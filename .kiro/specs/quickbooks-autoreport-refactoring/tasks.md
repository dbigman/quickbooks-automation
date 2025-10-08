# Implementation Plan

This implementation plan reflects the current state of the refactoring. Most core functionality has been implemented in a functional style. The remaining tasks focus on completing the architectural refactoring to match the hexagonal architecture design.

## Current Implementation Status

The codebase currently has:
- ✅ Working services layer (report_service, diagnostics_service, export_service, qbxml_generator, report_parser, scheduler)
- ✅ Working QuickBooks adapters (connection, error_handler, request_handler)
- ✅ Working utilities (file_utils, logging_utils)
- ✅ Working CLI and GUI applications
- ✅ Configuration management (config.py)
- ⚠️ Missing: Domain models (currently using dicts and config)
- ⚠️ Missing: Proper adapter classes with dependency injection
- ⚠️ Missing: Comprehensive test suite

---

## Phase 1: Domain Layer (Complete Missing Models)

- [x] 1. Create domain models




  - Create `domain/exceptions.py` with custom exception classes (QuickBooksError, QuickBooksConnectionError, ReportGenerationError, FileOperationError, SettingsError)
  - Create `domain/report_config.py` with ReportConfig dataclass to replace dict-based REPORT_CONFIGS
  - Create `domain/report_result.py` with ReportResult dataclass for structured return values
  - Create `domain/settings.py` with Settings dataclass to replace dict-based settings
  - Create `domain/diagnostics.py` with DiagnosticResult dataclass for diagnostic results
  - Add comprehensive type hints and validation methods
  - _Requirements: 2.1, 2.2, 2.3, 4.1, 4.2, 4.3, 4.4, 4.5_

- [ ]* 1.1 Write unit tests for domain models
  - Test ReportConfig creation and file path generation
  - Test ReportResult success/failure status
  - Test Settings validation
  - Test DiagnosticResult serialization
  - Test custom exception types
  - _Requirements: 7.1, 7.2, 7.3, 7.4_

---

## Phase 2: Refactor Adapters to Use Dependency Injection

- [ ] 2. Create proper adapter classes

  - Create `adapters/logger_adapter.py` with LoggerAdapter class wrapping logging_utils
  - Create `adapters/file_adapter.py` with FileAdapter class wrapping file_utils
  - Create `adapters/settings_adapter.py` with SettingsAdapter class wrapping config load/save
  - Refactor `adapters/quickbooks/connection.py` to use QuickBooksConnection class with context manager
  - Create `adapters/quickbooks/xml_builder.py` with XMLBuilder class wrapping qbxml_generator
  - Create `adapters/quickbooks/xml_parser.py` with XMLParser class wrapping report_parser
  - Add type hints to all adapter methods
  - _Requirements: 2.1, 2.2, 3.2, 3.3, 3.4, 6.1, 6.2, 6.3, 6.5_

- [ ]* 2.1 Write unit tests for adapters
  - Test logger adapter setup and emoji logging
  - Test file adapter read/write/hash operations
  - Test settings adapter load/save/validation
  - Test QuickBooks connection context manager
  - Test XML builder for all report types
  - Test XML parser for different response structures
  - _Requirements: 7.1, 7.2, 7.4_

---

## Phase 3: Refactor Services to Use Domain Models and DI

- [ ] 3. Refactor services to use domain models

  - Update `services/report_service.py` to use ReportConfig and ReportResult domain models
  - Update `services/export_service.py` to use ReportConfig domain model
  - Update `services/diagnostics_service.py` to use DiagnosticResult domain model
  - Create `services/csv_creator.py` with CSVCreator class (extract from export_service)
  - Create `services/excel_creator.py` with ExcelCreator class (extract from export_service)
  - Create `services/insights_generator.py` with InsightsGenerator class for data analysis
  - Refactor `services/scheduler.py` to use proper Scheduler class with dependency injection
  - Create `services/report_generator.py` as main orchestrator with full dependency injection
  - _Requirements: 2.1, 2.2, 3.1, 3.2, 3.3, 3.5, 3.6, 3.7, 3.8, 6.2, 6.4, 6.6_

- [ ]* 3.1 Write unit tests for refactored services
  - Test report generator with mocked dependencies
  - Test CSV creator with various data
  - Test Excel creator with formatting
  - Test insights generator for each report type
  - Test scheduler start/stop and thread safety
  - _Requirements: 7.1, 7.2, 7.4_

---

## Phase 4: Refactor Application Layer

- [ ] 4. Refactor CLI to use dependency injection

  - Move CLI logic from `src/quickbooks_autoreport/cli.py` to `apps/cli/__main__.py`
  - Setup proper dependency injection container
  - Inject adapters and services instead of importing functions
  - Update argument parsing and workflow orchestration
  - Maintain all existing CLI functionality
  - _Requirements: 2.1, 2.2, 11.1, 11.2, 11.3, 11.4, 11.5, 11.6_

- [ ] 5. Refactor GUI to use dependency injection

  - Move GUI logic from `src/quickbooks_autoreport/gui.py` to `apps/gui/main_window.py`
  - Create `apps/gui/__main__.py` as entry point
  - Extract widgets to `apps/gui/widgets/` (status_panel.py, config_panel.py, report_grid.py)
  - Setup proper dependency injection for GUI
  - Inject services instead of importing functions
  - Maintain all existing GUI functionality
  - _Requirements: 2.1, 2.2, 10.1, 10.2, 10.3, 10.4, 10.5, 10.6_

- [ ]* 5.1 Write integration tests for applications
  - Test CLI with different argument combinations
  - Test diagnostic mode
  - Test report generation mode
  - Test GUI initialization and event handlers
  - Test settings persistence
  - _Requirements: 7.1, 7.3, 7.4_

---

## Phase 5: Testing and Validation

- [ ] 6. Create comprehensive test suite

  - Create `tests/integration/test_report_flow.py` for end-to-end testing
  - Create `tests/fixtures/sample_responses.xml` with sample QB responses
  - Create mock QuickBooks connection for testing
  - Create temporary directory fixtures for file operations
  - Test complete report generation flow
  - Test CLI workflow with real file system
  - Test settings persistence across runs
  - Test error recovery scenarios
  - _Requirements: 7.1, 7.2, 7.3, 7.5, 7.6_

- [ ] 7. Verify backward compatibility

  - Test all 9 report types generate correctly
  - Verify CSV output matches original format
  - Verify Excel output matches original format
  - Verify settings file format compatibility
  - Verify log file format compatibility
  - Test scheduled execution works identically
  - Test diagnostics provide same information
  - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5, 12.6, 12.7_

- [ ] 8. Performance testing

  - Benchmark report generation time vs original
  - Benchmark Excel creation time vs original
  - Benchmark GUI startup time vs original
  - Benchmark memory usage vs original
  - Ensure performance is equivalent or better
  - _Requirements: 13.1, 13.2, 13.3, 13.4, 13.5_

- [ ] 9. Run code quality checks
  - Run `ruff check .` and fix all issues
  - Run `black --check .` and fix formatting
  - Run `isort --check-only .` and fix imports
  - Run `mypy src` and fix all type errors
  - Verify test coverage is >90% for core modules
  - _Requirements: 2.6, 7.4_

---

## Phase 6: Documentation and Cleanup

- [ ] 10. Update project documentation

  - Update `README.md` with new structure and usage
  - Create `docs/architecture.md` with architecture diagrams
  - Create `docs/migration_guide.md` for users
  - Create `docs/api_reference.md` from docstrings
  - Update `CHANGELOG.md` with refactoring details
  - _Requirements: 14.1, 14.2, 14.3, 14.4, 14.5_

- [ ] 11. Create migration script

  - Create script to help users migrate from old to new structure
  - Handle settings file migration if needed
  - Provide clear migration instructions
  - _Requirements: 14.4_

- [ ] 12. Final validation and cleanup
  - Run full test suite and verify all tests pass
  - Run all code quality checks and verify they pass
  - Test both CLI and GUI thoroughly
  - Verify all requirements are met
  - Remove or archive old `quickbooks_autoreport.py` file
  - Tag release with version number
  - _Requirements: All requirements_

---

## Implementation Notes

### Current Architecture vs Target

**Current State:**
- Functional programming style with module-level functions
- Dict-based configuration and return values
- Direct imports between modules
- Working but not following hexagonal architecture

**Target State:**
- Object-oriented with dependency injection
- Domain models (dataclasses) for all data structures
- Adapters injected into services
- Services injected into applications
- Clear separation of concerns

### Migration Strategy

1. **Create domain models first** - These are pure Python with no dependencies
2. **Wrap existing code in adapter classes** - Minimal changes to working code
3. **Refactor services to use domain models** - Update function signatures
4. **Update applications to use DI** - Wire everything together
5. **Add comprehensive tests** - Validate refactoring didn't break functionality
6. **Clean up old code** - Remove deprecated modules

### Key Principles

- **Don't break working code** - Wrap and refactor incrementally
- **Maintain backward compatibility** - All existing functionality must work
- **Test continuously** - Validate after each phase
- **Keep it simple** - Don't over-engineer the refactoring

## Success Criteria

The refactoring is complete when:

- ✅ All domain models are implemented and tested
- ✅ All adapters use dependency injection
- ✅ All services use domain models and DI
- ✅ Applications use proper DI containers
- ✅ Test coverage is >90% for core modules
- ✅ All linting and type checking passes
- ✅ Performance is equivalent or better
- ✅ All functionality works identically
- ✅ Documentation is complete
- ✅ Code follows hexagonal architecture principles
