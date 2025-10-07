# Technology Stack

## Core Technologies

- **Python 3.10+**: Primary programming language with type hints support
- **pandas**: Data manipulation and analysis for sales orders, inventory, and BOM data
- **numpy**: Numerical computations for MRP calculations
- **requests**: HTTP client for Odoo JSON-RPC API integration
- **openpyxl**: Excel file generation and formatting
- **python-dotenv**: Environment variable management for configuration

## Development Tools

- **pytest**: Testing framework with coverage support
- **black**: Code formatting (4 spaces, 80 char lines)
- **flake8**: Linting and style checking
- **mypy**: Static type checking
- **jupyter**: Interactive development and analysis notebooks

## Build System

- **uv**: Modern Python package manager (primary)
- **pip**: Fallback package manager
- **pyproject.toml**: Project configuration and dependencies
- **requirements.txt**: Legacy dependency specification

## Environment Configuration

### Required Environment Variables (.env file)
```bash
# === ODOO CONFIGURATION ===
ODOO_URL=http://192.168.1.200
ODOO_DATABASE=Gasco
ODOO_USERNAME=dbigman@gascoindustrial.com
ODOO_PASSWORD=Malcomz1*e1

# === REDIS CONFIGURATION ===
REDIS_URL=redis://localhost:6379
REDIS_PASSWORD=
REDIS_MAX_RETRIES=3
REDIS_RETRY_DELAY=1000

# === APPLICATION CONFIGURATION ===
PORT=3000
NODE_ENV=development
LOG_LEVEL=info

# === CACHE CONFIGURATION ===
DEFAULT_CACHE_TTL=300
INVENTORY_CACHE_TTL=60
ORDERS_CACHE_TTL=180
BOM_CACHE_TTL=600

# === PERFORMANCE CONFIGURATION ===
MAX_WORKERS=4
REQUEST_TIMEOUT_MS=30000
SCHEDULE_REFRESH_INTERVAL_MS=30000

# === SCHEDULER CONFIGURATION ===
SCHEDULER_MAX_ITERATIONS=10
SCHEDULER_DEFAULT_ALGORITHM=PRIORITY
SCHEDULER_TIME_SLOT_MINUTES=15

# === KPI TARGETS ===
KPI_ORDER_COMPLETION_TARGET=95
KPI_LEAD_TIME_TARGET_DAYS=5
KPI_SCHEDULE_ADHERENCE_TARGET=90
KPI_RESOURCE_UTILIZATION_TARGET=85
```

## Common Commands

```bash
# Environment setup
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # Windows PowerShell
source .venv/bin/activate     # macOS/Linux

# Install dependencies
pip install -r requirements.txt
# or with uv
uv sync

# Run application
python main.py
python main.py --interactive
python main.py --algorithm fifo --date-from 2024-01-01

# Testing
pytest -q
pytest tests/
pytest -v --cov

# Code quality
black .
flake8 .
mypy .

# Jupyter notebooks
jupyter notebook notebooks/
```

## MCP (Model Context Protocol) Integration

The project supports MCP servers for enhanced functionality:

### Configured MCP Servers
- **fetch**: Web content retrieval (`uvx mcp-server-fetch`)
- **Context7**: Documentation and context (`npx -y @upstash/context7-mcp`)
- **playwright**: Browser automation (`npx @playwright/mcp@latest`)
- **pampa**: Additional MCP functionality (`npx -y pampa mcp --debug`)

### API Keys Required
- **VOYAGE_API_KEY**: For voyage embeddings
- **OPENROUTER_API_KEY**: For OpenRouter API access

## Configuration

- **Environment Variables**: Stored in `.env` file for Odoo credentials and settings
- **Logging**: Automatic timestamped log files in `logs/` directory with configurable levels
- **Output**: Excel reports generated in `output/` directory with timestamps
- **Database**: SQLite database at `./data/mps.db` with backups in `./data/backups`
- **Cache**: Redis-based caching with configurable TTL values
- **Monitoring**: Optional email alerts and performance monitoring