# Google-Maps-Scrapper
This Python script utilizes the Playwright library to perform web scraping and data extraction from Google Maps. It is particularly designed for obtaining information about businesses, including their name, address, website, phone number, reviews, and more.
## Table of Contents

- [Prerequisite](#prerequisite)
- [Key Features](#key-features)
- [Installation](#installation)
- [How to Use](#how-to-use)

## Prerequisite
- This code requires a python version below 3.10
- Any version of python beyond 3.10 may cause issues and may not work properly

## Key Features
- Data Scraping: The script scrapes data from Google Maps listings, extracting valuable information about businesses, such as their name, address,address short code, website, and contact details.

- Review Analysis: It extracts review counts and average ratings, providing insights into businesses' online reputation.

- Business Type Detection: The script identifies whether a business offers in-store shopping, in-store pickup, or delivery services.

- Operating Hours: It extracts information about the business's operating hours.

- Introduction Extraction: The script also scrapes introductory information about the businesses when available.

- Data Cleansing: It cleanses and organizes the scraped data, removing redundant or unnecessary columns.

- CSV Export: The cleaned data is exported to a CSV file for further analysis or integration with other tools.

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

   


## How to Use:

To use this script, follow these steps:

1. Run the script with Python:
    ```bash
     python main.py -s "search term" -t total
    ```
    Load all your Quries in Query.txt, 
   ```bash
     python run.py
    ```

3. The script will launch a browser, perform the search, and start scraping information. It will display the progress and save the results to a CSV file called searchname_results.csv.

## Docker :

If you want to run in Docker ,In Docker/app : update Query.txt and Modify Server details in Scrapper.py and add your Linux SSH Details so Scrapped data can be stored in your Linux server.
    Execute below command in Docker folder . [Note You Must Have Docker Installed in your Win/Linux]
   ```bash
     docker-compose up --build
    ```
   
Other Helpful Docker Commands : [https://github.com/r7avi/Google-Maps-Scrapper/blob/main/docker/Docker-Commands.txt](https://github.com/r7avi/Google-Maps-Scrapper/blob/main/docker/Docker-Commands.txt)
