# Implementation Plan

This implementation plan reflects the current state of the refactoring. Significant progress has been made on the hexagonal architecture refactoring. The remaining tasks focus on completing the integration and testing.

## Current Implementation Status

The codebase currently has:

- ✅ Domain models fully implemented (exceptions, report_config, report_result, settings, diagnostics)
- ✅ Adapter classes with dependency injection (logger_adapter, file_adapter, settings_adapter, xml_builder, xml_parser)
- ✅ Apps layer structure created (apps/cli/__main__.py, apps/gui/__main__.py)
- ✅ Test structure created (unit/, integration/, fixtures/)
- ✅ Services layer implemented (report_generator, excel_creator, csv_creator, scheduler, diagnostics_service)
- ✅ GUI class implemented (QuickBooksAutoReporterGUI in src/quickbooks_autoreport/gui.py)
- ⚠️ Partial: QuickBooks connection adapter (still uses functional style, needs class-based refactor)
- ⚠️ Partial: CLI (functional implementation exists but apps/cli/__main__.py expects a CLI class)
- ⚠️ Partial: GUI (class exists but apps/gui/__main__.py expects a GUI class with different interface)
- ⚠️ Missing: Comprehensive test coverage
- ⚠️ Missing: Full integration of domain models in report_service.py (still uses old functional style)

---

## Phase 1: Complete QuickBooks Connection Adapter

- [x] 1. Refactor QuickBooks connection to class-based adapter
  - Create `QuickBooksConnection` class in `adapters/quickbooks/connection.py` with context manager support
  - Implement `__enter__` and `__exit__` methods for connection lifecycle
  - Add dependency injection for logger
  - Migrate functional code (open_connection, try_begin_session, etc.) to class methods
  - Update error handling to use domain exceptions
  - _Requirements: 2.1, 2.2, 3.2, 6.1, 6.2_

- [x]* 1.1 Write unit tests for QuickBooks connection adapter
  - Test connection context manager lifecycle
  - Test connection fallback strategies
  - Test session management
  - Test error translation to domain exceptions
  - _Requirements: 7.1, 7.2, 7.4_

---

## Phase 2: Complete Services Layer Refactoring

- [x] 2. Refactor report_service.py to use domain models and DI
  - Update `export_report()` to accept ReportConfig instead of report_key
  - Return ReportResult instead of dict
  - Inject QuickBooksConnection, FileAdapter, and other dependencies
  - Remove direct imports from config module
  - Update error handling to use domain exceptions
  - _Requirements: 2.1, 2.2, 3.1, 3.2, 6.2, 6.4_

- [x] 3. Complete report_generator.py implementation
  - Remove mock implementations from report_generator.py
  - Integrate with real QuickBooksConnection adapter (once Task 1 is complete)
  - Use CSVCreator and ExcelCreator services properly
  - Implement full change detection logic
  - Add insights generation integration
  - _Requirements: 3.1, 3.2, 3.5, 3.6, 6.2_

- [x] 4. Verify diagnostics_service.py implementation
  - ✅ Already returns proper diagnostic dict structure
  - ✅ Uses functional connection code (will use class once Task 1 complete)
  - ✅ Has comprehensive error handling
  - ✅ Creates Excel diagnostic reports
  - _Requirements: 2.1, 2.2, 3.7, 6.2_

- [x] 5. Verify CSVCreator and ExcelCreator services
  - ✅ CSVCreator properly extracted in services/csv_creator.py
  - ✅ ExcelCreator properly extracted in services/excel_creator.py
  - ✅ Both use logger injection
  - ✅ Both handle various data formats
  - _Requirements: 3.5, 3.6, 6.2_

- [x] 6. Verify scheduler.py implementation
  - ✅ SchedulerManager properly implements DI pattern
  - ✅ Uses callback pattern for status updates
  - ✅ Thread-safe with proper event handling
  - ✅ Supports dynamic interval and date range updates
  - _Requirements: 3.8, 6.2, 6.4_

