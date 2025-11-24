#!/usr/bin/env python3
"""
ICBC Net-Value Disclosure Scraper

This module provides functionality to scrape financial disclosure data from
the ICBC (Industrial and Commercial Bank of China) net-value disclosure page.

The scraper handles:
- Fetching the target webpage with appropriate headers
- Parsing HTML content
- Extracting net-value disclosure information
- Handling dynamic content (if present)
- Error handling for network and parsing issues
- Saving data in multiple formats (JSON, CSV)
"""

import json
import csv
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from urllib.parse import urlparse, parse_qs

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('icbc_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ICBCNetValueScraper:
    """
    Scraper for ICBC net-value disclosure data.
    
    Attributes:
        base_url (str): The base URL for the ICBC net-value disclosure page
        headers (dict): HTTP headers for requests
        session (requests.Session): Session for making HTTP requests with retries
    """
    
    # Default headers to avoid being blocked by the server
    DEFAULT_HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    def __init__(self, base_url: str, timeout: int = 30, max_retries: int = 3):
        """
        Initialize the ICBC scraper.
        
        Args:
            base_url (str): The URL to scrape
            timeout (int): Request timeout in seconds
            max_retries (int): Maximum number of retries for failed requests
        """
        self.base_url = base_url
        self.timeout = timeout
        self.session = self._create_session(max_retries)
        logger.info(f"Initialized scraper for URL: {base_url}")
    
    def _create_session(self, max_retries: int = 3) -> requests.Session:
        """
        Create a requests session with retry strategy.
        
        Args:
            max_retries (int): Maximum number of retries
            
        Returns:
            requests.Session: Configured session with retry strategy
        """
        session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        session.headers.update(self.DEFAULT_HEADERS)
        
        return session
    
    def fetch_page(self) -> Optional[str]:
        """
        Fetch the webpage content.
        
        Returns:
            Optional[str]: HTML content of the page, or None if fetch failed
            
        Raises:
            Logs errors but continues gracefully
        """
        try:
            logger.info(f"Fetching page: {self.base_url}")
            response = self.session.get(
                self.base_url,
                timeout=self.timeout,
                verify=True
            )
            response.raise_for_status()
            logger.info(f"Successfully fetched page. Status: {response.status_code}")
            return response.text
        except requests.exceptions.Timeout:
            logger.error(f"Request timed out after {self.timeout} seconds")
            return None
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection error: {e}")
            return None
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error: {e}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error while fetching page: {e}")
            return None
    
    def parse_page(self, html_content: str) -> Dict[str, Any]:
        """
        Parse the HTML content and extract net-value disclosure data.
        
        Args:
            html_content (str): HTML content of the page
            
        Returns:
            Dict[str, Any]: Extracted data including metadata and net-value information
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            data = {
                'scraped_at': datetime.now().isoformat(),
                'url': self.base_url,
                'page_title': None,
                'tables': [],
                'content_sections': [],
                'metadata': {}
            }
            
            # Extract page title
            title_tag = soup.find('title')
            if title_tag:
                data['page_title'] = title_tag.text.strip()
                logger.info(f"Page title: {data['page_title']}")
            
            # Extract URL parameters
            parsed_url = urlparse(self.base_url)
            params = parse_qs(parsed_url.query)
            data['url_parameters'] = {k: v[0] if len(v) == 1 else v for k, v in params.items()}
            logger.info(f"URL parameters: {data['url_parameters']}")
            
            # Extract tables (net-value data is typically in tables)
            tables = soup.find_all('table')
            logger.info(f"Found {len(tables)} table(s)")
            
            for table_idx, table in enumerate(tables):
                table_data = self._parse_table(table)
                if table_data['rows']:  # Only include non-empty tables
                    data['tables'].append({
                        'index': table_idx,
                        'headers': table_data['headers'],
                        'rows': table_data['rows']
                    })
                    logger.info(f"Table {table_idx}: {len(table_data['rows'])} rows extracted")
            
            # Extract main content sections
            main_content = soup.find('main') or soup.find('div', class_='content') or soup.find('body')
            if main_content:
                sections = main_content.find_all(['div', 'section'], recursive=False)
                for section in sections:
                    text = section.get_text(strip=True)
                    if text and len(text) > 10:
                        data['content_sections'].append({
                            'tag': section.name,
                            'class': section.get('class', []),
                            'text': text[:500]  # First 500 characters
                        })
            
            # Extract meta information
            meta_tags = soup.find_all('meta')
            for meta in meta_tags:
                name = meta.get('name') or meta.get('property')
                content = meta.get('content')
                if name and content:
                    data['metadata'][name] = content
            
            logger.info("Page parsed successfully")
            return data
            
        except Exception as e:
            logger.error(f"Error parsing page: {e}")
            return {
                'scraped_at': datetime.now().isoformat(),
                'url': self.base_url,
                'error': str(e),
                'tables': [],
                'content_sections': []
            }
    
    def _parse_table(self, table) -> Dict[str, List]:
        """
        Parse a single HTML table element.
        
        Args:
            table: BeautifulSoup table element
            
        Returns:
            Dict[str, List]: Dictionary with 'headers' and 'rows' lists
        """
        headers = []
        rows = []
        
        try:
            # Extract headers
            header_row = table.find('thead')
            if header_row:
                headers = [th.get_text(strip=True) for th in header_row.find_all(['th', 'td'])]
            else:
                first_row = table.find('tr')
                if first_row:
                    headers = [cell.get_text(strip=True) for cell in first_row.find_all(['th', 'td'])]
            
            # Extract rows
            tbody = table.find('tbody')
            if tbody:
                table_rows = tbody.find_all('tr')
            else:
                table_rows = table.find_all('tr')[1:] if headers else table.find_all('tr')
            
            for row in table_rows:
                cells = row.find_all(['td', 'th'])
                if cells:
                    row_data = [cell.get_text(strip=True) for cell in cells]
                    rows.append(row_data)
            
        except Exception as e:
            logger.error(f"Error parsing table: {e}")
        
        return {'headers': headers, 'rows': rows}
    
    def scrape(self) -> Optional[Dict[str, Any]]:
        """
        Perform the complete scraping operation.
        
        Returns:
            Optional[Dict[str, Any]]: Extracted data or None if scraping failed
        """
        html_content = self.fetch_page()
        if not html_content:
            logger.error("Failed to fetch page content")
            return None
        
        data = self.parse_page(html_content)
        return data
    
    def save_to_json(self, data: Dict[str, Any], output_dir: str = 'output') -> str:
        """
        Save scraped data to a JSON file.
        
        Args:
            data (Dict[str, Any]): Scraped data
            output_dir (str): Directory to save the output
            
        Returns:
            str: Path to the saved file
        """
        try:
            output_path = Path(output_dir)
            output_path.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'icbc_net_value_{timestamp}.json'
            filepath = output_path / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Data saved to JSON: {filepath}")
            return str(filepath)
        except Exception as e:
            logger.error(f"Error saving to JSON: {e}")
            return ""
    
    def save_tables_to_csv(self, data: Dict[str, Any], output_dir: str = 'output') -> List[str]:
        """
        Save extracted tables to CSV files.
        
        Args:
            data (Dict[str, Any]): Scraped data containing tables
            output_dir (str): Directory to save the output
            
        Returns:
            List[str]: List of saved file paths
        """
        saved_files = []
        try:
            output_path = Path(output_dir)
            output_path.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            for table_idx, table in enumerate(data.get('tables', [])):
                filename = f'icbc_net_value_table_{table_idx}_{timestamp}.csv'
                filepath = output_path / filename
                
                try:
                    with open(filepath, 'w', newline='', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        
                        # Write headers
                        if table.get('headers'):
                            writer.writerow(table['headers'])
                        
                        # Write rows
                        for row in table.get('rows', []):
                            writer.writerow(row)
                    
                    logger.info(f"Table {table_idx} saved to CSV: {filepath}")
                    saved_files.append(str(filepath))
                except Exception as e:
                    logger.error(f"Error saving table {table_idx} to CSV: {e}")
            
            return saved_files
        except Exception as e:
            logger.error(f"Error in save_tables_to_csv: {e}")
            return saved_files


def main():
    """Main entry point for the scraper."""
    
    # Target URL for ICBC net-value disclosure
    target_url = "https://www.icbc.com.cn/webpage/finance/disclosure/detail/net-value/?prodId=21GS6173&saleTarget=7"
    
    try:
        logger.info("=" * 80)
        logger.info("Starting ICBC Net-Value Disclosure Scraper")
        logger.info("=" * 80)
        
        # Create scraper instance
        scraper = ICBCNetValueScraper(
            base_url=target_url,
            timeout=30,
            max_retries=3
        )
        
        # Perform scraping
        logger.info("Beginning scraping operation...")
        data = scraper.scrape()
        
        if data is None:
            logger.error("Scraping failed - no data retrieved")
            return 1
        
        # Save results in multiple formats
        logger.info("Saving results...")
        json_file = scraper.save_to_json(data)
        csv_files = scraper.save_tables_to_csv(data)
        
        # Print summary
        logger.info("=" * 80)
        logger.info("Scraping Complete - Summary")
        logger.info("=" * 80)
        logger.info(f"JSON file saved: {json_file}")
        logger.info(f"CSV files saved: {len(csv_files)}")
        for csv_file in csv_files:
            logger.info(f"  - {csv_file}")
        logger.info(f"Total tables extracted: {len(data.get('tables', []))}")
        logger.info("=" * 80)
        
        return 0
        
    except Exception as e:
        logger.error(f"Unexpected error in main: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    exit(main())
