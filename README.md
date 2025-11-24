# ICBC Net-Value Disclosure Scraper

A Python web scraper designed to extract financial disclosure data from the ICBC (Industrial and Commercial Bank of China) net-value disclosure page.

## Overview

This project provides automated scraping functionality to retrieve net-value information from ICBC's financial disclosure system. The scraper handles HTTP requests with proper error handling, parses HTML content using BeautifulSoup, and exports data in multiple formats (JSON and CSV).

## Features

- **Robust HTTP Handling**: Implements automatic retries with exponential backoff for failed requests
- **Error Handling**: Comprehensive error handling for network issues and parsing failures
- **Multiple Output Formats**: Exports data as both JSON and CSV for flexibility
- **Structured Data Extraction**: Captures tables, metadata, and content sections from the disclosure page
- **Logging**: Detailed logging for monitoring and debugging scraping operations
- **User-Agent Rotation**: Uses realistic headers to avoid being blocked by servers

## Requirements

- Python 3.7+
- Dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd icbc-scraper
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the scraper with default settings:

```bash
python icbc_scraper.py
```

This will:
1. Fetch the ICBC net-value disclosure page
2. Parse the HTML content and extract data
3. Save results to `output/` directory in both JSON and CSV formats
4. Generate detailed logs to `icbc_scraper.log`

### Programmatic Usage

```python
from icbc_scraper import ICBCNetValueScraper

# Initialize scraper with target URL
scraper = ICBCNetValueScraper(
    base_url="https://www.icbc.com.cn/webpage/finance/disclosure/detail/net-value/?prodId=21GS6173&saleTarget=7",
    timeout=30,
    max_retries=3
)

# Perform scraping
data = scraper.scrape()

# Save results
json_file = scraper.save_to_json(data)
csv_files = scraper.save_tables_to_csv(data)
```

## Output

### JSON Output Structure

The JSON output includes:

```json
{
  "scraped_at": "2024-01-01T12:00:00.000000",
  "url": "https://www.icbc.com.cn/...",
  "page_title": "Page Title",
  "tables": [
    {
      "index": 0,
      "headers": ["Column 1", "Column 2", ...],
      "rows": [
        ["value1", "value2", ...],
        ...
      ]
    }
  ],
  "content_sections": [...],
  "metadata": {...},
  "url_parameters": {...}
}
```

### CSV Output

Each table from the page is saved as a separate CSV file with:
- Column headers from the original table
- All row data preserved
- UTF-8 encoding for Chinese character support

## Configuration

### Timeout

Adjust request timeout (default: 30 seconds):

```python
scraper = ICBCNetValueScraper(base_url, timeout=60)
```

### Retries

Adjust maximum number of retries (default: 3):

```python
scraper = ICBCNetValueScraper(base_url, max_retries=5)
```

### Output Directory

Save to custom directory:

```python
scraper.save_to_json(data, output_dir='custom_output')
scraper.save_tables_to_csv(data, output_dir='custom_output')
```

## Error Handling

The scraper gracefully handles:

- **Network Timeouts**: Configurable timeout with automatic retries
- **Connection Errors**: Logs errors and returns None
- **HTTP Errors**: Handles all HTTP error codes
- **Parsing Errors**: Continues parsing even if some elements fail
- **File I/O Errors**: Catches and logs file writing issues

All errors are logged to `icbc_scraper.log` for debugging.

## Logging

Logs are written to both console and file (`icbc_scraper.log`). Log levels:

- **INFO**: General operation information
- **ERROR**: Error messages with context

Example log output:

```
2024-01-01 12:00:00,000 - icbc_scraper - INFO - Initialized scraper for URL: ...
2024-01-01 12:00:00,100 - icbc_scraper - INFO - Fetching page: ...
2024-01-01 12:00:00,500 - icbc_scraper - INFO - Successfully fetched page. Status: 200
2024-01-01 12:00:01,000 - icbc_scraper - INFO - Page parsed successfully
```

## Target URL

**Product ID**: 21GS6173  
**Sale Target**: 7

This combination retrieves a specific net-value product's disclosure information from ICBC's financial system.

## Notes

- The scraper respects the target server's rate limits with delays
- Uses realistic User-Agent headers to identify as a browser
- Supports Chinese characters in data extraction
- All timestamps use ISO 8601 format

## Troubleshooting

### "Connection refused" or "Cannot reach server"

- Check internet connection
- Verify the target URL is accessible
- Check if the server is blocking requests (try adjusting User-Agent)

### "No data extracted"

- The page structure may have changed
- Try increasing timeout value
- Check HTML structure to ensure tables exist

### "UnicodeDecodeError"

- Ensure UTF-8 encoding is set correctly
- The scraper handles this automatically in most cases

## License

This project is provided as-is for educational and authorized use only.

## Disclaimer

This scraper is designed for authorized access to ICBC's public financial disclosure data. Ensure you have permission to scrape the target website and comply with their terms of service and robots.txt.
