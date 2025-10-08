# Tasks Document

This tasks plan is aligned to the approved requirements [requirements.md](.spec-workflow/specs/quickbooks-autoreport-refactoring/requirements.md:1) and design [design.md](.spec-workflow/specs/quickbooks-autoreport-refactoring/design.md:1). Follow spec-workflow Implementation rules: mark each task as in-progress by changing "[ ]" to "[-]" when you start, and mark complete by changing "[-]" to "[x]" when finished.

- [x] 1. Write unit tests for domain models

  - Files: [tests/unit/test_domain/test_report_config.py](tests/unit/test_domain/test_report_config.py), [tests/unit/test_domain/test_report_result.py](tests/unit/test_domain/test_report_result.py), [tests/unit/test_domain/test_settings.py](tests/unit/test_domain/test_settings.py), [tests/unit/test_domain/test_diagnostics.py](tests/unit/test_domain/test_diagnostics.py)
  - Purpose: Verify dataclass behavior, validation, and serialization for domain models
  - Steps:
    - Add tests for creation, immutability (where applicable), and methods
    - Validate error cases and edge cases (invalid dates, intervals)
    - Ensure serialization methods return correct structures
  - \_Leverage: [report_config.py](src/quickbooks_autoreport/domain/report_config.py:1), [report_result.py](src/quickbooks_autoreport/domain/report_result.py:1), [settings.py](src/quickbooks_autoreport/domain/settings.py:1), [diagnostics.py](src/quickbooks_autoreport/domain/diagnostics.py:1)
  - \_Requirements: 2.1, 2.2, 2.3, 4.1, 4.2, 4.3, 4.4, 7.1, 7.2, 7.3, 7.4
  - \_Prompt: Implement the task for spec quickbooks-autoreport-refactoring, first run spec-workflow-guide to get the workflow guide then implement the task: Create comprehensive unit tests for domain models with clear success/failure scenarios. Restrictions: do not modify domain model APIs; preserve immutability where declared; follow naming conventions. Success: tests run deterministic, cover positive and negative paths, and pass in CI. Instructions: Edit [tasks.md](.spec-workflow/specs/quickbooks-autoreport-refactoring/tasks.md:1) and change this task to [-] when starting, then [x] when complete.

- [x] 2. Establish adapter classes and explicit DI

  - Files: [logger_adapter.py](src/quickbooks_autoreport/adapters/logger_adapter.py), [file_adapter.py](src/quickbooks_autoreport/adapters/file_adapter.py), [settings_adapter.py](src/quickbooks_autoreport/adapters/settings_adapter.py), [connection.py](src/quickbooks_autoreport/adapters/quickbooks/connection.py:1), [request_handler.py](src/quickbooks_autoreport/adapters/quickbooks/request_handler.py:1), [error_handler.py](src/quickbooks_autoreport/adapters/quickbooks/error_handler.py:1)
  - Purpose: Provide clear interfaces for I/O and QuickBooks integration with injected dependencies
  - Steps:
    - Wrap existing utilities into adapter classes
    - Ensure all adapters accept dependencies via constructor (logger, settings path, etc.)
    - Document public methods and types
  - \_Leverage: [file_utils.py](src/quickbooks_autoreport/utils/file_utils.py:1), [logging_utils.py](src/quickbooks_autoreport/utils/logging_utils.py:1)
  - \_Requirements: 2.1, 2.2, 3.2, 3.3, 3.8, 6.1, 6.2, 6.3, 6.5
  - \_Prompt: Implement the task for spec quickbooks-autoreport-refactoring, first run spec-workflow-guide to get the workflow guide then implement the task: Create adapter classes with explicit constructors and typed methods, encapsulating I/O and QuickBooks COM operations. Restrictions: do not introduce side effects in services; do not hardcode paths; avoid global state. Success: adapters are testable and injectable with clear interfaces.

