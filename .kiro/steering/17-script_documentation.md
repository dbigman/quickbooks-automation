---
inclusion: always
---
# Script Documentation Generator

Generate comprehensive documentation for Python scripts following project standards and best practices.

## Core Requirements

1. **Extract Complete API Surface**
   - Function signatures with type hints
   - Class definitions and methods
   - Module-level constants and variables
   - Import dependencies and requirements

2. **Documentation Structure**
   - Follow the established README format pattern
   - Include Quick Start section
   - Provide API Reference with examples
   - Add Configuration and Usage sections
   - Include troubleshooting guidance

3. **Content Standards**
   - Use clear, descriptive language
   - Provide practical usage examples
   - Include parameter descriptions and return types
   - Add error handling examples where relevant
   - Document environment variables and configuration

## Documentation Generation Process

### Step 1: Script Analysis
- Parse the target script to extract all public functions, classes, and constants
- Identify dependencies and requirements
- Extract existing docstrings and comments
- Analyze usage patterns within the script

### Step 2: Context7 Integration
- Use Context7 to gather additional documentation and examples from related libraries
- Research best practices for documented APIs and patterns
- Enhance examples with industry-standard approaches
- Validate technical accuracy of generated content

### Step 3: Content Generation
- Create comprehensive README following the established template:
  ```
  # [Script Name]
  
  [Brief description and purpose]
  
  ---
  **Documentation Metadata:**
  - **Created:** [YYYY-MM-DD HH:MM:SS UTC]
  - **Last Updated:** [YYYY-MM-DD HH:MM:SS UTC]  
  - **Version:** [Script Version or Documentation Version]
  - **Maintainer:** [Author/Team Name]
  ---
  
  ## Features
  - [Key capabilities]
  
  ## Quick Start
  ### Prerequisites
  ### Installation  
  ### Basic Usage
  
  ## API Reference
  ### Core Functions
  ### Utility Functions
  ### Classes (if applicable)
  
  ## Configuration
  ### Environment Variables
  ### Constants
  
  ## Output Files/Results
  ## Error Handling
  ## Integration Examples
  ## Troubleshooting
  
  ## Documentation Changelog
  
  ### [YYYY-MM-DD HH:MM:SS] - [Update Type]
  - **Added:** [New content added]
  - **Updated:** [Content that was modified]
  - **Fixed:** [Corrections made]
  - **Removed:** [Content that was removed]
  
  ## Contributing
  ## License
  ## Support
  ```

### Step 4: Quality Assurance
- Ensure all public APIs are documented
- Verify code examples are syntactically correct
- Check that documentation follows project style guidelines
- Validate that examples match actual script functionality

## Implementation Guidelines

### Function Documentation Format
```python
#### `function_name(param1: type, param2: type) -> return_type`

[Brief description of what the function does]

**Parameters:**
- `param1`: Description of parameter and its purpose
- `param2`: Description of parameter and its purpose

**Returns:**
- Description of return value and its type/structure

**Raises:**
- `ExceptionType`: When this exception occurs

**Example:**
```python
# Practical usage example
result = function_name("example", 42)
print(f"Result: {result}")
```
```

### Class Documentation Format
```python
#### `ClassName`

[Brief description of the class purpose and functionality]

**Key Methods:**

##### `method_name(param: type) -> return_type`
[Description of method functionality]

**Example:**
```python
# Class instantiation and usage
instance = ClassName()
result = instance.method_name("example")
```
```

### Configuration Documentation
- Document all environment variables with defaults
- Explain configuration file formats if applicable
- Provide example configurations
- Include validation rules and constraints

### Error Handling Documentation
- Document common error scenarios
- Provide troubleshooting steps
- Include example error messages
- Suggest solutions and workarounds

## Context7 Usage Guidelines

### Library Research
- When documenting functions that use external libraries, research the library using Context7
- Include relevant library-specific best practices
- Provide links to official documentation where helpful
- Ensure compatibility information is accurate

### Example Enhancement
- Use Context7 to find real-world usage patterns
- Enhance basic examples with production-ready code
- Include error handling patterns from industry standards
- Validate technical approaches against current best practices

### Technical Validation
- Cross-reference technical details with authoritative sources
- Verify API usage patterns are current and recommended
- Ensure security best practices are followed
- Validate performance considerations

## Change Tracking and Timestamp Management

### Documentation Metadata Requirements
- **All README files must include a metadata section** with creation and last updated timestamps
- **All documentation changes files must include detailed timestamps** for each modification
- **Use UTC timezone** for all timestamps to ensure consistency across different environments
- **Include version tracking** for both script and documentation versions

### README Timestamp Format
```markdown
---
**Documentation Metadata:**
- **Created:** 2025-01-15 14:30:22 UTC
- **Last Updated:** 2025-01-15 16:45:33 UTC
- **Script Version:** 7.2a
- **Documentation Version:** 2.1
- **Maintainer:** Development Team
- **Auto-Generated:** Yes/No
---
```

