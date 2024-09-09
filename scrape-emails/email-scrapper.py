import pandas as pd
import re
import asyncio
from playwright.async_api import async_playwright
import tkinter as tk
from tkinter import filedialog
import traceback
import os
from urllib.parse import urljoin

async def scrape_emails_from_page(page):
    try:
        content = await page.content()
        from lxml import html
        tree = html.fromstring(content)
        page_text = tree.text_content()
        
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = set(re.findall(email_regex, page_text))
        
        valid_emails = set()
        for email in emails:
            if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                valid_emails.add(email)
        
        return valid_emails
    except Exception as e:
        return set()

async def scrape_emails_from_contact_page(browser, href, base_url):
    contact_emails = set()
    try:
        # Create a new browser context and page for the contact link
        context = await browser.new_context()
        page = await context.new_page()
        
        # Convert href to absolute URL if it's relative
        if not href.startswith(('http://', 'https://')):
            href = urljoin(base_url, href)
        
        try:
            await page.goto(href, wait_until='networkidle')
            emails = await scrape_emails_from_page(page)
            if emails:
                contact_emails.update(emails)
        except Exception as e:
            print(f"Error navigating to contact link {href}: {e}")
            with open('error_log.txt', 'a') as log_file:
                log_file.write(f"Error navigating to contact link {href}: {e}\n")
        finally:
            await page.close()
            await context.close()
    except Exception as e:
        print(f"Error processing contact link: {e}")
        with open('error_log.txt', 'a') as log_file:
            log_file.write(f"Error processing contact link: {e}\n")
    
    return contact_emails

async def process_website(url, browser):
    try:
        # Create a new browser context and page for the main website
        context = await browser.new_context()
        page = await context.new_page()
        
        await page.goto(url, wait_until='networkidle')
        
        main_page_emails = await scrape_emails_from_page(page)
        
        contact_page_emails = set()
        contact_links = await page.query_selector_all('a')
        
        for link in contact_links:
            try:
                link_text = await link.text_content()
                href = await link.get_attribute('href')
                
                if href and 'contact' in link_text.lower():
                    contact_emails = await scrape_emails_from_contact_page(browser, href, url)
                    if contact_emails:
                        contact_page_emails.update(contact_emails)
            except Exception as e:
                print(f"Error processing contact link: {e}")
                with open('error_log.txt', 'a') as log_file:
                    log_file.write(f"Error processing contact link: {e}\n")
        
        all_emails = main_page_emails.union(contact_page_emails)
        if all_emails:
            return ', '.join(all_emails)
        else:
            return ''  # Return empty string if no emails found
    except Exception as e:
        print(f"Error processing website {url}: {e}")
        with open('error_log.txt', 'a') as log_file:
            log_file.write(f"Error processing website {url}: {e}\n")
        return ''  # Return empty string in case of error
    finally:
        await page.close()
        await context.close()

async def main():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    
    input_file = filedialog.askopenfilename(
        title="Select CSV File",
        filetypes=[("CSV files", "*.csv")]
    )
    
    if not input_file:
        print("No file selected. Exiting.")
        return
    
    print(f"Selected file: {input_file}")

    try:
        df = pd.read_csv(input_file)
        print("CSV file read successfully.")
        
        if 'Website' not in df.columns:
            raise ValueError("The 'Website' column is missing from the CSV file.")
        
        df = df.dropna(subset=['Website'])
        df['Website'] = df['Website'].apply(lambda url: 'https://' + url if not url.startswith('https://') else url)
        
        print(f"Found {len(df)} valid website links. Starting scraping...")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=False,  # Show browser window
                executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe'  # Path to Chrome executable
            )
            
            results = []
            for url in df['Website']:
                result = await process_website(url, browser)
                results.append(result)
            
            await browser.close()
        
        df['Email'] = results
        
        columns = list(df.columns)
        website_index = columns.index('Website')
        columns.insert(website_index + 1, columns.pop(columns.index('Email')))
        df = df[columns]
        
        base_name, ext = os.path.splitext(input_file)
        output_file = f"{base_name}_email_scrapped{ext}"
        
        df.to_csv(output_file, index=False)
        print(f"Scraping complete. Results saved to {output_file}")

    except Exception as e:
        error_message = f"An error occurred: {str(e)}\n{traceback.format_exc()}"
        print(error_message)
        with open('error_log.txt', 'a') as log_file:
            log_file.write(error_message + '\n')

    print("Press Enter to exit...")
    input()

# Run the main function using asyncio
asyncio.run(main())