- [x] 3. Adapter unit tests

  - Files: [tests/unit/test_adapters/test_file_adapter.py](tests/unit/test_adapters/test_file_adapter.py), [tests/unit/test_adapters/test_settings_adapter.py](tests/unit/test_adapters/test_settings_adapter.py), [tests/unit/test_adapters/test_connection.py](tests/unit/test_adapters/test_connection.py), [tests/unit/test_adapters/test_xml_pipeline.py](tests/unit/test_adapters/test_xml_pipeline.py)
  - Purpose: Validate adapters independently with mocks/fakes
  - Steps:
    - Test file read/write/hash and directory handling
    - Test settings load/save/defaults/validation
    - Test connection lifecycle with context manager patterns
    - Test qbXML build/parse flows via request/response samples
  - \_Leverage: [connection.py](src/quickbooks_autoreport/adapters/quickbooks/connection.py:1), [qbxml_generator.py](src/quickbooks_autoreport/services/qbxml_generator.py:1), [report_parser.py](src/quickbooks_autoreport/services/report_parser.py:1)
  - \_Requirements: 7.1, 7.2, 7.4
  - \_Prompt: Implement the task for spec quickbooks-autoreport-refactoring, first run spec-workflow-guide to get the workflow guide then implement the task: Write isolated adapter tests using mocks and fixture data. Restrictions: do not call real COM; do not perform real filesystem writes without tmp directories. Success: high coverage, deterministic behavior, and robust error scenario tests.

- [x] 4. Refactor services to use domain models and DI

  - Files: [report_service.py](src/quickbooks_autoreport/services/report_service.py:1), [export_service.py](src/quickbooks_autoreport/services/export_service.py:1), [diagnostics_service.py](src/quickbooks_autoreport/services/diagnostics_service.py:1), [scheduler.py](src/quickbooks_autoreport/services/scheduler.py:1), [report_generator.py](src/quickbooks_autoreport/services/report_generator.py), [csv_creator.py](src/quickbooks_autoreport/services/csv_creator.py), [excel_creator.py](src/quickbooks_autoreport/services/excel_creator.py), [insights_generator.py](src/quickbooks_autoreport/services/insights_generator.py)
  - Purpose: Ensure business logic orchestrates adapters and uses typed domain models end-to-end
  - Steps:
    - Update signatures to accept domain models (ReportConfig, ReportResult)
    - Inject adapters via constructors; remove internal instantiations
    - Extract CSV/Excel creators into dedicated classes
    - Implement ReportGenerator orchestrator with typed return values
  - \_Leverage: [report_config.py](src/quickbooks_autoreport/domain/report_config.py:1), [report_result.py](src/quickbooks_autoreport/domain/report_result.py:1)
  - \_Requirements: 2.1, 2.2, 3.1, 3.2, 3.5, 3.6, 3.7, 3.8, 6.2, 6.4, 6.6
  - \_Prompt: Implement the task for spec quickbooks-autoreport-refactoring, first run spec-workflow-guide to get the workflow guide then implement the task: Refactor service layer to dependency injection and typed models. Restrictions: do not perform I/O in services; respect separation of concerns. Success: services compile, tests pass, and logic is isolated from I/O.

- [x] 5. Service unit tests

  - Files: [tests/unit/test_services/test_report_generator.py](tests/unit/test_services/test_report_generator.py), [tests/unit/test_services/test_csv_creator.py](tests/unit/test_services/test_csv_creator.py), [tests/unit/test_services/test_excel_creator.py](tests/unit/test_services/test_excel_creator.py), [tests/unit/test_services/test_insights_generator.py](tests/unit/test_services/test_insights_generator.py), [tests/unit/test_services/test_scheduler.py](tests/unit/test_services/test_scheduler.py)
  - Purpose: Validate business logic correctness and error handling
  - Steps:
    - Mock adapters for orchestration tests
    - Validate formatting outputs and insights generation
    - Verify scheduler start/stop/thread safety
  - \_Leverage: [qbxml_generator.py](src/quickbooks_autoreport/services/qbxml_generator.py:1), [report_parser.py](src/quickbooks_autoreport/services/report_parser.py:1)
  - \_Requirements: 7.1, 7.2, 7.4
  - \_Prompt: Implement the task for spec quickbooks-autoreport-refactoring, first run spec-workflow-guide to get the workflow guide then implement the task: Write comprehensive unit tests for services using mocks and fixtures. Restrictions: no real I/O; ensure deterministic tests. Success: coverage and reliability meet thresholds.

