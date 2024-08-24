import argparse
from scraper import scrape_google_maps

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--search", type=str, help="Search query for Google Maps")
    parser.add_argument("-t", "--total", type=int, default=20, help="Total number of listings to scrape (default: 20)")
    args = parser.parse_args()

    if not args.search:
        args.search = input("Enter the search query (e.g., 'restaurant in delhi'): ")

    scrape_google_maps(args.search, args.total)

if __name__ == "__main__":
    main()