### Documentation Changes Timestamp Format
```markdown
# Documentation Changes Log

## [Script Name] - Documentation Enhancement

**Date:** 2025-01-15 16:45:33 UTC
**Script Version:** 7.2a
**Documentation Version:** 2.1
**Change Type:** Enhancement/Update/Fix/Initial Creation
**Maintainer:** [Author/Team Name]

### Timestamp Details
- **Started:** 2025-01-15 16:30:00 UTC
- **Completed:** 2025-01-15 16:45:33 UTC
- **Duration:** 15 minutes 33 seconds
- **Files Modified:** 3
- **Lines Changed:** +127 -23

### Changes Made

#### [16:32:15] - Enhanced Module Docstring
- **Added:** Comprehensive module-level documentation
- **Updated:** Feature overview and build instructions
- **Lines:** +45

#### [16:38:42] - Function Documentation Updates
- **Added:** Type hints for all public functions
- **Updated:** Parameter descriptions and return types
- **Lines:** +67 -15

#### [16:43:20] - README Generation
- **Created:** README_[script_name].md
- **Added:** Complete API reference with examples
- **Lines:** +234

### Validation Checklist
- [ ] All timestamps in UTC format
- [ ] Version numbers updated
- [ ] Change descriptions include line counts
- [ ] Duration calculated and recorded
- [ ] Files modified list is complete
```

### Automated Timestamp Generation
- **Creation timestamps:** Automatically set when documentation is first generated
- **Update timestamps:** Updated every time documentation is modified
- **Change tracking:** Each modification logged with specific timestamp and details
- **Version incrementation:** Automatic version bumping based on change type

### Timestamp Validation Rules
- All timestamps must follow ISO 8601 format: `YYYY-MM-DD HH:MM:SS UTC`
- Creation timestamp never changes after initial generation
- Last updated timestamp reflects the most recent modification
- Documentation version increments with each significant change
- Change log entries must be in chronological order (newest first)

## Quality Standards

### Content Requirements
- All public functions must have complete documentation
- Examples must be tested and functional
- Parameter types must match actual function signatures
- Return value documentation must be accurate

### Style Consistency
- Use consistent terminology throughout
- Follow project naming conventions
- Maintain consistent formatting and structure
- Use active voice and clear, concise language

### Technical Accuracy
- Verify all code examples execute without errors
- Ensure parameter descriptions match actual behavior
- Validate that error conditions are accurately documented
- Check that configuration options work as described

## Automation Considerations

### Script Integration
- Generate documentation that can be automatically updated
- Include metadata for tracking documentation freshness
- Design for integration with CI/CD pipelines
- Support incremental updates when script changes

### Maintenance
- Flag when script changes but documentation hasn't been updated
- Suggest documentation updates when new functions are added
- Validate that examples still work with current script version
- Check for broken links or outdated references

### Timestamp-Based Maintenance Alerts
- **Stale documentation warning:** Alert when documentation is >30 days older than script
- **Version mismatch detection:** Flag when script version doesn't match documented version
- **Automatic timestamp updates:** Update "Last Updated" timestamp on any documentation change
- **Change frequency tracking:** Monitor documentation update patterns for maintenance planning

## Special Considerations

### Legacy Code
- When documenting existing scripts, preserve historical context
- Note deprecated functions and suggest alternatives
- Include migration guidance where applicable
- Document backward compatibility considerations

### Security Documentation
- Document security considerations and best practices
- Include information about sensitive data handling
- Note authentication and authorization requirements
- Provide secure configuration examples

### Performance Documentation
- Include performance characteristics where relevant
- Document resource requirements and limitations
- Provide optimization suggestions
- Include benchmarking information if available

## Timestamp Implementation Guidelines

### Python Timestamp Generation
```python
import datetime

def generate_documentation_timestamp():
    """Generate UTC timestamp for documentation metadata."""
    return datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

def update_readme_timestamp(readme_path: str):
    """Update the 'Last Updated' timestamp in README metadata section."""
    timestamp = generate_documentation_timestamp()
    # Implementation to update the timestamp in the file
    pass

def create_change_log_entry(change_type: str, description: str):
    """Create a timestamped entry for documentation changes log."""
    timestamp = generate_documentation_timestamp()
    return f"#### [{timestamp}] - {change_type}\n- {description}"
```

### Timestamp Integration Examples
```markdown
<!-- Example README metadata section -->
---
**Documentation Metadata:**
- **Created:** 2025-01-15 14:30:22 UTC
- **Last Updated:** 2025-01-15 16:45:33 UTC
- **Script Version:** 7.2a
- **Documentation Version:** 2.1
- **Maintainer:** Development Team
- **Auto-Generated:** Yes
- **Next Review:** 2025-02-15 14:30:22 UTC
---

<!-- Example changelog entry with precise timestamps -->
#### [16:45:33] - API Enhancement
- **Added:** New export_with_filters() function
- **Updated:** Configuration section with new parameters
- **Duration:** 12 minutes
- **Lines:** +89 -12
- **Validated:** All examples tested and functional
```

### Automated Timestamp Workflows
1. **On Documentation Creation:**
   - Set creation timestamp (never changes)
   - Set initial last updated timestamp
   - Initialize documentation version to 1.0

2. **On Documentation Update:**
   - Update last updated timestamp
   - Increment documentation version
   - Add timestamped changelog entry
   - Calculate and record change duration

3. **On Script Modification:**
   - Flag documentation for review
   - Compare script and documentation versions
   - Generate maintenance alerts if needed

### Best Practices for Timestamp Management
- **Consistency:** Always use UTC timezone for all timestamps
- **Precision:** Use second-level precision for accurate tracking
- **Automation:** Implement automated timestamp updates where possible
- **Validation:** Verify timestamp formats match ISO 8601 standard
- **Archival:** Preserve historical timestamps in changelog entries