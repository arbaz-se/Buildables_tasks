import pandas as pd
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--log-level=3")

service = Service("chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)

base_url = "https://www.zameen.com/Houses_Property/Islamabad_B_17_MPCHS___Multi_Gardens-3115-{}.html"
properties = []
max_pages = 20  # limit to 20 pages
page = 1

try:
    while page <= max_pages:
        url = base_url.format(page)
        driver.get(url)
        print(f"\nScraping page {page}...")

        wait = WebDriverWait(driver, 10)
        try:
            cards = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div._52d0f124")))
        except:
            print(f"No listings found on page {page}. Stopping...")
            break

        for card in cards:
            try:
                title = card.find_element(By.XPATH, ".//ancestor::li//a[@class='d870ae17']").get_attribute("title")
            except:
                title = None

                    
            try:
    # Get price using full XPath
                price = card.find_element(By.XPATH, ".//ancestor::li//span[@aria-label='Price']").text.strip()
            except:
                price = None

 

            try:
                area = card.find_element(By.CSS_SELECTOR, 'span[aria-label="Area"] span').text.strip()
            except:
                area = None

            try:
                beds = card.find_element(By.CSS_SELECTOR, 'span[aria-label="Beds"]').text.strip()
            except:
                beds = None

            try:
                baths = card.find_element(By.CSS_SELECTOR, 'span[aria-label="Baths"]').text.strip()
            except:
                baths = None

            try:
                location = card.find_element(By.CSS_SELECTOR, 'div[aria-label="Location"]').text.strip()
            except:
                location = None

            listing = {
                "Title": title,
                "Price": price,
                "Area": area,
                "Bedrooms": beds,
                "Bathrooms": baths,
                "Location": location
            }

            # Add to list
            properties.append(listing)

            # Print to terminal
            print(listing)

        page += 1
        time.sleep(1)  # Polite delay

finally:
    driver.quit()

# Save to CSV
df = pd.DataFrame(properties)
df.to_csv("zameen_listings.csv", index=False)
print("\nData saved to zameen_listings.csv")

# Save to JSON
with open("zameen_listings.json", "w", encoding="utf-8") as f:
    json.dump(properties, f, ensure_ascii=False, indent=4)
print("Data saved to zameen_listings.json")

print(f"Total listings scraped: {len(properties)}")