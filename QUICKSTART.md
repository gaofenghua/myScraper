# Quick Start Guide - ICBC Net-Value Disclosure Scraper

## 5-Minute Setup

### Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### Running the Scraper

```bash
# Simple one-liner to scrape and save data
python icbc_scraper.py
```

That's it! The scraper will:
1. Fetch the ICBC net-value disclosure page
2. Parse the HTML and extract tables
3. Save results to `output/` directory (both JSON and CSV)
4. Log all operations to `icbc_scraper.log`

## Output Files

After running the scraper, you'll find:

- **JSON Output**: `output/icbc_net_value_YYYYMMDD_HHMMSS.json`
  - Contains all extracted data in structured format
  - Includes tables, metadata, and page information

- **CSV Output**: `output/icbc_net_value_table_0_YYYYMMDD_HHMMSS.csv`
  - Each table is saved as a separate CSV
  - Easy to open in Excel or data analysis tools

- **Log File**: `icbc_scraper.log`
  - Detailed operation logs
  - Error messages with context

## Common Use Cases

### Use Case 1: Basic Scraping

```python
from icbc_scraper import ICBCNetValueScraper

scraper = ICBCNetValueScraper("https://www.icbc.com.cn/...")
data = scraper.scrape()

if data:
    scraper.save_to_json(data)
    scraper.save_tables_to_csv(data)
```

### Use Case 2: Get Financial Data

```python
from icbc_scraper import ICBCNetValueScraper
from utils import extract_financial_data

scraper = ICBCNetValueScraper("https://www.icbc.com.cn/...")
data = scraper.scrape()

# Extract net-value specific data
financial_data = extract_financial_data(data)

# Access the net values
for record in financial_data['net_values']:
    print(record)
```

### Use Case 3: Custom Configuration

```python
from icbc_scraper import ICBCNetValueScraper

# Create scraper with custom settings
scraper = ICBCNetValueScraper(
    base_url="https://www.icbc.com.cn/...",
    timeout=60,      # Longer timeout
    max_retries=5    # More retries
)

data = scraper.scrape()
scraper.save_to_json(data, output_dir="my_data")
```

### Use Case 4: Generate Report

```python
from icbc_scraper import ICBCNetValueScraper
from utils import generate_report, create_output_directory

scraper = ICBCNetValueScraper("https://www.icbc.com.cn/...")
data = scraper.scrape()

# Create output directory
create_output_directory("reports")

# Generate report
report = generate_report(data, "reports/summary.txt")
print(report)
```

### Use Case 5: Process Dynamic Content (JavaScript)

For pages that require JavaScript rendering:

```python
from icbc_scraper_selenium import ICBCNetValueScraperSelenium

scraper = ICBCNetValueScraperSelenium(
    base_url="https://www.icbc.com.cn/...",
    headless=True,        # Run in background
    wait_timeout=30       # Wait up to 30s for content
)

data = scraper.scrape()
```

## Configuration

Edit `config.py` to customize:

- **Target URL**: Change `ICBC_TARGET_URL`
- **Timeouts**: Adjust `REQUEST_TIMEOUT`
- **Retries**: Change `MAX_RETRIES`
- **Output**: Modify `OUTPUT_DIR`, `SAVE_JSON`, `SAVE_CSV`
- **Logging**: Adjust `LOG_LEVEL`

Example:
```python
# config.py
REQUEST_TIMEOUT = 60          # Increase timeout
MAX_RETRIES = 5               # More retries
OUTPUT_DIR = "my_output"      # Custom output
LOG_LEVEL = "DEBUG"           # Detailed logging
```

## Error Handling

The scraper automatically handles:

- ✓ Network timeouts
- ✓ Connection failures
- ✓ HTTP errors
- ✓ Parsing errors
- ✓ File I/O errors

All errors are logged to `icbc_scraper.log` for debugging.

## Testing

Run the test suite to verify everything works:

```bash
# Run all tests
python -m unittest test_scraper -v

# Run specific test
python -m unittest test_scraper.TestICBCScraperBasics -v
```

Expected output: `OK` with 16 tests passed

## Troubleshooting

### "Connection refused" or "Cannot reach server"
- Check internet connection
- Verify the target URL is correct
- Check if server is blocking requests

### "No data extracted"
- Increase timeout: `timeout=60`
- Check HTML structure (may have changed)
- Try Selenium version for dynamic content

### "UnicodeDecodeError"
- Usually handled automatically
- Check file encoding is UTF-8

## Examples

See `example_usage.py` for 7 detailed examples:

1. Basic scraping
2. Data validation
3. Financial data extraction
4. Report generation
5. Custom timeouts
6. Batch processing
7. Error handling

Run examples:
```bash
python example_usage.py
```

## File Structure

```
project/
├── icbc_scraper.py              # Main scraper (requests + BeautifulSoup)
├── icbc_scraper_selenium.py     # Alternative scraper (Selenium)
├── config.py                    # Configuration settings
├── utils.py                     # Utility functions
├── example_usage.py             # Usage examples
├── test_scraper.py              # Test suite (16 tests)
├── requirements.txt             # Dependencies
├── setup.py                     # Package setup
├── README.md                    # Full documentation
├── CONTRIBUTING.md              # Developer guidelines
├── CHANGELOG.md                 # Version history
└── output/                      # Output directory (created at runtime)
```

## Next Steps

1. **Read** `README.md` for complete documentation
2. **Check** `example_usage.py` for usage patterns
3. **Review** `config.py` for customization options
4. **Run** tests with `python -m unittest test_scraper -v`
5. **Execute** main scraper with `python icbc_scraper.py`

## Support

- Check logs in `icbc_scraper.log`
- Review error messages carefully
- Look at examples in `example_usage.py`
- Read `README.md` for detailed info
- Review `CONTRIBUTING.md` for development

## Performance Tips

- Increase timeout for slow connections
- Use CSV export for large tables
- Enable headless mode for Selenium
- Check logs to identify bottlenecks

## Security

- SSL verification is enabled
- No sensitive data is logged
- User-Agent headers are realistic
- Rate limiting respects server resources

---

**Happy Scraping! 🚀**
