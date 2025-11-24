# Contributing to ICBC Net-Value Disclosure Scraper

Thank you for your interest in contributing to this project!

## Development Setup

### Prerequisites
- Python 3.7 or higher
- pip
- virtualenv (optional but recommended)

### Setting Up Development Environment

1. Clone the repository:
```bash
git clone <repository-url>
cd icbc-scraper
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -r requirements.txt
pip install pytest pytest-cov  # For testing
```

## Project Structure

```
icbc-scraper/
├── icbc_scraper.py           # Main scraper module
├── icbc_scraper_selenium.py  # Selenium-based scraper for dynamic content
├── config.py                  # Configuration settings
├── utils.py                   # Utility functions
├── test_scraper.py           # Test suite
├── example_usage.py          # Usage examples
├── requirements.txt          # Python dependencies
├── setup.py                  # Package configuration
├── README.md                 # Project documentation
└── output/                   # Output directory (created at runtime)
```

## Code Style

### Style Guidelines
- Follow PEP 8 conventions
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep lines under 100 characters where practical
- Use type hints where applicable

### Example:
```python
def fetch_data(url: str, timeout: int = 30) -> Optional[str]:
    """
    Fetch data from the given URL.
    
    Args:
        url (str): The URL to fetch from
        timeout (int): Request timeout in seconds
        
    Returns:
        Optional[str]: Response content or None if fetch failed
    """
    try:
        response = requests.get(url, timeout=timeout)
        return response.text
    except Exception as e:
        logger.error(f"Error fetching {url}: {e}")
        return None
```

## Testing

### Running Tests
```bash
# Run all tests
python -m unittest test_scraper -v

# Run specific test class
python -m unittest test_scraper.TestICBCScraperBasics -v

# Run specific test
python -m unittest test_scraper.TestICBCScraperBasics.test_scraper_initialization -v
```

### Writing Tests
- Create test classes inheriting from `unittest.TestCase`
- Use descriptive test method names starting with `test_`
- Add docstrings explaining what is being tested
- Mock external dependencies (HTTP requests, etc.)

Example:
```python
class TestMyFeature(unittest.TestCase):
    """Test my new feature."""
    
    def test_feature_works_correctly(self):
        """Test that feature works as expected."""
        result = my_function()
        self.assertEqual(result, expected_value)
```

## Making Changes

### Before Making Changes
1. Create a feature branch: `git checkout -b feature/my-feature`
2. Keep changes focused on a single feature or bug fix
3. Update documentation if needed

### Commit Messages
- Use clear, descriptive commit messages
- Start with a verb (e.g., "Add", "Fix", "Update")
- Keep first line under 50 characters
- Add detailed description if needed

Example:
```
Add Selenium-based scraper for dynamic content

- Implements automatic wait for dynamic elements
- Supports multiple content loading patterns
- Includes timeout and retry configuration
```

### Pull Requests
1. Push your branch to the repository
2. Create a pull request with a clear description
3. Reference any related issues
4. Ensure all tests pass
5. Address code review comments

## Common Tasks

### Adding a New Feature
1. Update configuration in `config.py` if needed
2. Implement the feature in appropriate module
3. Add comprehensive logging
4. Write tests in `test_scraper.py`
5. Update README.md with usage examples
6. Create an example in `example_usage.py`

### Fixing a Bug
1. Create a test that reproduces the bug
2. Fix the issue
3. Verify the test passes
4. Check for similar issues elsewhere
5. Update CHANGELOG if applicable

### Improving Error Handling
1. Identify the error scenario
2. Add appropriate error handling
3. Log errors with context
4. Write tests for error paths
5. Document the error handling in comments

## Running the Scraper

### Basic Usage
```bash
python icbc_scraper.py
```

### Using in Your Code
```python
from icbc_scraper import ICBCNetValueScraper

scraper = ICBCNetValueScraper("https://...")
data = scraper.scrape()
scraper.save_to_json(data)
```

### Running Examples
```bash
python example_usage.py
```

## Reporting Issues

When reporting issues, please include:
- Python version
- Exact error message
- Steps to reproduce
- Expected vs actual behavior
- Any relevant logs

## Requesting Features

When requesting features:
- Describe the use case
- Explain expected behavior
- Provide examples if possible
- Consider impact on existing functionality

## Documentation

### Updating README
- Keep README.md up to date with changes
- Include examples for new features
- Document configuration options
- Explain error handling approaches

### Code Comments
- Use comments to explain "why" not "what"
- Keep comments concise and current
- Update comments when code changes

## Performance Considerations

- Minimize HTTP requests
- Use appropriate timeouts
- Handle large datasets efficiently
- Consider memory usage with large data

## Security Considerations

- Never hardcode sensitive information
- Use environment variables for credentials
- Validate and sanitize data
- Handle URLs securely
- Check SSL certificates

## Questions or Need Help?

Feel free to:
- Open an issue with your question
- Check existing documentation
- Review code examples
- Look at test cases for usage patterns

Thank you for contributing!
