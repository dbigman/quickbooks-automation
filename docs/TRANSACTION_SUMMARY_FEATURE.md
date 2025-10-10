# Transaction Summary Feature

## Overview

Added transaction-level summary table that groups line items by transaction number (Num) and shows the date, customer, type, and total amount for each transaction.

## Purpose

The Transaction Summary provides a high-level view of all transactions:
- **Invoice totals**: See complete invoice amounts
- **Transaction tracking**: Track individual transactions by number
- **Customer analysis**: View all transactions per customer
- **Date-based reporting**: Analyze transactions by date
- **Return tracking**: Identify credit memos and their amounts

## Structure

### Grouping
Transactions are grouped by `Num` (transaction number), which uniquely identifies each invoice, credit memo, sales receipt, etc.

### Columns
- **Num**: Transaction number (e.g., INV25-10792, CR25-0536)
- **Date**: Transaction date
- **Type**: Transaction type (Invoice, Credit Memo, Sales Receipt, etc.)
- **Customer**: Customer name
- **Transaction_Total**: Sum of all line item amounts for that transaction

## Calculation

```python
Transaction_Total = SUM(Amount) for all lines with same Num
```

Each transaction can have multiple line items (products), and the Transaction_Total is the sum of all those line amounts.

## Examples

### Multi-Line Invoice
```
Transaction: INV25-10792
Line 1: DOT Mold Cleaner 1 gal. × 500 = $1,800.00
Line 2: DOT Mold Cleaner 1 gal. × 500 = $1,800.00
Line 3: DOT Mold Cleaner 1 gal. × 500 = $1,800.00
Line 4: DOT Mold Cleaner 1 gal. × 500 = $1,800.00
Line 5: DOT Mold Cleaner 1 gal. × 400 = $1,440.00
Line 6: DOT Mold Cleaner 1 gal. × 500 = $1,800.00
Line 7: DOT Mold Cleaner 32 oz. × 300 = $294.00
Line 8: DOT Mold Cleaner 32 oz. × 700 = $686.00
... (more lines)
Transaction_Total: $12,811.00
```

### Credit Memo
```
Transaction: CR25-0536
Line 1: BELCA Vinagre × -109 = -$1,232.79
Transaction_Total: -$1,232.79
```

## Sample Output

### Largest Transactions
```
        Num                               Customer  Transaction_Total
INV25-10792                             Sudoc, LLC           12811.00
INV25-10790                             Sudoc, LLC            8193.00
INV25-10778                          Prime Lab LLC            3322.62
INV25-10777 Colegio Aguadeño San Francisco de Asis            3173.30
INV25-10774               Union de Mayoristas Coop            3000.00
```

### All Transaction Types
```
        Num       Date        Type                               Customer  Transaction_Total
  CR25-0535 2025-10-06 Credit Memo                     Sánchez Food Sales           -1006.48
  CR25-0536 2025-10-06 Credit Memo                 Mister Price, Mayagüez           -1232.79
INV25-10774 2025-10-06     Invoice               Union de Mayoristas Coop            3000.00
INV25-10775 2025-10-06     Invoice                             Pharma Max             361.92
INV25-10776 2025-10-06     Invoice                 Parador Boquemar, INC.             343.82
```

## Use Cases

### 1. Transaction Verification
Verify that transaction totals match expected amounts:
```python
# Find specific transaction
transaction = df[df['Num'] == 'INV25-10792']
print(f"Invoice total: ${transaction['Transaction_Total'].values[0]:,.2f}")
```

### 2. Daily Sales Summary
Group by date to see daily totals:
```python
daily_sales = df.groupby('Date')['Transaction_Total'].sum()
```

### 3. Customer Transaction History
View all transactions for a specific customer:
```python
customer_trans = df[df['Customer'] == 'Sudoc, LLC']
print(customer_trans[['Num', 'Date', 'Transaction_Total']])
```

### 4. Return Analysis
Identify all credit memos:
```python
returns = df[df['Type'] == 'Credit Memo']
print(f"Total returns: ${returns['Transaction_Total'].sum():,.2f}")
```

### 5. Average Transaction Size
Calculate average transaction value:
```python
avg_transaction = df['Transaction_Total'].mean()
print(f"Average transaction: ${avg_transaction:,.2f}")
```

## Validation

The sum of all Transaction_Total values equals the sum of all line item amounts:
```
Sum of all transaction lines: $46,019.31
Sum of transaction totals:    $46,019.31
✓ Match confirmed
```

## Statistics

From test data (`data/item sales detail wk 41w.CSV`):
- **Total transactions**: 33
- **Total line items**: 86
- **Average lines per transaction**: 2.6
- **Largest transaction**: $12,811.00 (INV25-10792)
- **Smallest transaction**: -$1,232.79 (CR25-0536, credit memo)

## Output Locations

Transaction Summary appears in:
1. **Transaction Summary** sheet in Excel (`output/sales_analysis_YYYYMMDD_HHMMSS.xlsx`) - All transactions sorted by date
2. **Console output** - Sample of first 15 transactions (also shows top 10 products and top 10 customers)
3. **Available via API** - `create_transaction_summary()` function

The `output` directory is automatically created if it doesn't exist.

**Filename includes timestamp** to prevent overwriting previous analyses.

## Implementation

### Files Modified

1. **`analyze_sales_data.py`**
   - Added `create_transaction_summary()` function
   - Updated main() to generate and display transaction summary
   - Added Transaction Summary sheet to Excel export

2. **`src/quickbooks_autoreport/extractors/item_sales_detail_extractor.py`**
   - Added `create_transaction_summary()` method
   - Updated `export_all_dataframes()` to include transaction summary

3. **Documentation**
   - Updated `docs/item_sales_detail_extractor.md`
   - Created `TRANSACTION_SUMMARY_FEATURE.md`

## Testing

Verified with `data/item sales detail wk 41w.CSV`:
- ✅ 33 unique transactions identified
- ✅ Transaction totals calculated correctly
- ✅ Multi-line transactions summed properly
- ✅ Credit memos show negative totals
- ✅ Total validation: line items sum = transaction totals sum
- ✅ Excel output includes Transaction Summary sheet
- ✅ Sorted by date and transaction number

## Usage

```python
from pathlib import Path
from analyze_sales_data import (
    extract_transactions,
    create_transaction_summary
)

# Load data
csv_path = Path("data/item sales detail wk 41w.CSV")
transactions = extract_transactions(csv_path)

# Create transaction summary
trans_summary = create_transaction_summary(transactions)

# Analyze
print(f"Total transactions: {len(trans_summary)}")
print(f"Total amount: ${trans_summary['Transaction_Total'].sum():,.2f}")

# Find largest transactions
top_5 = trans_summary.nlargest(5, 'Transaction_Total')
print(top_5[['Num', 'Customer', 'Transaction_Total']])
```
