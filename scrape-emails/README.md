# Email Scraper

This Python-based email scraper extracts email addresses from websites listed in a CSV file. It uses the Playwright library to interact with web pages and locate email addresses on both the main page and designated contact pages.

## Features

- Scrapes email addresses from the main page of a website.
- Follows and scrapes contact pages linked from the main page.
- Converts relative URLs to absolute URLs.
- Logs errors to `error_log.txt` for troubleshooting.
- Saves results to a new CSV file with an additional 'Email' column.

## Prerequisites

- Python 3.10
- Google Chrome or Chromium browser

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/r7avi/Scrape-Emails-from-Websites.git
   cd email-scraper

2. **Set up a virtual environment (optional but recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

3. **Install required packages:**
   
   ```bash
   pip install -r requirements.txt


4. **Download and install Google Chrome or Chromium:**

   ```bash
   Ensure you have Google Chrome or Chromium installed. The script uses Playwright's Chromium driver by default but you can specify the path to Chrome if needed.

5. **Run the script:**

   ```bash
   python email-scrapper.py

6. **Select a CSV file:**

   ```bash
   A file dialog will prompt you to select a CSV file containing website URLs. Ensure the CSV file has a column named Website.

7. **Review results:**

   ```bash
   The script will process each website, extract email addresses, and save the results to a new CSV file with an added Email column.


## Error Logging

Errors encountered during the scraping process are logged in error_log.txt. Review this file for troubleshooting any issues.







