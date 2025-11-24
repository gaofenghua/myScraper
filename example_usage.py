#!/usr/bin/env python3
"""
Example usage of the ICBC Net-Value Disclosure Scraper.

This script demonstrates various ways to use the scraper module
for different scraping scenarios.
"""

import logging
from pathlib import Path

from icbc_scraper import ICBCNetValueScraper
from config import ICBC_TARGET_URL, OUTPUT_DIR, LOG_FILE
from utils import (
    validate_data,
    extract_financial_data,
    generate_report,
    merge_json_files,
    convert_json_to_csv,
    create_output_directory
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def example_basic_scraping():
    """Example 1: Basic scraping with default settings."""
    logger.info("\n" + "="*80)
    logger.info("EXAMPLE 1: Basic Scraping")
    logger.info("="*80)
    
    # Create scraper instance
    scraper = ICBCNetValueScraper(
        base_url=ICBC_TARGET_URL,
        timeout=30,
        max_retries=3
    )
    
    # Perform scraping
    data = scraper.scrape()
    
    if data:
        logger.info(f"Scraping successful!")
        logger.info(f"  Tables found: {len(data.get('tables', []))}")
        logger.info(f"  Content sections: {len(data.get('content_sections', []))}")
        
        # Save results
        json_file = scraper.save_to_json(data, OUTPUT_DIR)
        csv_files = scraper.save_tables_to_csv(data, OUTPUT_DIR)
        
        logger.info(f"Data saved:")
        logger.info(f"  JSON: {json_file}")
        logger.info(f"  CSV files: {len(csv_files)}")
        
        return data
    else:
        logger.error("Scraping failed")
        return None


def example_with_validation(data):
    """Example 2: Scraping with data validation."""
    logger.info("\n" + "="*80)
    logger.info("EXAMPLE 2: Scraping with Validation")
    logger.info("="*80)
    
    if not data:
        logger.warning("No data to validate")
        return False
    
    # Validate data structure
    is_valid = validate_data(data)
    logger.info(f"Data validation: {'PASSED' if is_valid else 'FAILED'}")
    
    return is_valid


def example_financial_extraction(data):
    """Example 3: Extract financial-specific data."""
    logger.info("\n" + "="*80)
    logger.info("EXAMPLE 3: Financial Data Extraction")
    logger.info("="*80)
    
    if not data:
        logger.warning("No data to extract from")
        return None
    
    financial_data = extract_financial_data(data)
    logger.info(f"Extracted {len(financial_data.get('net_values', []))} net-value records")
    
    # Display some sample records
    if financial_data['net_values']:
        logger.info("Sample records:")
        for i, record in enumerate(financial_data['net_values'][:3]):
            logger.info(f"  Record {i+1}: {record}")
    
    return financial_data


def example_report_generation(data):
    """Example 4: Generate text report."""
    logger.info("\n" + "="*80)
    logger.info("EXAMPLE 4: Report Generation")
    logger.info("="*80)
    
    if not data:
        logger.warning("No data to generate report from")
        return
    
    # Create output directory
    create_output_directory(OUTPUT_DIR)
    
    # Generate report
    report_file = Path(OUTPUT_DIR) / "scraping_report.txt"
    report_text = generate_report(data, str(report_file))
    
    # Display report
    logger.info("Generated Report:")
    logger.info(report_text)


def example_custom_timeout():
    """Example 5: Scraping with custom timeout settings."""
    logger.info("\n" + "="*80)
    logger.info("EXAMPLE 5: Custom Timeout Settings")
    logger.info("="*80)
    
    # Create scraper with longer timeout for slow connections
    scraper = ICBCNetValueScraper(
        base_url=ICBC_TARGET_URL,
        timeout=60,  # Longer timeout
        max_retries=5  # More retries
    )
    
    logger.info(f"Scraper configured with:")
    logger.info(f"  Timeout: {scraper.timeout}s")
    logger.info(f"  Max retries: 5")
    
    data = scraper.scrape()
    return data


def example_batch_processing():
    """Example 6: Processing multiple URLs (batch mode)."""
    logger.info("\n" + "="*80)
    logger.info("EXAMPLE 6: Batch Processing")
    logger.info("="*80)
    
    # Example: Multiple products
    product_configs = [
        {"prodId": "21GS6173", "saleTarget": "7"},
        # Add more products as needed
    ]
    
    all_data = []
    
    for config in product_configs:
        url = f"{ICBC_TARGET_URL}?prodId={config['prodId']}&saleTarget={config['saleTarget']}"
        logger.info(f"Processing: {config}")
        
        scraper = ICBCNetValueScraper(base_url=url)
        data = scraper.scrape()
        
        if data:
            all_data.append(data)
            logger.info(f"  ✓ Successfully scraped")
        else:
            logger.warning(f"  ✗ Failed to scrape")
    
    logger.info(f"Batch processing complete. Scraped {len(all_data)} products")
    return all_data


def example_error_handling():
    """Example 7: Handling various error scenarios."""
    logger.info("\n" + "="*80)
    logger.info("EXAMPLE 7: Error Handling")
    logger.info("="*80)
    
    # Test with invalid URL
    scraper = ICBCNetValueScraper(
        base_url="https://invalid.example.com/page",
        timeout=5,
        max_retries=1
    )
    
    data = scraper.scrape()
    
    if data is None:
        logger.info("Gracefully handled failed request (as expected)")
    else:
        logger.info(f"Unexpectedly received data: {data}")


def main():
    """Run all examples."""
    logger.info("\n")
    logger.info("*" * 80)
    logger.info("ICBC Net-Value Disclosure Scraper - Usage Examples")
    logger.info("*" * 80)
    
    # Create output directory
    create_output_directory(OUTPUT_DIR)
    
    # Run examples in sequence
    try:
        # Example 1: Basic scraping
        data = example_basic_scraping()
        
        if data:
            # Example 2: Validation
            example_with_validation(data)
            
            # Example 3: Financial data extraction
            example_financial_extraction(data)
            
            # Example 4: Report generation
            example_report_generation(data)
        
        # Example 5: Custom timeout
        # Uncomment to run (may take longer)
        # data2 = example_custom_timeout()
        
        # Example 6: Batch processing
        # Uncomment to run (may take longer)
        # batch_data = example_batch_processing()
        
        # Example 7: Error handling
        example_error_handling()
        
    except Exception as e:
        logger.error(f"Error running examples: {e}", exc_info=True)
    
    logger.info("\n")
    logger.info("*" * 80)
    logger.info("Examples Complete")
    logger.info("*" * 80)
    logger.info(f"Output files saved to: {OUTPUT_DIR}")
    logger.info(f"Logs saved to: {LOG_FILE}")


if __name__ == '__main__':
    main()
