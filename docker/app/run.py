import asyncio
import logging
from scraper import scrape_data, extract_listing, extract_listing_elements, navigate_with_retry
from utils import get_search_list, save_data, update_query_file, merge_excel_files, parse_coordinates
from playwright.async_api import async_playwright
import time
import data  # Ensure this is imported

# Configure logging
logging.basicConfig(filename='error_log.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

async def main():
    try:
        search_list = await get_search_list()
        total = 20  # Can set up to 150, 20-25 Recommended

        async with async_playwright() as p:
            start_time = time.time()
            browser = await p.chromium.launch(headless=True, args=['--lang=en-US', '--disable-gpu', '--disable-dev-shm-usage'])
            page = await browser.new_page()

            # Set viewport size to reduce rendering load
            await page.set_viewport_size({"width": 1280, "height": 800})

            # Disable image loading and other unnecessary resources
            await page.route("**/*", lambda route: route.continue_() if route.request.resource_type not in ["image", "media", "font"] else route.abort())

            await page.goto("https://www.google.com/maps?hl=en", timeout=60000)
            await page.wait_for_selector('//input[@id="searchboxinput"]', timeout=5000)

            for search_for in search_list:
                try:
                    print(f"------ {search_for} ------")
                    await page.locator('//input[@id="searchboxinput"]').fill(search_for)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(500)
                    
                    await page.wait_for_selector('//a[contains(@href, "https://www.google.com/maps/place")]', timeout=10000)

                    listings = await scrape_data(page, total)
                    print(f'Processing on: {listings}')
                    await extract_listing(page, listings)
                    await extract_listing_elements()
                    parse_coordinates()
                    save_data(search_for)

                    # Clear data after saving
                    for key in data.data.keys():
                        data.data[key].clear()

                except Exception as e:
                    logging.error(f"Error processing search '{search_for}': {e}")
                    logging.error(f"Skipping and removing '{search_for}'")
                    update_query_file(search_for)  # Remove the problematic line

            end_time = time.time()
            print(f"Scraping took {(end_time - start_time) / 60:.2f} minutes.")

            if len(search_list) > 1:
                merge_excel_files()

            print("Scraping completed successfully.")

    except Exception as e:
        logging.error(f"An error occurred in the main process: {e}")

if __name__ == "__main__":
    asyncio.run(main())