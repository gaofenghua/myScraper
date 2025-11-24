#!/usr/bin/env python3
"""
Configuration settings for ICBC scraper.

This module centralizes all configuration parameters for the scraper,
including URLs, timeouts, and output settings.
"""

from pathlib import Path

# ============================================================================
# Target URL Configuration
# ============================================================================

ICBC_BASE_URL = "https://www.icbc.com.cn/webpage/finance/disclosure/detail/net-value/"

# Target product parameters
TARGET_PRODUCT_ID = "21GS6173"
TARGET_SALE_TARGET = "7"

# Full target URL
ICBC_TARGET_URL = (
    f"{ICBC_BASE_URL}?prodId={TARGET_PRODUCT_ID}&saleTarget={TARGET_SALE_TARGET}"
)

# ============================================================================
# Request Configuration
# ============================================================================

# Timeout for HTTP requests (seconds)
REQUEST_TIMEOUT = 30

# Maximum number of retries for failed requests
MAX_RETRIES = 3

# User-Agent string to use in requests
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
)

# ============================================================================
# Selenium Configuration (for dynamic content)
# ============================================================================

# Run browser in headless mode
SELENIUM_HEADLESS = True

# Timeout for waiting elements with Selenium (seconds)
SELENIUM_WAIT_TIMEOUT = 30

# Timeout for page load with Selenium (seconds)
SELENIUM_PAGE_LOAD_TIMEOUT = 60

# ============================================================================
# Output Configuration
# ============================================================================

# Output directory
OUTPUT_DIR = "output"

# Create output directory path
OUTPUT_PATH = Path(OUTPUT_DIR)

# Save data in JSON format
SAVE_JSON = True

# Save data in CSV format
SAVE_CSV = True

# Save data in database (requires database configuration)
SAVE_DATABASE = False

# JSON output filename pattern
JSON_FILENAME_PATTERN = "icbc_net_value_{timestamp}.json"

# CSV output filename pattern for tables
CSV_FILENAME_PATTERN = "icbc_net_value_table_{index}_{timestamp}.csv"

# ============================================================================
# Logging Configuration
# ============================================================================

# Log file path
LOG_FILE = "icbc_scraper.log"

# Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL = "INFO"

# Log format
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Also log to console
LOG_TO_CONSOLE = True

# ============================================================================
# Data Processing Configuration
# ============================================================================

# Whether to clean and parse numeric data
CLEAN_NUMERIC_DATA = True

# Whether to extract financial-specific information
EXTRACT_FINANCIAL_DATA = True

# Columns to prioritize (if present in tables)
PRIORITY_COLUMNS = [
    'net_value', '净值',
    'date', '日期',
    'price', '价格',
    'product', '产品'
]

# ============================================================================
# Database Configuration (if SAVE_DATABASE is True)
# ============================================================================

# Database type: 'sqlite', 'mysql', 'postgresql'
DATABASE_TYPE = "sqlite"

# Database connection string
DATABASE_CONNECTION = "sqlite:///icbc_scraper.db"

# Database table names
TABLE_SCRAPE_RECORDS = "scrape_records"
TABLE_PRODUCTS = "products"
TABLE_NET_VALUES = "net_values"

# ============================================================================
# Advanced Settings
# ============================================================================

# Maximum number of concurrent scraping operations
MAX_CONCURRENT_SCRAPES = 1

# Delay between requests in seconds (to be respectful to the server)
REQUEST_DELAY = 1

# Verify SSL certificates
VERIFY_SSL = True

# Number of days to retain output files before cleanup
OUTPUT_FILE_RETENTION_DAYS = 30

# ============================================================================
# Feature Flags
# ============================================================================

# Use Selenium for dynamic content (requires ChromeDriver)
USE_SELENIUM = False

# Enable data validation
ENABLE_DATA_VALIDATION = True

# Generate HTML report after scraping
GENERATE_HTML_REPORT = False

# Send email notification after scraping
SEND_EMAIL_NOTIFICATION = False

# ============================================================================
# Email Configuration (if SEND_EMAIL_NOTIFICATION is True)
# ============================================================================

EMAIL_SENDER = "scraper@icbc.local"
EMAIL_RECIPIENTS = ["admin@icbc.local"]
EMAIL_SMTP_HOST = "localhost"
EMAIL_SMTP_PORT = 25
EMAIL_USE_TLS = False


def get_config_summary() -> str:
    """
    Get a summary of current configuration.
    
    Returns:
        str: Configuration summary
    """
    return f"""
ICBC Scraper Configuration Summary
==================================
Target URL: {ICBC_TARGET_URL}
Product ID: {TARGET_PRODUCT_ID}
Sale Target: {TARGET_SALE_TARGET}

Request Settings:
  Timeout: {REQUEST_TIMEOUT}s
  Max Retries: {MAX_RETRIES}

Output Settings:
  Directory: {OUTPUT_DIR}
  Save JSON: {SAVE_JSON}
  Save CSV: {SAVE_CSV}

Logging:
  File: {LOG_FILE}
  Level: {LOG_LEVEL}
  Console: {LOG_TO_CONSOLE}

Advanced:
  Use Selenium: {USE_SELENIUM}
  Verify SSL: {VERIFY_SSL}
    """


if __name__ == '__main__':
    print(get_config_summary())
