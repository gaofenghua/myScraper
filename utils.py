#!/usr/bin/env python3
"""
Utility functions for ICBC scraper data processing and analysis.

This module provides helper functions for:
- Data validation and cleaning
- Format conversion
- Filtering and aggregation
- Error logging and reporting
"""

import json
import csv
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


def validate_data(data: Dict[str, Any]) -> bool:
    """
    Validate scraped data structure.
    
    Args:
        data (Dict[str, Any]): Data to validate
        
    Returns:
        bool: True if data is valid, False otherwise
    """
    if not isinstance(data, dict):
        logger.error("Data is not a dictionary")
        return False
    
    required_fields = ['scraped_at', 'url']
    for field in required_fields:
        if field not in data:
            logger.error(f"Missing required field: {field}")
            return False
    
    logger.info("Data validation successful")
    return True


def merge_json_files(input_files: List[str], output_file: str) -> bool:
    """
    Merge multiple JSON files into one.
    
    Args:
        input_files (List[str]): List of input JSON file paths
        output_file (str): Output file path
        
    Returns:
        bool: True if merge successful, False otherwise
    """
    try:
        all_data = []
        
        for input_file in input_files:
            try:
                with open(input_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    all_data.append(data)
                logger.info(f"Loaded: {input_file}")
            except Exception as e:
                logger.error(f"Error loading {input_file}: {e}")
                continue
        
        # Write merged data
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Merged {len(all_data)} files into {output_file}")
        return True
        
    except Exception as e:
        logger.error(f"Error merging JSON files: {e}")
        return False


def convert_json_to_csv(json_file: str, output_file: str, table_index: int = 0) -> bool:
    """
    Convert JSON data to CSV format.
    
    Args:
        json_file (str): Input JSON file path
        output_file (str): Output CSV file path
        table_index (int): Index of table to convert (if multiple tables)
        
    Returns:
        bool: True if conversion successful, False otherwise
    """
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        tables = data.get('tables', [])
        if table_index >= len(tables):
            logger.error(f"Table index {table_index} out of range")
            return False
        
        table = tables[table_index]
        headers = table.get('headers', [])
        rows = table.get('rows', [])
        
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if headers:
                writer.writerow(headers)
            for row in rows:
                writer.writerow(row)
        
        logger.info(f"Converted JSON to CSV: {output_file}")
        return True
        
    except Exception as e:
        logger.error(f"Error converting JSON to CSV: {e}")
        return False


def extract_financial_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract financial-specific data from scraped content.
    
    Args:
        data (Dict[str, Any]): Scraped data
        
    Returns:
        Dict[str, Any]: Extracted financial data
    """
    financial_data = {
        'url': data.get('url'),
        'scraped_at': data.get('scraped_at'),
        'net_values': [],
        'metadata': data.get('metadata', {})
    }
    
    try:
        # Process tables for net-value information
        for table in data.get('tables', []):
            headers = table.get('headers', [])
            rows = table.get('rows', [])
            
            # Identify net-value related columns
            net_value_cols = [i for i, h in enumerate(headers) 
                            if 'net' in h.lower() or 'value' in h.lower() or '净值' in h]
            
            if net_value_cols:
                for row in rows:
                    row_dict = {headers[i]: row[i] if i < len(row) else '' 
                               for i in range(len(headers))}
                    financial_data['net_values'].append(row_dict)
        
        logger.info(f"Extracted {len(financial_data['net_values'])} net-value records")
        return financial_data
        
    except Exception as e:
        logger.error(f"Error extracting financial data: {e}")
        return financial_data


def generate_report(data: Dict[str, Any], output_file: str = None) -> str:
    """
    Generate a text report from scraped data.
    
    Args:
        data (Dict[str, Any]): Scraped data
        output_file (str): Optional output file path
        
    Returns:
        str: Report text
    """
    report_lines = []
    
    try:
        report_lines.append("=" * 80)
        report_lines.append("ICBC Net-Value Disclosure Scraping Report")
        report_lines.append("=" * 80)
        report_lines.append("")
        
        report_lines.append(f"Scraped at: {data.get('scraped_at')}")
        report_lines.append(f"Source URL: {data.get('url')}")
        report_lines.append(f"Page Title: {data.get('page_title')}")
        report_lines.append("")
        
        report_lines.append("URL Parameters:")
        for key, value in data.get('url_parameters', {}).items():
            report_lines.append(f"  {key}: {value}")
        report_lines.append("")
        
        report_lines.append(f"Tables Extracted: {len(data.get('tables', []))}")
        for table_idx, table in enumerate(data.get('tables', [])):
            headers = table.get('headers', [])
            rows = table.get('rows', [])
            report_lines.append(f"  Table {table_idx}: {len(headers)} columns, {len(rows)} rows")
            if headers:
                report_lines.append(f"    Columns: {', '.join(headers[:5])}")
                if len(headers) > 5:
                    report_lines.append(f"             ... ({len(headers) - 5} more)")
        
        report_lines.append("")
        report_lines.append(f"Content Sections: {len(data.get('content_sections', []))}")
        report_lines.append(f"Metadata Fields: {len(data.get('metadata', {}))}")
        report_lines.append("")
        report_lines.append("=" * 80)
        
        report_text = "\n".join(report_lines)
        
        if output_file:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report_text)
            logger.info(f"Report saved to: {output_file}")
        
        return report_text
        
    except Exception as e:
        logger.error(f"Error generating report: {e}")
        return ""


def clean_numeric_data(value: str) -> Optional[float]:
    """
    Clean and convert string data to numeric format.
    
    Args:
        value (str): String value to clean
        
    Returns:
        Optional[float]: Numeric value or None
    """
    try:
        # Remove common formatting
        value = str(value).strip()
        value = value.replace(',', '')
        value = value.replace('¥', '')
        value = value.replace('%', '')
        value = value.replace('元', '')
        
        return float(value)
    except (ValueError, AttributeError):
        return None


def filter_tables_by_header(data: Dict[str, Any], search_term: str) -> List[Dict]:
    """
    Filter tables that contain specific header.
    
    Args:
        data (Dict[str, Any]): Scraped data
        search_term (str): Term to search in headers
        
    Returns:
        List[Dict]: Matching tables
    """
    matching_tables = []
    
    for table in data.get('tables', []):
        headers = table.get('headers', [])
        if any(search_term.lower() in h.lower() for h in headers):
            matching_tables.append(table)
    
    logger.info(f"Found {len(matching_tables)} tables matching '{search_term}'")
    return matching_tables


def create_output_directory(base_path: str = 'output') -> Path:
    """
    Create output directory if it doesn't exist.
    
    Args:
        base_path (str): Base output path
        
    Returns:
        Path: Created directory path
    """
    output_path = Path(base_path)
    output_path.mkdir(parents=True, exist_ok=True)
    logger.info(f"Output directory ready: {output_path}")
    return output_path


if __name__ == '__main__':
    # Example usage
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("ICBC Scraper Utilities Module")
    print("Import this module to use utility functions in your scripts")
