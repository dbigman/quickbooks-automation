# Sales Dashboard Design Document

## Overview

The Sales Dashboard is a Streamlit-based web application that provides interactive visualization and analysis of sales data from Excel files. The application follows a clean architecture pattern with separation between data loading, business logic, and presentation layers.

**Key Design Principles:**
- Single-page application with sidebar controls
- Reactive data updates via polling or manual refresh
- Graceful error handling with user-friendly feedback
- Performance-optimized for files up to 10MB
- Modular code structure for maintainability

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Streamlit UI Layer                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Sidebar    │  │  Metrics     │  │   Charts     │  │
│  │   Controls   │  │  Display     │  │  Display     │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                  Business Logic Layer                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Metrics    │  │ Aggregation  │  │   Chart      │  │
│  │ Calculator   │  │   Engine     │  │  Generator   │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                   Data Access Layer                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ File Scanner │  │ Excel Loader │  │   Data       │  │
│  │              │  │              │  │ Validator    │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
                  ┌──────────────┐
                  │  Excel Files │
                  │   (output/)  │
                  └──────────────┘
```

### Application Structure

```
apps/
└── dashboard/
    ├── Home.py                    # Main Streamlit entry point
    └── pages/
        └── Sales_Analysis.py      # Sales dashboard page

src/
└── yourapp/
    ├── dashboard/
    │   ├── __init__.py
    │   ├── data_loader.py         # File scanning and Excel loading
    │   ├── metrics.py             # Metrics calculation logic
    │   ├── charts.py              # Chart generation logic
    │   └── utils.py               # Utility functions (formatting, etc.)
    └── domain/
        └── sales_data.py          # Data models and validation

tests/
└── dashboard/
    ├── test_data_loader.py
    ├── test_metrics.py
    └── test_charts.py
```

## Components and Interfaces

### 1. Data Access Layer

#### FileScanner
**Responsibility:** Discover and monitor Excel files in the output directory

```python
class FileScanner:
    def __init__(self, directory: str = "output"):
        self.directory = Path(directory)
    
    def list_excel_files(self) -> List[Path]:
        """Return list of .xlsx files in directory"""
        
    def get_file_modified_time(self, filepath: Path) -> datetime:
        """Get last modification timestamp of file"""
        
    def file_exists(self, filepath: Path) -> bool:
        """Check if file exists"""
```

#### ExcelLoader
**Responsibility:** Load and validate Excel data

```python
class ExcelLoader:
    REQUIRED_COLUMNS = ['Transaction_Total', 'Sales_Amount', 'Sales_Qty']
    
    def load_file(self, filepath: Path) -> pd.DataFrame:
        """Load Excel file and return DataFrame"""
        
    def validate_columns(self, df: pd.DataFrame) -> Tuple[bool, List[str]]:
        """Validate required columns exist, return (is_valid, missing_columns)"""
        
    def add_weekday_column(self, df: pd.DataFrame, date_column: str) -> pd.DataFrame:
        """Add weekday name column from date column"""
```

### 2. Business Logic Layer

#### MetricsCalculator
**Responsibility:** Calculate sales metrics and aggregations

```python
class MetricsCalculator:
    def __init__(self, df: pd.DataFrame):
        self.df = df
    
    def calculate_total_revenue(self) -> float:
        """Sum of Transaction_Total"""
        
    def calculate_total_units(self) -> int:
        """Sum of Sales_Qty"""
        
    def get_top_products_by_revenue(self, top_n: int = 5) -> pd.DataFrame:
        """Top N products by Sales_Amount"""
        
    def get_top_products_by_units(self, top_n: int = 5) -> pd.DataFrame:
        """Top N products by Sales_Qty"""
        
    def aggregate_by_weekday(self, value_column: str) -> pd.DataFrame:
        """Aggregate values by weekday in chronological order"""
```

#### ChartGenerator
**Responsibility:** Generate chart configurations for Streamlit

```python
class ChartGenerator:
    @staticmethod
    def create_weekday_line_chart(
        data: pd.DataFrame,
        x_column: str,
        y_column: str,
        title: str,
        y_label: str
    ) -> dict:
        """Create line chart configuration for weekday trends"""
        
    @staticmethod
    def create_bar_chart(
        data: pd.DataFrame,
        x_column: str,
        y_column: str,
        title: str,
        orientation: str = 'h'
    ) -> dict:
        """Create horizontal bar chart for top products"""
