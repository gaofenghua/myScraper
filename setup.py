#!/usr/bin/env python3
"""
Setup configuration for ICBC Net-Value Disclosure Scraper.

This file allows the package to be installed and distributed.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    requirements = [
        line.strip() for line in requirements_file.read_text().splitlines()
        if line.strip() and not line.startswith("#")
    ]

setup(
    name="icbc-net-value-scraper",
    version="1.0.0",
    description="Python web scraper for ICBC net-value disclosure data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Development Team",
    author_email="dev@example.com",
    url="https://github.com/example/icbc-scraper",
    license="MIT",
    
    py_modules=["icbc_scraper", "icbc_scraper_selenium", "config", "utils"],
    
    install_requires=requirements,
    
    python_requires=">=3.7",
    
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    
    entry_points={
        "console_scripts": [
            "icbc-scraper=icbc_scraper:main",
        ],
    },
    
    keywords="icbc scraper financial disclosure net-value",
    
    project_urls={
        "Documentation": "https://github.com/example/icbc-scraper",
        "Source": "https://github.com/example/icbc-scraper",
        "Bug Reports": "https://github.com/example/icbc-scraper/issues",
    },
)