- [x] 6. Refactor CLI to dependency injection

  - Files: [**main**.py](apps/cli/__main__.py), [cli.py](src/quickbooks_autoreport/cli.py:1)
  - Purpose: Use DI to compose services/adapters for CLI workflows
  - Steps:
    - Create apps/cli entry point and wire dependencies
    - Move orchestration from src CLI into apps CLI with DI
    - Preserve command-line options and diagnostic mode
  - \_Leverage: [LoggerAdapter](src/quickbooks_autoreport/adapters/logger_adapter.py), [SettingsAdapter](src/quickbooks_autoreport/adapters/settings_adapter.py), [ReportGenerator](src/quickbooks_autoreport/services/report_generator.py)
  - \_Requirements: 2.1, 2.2, 11.1, 11.2, 11.3, 11.4, 11.5, 11.6
  - \_Prompt: Implement the task for spec quickbooks-autoreport-refactoring, first run spec-workflow-guide to get the workflow guide then implement the task: Refactor CLI to apps/cli with DI. Restrictions: maintain existing flags and behaviors; do not break diagnostic mode. Success: CLI runs and composes dependencies via DI.

- [x] 7. Refactor GUI to dependency injection

  - Files: [**main**.py](apps/gui/__main__.py), [main_window.py](apps/gui/main_window.py), [gui.py](src/quickbooks_autoreport/gui.py:1), [widgets/**init**.py](apps/gui/widgets/__init__.py), [widgets/status_panel.py](apps/gui/widgets/status_panel.py), [widgets/config_panel.py](apps/gui/widgets/config_panel.py), [widgets/report_grid.py](apps/gui/widgets/report_grid.py)
  - Purpose: Initialize GUI via DI and modularize widgets
  - Steps:
    - Create apps/gui structure with entry point and widgets
    - Inject services into GUI components
    - Ensure responsiveness and settings persistence
  - \_Leverage: [Scheduler](src/quickbooks_autoreport/services/scheduler.py:1), [ReportGenerator](src/quickbooks_autoreport/services/report_generator.py)
  - \_Requirements: 2.1, 2.2, 10.1, 10.2, 10.3, 10.4, 10.5, 10.6
  - \_Prompt: Implement the task for spec quickbooks-autoreport-refactoring, first run spec-workflow-guide to get the workflow guide then implement the task: Refactor GUI to apps/gui with DI. Restrictions: preserve GUI feature parity and responsiveness. Success: GUI initializes and operates with injected services.

- [x] 8. Application integration tests

  - Files: [tests/integration/test_cli_workflows.py](tests/integration/test_cli_workflows.py), [tests/integration/test_gui_init.py](tests/integration/test_gui_init.py)
  - Purpose: Validate end-to-end flows for CLI and GUI
  - Steps:
    - Test CLI arguments, diagnostic mode, and report generation flow
    - Test GUI initialization and event handlers with mocks
  - \_Leverage: [tests/fixtures](tests/fixtures)
  - \_Requirements: 7.1, 7.3, 7.4
  - \_Prompt: Implement the task for spec quickbooks-autoreport-refactoring, first run spec-workflow-guide to get the workflow guide then implement the task: Write integration tests for apps. Restrictions: maintain isolation; use fixtures and tmp dirs. Success: key workflows validated.

- [x] 9. Comprehensive report flow testing

  - Files: [tests/integration/test_report_flow.py](tests/integration/test_report_flow.py), [tests/fixtures/sample_responses.xml](tests/fixtures/sample_responses.xml)
  - Purpose: Validate complete report generation pipeline
  - Steps:
    - Build fixtures for sample qbXML responses and expected outputs
    - Verify CSV/Excel outputs and change detection/hash updates
  - \_Leverage: [qbxml_generator.py](src/quickbooks_autoreport/services/qbxml_generator.py:1), [report_parser.py](src/quickbooks_autoreport/services/report_parser.py:1), [file_utils.py](src/quickbooks_autoreport/utils/file_utils.py:1)
  - \_Requirements: 7.1, 7.2, 7.3, 7.5, 7.6
  - \_Prompt: Implement the task for spec quickbooks-autoreport-refactoring, first run spec-workflow-guide to get the workflow guide then implement the task: Test end-to-end report flow across report types. Restrictions: avoid real QuickBooks; simulate responses. Success: end-to-end validation passes.

- [x] 10. Backward compatibility verification

  - Files: [quickbooks_autoreport.py](quickbooks_autoreport.py:1), [export_service.py](src/quickbooks_autoreport/services/export_service.py:1)
  - Purpose: Ensure behavior parity for outputs, settings, logs, and scheduling
  - Steps:
    - Compare outputs to historical formats
    - Validate settings file format and log compatibility
    - Verify all 9 report types generate correctly
  - \_Leverage: [README.md](README.md:1)
  - \_Requirements: 12.1, 12.2, 12.3, 12.4, 12.5, 12.6, 12.7
  - \_Prompt: Implement the task for spec quickbooks-autoreport-refactoring, first run spec-workflow-guide to get the workflow guide then implement the task: Verify backward compatibility. Restrictions: do not change public-facing formats. Success: parity across outputs and features.

- [x] 11. Performance testing

  - Files: [tests/integration/test_performance.py](tests/integration/test_performance.py)
  - Purpose: Benchmark report generation, Excel creation, GUI startup, and memory
  - Steps:
    - Add micro-benchmarks and scenario timings
    - Ensure performance is equivalent or better than current implementation
  - \_Leverage: [scheduler.py](src/quickbooks_autoreport/services/scheduler.py:1)
  - \_Requirements: 13.1, 13.2, 13.3, 13.4, 13.5
  - \_Prompt: Implement the task for spec quickbooks-autoreport-refactoring, first run spec-workflow-guide to get the workflow guide then implement the task: Create performance tests and compare baselines. Restrictions: avoid flaky measurements; use controlled environments. Success: meets performance targets.

- [x] 12. Code quality checks

  - Files: [pyproject.toml](pyproject.toml:1)
  - Purpose: Enforce ruff, black, isort, mypy with strict settings
  - Steps:
    - Configure and run tools; fix issues
    - Achieve >90% coverage in core modules
  - \_Leverage: [tests/test_basic.py](tests/test_basic.py:1)
  - \_Requirements: 2.6, 7.4
  - \_Prompt: Implement the task for spec quickbooks-autoreport-refactoring, first run spec-workflow-guide to get the workflow guide then implement the task: Run and satisfy code quality gates. Restrictions: do not relax strict mode; fix issues properly. Success: all checks pass.

- [x] 13. Documentation updates

  - Files: [README.md](README.md:1), [ARCHITECTURE.md](ARCHITECTURE.md:1), [docs/migration_guide.md](docs/migration_guide.md), [docs/api_reference.md](docs/api_reference.md)
  - Purpose: Reflect new architecture, migration path, and public APIs
  - Steps:
    - Update README with structure/usage
    - Add architecture diagrams and ADRs if applicable
    - Document public APIs from docstrings; write migration guide
  - \_Leverage: [design.md](.spec-workflow/specs/quickbooks-autoreport-refactoring/design.md:1), [requirements.md](.spec-workflow/specs/quickbooks-autoreport-refactoring/requirements.md:1)
  - \_Requirements: 14.1, 14.2, 14.3, 14.4, 14.5
  - \_Prompt: Implement the task for spec quickbooks-autoreport-refactoring, first run spec-workflow-guide to get the workflow guide then implement the task: Update documentation per spec. Restrictions: ensure accuracy and consistency; do not expose sensitive info. Success: docs are complete and accurate.

- [x] 14. Migration script (optional if parity confirmed)

  - Files: [scripts/migrate_monolith_to_hex.py](scripts/migrate_monolith_to_hex.py)
  - Purpose: Assist users in migrating old settings/files to new structure
  - Steps:
    - Provide re-mapping for settings paths and logs
    - Validate migrated environment
  - \_Leverage: [settings.py](src/quickbooks_autoreport/domain/settings.py:1)
  - \_Requirements: 14.4
  - \_Prompt: Implement the task for spec quickbooks-autoreport-refactoring, first run spec-workflow-guide to get the workflow guide then implement the task: Create migration helper script. Restrictions: non-destructive; backup originals. Success: migrations succeed with validations.

- [x] 15. Final validation and cleanup
  - Files: [CHANGELOG.md](CHANGELOG.md), [PROJECT_COMPLETE.md](PROJECT_COMPLETE.md:1)
  - Purpose: Validate all tasks and quality gates, archive obsolete artifacts if any
  - Steps:
    - Run full test suite; confirm all green
    - Re-run code quality; confirm strict compliance
    - Comprehensive manual verification (CLI/GUI)
    - Tag release version and compile final report
  - \_Leverage: [spec-status](.spec-workflow/specs/quickbooks-autoreport-refactoring/tasks.md:1)
  - \_Requirements: All
  - \_Prompt: Implement the task for spec quickbooks-autoreport-refactoring, first run spec-workflow-guide to get the workflow guide then implement the task: Perform final validation and cleanup. Restrictions: do not remove needed files; ensure full parity. Success: release tagged and documentation finalized.
