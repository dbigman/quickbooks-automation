---
inclusion: always
---

## inclusion: always

# MCP Tool Usage

## When to Use MCP Tools

Use MCP tools strategically to enhance code quality and decision-making in this QuickBooks Auto Reporter project.

## Sequential Thinking

**Tool**: `mcp_sequentialthinking_sequentialthinking`

**Use when**:

- Designing multi-step refactoring (e.g., domain model extraction)
- Debugging complex QuickBooks XML parsing issues
- Planning architectural changes to services or adapters
- Analyzing trade-offs between implementation approaches
- Breaking down non-trivial tasks from `tasks/tasks.md`

**Pattern**: Generate hypothesis → verify against requirements → iterate → provide solution

**Example scenarios**:

- "How should I refactor the MPS calculator to separate domain logic from Odoo adapter?"
- "What's causing this qbXML parsing failure with ItemInventoryQuery?"
- "Should I use dataclasses or Pydantic models for report configuration?"

## Context7

**Tools**: `mcp_context7_resolve_library_id`, `mcp_context7_get_library_docs`

**Use when**:

- Integrating new Python libraries (pandas, pydantic, streamlit)
- Verifying correct API usage for existing dependencies
- Checking for library updates or deprecated patterns
- Understanding best practices for unfamiliar libraries

**Required sequence**:

1. Call `resolve_library_id` with library name
2. Use returned ID with `get_library_docs` and specific topic

**Example scenarios**:

- "What's the current best practice for Pydantic v2 model validation?"
- "How should I use pandas for memory-efficient DataFrame operations?"
- "What's the recommended pattern for Streamlit multipage apps?"

## Time MCP

**Tools**: `mcp_time_get_current_time`, `mcp_time_convert_time`

**Use when**:

- Generating timestamps for reports, logs, or diagnostics
- Setting default date ranges in configuration
- Creating time-based filenames (e.g., `MPS_SheetName_YYYYMMDD_HHMMSS.xlsx`)
- Logging time-based events with accurate timestamps
- Converting between timezones for multi-region deployments
- Validating date ranges in user input

**Best practices**:

- Always use UTC for internal timestamps and storage
- Convert to local timezone only for display purposes
- Use ISO 8601 format (YYYY-MM-DDTHH:MM:SS) for consistency
- Document timezone assumptions in docstrings
- Use `America/Buenos_Aires` as local timezone when needed

**Example scenarios**:

- "Generate a UTC timestamp for the current report execution"
- "Create a filename with current date/time in YYYYMMDD_HHMMSS format"
- "Convert report timestamp from UTC to local timezone for display"
- "Validate that report_date_from is before report_date_to"

**Usage pattern**:

```python
# Get current time in UTC (recommended for all internal timestamps)
current_time = mcp_time_get_current_time(timezone="UTC")

# Get local time for display
local_time = mcp_time_get_current_time(timezone="America/Buenos_Aires")

# Convert between timezones
converted = mcp_time_convert_time(
    time="14:30",
    source_timezone="America/Buenos_Aires",
    target_timezone="UTC"
)
```

## Tool Selection Decision Tree

```text
Task type → Recommended tool

Complex logic/architecture → Sequential Thinking
Library documentation → Context7
Time/date operations → Time MCP
Code generation (boilerplate) → Standard code generation
Combination needed → Sequential Thinking (plan) + Context7 (verify) + Time MCP (timestamps)
```

## Integration with Project Workflow

**Before implementing**:

- Use Sequential Thinking for design planning
- Use Context7 to verify library patterns match current best practices

**During implementation**:

- Validate generated code against project patterns in `docs/technical.md`
- Ensure compliance with type hints and error handling standards
- Follow manufacturing domain patterns (FIFO, inventory tracking, etc.)

**After implementation**:

- Verify changes don't violate architectural boundaries
- Confirm test coverage meets >90% requirement for core modules

## Project-Specific Considerations

**QuickBooks Integration**:

- Always reference `QuickBooks_Desktop_qbXML_Report_Query_Guide.md` for qbXML generation
- Use Sequential Thinking for complex query construction
- Validate XML structure against SDK requirements

**Manufacturing Domain**:

- Maintain pandas/numpy patterns for data processing
- Preserve emoji-based logging (📥 📊 ✅)
- Keep warehouse location and BOM processing logic intact

**Performance Requirements**:

- MPS runs must complete within 2 minutes for 1000+ SKUs
- Memory optimization is critical for large datasets
- Use Context7 to verify efficient pandas patterns

## Validation Rules

- Always validate MCP tool outputs against existing project patterns
- Don't introduce new libraries without checking Context7 for best practices
- Use Sequential Thinking to verify architectural compliance before major changes
- Use Time MCP for all timestamp generation to ensure consistency and timezone accuracy
- Combine tools when appropriate (planning + verification + implementation + time operations)
