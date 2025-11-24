#!/usr/bin/env python3
"""
ICBC Net-Value Disclosure Scraper with Selenium Support

This module extends the basic scraper with Selenium support for handling
dynamic content loading via JavaScript. Use this when the basic requests-based
scraper fails to retrieve complete data.

Selenium allows for:
- Waiting for dynamically loaded content
- Handling JavaScript-rendered pages
- Simulating user interactions
- Working with SPAs (Single Page Applications)
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class ICBCNetValueScraperSelenium:
    """
    Selenium-based scraper for ICBC net-value disclosure data.
    
    Use this version when dynamic content loading is required or when
    the page heavily relies on JavaScript rendering.
    """
    
    def __init__(
        self,
        base_url: str,
        headless: bool = True,
        wait_timeout: int = 30,
        page_load_timeout: int = 60
    ):
        """
        Initialize Selenium-based scraper.
        
        Args:
            base_url (str): The URL to scrape
            headless (bool): Run browser in headless mode
            wait_timeout (int): Timeout for waiting for elements (seconds)
            page_load_timeout (int): Timeout for page load (seconds)
        """
        self.base_url = base_url
        self.wait_timeout = wait_timeout
        self.page_load_timeout = page_load_timeout
        self.headless = headless
        self.driver = None
        
        logger.info(f"Initialized Selenium scraper for URL: {base_url}")
    
    def _setup_driver(self) -> webdriver.Chrome:
        """
        Set up and configure the Chrome WebDriver.
        
        Returns:
            webdriver.Chrome: Configured Chrome driver
        """
        chrome_options = ChromeOptions()
        
        if self.headless:
            chrome_options.add_argument('--headless')
        
        # Additional options for stability
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        
        # Set user agent to avoid detection
        chrome_options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        )
        
        try:
            driver = webdriver.Chrome(options=chrome_options)
            driver.set_page_load_timeout(self.page_load_timeout)
            logger.info("Chrome driver initialized successfully")
            return driver
        except Exception as e:
            logger.error(f"Failed to initialize Chrome driver: {e}")
            raise
    
    def fetch_page_with_selenium(self) -> Optional[str]:
        """
        Fetch page using Selenium and wait for dynamic content.
        
        Returns:
            Optional[str]: HTML content of the page after JS execution
        """
        self.driver = self._setup_driver()
        
        try:
            logger.info(f"Loading page with Selenium: {self.base_url}")
            self.driver.get(self.base_url)
            
            # Wait for main content to load
            wait = WebDriverWait(self.driver, self.wait_timeout)
            
            # Wait for common data table containers to be present
            try:
                wait.until(EC.presence_of_all_elements_located(
                    (By.TAG_NAME, 'table')
                ))
                logger.info("Tables loaded successfully")
            except Exception:
                logger.warning("Timeout waiting for tables, continuing anyway...")
            
            # Additional wait for dynamic content
            import time
            time.sleep(2)
            
            # Get page source after JS execution
            html_content = self.driver.page_source
            logger.info("Page content retrieved after JavaScript execution")
            
            return html_content
            
        except Exception as e:
            logger.error(f"Error loading page with Selenium: {e}")
            return None
        finally:
            self.close_driver()
    
    def close_driver(self):
        """Close the Selenium WebDriver."""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("Chrome driver closed")
            except Exception as e:
                logger.error(f"Error closing driver: {e}")
    
    def scrape(self) -> Optional[Dict[str, Any]]:
        """
        Perform scraping using Selenium.
        
        Returns:
            Optional[Dict[str, Any]]: Extracted data
        """
        try:
            html_content = self.fetch_page_with_selenium()
            if not html_content:
                logger.error("Failed to fetch page with Selenium")
                return None
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            
            data = {
                'scraped_at': datetime.now().isoformat(),
                'url': self.base_url,
                'method': 'selenium',
                'page_title': None,
                'tables': [],
                'metadata': {}
            }
            
            # Extract title
            title_tag = soup.find('title')
            if title_tag:
                data['page_title'] = title_tag.text.strip()
            
            # Extract tables
            tables = soup.find_all('table')
            logger.info(f"Found {len(tables)} table(s)")
            
            for table_idx, table in enumerate(tables):
                table_data = self._parse_table(table)
                if table_data['rows']:
                    data['tables'].append({
                        'index': table_idx,
                        'headers': table_data['headers'],
                        'rows': table_data['rows']
                    })
            
            logger.info("Page parsed successfully with Selenium")
            return data
            
        except Exception as e:
            logger.error(f"Error during scraping: {e}")
            return None
    
    def _parse_table(self, table) -> Dict[str, list]:
        """
        Parse HTML table element.
        
        Args:
            table: BeautifulSoup table element
            
        Returns:
            Dict with headers and rows
        """
        headers = []
        rows = []
        
        try:
            # Extract headers
            header_row = table.find('thead')
            if header_row:
                headers = [th.get_text(strip=True) for th in header_row.find_all(['th', 'td'])]
            
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


def main():
    """Example usage of Selenium-based scraper."""
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    target_url = "https://www.icbc.com.cn/webpage/finance/disclosure/detail/net-value/?prodId=21GS6173&saleTarget=7"
    
    try:
        logger.info("Starting Selenium-based ICBC scraper...")
        
        scraper = ICBCNetValueScraperSelenium(
            base_url=target_url,
            headless=True,
            wait_timeout=30
        )
        
        data = scraper.scrape()
        
        if data:
            # Save to file
            output_path = Path('output')
            output_path.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filepath = output_path / f'icbc_selenium_{timestamp}.json'
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Data saved to: {filepath}")
            logger.info(f"Tables extracted: {len(data.get('tables', []))}")
        
    except Exception as e:
        logger.error(f"Error: {e}")


if __name__ == '__main__':
    main()
