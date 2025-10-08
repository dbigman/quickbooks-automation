# QuickBooks _Item Sales Detail_ — Column Definitions (Team Convention)

Purpose: LLM-ready semantics for QuickBooks **Item Sales Detail** exports, **with Gasco convention that `Memo` = _Product Name_**.

---

## Columns

| Column                    | Data type                   | Definition                                                                        | Examples / Allowed values                                                       | Notes & Edge Cases                                             |
| ------------------------- | --------------------------- | --------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| **Type**                  | categorical (string)        | Transaction type that produced the line.                                          | `Invoice`, `Sales Receipt`, `Credit Memo`, `Refund Receipt`, `Statement Charge` | Use to infer sign conventions (credits/returns).               |
| **Date**                  | date (YYYY-MM-DD)           | Posting date of the transaction (date it hits the books).                         | `2025-10-01`                                                                    | Not necessarily the ship/delivery date.                        |
| **Num**                   | string                      | Transaction/reference number.                                                     | `INV-10234`, `SR-7788`                                                          | May be blank.                                                  |
| **Memo** _(Product Name)_ | string                      | **Gasco override:** Treat as the **Product Name** for the line.                   | `Detergent Ultra 5L`, `Softener Fresh 1L`                                       | Use `Memo` for item-level grouping, ranking, and mix analysis. |
| **Name**                  | string                      | Customer or Customer:Job (sub-customer).                                          | `Acme Co`, `Acme Co:Store 12`                                                   | Split on `:` to roll up.                                       |
| **Qty**                   | numeric (float)             | Quantity sold on the line.                                                        | `1`, `3.5`, `-2`                                                                | Credits/returns negative.                                      |
| **Sales Price**           | numeric (currency per unit) | Unit selling price (pre-tax).                                                     | `12.50`                                                                         | May reflect line-level discounts.                              |
| **Amount**                | numeric (currency)          | Extended line amount, usually `Qty × Sales Price` after line discounts (pre-tax). | `125.00`, `-19.99`                                                              | Credits/returns negative. Sales tax excluded.                  |
| **Balance**               | numeric (currency)          | Remaining **open balance** of the full transaction as of report date.             | `0.00`, `45.23`                                                                 | Transaction-level field, not line residual.                    |

---

## Product Code Extraction

The `Type` column contains product header rows with the format:

```
A00403 (BELCA Vinagre Imitación Blanco 4/1 gal.)
```

**Extraction Pattern**: `^([A-Z0-9\-]+)\s*\(`

This extracts the product code (e.g., `A00403`) which is then forward-filled to all transaction rows for that product.

## Modeling & BI Guidance (using `Memo` as Product)

- **Product identification**: Use extracted `Product_Code` for unique product identification
- **Product mix / top sellers**: Group by `Product_Code` or `Memo` to rank products by `Amount` and `Qty`.
- **Returns**: Identify credits via `Type` ∈ {`Credit Memo`, `Refund Receipt`} and/or negative `Qty`/`Amount`; subtract from product totals.
- **Customer-product matrix**: Group by `Name` × `Product_Code` for key accounts.
- **Pricing**: Compute realized unit price = `Amount` / `Qty` (guard for division by zero/NaN).
