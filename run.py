import os
import time
import logging
from scraper import scrape_google_maps

def main():
    # Define the path to the Queries.txt file and the error log file
    queries_file_path = 'Queries.txt'
    error_log_path = 'error_log.txt'
    
    # Setup logging configuration
    logging.basicConfig(filename=error_log_path, level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Check if the Queries.txt file exists
    if not os.path.isfile(queries_file_path):
        print(f"Error: The file '{queries_file_path}' does not exist.")
        return

    # Read queries from the file
    with open(queries_file_path, 'r') as file:
        queries = [line.strip() for line in file if line.strip()]

    total_listings = 5  # Default number of listings to scrape is 20-25 , dont exceed

    # Scrape for each query with error handling
    for query in queries:
        try:
            print(f"Scraping for query: {query}")
            scrape_google_maps(query, total_listings)
            time.sleep(5)  # 5-second gap between queries
        except Exception as e:
            # Log the error and continue with the next query
            logging.error(f"Error scraping for query '{query}': {e}")
            print(f"Error scraping for query '{query}'. Check error_log.txt for details.")

if __name__ == "__main__":
    main()
