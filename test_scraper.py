#!/usr/bin/env python3
"""
Test suite for ICBC Net-Value Disclosure Scraper.

This module contains tests to verify scraper functionality and correctness.
"""

import json
import logging
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

from icbc_scraper import ICBCNetValueScraper
from config import ICBC_TARGET_URL
from utils import validate_data, extract_financial_data, clean_numeric_data

# Configure logging for tests
logging.basicConfig(level=logging.WARNING)


class TestICBCScraperBasics(unittest.TestCase):
    """Test basic scraper functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_url = ICBC_TARGET_URL
        self.scraper = ICBCNetValueScraper(
            base_url=self.test_url,
            timeout=10,
            max_retries=1
        )
    
    def test_scraper_initialization(self):
        """Test that scraper initializes correctly."""
        self.assertEqual(self.scraper.base_url, self.test_url)
        self.assertEqual(self.scraper.timeout, 10)
        self.assertIsNotNone(self.scraper.session)
    
    def test_session_has_default_headers(self):
        """Test that session has proper headers."""
        self.assertIn('User-Agent', self.scraper.session.headers)
    
    def test_parse_table_empty(self):
        """Test table parsing with empty table."""
        from bs4 import BeautifulSoup
        
        html = "<table></table>"
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table')
        
        result = self.scraper._parse_table(table)
        
        self.assertIn('headers', result)
        self.assertIn('rows', result)
        self.assertEqual(len(result['headers']), 0)
        self.assertEqual(len(result['rows']), 0)
    
    def test_parse_table_with_data(self):
        """Test table parsing with actual data."""
        from bs4 import BeautifulSoup
        
        html = """
        <table>
            <thead>
                <tr><th>Name</th><th>Value</th></tr>
            </thead>
            <tbody>
                <tr><td>Item 1</td><td>100</td></tr>
                <tr><td>Item 2</td><td>200</td></tr>
            </tbody>
        </table>
        """
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table')
        
        result = self.scraper._parse_table(table)
        
        self.assertEqual(len(result['headers']), 2)
        self.assertEqual(result['headers'], ['Name', 'Value'])
        self.assertEqual(len(result['rows']), 2)
        self.assertEqual(result['rows'][0], ['Item 1', '100'])
    
    def test_save_to_json_creates_file(self):
        """Test that JSON file is created."""
        test_data = {
            'scraped_at': '2024-01-01T00:00:00',
            'url': self.test_url,
            'tables': [],
            'content_sections': []
        }
        
        test_dir = Path('test_output')
        json_file = self.scraper.save_to_json(test_data, str(test_dir))
        
        try:
            self.assertTrue(Path(json_file).exists())
            
            # Verify content
            with open(json_file, 'r', encoding='utf-8') as f:
                saved_data = json.load(f)
            
            self.assertEqual(saved_data['url'], self.test_url)
        finally:
            # Cleanup
            import shutil
            if test_dir.exists():
                shutil.rmtree(test_dir)


class TestDataValidation(unittest.TestCase):
    """Test data validation utilities."""
    
    def test_validate_valid_data(self):
        """Test validation of valid data."""
        data = {
            'scraped_at': '2024-01-01T00:00:00',
            'url': 'https://example.com',
            'tables': []
        }
        
        result = validate_data(data)
        self.assertTrue(result)
    
    def test_validate_missing_required_field(self):
        """Test validation fails with missing required field."""
        data = {
            'scraped_at': '2024-01-01T00:00:00'
            # Missing 'url'
        }
        
        result = validate_data(data)
        self.assertFalse(result)
    
    def test_validate_non_dict(self):
        """Test validation fails for non-dict input."""
        result = validate_data([])
        self.assertFalse(result)


class TestDataProcessing(unittest.TestCase):
    """Test data processing utilities."""
    
    def test_clean_numeric_data_float(self):
        """Test cleaning of numeric strings."""
        self.assertEqual(clean_numeric_data("123.45"), 123.45)
    
    def test_clean_numeric_data_with_comma(self):
        """Test cleaning numeric strings with commas."""
        self.assertEqual(clean_numeric_data("1,234.56"), 1234.56)
    
    def test_clean_numeric_data_with_currency(self):
        """Test cleaning currency formatted strings."""
        self.assertEqual(clean_numeric_data("¥1000"), 1000.0)
    
    def test_clean_numeric_data_with_percent(self):
        """Test cleaning percentage strings."""
        self.assertEqual(clean_numeric_data("5%"), 5.0)
    
    def test_clean_numeric_data_invalid(self):
        """Test cleaning invalid numeric strings."""
        result = clean_numeric_data("not a number")
        self.assertIsNone(result)
    
    def test_extract_financial_data(self):
        """Test financial data extraction."""
        data = {
            'url': 'https://example.com',
            'scraped_at': '2024-01-01T00:00:00',
            'tables': [
                {
                    'headers': ['Date', 'Net Value', 'Change'],
                    'rows': [
                        ['2024-01-01', '1.0000', '+0.0010'],
                        ['2024-01-02', '1.0010', '+0.0005']
                    ]
                }
            ]
        }
        
        result = extract_financial_data(data)
        
        self.assertEqual(len(result['net_values']), 2)
        self.assertIn('url', result)
        self.assertIn('scraped_at', result)


class TestPageParsing(unittest.TestCase):
    """Test HTML parsing functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.scraper = ICBCNetValueScraper("https://example.com")
    
    def test_parse_page_simple_html(self):
        """Test parsing simple HTML content."""
        html = """
        <html>
            <head><title>Test Page</title></head>
            <body>
                <table>
                    <tr><th>Header</th></tr>
                    <tr><td>Data</td></tr>
                </table>
            </body>
        </html>
        """
        
        result = self.scraper.parse_page(html)
        
        self.assertEqual(result['page_title'], 'Test Page')
        self.assertGreaterEqual(len(result['tables']), 1)
    
    def test_parse_page_with_error(self):
        """Test page parsing handles errors gracefully."""
        result = self.scraper.parse_page("")
        
        self.assertIn('scraped_at', result)
        self.assertIn('url', result)


def run_tests():
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestICBCScraperBasics))
    suite.addTests(loader.loadTestsFromTestCase(TestDataValidation))
    suite.addTests(loader.loadTestsFromTestCase(TestDataProcessing))
    suite.addTests(loader.loadTestsFromTestCase(TestPageParsing))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    exit(run_tests())