```

### 3. UI Layer

#### Sidebar Component
**Responsibility:** Render sidebar controls and status

```python
def render_sidebar(
    available_files: List[Path],
    current_file: Optional[Path],
    last_update: Optional[datetime]
) -> Tuple[Optional[Path], bool]:
    """
    Render sidebar with file selector, refresh button, and status.
    Returns: (selected_file, refresh_clicked)
    """
```

#### Metrics Display Component
**Responsibility:** Render metric cards and KPIs

```python
def render_metrics_section(calculator: MetricsCalculator):
    """Render revenue and units metrics with top products"""
```

#### Charts Display Component
**Responsibility:** Render visualization charts

```python
def render_charts_section(calculator: MetricsCalculator):
    """Render weekly revenue and movement charts"""
```

## Data Models

### SalesData
**Purpose:** Validated sales data container

```python
from dataclasses import dataclass
from datetime import datetime
import pandas as pd

@dataclass
class SalesData:
    """Container for validated sales data"""
    df: pd.DataFrame
    filepath: Path
    loaded_at: datetime
    row_count: int
    
    @classmethod
    def from_file(cls, filepath: Path, loader: ExcelLoader) -> 'SalesData':
        """Factory method to load and validate data from file"""
        
    def get_date_range(self) -> Tuple[datetime, datetime]:
        """Return min and max dates in dataset"""
```

### DashboardState
**Purpose:** Manage application state in Streamlit session

```python
@dataclass
class DashboardState:
    """Streamlit session state container"""
    current_file: Optional[Path] = None
    sales_data: Optional[SalesData] = None
    last_update: Optional[datetime] = None
    last_file_mtime: Optional[float] = None
    error_message: Optional[str] = None
    
    def should_reload(self, file_scanner: FileScanner) -> bool:
        """Check if file has been modified since last load"""
```

## Error Handling

### Error Categories and Responses

1. **File Not Found / Empty Directory**
   - Display: "No Excel files found in 'output' folder"
   - Action: Show instructions to add files

2. **File Read Error**
   - Display: "Unable to read file: {filename}. Error: {error_message}"
   - Action: Allow user to select different file

3. **Missing Columns**
   - Display: "Required columns missing: {column_list}"
   - Action: Show expected vs actual columns

4. **Data Validation Error**
   - Display: "Invalid data format in column: {column_name}"
   - Action: Show sample of problematic data

5. **Polling Error**
   - Log error silently
   - Continue with existing data
   - Display warning indicator in status

### Error Handling Pattern

```python
try:
    sales_data = SalesData.from_file(filepath, loader)
    st.session_state.error_message = None
except FileNotFoundError:
    st.error("File not found. Please select a valid file.")
except ValueError as e:
    st.error(f"Data validation error: {str(e)}")
except Exception as e:
    st.error(f"Unexpected error: {str(e)}")
    logger.exception("Error loading sales data")
```

## Testing Strategy

### Unit Tests

**Data Loader Tests** (`test_data_loader.py`)
- Test file scanning with various directory states
- Test Excel loading with valid/invalid files
- Test column validation with missing columns
- Test weekday extraction from dates

**Metrics Tests** (`test_metrics.py`)
- Test revenue calculations with sample data
- Test units calculations with edge cases (zero, negative)
- Test top N product aggregations
- Test weekday aggregations with multi-week data

**Charts Tests** (`test_charts.py`)
- Test chart configuration generation
- Test data formatting for charts
- Test weekday ordering in charts

### Integration Tests

**End-to-End Flow**
- Load sample Excel file → Calculate metrics → Generate charts
- File selection → Data refresh → UI update
- Polling detection → Auto-reload → Metrics update

### Test Data

Create fixture Excel files:
- `test_sales_valid.xlsx` - Valid data with all columns
- `test_sales_missing_columns.xlsx` - Missing required columns
- `test_sales_empty.xlsx` - Empty file
- `test_sales_multiweek.xlsx` - Data spanning multiple weeks

## Performance Considerations

### Optimization Strategies

1. **Caching**
   - Use `@st.cache_data` for file loading
   - Cache metric calculations when data unchanged
   - Cache chart configurations

2. **Lazy Loading**
   - Load data only when file selected
   - Defer chart rendering until data available

3. **Efficient Aggregations**
   - Use pandas groupby for aggregations
   - Convert data types early (numeric columns)
   - Filter data before aggregation when possible

4. **Polling Optimization**
   - Check file modification time before reloading
   - Use background thread for polling (if needed)
   - Debounce rapid file changes

### Memory Management

```python
# Convert numeric columns efficiently
df['Sales_Qty'] = pd.to_numeric(df['Sales_Qty'], errors='coerce')
df['Sales_Amount'] = pd.to_numeric(df['Sales_Amount'], errors='coerce')
df['Transaction_Total'] = pd.to_numeric(df['Transaction_Total'], errors='coerce')

