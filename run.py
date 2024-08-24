from scraper import scrape_google_maps
import os

def main():
    # Define the path to the Queries.txt file
    file_path = 'Queries.txt'
    
    # Check if the file exists
    if not os.path.isfile(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        return

    # Read queries from the file
    with open(file_path, 'r') as file:
        queries = [line.strip() for line in file if line.strip()]
    
    total_listings = 500  # Default number of listings to scrape

    # Scrape for each query
    for query in queries:
        print(f"Scraping for query: {query}")
        scrape_google_maps(query, total_listings)

if __name__ == "__main__":
    main()
