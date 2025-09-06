# import time
# import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials

# # Google Sheets Setup 
# SERVICE_ACCOUNT_FILE = "datacollection-470220-5f31625f6b01.json"
# SHEET_ID = "1BUtcvyn-TYoCm0ZzTLY5ITW1gcgAp1J8byOL143r0Wg"

# def connect_google_sheet():
#     scope = ["https://spreadsheets.google.com/feeds",
#              "https://www.googleapis.com/auth/drive"]
#     creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, scope)
#     client = gspread.authorize(creds)
#     sheet = client.open_by_key(SHEET_ID).sheet1
#     return sheet

# # Selenium Setup 
# def setup_driver():
#     options = Options()
#     # options.add_argument("--headless")  # Uncomment to run headless
#     options.add_argument("--window-size=1920,1080")
#     service = Service(ChromeDriverManager().install())
#     driver = webdriver.Chrome(service=service, options=options)
#     return driver

# # Extract GenAI Papers 
# def get_genai_papers(driver):
#     driver.get("https://www.sciencedirect.com/")

#     #  Accept cookies if popup appears 
#     try:
#         accept_btn = WebDriverWait(driver, 5).until(
#             EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
#         )
#         accept_btn.click()
#         time.sleep(1)
#     except:
#         print("No cookie popup found, continuing...")

#     #  Wait for search box 
#     search_box = WebDriverWait(driver, 15).until(
#         EC.element_to_be_clickable((By.ID, "qs"))
#     )
#     search_box.clear()
#     search_box.send_keys("GenAI")
#     search_box.send_keys(Keys.RETURN)
#     time.sleep(3)

#     # --- Filter by year 2025 using class "checkbox-label-value" ---
#     try:
#         filters = WebDriverWait(driver, 10).until(
#             EC.presence_of_all_elements_located((By.CLASS_NAME, "checkbox-label-value"))
#         )
#         for f in filters:
#             if "2025" in f.text:  # matches "2025 (761)"
#                 driver.execute_script("arguments[0].scrollIntoView(true);", f)
#                 f.click()
#                 time.sleep(2)
#                 break
#     except:
#         print("Could not apply year filter. Proceeding without it.")

#     # --- Extract titles and highlights ---
#     papers_data = []
#     papers = driver.find_elements(By.XPATH, "//div[contains(@class,'result-item-content')]")
#     for paper in papers[:20]:  # limit for demo
#         try:
#             title = paper.find_element(By.CLASS_NAME, "title-text").text
#         except:
#             title = "No Title"
#         try:
#             highlight = paper.find_element(By.CLASS_NAME, "abstract.author-highlights").text
#         except:
#             highlight = "No Highlights"
#         papers_data.append([title, highlight])
#     return papers_data

# # --- Save to Google Sheet ---
# def save_to_sheet(sheet, data):
#     for row in data:
#         sheet.append_row(row)

# # --- Main Workflow ---
# def main():
#     sheet = connect_google_sheet()
#     driver = setup_driver()
#     try:
#         papers = get_genai_papers(driver)
#         save_to_sheet(sheet, papers)
#         print(f"✅ Saved {len(papers)} GenAI papers to Google Sheet successfully!")
#     finally:
#         driver.quit()

# if __name__ == "__main__":
#     main()

import time
import gspread
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from oauth2client.service_account import ServiceAccountCredentials


SERVICE_ACCOUNT_FILE = "datacollection-470220-5f31625f6b01.json"   
SHEET_ID = "1BUtcvyn-TYoCm0ZzTLY5ITW1gcgAp1J8byOL143r0Wg"          


def setup_gsheet(clear_first=True):
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, scope)
    client = gspread.authorize(creds)

    sheet = client.open_by_key(SHEET_ID).sheet1

    if clear_first:  
        sheet.clear()
        
        sheet.append_row(["Title", "First Reference", "URL"])

    return sheet


def setup_driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])  # suppress Chrome logs
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver


def scrape_paper(driver, url):
    driver.get(url)
    time.sleep(3)


    try:
        title = driver.find_element(By.CSS_SELECTOR, "h1").text.strip()
    except:
        title = "N/A"

# First reference 
    try:
        first_ref = driver.find_element(By.CSS_SELECTOR, ".reference").text.strip()
    except:
        first_ref = "N/A"

    return [title, first_ref, url]


def main():
    sheet = setup_gsheet(clear_first=True)
    driver = setup_driver()

 
    search_url = "https://www.sciencedirect.com/search?qs=genAI&years=2025"
    driver.get(search_url)
    time.sleep(5)


    paper_links = []
    articles = driver.find_elements(By.CSS_SELECTOR, "a.result-list-title-link")
    for a in articles[:20]: 
        href = a.get_attribute("href")
        if href:
            paper_links.append(href)

    print(f"Found {len(paper_links)} papers (limited to 50)")


    all_data = []
    for link in paper_links:
        data = scrape_paper(driver, link)
        all_data.append(data)

 
    sheet.append_rows(all_data, value_input_option="RAW")

    print("stored in sheet")
    driver.quit()


if __name__ == "__main__":
    main()
