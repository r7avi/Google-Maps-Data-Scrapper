# Google-Maps-Scrapper
This project provides a set of Python scripts to scrape data from Google Maps using the Playwright library for automated web browsing. The data scraped includes names, addresses, phone numbers, websites, pluscode, longitude / latitude, ratings and other relevant details of listings found on Google Maps.

## Table of Contents

- [Prerequisite](#prerequisite)
- [Key Features](#key-features)
- [Installation](#installation)
- [How to Use](#how-to-use)

## Prerequisite

- This code requires a python version below 3.10
- Any version of python beyond 3.10 may cause issues and may not work properly

## Modules

- `scraper.py`: Contains functions to interact with Google Maps through a browser session, scroll through listings, and extract listing details.
- `utils.py`: Includes utility functions for reading search terms, saving data to Excel, merging Excel files, adjusting column widths in Excel, and parsing coordinates from URLs.
- `run.py`: Orchestrates the scraping process using functions from other modules, handles user inputs, and manages the overall flow of the application.

## Key Features

- **Interactive Search**: Users can choose to input search terms manually or use predefined terms from a `Query.txt` file.
- **Data Extraction**: Extracts detailed information about each listing, including links, names, types, plus codes, ratings, addresses, websites, phone numbers, and review counts.
- **Data Normalization & Cleansing**: Ensures all data lists are of the same length before saving & It cleanses and organizes the scraped data, removing redundant or unnecessary columns.
- **Coordinate Parsing**: Extracts latitude and longitude from Google Maps links.
- **Review Analysis**: It extracts review counts and average ratings, providing insights into businesses' online reputation.
- **Business Type Detection**: The script identifies whether a business offers in-store shopping, in-store pickup, or delivery services.
- **Excel Integration**: Saves individual search results into Excel files and can merge multiple results into a single file with adjusted column widths for better readability.


## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/r7avi/Google-Maps-Scrapper.git
2. Navigate to the project directory:
   ```bash
   cd google-maps-scraping
3. Update PIP:
    ```bash
     python -m pip install --upgrade pip

3. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```
    or
    ```bash
    pip install playwright pandas openpyxl tqdm playwright install
    ```

## How to Use:

To use this script, follow these steps:

1. Start the script `run.py`.

    ```bash
    python main.py
    ```
2. Choose to input a search term manually or use `Query.txt`.

   ```bash
   doctors in new york
   dentist in new yersy
    ```
3. Enter the total number of results you want to scrape.

   ```bash
   Min : 20 (Default) & Max : 150
    ```
4. The script will navigate to Google Maps, perform searches, scrape data, and save it into Excel files in the `output` directory.


## Docker :

1. If you want to run in Docker ,In Docker/app : update Query.txt and Modify Server details in Scrapper.py and add your Linux SSH Details so Scrapped data can be stored in your Linux server else It will be stored Locally in app/output.
    
    Execute below command in Docker folder . [Note You Must Have Docker Installed in your Win/Linux]
   ```bash
     docker-compose up --build
    ```

## Other Helpful Docker Commands : [https://github.com/r7avi/Google-Maps-Scrapper/blob/main/docker/Docker-Commands.txt](https://github.com/r7avi/Google-Maps-Scrapper/blob/main/docker/Docker-Commands.txt)
