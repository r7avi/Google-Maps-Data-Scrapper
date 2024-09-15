import asyncio
from scraper import scrape_data, extract_listing, extract_listing_elements
from utils import get_search_list, save_data, merge_excel_files, parse_coordinates
from playwright.async_api import async_playwright
import time
import data

async def main():
    try:
        search_list = await get_search_list()
        total = 25  # Can set upto 150, 120 Recommanded

        async with async_playwright() as p:
            start_time = time.time()
            browser = await p.chromium.launch(headless=True, args=['--lang=en-US'])
            page = await browser.new_page()
            await page.goto("https://www.google.com/maps?hl=en", timeout=60000)
            await page.wait_for_timeout(5000)

            for search_for in search_list:
                print(f"------ {search_for} ------")
                await page.locator('//input[@id="searchboxinput"]').fill(search_for)
                await page.wait_for_timeout(3000)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(4000)
                await page.hover('//a[contains(@href, "https://www.google.com/maps/place")]')

                listings = await scrape_data(page, total)
                print(f'Processing on: {listings}')
                await extract_listing(page, listings)
                await extract_listing_elements()
                parse_coordinates()
                save_data(search_for)

                # Clear data after saving
                for key in data.data.keys():
                    data.data[key].clear()

            end_time = time.time()
            print(f"Scraping took {(end_time - start_time) / 60:.2f} minutes.")

            if len(search_list) > 1:
                merge_excel_files()

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