- [x]* 6.1 Write unit tests for refactored services
  - Test report_service with mocked dependencies
  - Test report_generator orchestration
  - Test diagnostics_service with mocked QB connection
  - Test CSV and Excel creators with sample data
  - Test scheduler lifecycle and interval updates
  - _Requirements: 7.1, 7.2, 7.4_

---

## Phase 3: Complete Application Layer Integration

- [x] 7. Create CLI class wrapper for dependency injection
  - Create `CLI` class in `src/quickbooks_autoreport/cli.py` that wraps existing functional code
  - Accept injected dependencies (file_adapter, settings_adapter, xml_builder, xml_parser, logger_adapter, logger)
  - Implement `run(args)` method that delegates to existing functional code
  - Update `apps/cli/__main__.py` to work with the new CLI class
  - Maintain all existing CLI functionality and arguments
  - _Requirements: 2.1, 2.2, 11.1, 11.2, 11.3, 11.4, 11.5, 11.6_

- [x] 8. Create GUI class wrapper for dependency injection
  - Create `GUI` class in `src/quickbooks_autoreport/gui.py` that wraps QuickBooksAutoReporterGUI
  - Accept injected dependencies (file_adapter, settings_adapter, xml_builder, xml_parser, logger_adapter, logger)
  - Implement `run()` method that instantiates and runs QuickBooksAutoReporterGUI
  - Update `apps/gui/__main__.py` to work with the new GUI class
  - Maintain all existing GUI functionality
  - _Requirements: 2.1, 2.2, 10.1, 10.2, 10.3, 10.4, 10.5, 10.6_

- [x]* 8.1 Write integration tests for applications
  - Test CLI argument parsing and mode selection
  - Test CLI diagnostic mode execution
  - Test CLI report generation workflow
  - Test GUI initialization with mocked services
  - Test settings persistence through GUI
  - _Requirements: 7.1, 7.3, 7.4_

---

## Phase 4: Testing and Validation

- [x]* 9. Create comprehensive test suite
  - Implement `tests/integration/test_report_flow.py` for end-to-end testing
  - Enhance `tests/fixtures/sample_responses.xml` with all report types
  - Create mock QuickBooks connection for testing
  - Create temporary directory fixtures for file operations
  - Test complete report generation flow with real file I/O
  - Test error recovery scenarios
  - _Requirements: 7.1, 7.2, 7.3, 7.5, 7.6_

- [x] 10. Verify backward compatibility
  - Test all 9 report types generate correctly
  - Verify CSV output format matches original
  - Verify Excel output format matches original
  - Verify settings file format compatibility
  - Verify log file format and emoji indicators
  - Test scheduled execution works identically
  - Test diagnostics provide same information
  - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5, 12.6, 12.7_

- [x]* 11. Performance testing
  - Benchmark report generation time vs original implementation
  - Benchmark Excel creation time vs original
  - Benchmark GUI startup time vs original
  - Benchmark memory usage vs original
  - Ensure performance is equivalent or better
  - _Requirements: 13.1, 13.2, 13.3, 13.4, 13.5_

- [x] 12. Run code quality checks
  - Run `ruff check .` and fix all issues
  - Run `black --check .` and fix formatting
  - Run `isort --check-only .` and fix imports
  - Run `mypy src` and fix all type errors
  - Verify test coverage is >90% for core modules
  - _Requirements: 2.6, 7.4_

---

## Phase 5: Documentation and Cleanup

- [x] 13. Update project documentation
  - Update `README.md` with new structure and usage examples
  - Create `docs/architecture.md` with architecture diagrams
  - Create `docs/migration_guide.md` for users upgrading
  - Create `docs/api_reference.md` from docstrings
  - Update `CHANGELOG.md` with refactoring details
  - _Requirements: 14.1, 14.2, 14.3, 14.4, 14.5_

