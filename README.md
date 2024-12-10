# EGIS Applications Test Suite

## Overview
This repository contains automated test suites for various EGIS (Enterprise Geographic Information System) applications, including TDAT (Tribal Directory Assessment Tool). The tests are written in Python using Selenium WebDriver for browser automation and unittest for test organization.

## Applications Covered
- TDAT (Tribal Directory Assessment Tool)
- *(Add other EGIS applications as they are implemented)*

## Prerequisites
- Python 3.7+
- Chrome browser
- ChromeDriver (matching your Chrome version)

## Installation

1. Clone the repository:
- `git clone [repository-url]`
- `cd egis-automated-testing`
2. Create and activate a virtual environment (recommended):
- `python -m venv venv`
- `source venv/bin/activate` # On Windows: `venv\Scripts\activate`
3. Install required packages:
- `pip install -r requirements.txt`

## Project Structure
- **egis-automated-testing/**
  - **apps/**
    - **TDAT/**
      - `tdat_test.py`
      - `README.md`
    - **Other Apps/**
  - `requirements.txt`
  - `README.md`

## Running Tests
### Running All Tests
- `python -m unittest discover -s apps`

### Running Tests for Specific Application

- `python -m unittest apps/TDAT/tdat_test.py`

## Test Coverage

### TDAT Tests
The TDAT test suite (`tdat_test.py`) includes tests for:

1. **Basic Navigation**
   - Search for Tribes functionality
   - Advanced Search
   - Menu Access

2. **Search Features**
   - Tribe Selection
   - State/County Selection
   - Address Input
   - Map Interaction

3. **Data Export**
   - Export to Excel
   - Print Page functionality

4. **Map Features**
   - Map Zoom
   - Click on Map
   - Location Selection

5. **Documentation Access**
   - Alaska Special Instructions
   - TDAT User Guide
   - Process for Consultation
   - HUD Exchange Resources

6. **Additional Features**
   - Feedback and Corrections
   - Information by State

## Test Reports
- Test results are logged to both console and file (`tdat_tests.log`)
- A summary report is generated after test execution showing:
  - Passed tests
  - Failed tests
  - Total test count
  - Pass rate

## Contributing
1. Create a new branch for your feature/fix
2. Write tests following the existing pattern
3. Ensure all tests pass
4. Submit a pull request

## Best Practices
1. **Test Independence**: Each test should be independent and not rely on other tests
2. **Clear Naming**: Use descriptive test names that indicate functionality being tested
3. **Error Handling**: Include proper try-except blocks and logging
4. **Documentation**: Add docstrings and comments for complex logic
5. **Clean Up**: Use tearDown methods to clean up after tests

## Common Issues and Solutions
1. **ChromeDriver Version Mismatch**
   - Solution: Update ChromeDriver to match your Chrome browser version

2. **Element Not Found Errors**
   - Solution: Increase implicit/explicit wait times
   - Solution: Check if selectors are correct and unique

3. **Test Environment Issues**
   - Solution: Verify environment URL is correct
   - Solution: Check network connectivity

## Logging
- Logs are stored in `tdat_tests.log`
- Log format: `timestamp - level - message`
- Includes both success and failure messages
- Detailed error tracking for failed tests

## Support
For issues or questions:
- Create an issue in the repository
- Contact the EGIS development team
- *(Add specific contact information)*

## License
*(Add appropriate license information)*

---
Last Updated: [Current Date]