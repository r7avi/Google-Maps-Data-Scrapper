from playwright.async_api import async_playwright
from tqdm.asyncio import tqdm
from playwright_helpers import get_element_text, get_element_attribute
import data
import random

async def scrape_data(page, total): 
    try:
        listings = await page.locator('//a[contains(@href, "https://www.google.com/maps/place")]').count()
        print(f'Found: {listings}')
        previous_listings = listings
        scroll_attempts = 0
        max_scroll_attempts = 10  # Maximum number of scroll attempts before giving up

        while listings < total and scroll_attempts < max_scroll_attempts:
            await page.mouse.wheel(0, 10000)
            await page.wait_for_timeout(500)
            listings = await page.locator('//a[contains(@href, "https://www.google.com/maps/place")]').count()
            print(f'Scrolled to: {listings}')
            
            if listings == previous_listings:
                scroll_attempts += 1
                if await page.locator('//p[@class="fontBodyMedium "]//span[text()="You\'ve reached the end of the list."]').count() > 0:
                    print("You've reached the end of the search query.")
                    break
                elif scroll_attempts >= max_scroll_attempts:
                    print(f"No new listings found after {max_scroll_attempts} attempts. Moving to the next search query.")
                    break
                else:
                    inside_listings = await page.locator('//a[contains(@href, "https://www.google.com/maps/place")]').all()
                    if inside_listings:
                        click_index = max(0, listings - 3)
                        await inside_listings[click_index].click()
                        print(f'Clicked on: {click_index}')
                        await page.wait_for_timeout(500)
            else:
                scroll_attempts = 0  # Reset scroll attempts if new listings are found
            
            previous_listings = listings

        return min(listings, total)
    except Exception as e:
        print(f"An error occurred during scraping: {e}")
        return 0


async def navigate_with_retry(page, url, retries=1):  # Change retries to 1
    for attempt in range(retries):
        try:
            await page.goto(url, timeout=120000)
            await page.wait_for_load_state("networkidle")
            return True  # Success
        except Exception as e:
            print(f"Attempt {attempt + 1} failed for {url}: {e}")
            if attempt == retries - 1:
                return False  # Failed after retries



async def extract_listing(page, listings):
    try:
        glink_by_xpath = await page.locator('//a[contains(@href, "https://www.google.com/maps/place")]').all()
        for glink in tqdm(glink_by_xpath[:listings]):
            data.data['glinks'].append(await glink.get_attribute('href') if glink else None)
    except Exception as e:
        print(f"An error occurred during listing extraction: {e}")

async def extract_listing_elements():
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True, args=['--lang=en-US', '--disable-dev-shm-usage', '--no-sandbox'])
            page = await browser.new_page()
            failed_links = []  # List to store unresponsive links

            # Set viewport size to reduce rendering load
            await page.set_viewport_size({"width": 1280, "height": 800})

            # Disable image loading and other unnecessary resources
            await page.route("**/*", lambda route: route.continue_() if not route.request.resource_type in ["image", "media", "font"] else route.abort())

            
            for glink in tqdm(data.data['glinks']):
                success = await navigate_with_retry(page, glink)
                if success:
                    await page.wait_for_timeout(3000)
                    # Proceed with data extraction
                    data.data['links'].append(page.url)
                    data.data['names'].append(await get_element_text(page, '//div[@style="padding-bottom: 4px;"]//h1'))
                    data.data['type'].append(await get_element_text(page, '//div[@class="LBgpqf"]//button[@class="DkEaL "]'))
                    data.data['plus_code'].append(await get_element_text(page, '//button[contains(@aria-label, "Plus code:")]//div[contains(@class, "Io6YTe") and contains(@class, "fontBodyMedium")]'))
                    data.data['rates'].append(await get_element_text(page, '//div[@style="padding-bottom: 4px;"]//div[contains(@jslog,"mutable:true;")]/span[1]/span[1]'))
                    data.data['addresses'].append(await get_element_text(page, '//button[@data-item-id="address"]//div[contains(@class, "fontBodyMedium")]'))
                    data.data['websites'].append(await get_element_attribute(page, '//a[@data-value="Open website"]', 'href'))
                    data.data['phones'].append(await get_element_text(page, '//button[contains(@data-item-id, "phone:tel:")]//div[contains(@class, "fontBodyMedium")]'))
                    review = await get_element_text(page, '//div[@style="padding-bottom: 4px;"]//div[contains(@jslog,"mutable:true;")]/span[2]')
                    data.data['reviews_count'].append(review.replace(',', '').replace('(', '').replace(')', '').strip())
                    await page.wait_for_timeout(500)
                else:
                    # Log the failed link
                    failed_links.append(glink)
                    print(f"Skipped unresponsive link: {glink}")

            # After processing, log all failed links
            if failed_links:
                with open("failed_links.log", "a") as log_file:
                    for link in failed_links:
                        log_file.write(link + "\n")
                print(f"Logged {len(failed_links)} failed links to 'failed_links.log'.")

            await browser.close()
    except Exception as e:
        print(f"An error occurred during element extraction: {e}")