# Drop unnecessary columns after loading
df = df[REQUIRED_COLUMNS + ['Product', 'Date']]
```

## Configuration

### Environment Variables

```python
# .env.example
DASHBOARD_OUTPUT_DIR=output
DASHBOARD_POLL_INTERVAL=3600  # seconds (1 hour)
DASHBOARD_MAX_FILE_SIZE_MB=10
DASHBOARD_TOP_N_PRODUCTS=5
```

### Application Constants

```python
# src/yourapp/dashboard/config.py
from pathlib import Path

OUTPUT_DIR = Path("output")
POLL_INTERVAL_SECONDS = 3600
TOP_N_PRODUCTS = 5
REQUIRED_COLUMNS = ['Transaction_Total', 'Sales_Amount', 'Sales_Qty']
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
WEEKDAY_ORDER = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
```

## UI/UX Design

### Layout Structure

```
┌─────────────────────────────────────────────────────────────┐
│  Sales Analytics Dashboard                                   │
├──────────────┬──────────────────────────────────────────────┤
│              │  📊 Key Metrics                              │
│  Sidebar     │  ┌──────────┐  ┌──────────┐                 │
│              │  │ Revenue  │  │  Units   │                 │
│  📁 File     │  │ $XX,XXX  │  │  X,XXX   │                 │
│  Select      │  └──────────┘  └──────────┘                 │
│              │                                               │
│  🔄 Refresh  │  Top 5 Products by Revenue                   │
│  Data        │  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ Product A                  │
│              │  ▓▓▓▓▓▓▓▓▓▓ Product B                        │
│  ℹ️ Status   │  ▓▓▓▓▓▓▓ Product C                           │
│  Last Update │                                               │
│  2025-10-08  │  📈 Weekly Revenue Trend                     │
│  17:00:04    │  [Line Chart]                                │
│              │                                               │
│  File:       │  📦 Weekly Units Sold                        │
│  sales_...   │  [Line Chart]                                │
│              │                                               │
└──────────────┴──────────────────────────────────────────────┘
```

### Color Scheme and Styling

- Primary color: Streamlit default blue (#FF4B4B)
- Success indicators: Green (#00C853)
- Warning indicators: Orange (#FF9800)
- Error indicators: Red (#F44336)
- Neutral background: Light gray (#F0F2F6)

### Responsive Behavior

- Metrics displayed in columns (2 columns on desktop, 1 on mobile)
- Charts stack vertically on narrow screens
- Sidebar collapsible on mobile devices

## Deployment Considerations

### Running the Dashboard

```bash
# Development
streamlit run apps/dashboard/Home.py

# Production (with config)
streamlit run apps/dashboard/Home.py --server.port 8501 --server.address 0.0.0.0
```

### Dependencies

```toml
# pyproject.toml additions
[project]
dependencies = [
    "streamlit>=1.28.0",
    "pandas>=2.0.0",
    "openpyxl>=3.1.0",  # Excel file support
    "plotly>=5.17.0",   # Interactive charts
]
```

### Logging

```python
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Log key events
logger.info(f"📥 Loading file: {filepath}")
logger.info(f"📊 Calculated metrics for {row_count} rows")
logger.info(f"✅ Dashboard updated at {datetime.now()}")
```

## Future Enhancements

1. **Multi-file Comparison**
   - Compare metrics across multiple time periods
   - Trend analysis over multiple files

2. **Export Functionality**
   - Export filtered data to CSV
   - Download chart images

3. **Advanced Filtering**
   - Date range selector
   - Product category filters
   - Custom aggregation periods

4. **Real-time Notifications**
   - Alert when new files arrive
   - Notify on significant metric changes

5. **User Preferences**
   - Save preferred file selections
   - Customize chart colors and styles
   - Configure polling intervals
