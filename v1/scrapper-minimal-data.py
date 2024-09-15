## change run.py and main.py accorodingly to use scrapper-minimal-data.py

from playwright.sync_api import sync_playwright
import pandas as pd
import os

def extract_data(xpath, data_list, page):
    if page.locator(xpath).count() > 0:
        data = page.locator(xpath).inner_text()
    else:
        data = ""
    data_list.append(data)

def scrape_google_maps(search_for, total):
    names_list = []
    address_list = []
    plus_code_list = []  # List for Plus Codes
    website_list = []
    phones_list = []
    reviews_c_list = []
    place_t_list = []

    # Define the directory for saving the file
    folder = 'Scrapped'
    if not os.path.exists(folder):
        os.makedirs(folder)

    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path='C:\Program Files\Google\Chrome\Application\chrome.exe', headless=False)
        page = browser.new_page()

        page.goto("https://www.google.com/maps/@32.9817464,70.1930781,3.67z?", timeout=60000)
        page.wait_for_timeout(5000)

        page.locator('//input[@id="searchboxinput"]').fill(search_for)
        page.keyboard.press("Enter")
        page.wait_for_selector('//a[contains(@href, "https://www.google.com/maps/place")]')

        page.hover('//a[contains(@href, "https://www.google.com/maps/place")]')

        unique_urls = set()
        previously_counted = 0

        while True:
            page.mouse.wheel(0, 10000)
            page.wait_for_timeout(2000)
            page.mouse.wheel(0, 10000)
            page.wait_for_timeout(2000)
            page.wait_for_selector('//a[contains(@href, "https://www.google.com/maps/place")]')

            listings = page.locator('//a[contains(@href, "https://www.google.com/maps/place")]').all()
            for listing in listings:
                href = listing.get_attribute('href')
                unique_urls.add(href)

            if len(unique_urls) >= total:
                print(f"Total Unique URLs Found: {len(unique_urls)}")
                break
            else:
                if len(unique_urls) == previously_counted:
                    print(f"Arrived at all available\nTotal Unique URLs Found: {len(unique_urls)}")
                    break
                else:
                    previously_counted = len(unique_urls)
                    print(f"Currently Found: {len(unique_urls)}")

        unique_urls = list(unique_urls)[:total]

        for url in unique_urls:
            page.goto(url, timeout=60000)
            page.wait_for_selector('//div[@class="TIHn2 "]//h1[@class="DUwDvf lfPIob"]')

            name_xpath = '//div[@class="TIHn2 "]//h1[@class="DUwDvf lfPIob"]'
            address_xpath = '//button[@data-item-id="address"]//div[contains(@class, "fontBodyMedium")]'
            plus_code_xpath = '//div[@class="rogA2c "]//div[contains(@class, "Io6YTe") and contains(text(), "+")]'            
            website_xpath = '//a[@data-item-id="authority"]//div[contains(@class, "fontBodyMedium")]'
            phone_number_xpath = '//button[contains(@data-item-id, "phone:tel:")]//div[contains(@class, "fontBodyMedium")]'
            reviews_count_xpath = '//div[@class="TIHn2 "]//div[@class="fontBodyMedium dmRWX"]//div//span//span//span[@aria-label]'
            place_type_xpath = '//div[@class="LBgpqf"]//button[@class="DkEaL "]'
          
            extract_data(name_xpath, names_list, page)
            extract_data(address_xpath, address_list, page)
            extract_data(plus_code_xpath, plus_code_list, page)  # Extracting Plus Code
            extract_data(website_xpath, website_list, page)
            extract_data(phone_number_xpath, phones_list, page)
            extract_data(place_type_xpath, place_t_list, page)

            if page.locator(reviews_count_xpath).count() > 0:
                temp = page.locator(reviews_count_xpath).inner_text().replace('(','').replace(')','').replace(',','')
                reviews_c_list.append(int(temp))
            else:
                reviews_c_list.append("")

        df = pd.DataFrame(list(zip(names_list, website_list, phones_list, address_list, plus_code_list, reviews_c_list, place_t_list)),
                          columns=['Names', 'Website', 'Phone Number', 'Address', 'Plus Code', 'Review Count', 'Type'])
        
        # Save file in the 'Scrapped' folder with the search term as the filename
        search_term = search_for.replace(' ', '_')
        file_path = os.path.join(folder, f'{search_term}_results.csv')
        df.to_csv(file_path, index=False)
        browser.close()
        print(df.head())
