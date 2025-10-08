# Total Quantity Feature

## Overview

Added `Total_Qty` column to product summary to show the absolute sum of all transaction volumes for each product, regardless of transaction direction (sales or returns).

## Purpose

`Total_Qty` provides insight into total product movement and activity:
- **Inventory turnover**: Shows total volume handled
- **Return analysis**: Compare Total_Qty vs Net_Qty to identify high-return products
- **Activity metrics**: Measure product handling regardless of direction

## Calculation

```python
Total_Qty = Sales_Qty + Return_Qty
```

Where:
- `Sales_Qty` = Sum of positive quantities (Invoices, Sales Receipts)
- `Return_Qty` = Absolute sum of negative quantities (Credit Memos, Refund Receipts)

## Examples

### Product with No Returns
```
Product: DOT Mold Cleaner 1 gal.
Sales_Qty:   2900
Return_Qty:     0
Total_Qty:   2900  (2900 + 0)
Net_Qty:     2900  (2900 - 0)
```

### Product with Returns
```
Product: GASCÓ Vainilla Flavor 4/1 gal.
Sales_Qty:     27
Return_Qty:    46
Total_Qty:     73  (27 + 46)
Net_Qty:      -19  (27 - 46)
```

### Product with Only Returns
```
Product: BELCA Vinagre Imitación Blanco 4/1 gal.
Sales_Qty:      0
Return_Qty:   109
Total_Qty:    109  (0 + 109)
Net_Qty:     -109  (0 - 109)
```

## Use Cases

### 1. Return Rate Analysis
```python
Return_Rate = Return_Qty / Total_Qty * 100

Example:
GASCÓ Vainilla: 46 / 73 = 63% return rate
```

### 2. Product Activity Ranking
Sort by `Total_Qty` to see which products have the most transaction volume:
```
Product_Code  Product_Name                Total_Qty  Net_Qty
D18015        DOT Mold Cleaner 1 gal.          2900     2900
D18017        DOT Mold Cleaner 32 oz.          2300     2300
D11222        Hand Soap Lotion                  189      189
```

### 3. Problem Product Identification
Products where `Total_Qty` >> `Net_Qty` indicate high return activity:
```
Product_Code  Product_Name           Total_Qty  Net_Qty  Issue
A00403        BELCA Vinagre               109     -109  100% returns
A00609        GASCÓ Vainilla               73      -19  High returns
```

## Output Locations

`Total_Qty` appears in:
1. **Product Summary** sheet - All products with Total_Qty
2. **Top Products** sheet - Top 10 products with Total_Qty
3. **Console output** - Displayed in top products table

## Implementation

### Files Modified

1. **`analyze_sales_data.py`**
   - Added `Total_Qty` calculation in `create_product_summary()`
   - Updated display columns to include `Total_Qty`

2. **`src/quickbooks_autoreport/extractors/item_sales_detail_extractor.py`**
   - Added `Total_Qty` calculation in `create_product_summary()`

3. **Documentation**
   - Updated `docs/item_sales_detail_extractor.md`
   - Updated `PRODUCT_CODE_EXTRACTION.md`
   - Created `TOTAL_QTY_FEATURE.md`

## Testing

Verified with `data/item sales detail wk 41w.CSV`:
- ✅ Total_Qty calculated correctly for products with no returns
- ✅ Total_Qty calculated correctly for products with returns
- ✅ Total_Qty calculated correctly for products with only returns
- ✅ Excel output includes Total_Qty column
- ✅ Console display shows Total_Qty

## Column Order

Product Summary columns now appear in this order:
1. Product_Code
2. Product_Name
3. Sales_Qty
4. Sales_Amount
5. Sales_Transactions
6. Return_Qty
7. Return_Amount
8. Return_Transactions
9. **Total_Qty** ← New
10. Net_Qty
11. Net_Amount
12. Avg_Unit_Price
