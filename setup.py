from setuptools import setup, find_packages

setup(
    name="quickbooks-order-exporter",
    version="1.0.0",
    description="QuickBooks Order Exporter with Odoo Integration",
    author="Your Company",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.5.0",
        "numpy>=1.21.0",
        "openpyxl>=3.0.0",
        "requests>=2.32.3",
        "python-dotenv>=1.0.0",
        "python-dateutil>=2.8.0",
        "typing-extensions>=4.0.0",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "export-orders=quickbooks.cli:main",
        ],
    },
)
