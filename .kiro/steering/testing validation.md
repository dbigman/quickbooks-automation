---
inclusion: always
---

# Testing & Validation Standards

## Test Requirements

### Mandatory Test Coverage

- **>90% coverage** for `calculator.py`, `connector.py`, `exporter.py`
- **Unit tests** in `tests/test_*.py` using pytest framework
- **Integration tests** for Odoo JSON-RPC API calls and Excel generation
- **Performance tests** must complete <2 minutes for 1000+ SKU datasets

### Critical Business Logic Tests

- **MPS Algorithms**: Test FIFO, LIFO, EDD, Priority with realistic order data
- **Inventory Calculations**: Validate warehouse locations (WH1/Stock, WH2/Stock, A1A-A2C racks)
- **BOM Processing**: Multi-level component explosion with shortage classification
- **Priority Scoring**: Customer importance, delivery urgency, order value weighting

## Test Data Standards

### Required DataFrame Structures

```python
# Sales Orders Test Data
orders_df = pd.DataFrame({
    'product_id': [1, 2, 3],
    'quantity': [100, 50, 200],
    'delivery_date': ['2024-08-15', '2024-08-20', '2024-08-10'],
    'customer': ['Customer A', 'Customer B', 'Customer C'],
    'priority': [1, 2, 3]
})

# Inventory Test Data (with warehouse locations)
inventory_df = pd.DataFrame({
    'product_id': [1, 2, 3],
    'WH1/Stock': [50, 100, 0],
    'WH2/Stock': [25, 0, 150],
    'total_available_qty': [75, 100, 150]
})
```

### Edge Cases to Test

- **Zero/negative inventory** products
- **Missing BOM** components
- **Past delivery dates** (overdue orders)
- **Large datasets** (1000+ products for performance)
- **Malformed data** (NaN values, wrong data types)

## Validation Patterns

### Standard DataFrame Validation

```python
def validate_mps_dataframe(df: pd.DataFrame) -> None:
    """Validate MPS calculation results."""
    required_cols = ['product_id', 'priority_score', 'shortage_status']
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    # Business logic validation
    assert df['priority_score'].min() >= 0, "Priority scores must be non-negative"
    assert df['shortage_status'].isin(['OK', 'MINOR', 'MODERATE', 'CRITICAL']).all()
```

### Algorithm Output Validation

```python
def test_priority_algorithm_output(result_df: pd.DataFrame) -> None:
    """Test priority algorithm produces valid business results."""
    # Structural validation
    assert 'priority_score' in result_df.columns
    assert len(result_df) > 0

    # Business logic validation
    urgent_orders = result_df[result_df['delivery_date'] <= pd.Timestamp.now()]
    if not urgent_orders.empty:
        assert urgent_orders['priority_score'].min() > 0.7  # Urgent orders get high priority
```

## Integration Testing

### Odoo API Testing

- **Mock Odoo responses** for consistent testing
- **Test authentication failure** scenarios
- **Validate DataFrame structure** from API responses
- **Test network timeout** handling with retry logic

### Excel Export Testing

- **Verify file creation** in `output/` directory
- **Validate multi-sheet structure** (Summary, Orders, Inventory, Shortages)
- **Test conditional formatting** application
- **Performance test** with large datasets

## Performance & Memory Standards

### Performance Benchmarks

- **MPS calculation**: <2 minutes for 1000 SKUs
- **Memory optimization**: Use `pd.to_numeric()` early, achieve >20% memory reduction
- **Excel export**: Handle large reports efficiently without memory errors

### Memory Testing Pattern

```python
def test_memory_optimization():
    """Test memory usage optimization for large datasets."""
    large_df = create_large_test_dataset(1000)  # 1000 products
    initial_memory = large_df.memory_usage(deep=True).sum()

    optimized_df = optimize_dataframe_types(large_df)
    final_memory = optimized_df.memory_usage(deep=True).sum()

    memory_reduction = (initial_memory - final_memory) / initial_memory
    assert memory_reduction > 0.2  # >20% memory reduction required
```

## Error Handling Tests

### Network Failure Simulation

```python
@patch('requests.post')
def test_odoo_connection_failure(mock_post):
    """Test graceful handling of Odoo connection failures."""
    mock_post.side_effect = requests.ConnectionError("Network unreachable")

    connector = OdooConnector(logger)
    with pytest.raises(ConnectionError):
        connector.authenticate()

    # Verify proper error logging occurred
    assert "Network unreachable" in caplog.text
```

### Data Quality Issue Handling

- **Test malformed CSV** data handling
- **Validate graceful degradation** for missing data
- **Ensure warnings logged** without stopping execution

## Test Execution Requirements

### Pre-commit Validation

```bash
# Run before any commit
pytest tests/ -v --cov --cov-report=term-missing --cov-fail-under=90
black . --check
flake8 . --max-line-length=80
mypy . --strict
```

### Manufacturing Domain Tests

- **Warehouse location mapping** accuracy (8 active locations)
- **Product category validation** (Packaging Material, Materia Prima, etc.)
- **BOM explosion logic** for multi-level components
- **Shortage classification** business rules (days of supply thresholds)

## Quality Gates

### Commit Requirements

- [ ] All tests pass with >90% coverage
- [ ] No linting errors (black, flake8, mypy)
- [ ] Performance benchmarks met
- [ ] Manufacturing business logic validated

### Release Requirements

- [ ] Integration tests with Odoo API succeed
- [ ] Excel exports generate with proper formatting
- [ ] Error scenarios handled gracefully
- [ ] Memory usage optimized for production datasets