- [x]* 14. Create migration script
  - Create script to help users migrate settings from old to new format
  - Handle output directory migration if needed
  - Provide clear migration instructions and warnings
  - _Requirements: 14.4_

- [x] 15. Final validation and cleanup
  - Run full test suite and verify all tests pass
  - Run all code quality checks and verify they pass
  - Test both CLI and GUI thoroughly in real environment
  - Verify all requirements are met
  - Remove or archive old monolithic files if no longer needed
  - Update version number and tag release
  - _Requirements: All requirements_

---

## Implementation Notes

### Current Architecture vs Target

**Current State (Mostly Refactored):**

- ✅ Domain models implemented (dataclasses for all core entities)
- ✅ Adapter classes created with DI (logger, file, settings, xml_builder, xml_parser)
- ✅ Apps layer structure with DI entry points created
- ✅ Services layer implemented (report_generator, excel_creator, csv_creator, scheduler, diagnostics)
- ✅ GUI class implemented (QuickBooksAutoReporterGUI)
- ✅ CLI functional implementation complete
- ⚠️ QuickBooks connection still functional (needs class-based refactor)
- ⚠️ report_service.py still uses old functional style (needs refactor to use domain models)
- ⚠️ Apps layer expects CLI/GUI wrapper classes that don't exist yet

**Target State:**

- Object-oriented with full dependency injection throughout
- All services use domain models (ReportConfig, ReportResult, Settings, etc.)
- QuickBooksConnection as class with context manager
- All business logic in services, all I/O in adapters
- CLI and GUI in apps/ with thin DI wrappers around existing implementations
- Clear separation of concerns following hexagonal architecture

### Migration Strategy

1. ✅ **Domain models created** - All core entities as dataclasses
2. ✅ **Adapter classes created** - File, logger, settings, XML adapters with DI
3. ✅ **Services layer implemented** - Most services complete (scheduler, diagnostics, excel_creator, csv_creator)
4. ⚠️ **QuickBooks connection** - Still functional, needs class-based refactor
5. ⚠️ **report_service.py** - Needs refactor to use domain models instead of dicts
6. ⚠️ **Applications** - Need thin wrapper classes for DI compatibility
7. ⚠️ **Testing** - Structure created, need comprehensive tests
8. ⚠️ **Cleanup pending** - Need to verify all functionality and run quality checks

### Key Principles

- **Incremental migration** - Complete one service at a time
- **Maintain backward compatibility** - All existing functionality must work
- **Test as you go** - Add tests for each refactored component
- **Keep it simple** - Don't over-engineer, follow established patterns

### Critical Path

The most important tasks to complete the refactoring:

1. **QuickBooksConnection class** (Task 1) - Foundation for all QB interactions
2. **report_service.py refactor** (Task 2) - Update to use domain models
3. **report_generator.py completion** (Task 3) - Remove mocks, integrate real connection
4. **Application layer wrappers** (Tasks 7-8) - Create CLI/GUI wrapper classes for DI
5. **Backward compatibility validation** (Task 10) - Ensure all functionality works
6. **Code quality checks** (Task 12) - Run linting, formatting, type checking
7. **Final cleanup** (Task 15) - Verify everything and prepare for release

## Success Criteria

The refactoring is complete when:

- ✅ All domain models are implemented
- ⚠️ All adapters use dependency injection (QuickBooksConnection needs class-based refactor)
- ⚠️ All services use domain models and DI (report_service.py needs update)
- ⚠️ Applications use proper DI containers (wrapper classes needed)
- ⚠️ Test coverage is >90% for core modules (tests need implementation)
- ⚠️ All linting and type checking passes (needs verification)
- ⚠️ Performance is equivalent or better (needs validation)
- ⚠️ All functionality works identically (needs validation)
- ⚠️ Documentation is complete (needs updates)
- ⚠️ Code follows hexagonal architecture principles (mostly complete, needs final touches)
