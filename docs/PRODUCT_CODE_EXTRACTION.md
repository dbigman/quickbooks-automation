# Product Code Extraction Feature

## Overview

Added automatic extraction of product codes from QuickBooks Item Sales Detail reports.

## Implementation

### Pattern Recognition

Product codes are extracted from the `Type` column using regex pattern:
```python
product_code_pattern = r'^([A-Z0-9\-]+)\s*\('
```

### Example

From this Type column value:
```
A00403 (BELCA Vinagre Imitación Blanco 4/1 gal.)
```

Extracts: `A00403`

### Forward Fill

Product codes appear in header rows and are forward-filled to all subsequent transaction rows until the next product header is encountered.

## Data Flow

```
Raw CSV
  ↓
Extract product codes from Type column (regex)
  ↓
Forward fill codes to transaction rows (ffill)
  ↓
Include Product_Code in all aggregations
  ↓
Output to Excel with Product_Code column
```

## Updated DataFrames

All output DataFrames now include `Product_Code` and `Total_Qty`:

1. **Transactions**: Each transaction row has its product code
2. **Product Summary**: Grouped by Product_Name with Product_Code and Total_Qty
   - `Total_Qty` = `Sales_Qty` + `Return_Qty` (absolute sum of all transaction volumes)
   - Useful for understanding total product movement regardless of direction
3. **Customer-Product Matrix**: Includes Product_Code for each combination
4. **Top Products**: Shows Product_Code and Total_Qty alongside Product_Name
5. **Top Customers**: (No change - customer-level only)

## Sample Output

```
Product_Code                                          Product_Name  Total_Qty  Net_Qty  Net_Amount
      D18015 DOT Mold Deep Stain and Extra Strength Cleaner 1 gal.       2900     2900    10440.00
      D60016          PROFESSIONAL SERVICES MRS ANDREA  SEPT. 2025        160      160     5376.00
      D11222               Hand Soap Lotion 4/1 gal. (NO ETIQUETA)        189      189     3322.62
      D12271          FUSIÓN Ethyl Alcohol Antiseptic 70% 4/1 gal.        100      100     3000.00
      D13041               GASCÓ Alcohol Isopropílico 70% 4/1 gal.         87       87     2714.72
      A00602        GASCÓ Premium White Distilled Vinegar 4/1 gal.        166      166     2265.90
```

### Products with Returns

```
Product_Code                            Product_Name  Sales_Qty  Return_Qty  Total_Qty  Net_Qty
      A00609          GASCÓ Vainilla Flavor 4/1 gal.         27          46         73      -19
      A00403 BELCA Vinagre Imitación Blanco 4/1 gal.          0         109        109     -109
```

## Code Changes

### Files Modified

1. **`analyze_sales_data.py`**
   - Added product code extraction in `extract_transactions()`
   - Updated `create_product_summary()` to include Product_Code
   - Updated `create_customer_product_matrix()` to include Product_Code
   - Updated display to show Product_Code column

2. **`src/quickbooks_autoreport/extractors/item_sales_detail_extractor.py`**
   - Added product code extraction in `load_raw_data()`
   - Updated aggregations to include Product_Code

3. **`docs/item_sales_detail_extractor.md`**
   - Documented Product_Code in all DataFrame descriptions
   - Added to Key Features section

4. **`docs/quickbooks_item_sales_detail_columns_gasco.md`**
   - Added Product Code Extraction section
   - Updated modeling guidance

## Testing

Tested with `data/item sales detail wk 41w.CSV`:
- ✅ 86 transactions processed
- ✅ 59 unique product codes extracted
- ✅ All product codes correctly assigned to transactions
- ✅ Excel output includes Product_Code in all relevant sheets
- ✅ No deprecation warnings

## Usage

No changes required to existing usage:

```bash
python analyze_sales_data.py
```

Product codes are automatically extracted and included in all outputs.
