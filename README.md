# LinkedIn Job Scraper

A Python tool for automated collection of job listings from LinkedIn.

## Prerequisites

- Python 3.6+
- Conda environment management
- Chrome browser installed

## Installation

1. Clone or download this repository to your local machine
2. Activate your Conda environment:
   ```bash
   conda activate myenv
   ```
3. Install required dependencies:
   ```bash
   pip install linkedin_jobs_scraper
   ```

## Usage

1. Activate your Conda environment:
   ```bash
   conda activate myenv
   ```

2. Run the script:
   ```bash
   python linkedin_scraper.py
   ```

3. Follow the interactive prompts to enter search parameters:
   - Job title (default: "software engineer")
   - Location (default: "United States")
   - Experience level (optional)
   - Remote/on-site preference (optional)
   - Time filter (optional)
   - Job type (optional)
   - Relevance (optional)
   - Number of results to fetch (optional)

4. Results will be appended to `linkedin_jobs.csv` in the same directory

## Notes

- The script appends new results to the existing CSV file
- Default parameters are used when inputs are not provided
- Running this tool frequently may violate LinkedIn's Terms of Service
- Recommended to use with caution and reasonable request frequency

## Troubleshooting

- If encountering errors, verify your Python installation and dependencies
- Ensure your Conda environment is activated before running the script
- Check your internet connection if no results are returned
- LinkedIn may periodically update their site structure, requiring script updates

## Contact

For technical assistance, please contact the development team.
