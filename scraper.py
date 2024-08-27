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
    plus_code_list = []  # New list for Plus Code
    website_list = []
    phones_list = []
    reviews_c_list = []
    reviews_a_list = []
    store_s_list = []
    in_store_list = []
    store_del_list = []
    place_t_list = []
    open_list = []
    intro_list = []

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

        # Scraping data from each unique URL
        for url in unique_urls:
            page.goto(url, timeout=60000)
            page.wait_for_selector('//div[@class="TIHn2 "]//h1[@class="DUwDvf lfPIob"]')

            name_xpath = '//div[@class="TIHn2 "]//h1[@class="DUwDvf lfPIob"]'
            address_xpath = '//button[@data-item-id="address"]//div[contains(@class, "fontBodyMedium")]'
            plus_code_xpath = '//div[@class="rogA2c "]//div[contains(@class, "Io6YTe") and contains(text(), "+")]' 
            website_xpath = '//a[@data-item-id="authority"]//div[contains(@class, "fontBodyMedium")]'
            phone_number_xpath = '//button[contains(@data-item-id, "phone:tel:")]//div[contains(@class, "fontBodyMedium")]'
            reviews_count_xpath = '//div[@class="TIHn2 "]//div[@class="fontBodyMedium dmRWX"]//div//span//span//span[@aria-label]'
            reviews_average_xpath = '//div[@class="TIHn2 "]//div[@class="fontBodyMedium dmRWX"]//div//span[@aria-hidden]'
            info1 = '//div[@class="LTs0Rc"][1]'
            info2 = '//div[@class="LTs0Rc"][2]'
            info3 = '//div[@class="LTs0Rc"][3]'
            opens_at_xpath = '//button[contains(@data-item-id, "oh")]//div[contains(@class, "fontBodyMedium")]'
            opens_at_xpath2 = '//div[@class="MkV9"]//span[@class="ZDu9vd"]//span[2]'
            place_type_xpath = '//div[@class="LBgpqf"]//button[@class="DkEaL "]'
            intro_xpath = '//div[@class="WeS02d fontBodyMedium"]//div[@class="PYvSYb "]'
          
            if page.locator(intro_xpath).count() > 0:
                Introduction = page.locator(intro_xpath).inner_text()
                intro_list.append(Introduction)
            else:
                intro_list.append("None Found")
            
            if page.locator(reviews_count_xpath).count() > 0:
                temp = page.locator(reviews_count_xpath).inner_text().replace('(','').replace(')','').replace(',','')
                Reviews_Count = int(temp)
                reviews_c_list.append(Reviews_Count)
            else:
                reviews_c_list.append("")

            if page.locator(reviews_average_xpath).count() > 0:
                temp = page.locator(reviews_average_xpath).inner_text().replace(' ','').replace(',','.')
                Reviews_Average = float(temp)
                reviews_a_list.append(Reviews_Average)
            else:
                reviews_a_list.append("")

            if page.locator(info1).count() > 0:
                temp = page.locator(info1).inner_text().split('·')
                check = temp[1].replace("\n","")
                if 'shop' in check:
                    store_s_list.append("Yes")
                elif 'pickup' in check:
                    in_store_list.append("Yes")
                elif 'delivery' in check:
                    store_del_list.append("Yes")
            else:
                store_s_list.append("No")

            if page.locator(info2).count() > 0:
                temp = page.locator(info2).inner_text().split('·')
                check = temp[1].replace("\n","")
                if 'pickup' in check:
                    in_store_list.append("Yes")
                elif 'shop' in check:
                    store_s_list.append("Yes")
                elif 'delivery' in check:
                    store_del_list.append("Yes")
            else:
                in_store_list.append("No")
            
            if page.locator(info3).count() > 0:
                temp = page.locator(info3).inner_text().split('·')
                check = temp[1].replace("\n","")
                if 'Delivery' in check:
                    store_del_list.append("Yes")
                elif 'pickup' in check:
                    in_store_list.append("Yes")
                elif 'shop' in check:
                    store_s_list.append("Yes")
            else:
                store_del_list.append("No")
            
            if page.locator(opens_at_xpath).count() > 0:
                opens = page.locator(opens_at_xpath).inner_text().split('⋅')
                if len(opens) != 1:
                    opens = opens[1]
                else:
                    opens = page.locator(opens_at_xpath).inner_text()
                open_list.append(opens.replace("\u202f",""))
            else:
                open_list.append("")

            if page.locator(opens_at_xpath2).count() > 0:
                opens = page.locator(opens_at_xpath2).inner_text().split('⋅')[1].replace("\u202f","")
                open_list.append(opens)

            extract_data(name_xpath, names_list, page)
            extract_data(address_xpath, address_list, page)
            extract_data(plus_code_xpath, plus_code_list, page)  # Extracting Plus Code
            extract_data(website_xpath, website_list, page)
            extract_data(phone_number_xpath, phones_list, page)
            extract_data(place_type_xpath, place_t_list, page)

        df = pd.DataFrame(list(zip(names_list, website_list, intro_list, phones_list, address_list, reviews_c_list, reviews_a_list, store_s_list, in_store_list, store_del_list, place_t_list, open_list)),
                          columns=['Names','Website','Introduction','Phone Number','Address','Review Count','Average Review Count','Store Shopping','In Store Pickup','Delivery','Type','Opens At'])
        
        # Save file in the 'Scrapped' folder with the search term as the filename
        search_term = search_for.replace(' ', '_')
        file_path = os.path.join(folder, f'{search_term}_results.csv')
        df.to_csv(file_path, index=False)
        browser.close()
        print(df.head())
