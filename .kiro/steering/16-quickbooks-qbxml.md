---
inclusion: fileMatch
fileMatchPattern: ['**/quickbooks/**/*.*', '**/scripts/quickbooks/**/*.*', '**/*quickbooks*.*', '**/*qbxml*.*', '**/*qb_*.*']
---

# QuickBooks qbXML Report Generation

When generating QuickBooks-related code that creates qbXML requests, **ALWAYS** follow the QuickBooks Desktop qbXML Report Query Guide located at: `QuickBooks_Desktop_qbXML_ Report_Query_Guide.md`

## Critical Requirements

1. **Use the Guide**: Reference the complete guide before generating any qbXML code
2. **Follow Decision Flow**: Use the 6-step decision process outlined in the guide
3. **Validate Categories**: Only use supported options for each report category
4. **Required Filters**: Include mandatory filters (e.g., Missing Checks REQUIRES account filter)
5. **Use Date Macros**: Prefer date macros over explicit dates when possible

## Code Generation Rules

- **Always validate** report category and type combinations against the guide
- **Include proper XML envelope** with schema version 16.0
- **Use IncludeColumn** to specify only needed columns for lean payloads
- **Add category restrictions** as code comments for future developers
- **Generate debug mode** JSON planning when requested

## Example Integration

```python
def generate_qbxml_report(request_type: str, date_range: str, **options):
    """
    Generate qbXML report following QuickBooks Desktop SDK guidelines.
    
    Reference: QuickBooks_Desktop_qbXML_ Report_Query_Guide.md
    """
    # Step 1: Identify category based on request type
    # Step 2: Select specific report type
    # Step 3: Configure date range (prefer macros)
    # etc...
```

## Validation Checklist

Before generating qbXML code, ensure:
- [ ] Correct category selection
- [ ] Valid report type enum
- [ ] Supported options only
- [ ] Required filters included
- [ ] Proper XML structure