import asyncio
import logging
from scraper import scrape_data, extract_listing, extract_listing_elements
from utils import get_search_list, save_data, merge_excel_files, parse_coordinates
from playwright.async_api import async_playwright
import time
import data

# Configure logging
logging.basicConfig(filename='error_log.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

async def main():
    try:
        search_list = await get_search_list()
        total = 25  # Can set up to 150, 120 Recommended

        async with async_playwright() as p:
            start_time = time.time()
            browser = await p.chromium.launch(executable_path='C:\Program Files\Google\Chrome\Application\chrome.exe',headless=False, args=['--lang=en-US'])           
            page = await browser.new_page()
            await page.goto("https://www.google.com/maps?hl=en", timeout=60000)
            await page.wait_for_timeout(3000)

            for search_for in search_list:
                try:
                    print(f"------ {search_for} ------")
                    await page.locator('//input[@id="searchboxinput"]').fill(search_for)
                    await page.wait_for_timeout(3000)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(3000)                    
                 ## await page.hover('//a[contains(@href, "https://www.google.com/maps/place")]') - removed as it was causing issues
                    await page.wait_for_selector('//a[contains(@href, "https://www.google.com/maps/place")]') # Added to wait for the element to appear


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
                    continue  # Skip to the next task

            end_time = time.time()
            print(f"Scraping took {(end_time - start_time) / 60:.2f} minutes.")

            if len(search_list) > 1:
                merge_excel_files()

    except Exception as e:
        logging.error(f"An error occurred in the main process: {e}")

if __name__ == "__main__":
    asyncio.run(main())
