"""
Create test sales data file for the dashboard.

This script creates a sample Excel file with the correct column format
that the Sales Dashboard expects.
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

# Create output directory if it doesn't exist
output_dir = Path('output')
output_dir.mkdir(exist_ok=True)

# Create sample sales data
data = {
    'Transaction_Total': [
        125.50, 250.00, 175.75, 300.00, 225.25,
        150.00, 275.50, 200.00, 325.75, 180.00,
        210.50, 290.00, 165.25, 240.00, 195.75,
        310.00, 185.50, 255.25, 220.00, 270.75
    ],
    'Sales_Amount': [
        112.95, 225.00, 158.18, 270.00, 202.73,
        135.00, 247.95, 180.00, 293.18, 162.00,
        189.45, 261.00, 148.73, 216.00, 176.18,
        279.00, 166.95, 229.73, 198.00, 243.68
    ],
    'Sales_Qty': [
        10, 25, 15, 30, 20,
        12, 28, 18, 32, 16,
        14, 26, 13, 24, 17,
        31, 11, 23, 19, 27
    ],
    'Product': [
        'GASCÓ Premium White Vinegar 4/1 gal',
        'BELCA Vinagre Imitación Blanco 4/1 gal',
        'GASCÓ Salsa Soya 4/1 gal',
        'GASCÓ Vainilla Flavor 4/1 gal',
        'BELCA Aceite Vegetal 4/1 gal',
        'GASCÓ Premium White Vinegar 4/1 gal',
        'BELCA Vinagre Imitación Blanco 4/1 gal',
        'GASCÓ Salsa Soya 4/1 gal',
        'GASCÓ Vainilla Flavor 4/1 gal',
        'BELCA Aceite Vegetal 4/1 gal',
        'GASCÓ Premium White Vinegar 4/1 gal',
        'BELCA Vinagre Imitación Blanco 4/1 gal',
        'GASCÓ Salsa Soya 4/1 gal',
        'GASCÓ Vainilla Flavor 4/1 gal',
        'BELCA Aceite Vegetal 4/1 gal',
        'GASCÓ Premium White Vinegar 4/1 gal',
        'BELCA Vinagre Imitación Blanco 4/1 gal',
        'GASCÓ Salsa Soya 4/1 gal',
        'GASCÓ Vainilla Flavor 4/1 gal',
        'BELCA Aceite Vegetal 4/1 gal'
    ],
    'Date': pd.date_range('2025-10-06', periods=20, freq='D')
}

# Create DataFrame
df = pd.DataFrame(data)

# Generate filename with timestamp
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
filename = f'sales_dashboard_test_data_{timestamp}.xlsx'
filepath = output_dir / filename

# Save to Excel
df.to_excel(filepath, index=False)

print(f"✅ Test file created successfully!")
print(f"📁 Location: {filepath}")
print(f"📊 Rows: {len(df)}")
print(f"📋 Columns: {list(df.columns)}")
print(f"\n🚀 Now refresh your dashboard and select: {filename}")
print(f"\n💡 The dashboard should now load successfully!")
