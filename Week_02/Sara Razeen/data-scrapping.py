# # ==============================
# # Saya Product Scraper → Google Sheets
# # ==============================

# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.by import By
# import pandas as pd
# import time
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials

# # ------------------------------
# # Selenium setup
# # ------------------------------
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')  # Run in background
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')
# chrome_options.add_argument('--disable-gpu')

# driver = webdriver.Chrome(
#     service=Service(ChromeDriverManager().install()), 
#     options=chrome_options
# )

# # ------------------------------
# # Open Saya collection page
# # ------------------------------
# url = "https://saya.pk/collections/saya-lawn-collection-printed-emrboirdered-stitched-ready-to-wear-418208121064"
# driver.get(url)
# time.sleep(5)  # Wait for page to load

# # ------------------------------
# # Scrape products
# # ------------------------------
# products = driver.find_elements(By.CLASS_NAME, "t4s-product-wrapper")

# data = []
# for product in products:
#     # Title
#     try:
#         title = product.find_element(By.CLASS_NAME, "t4s-product-title").text
#     except:
#         title = None

#     # Price
#     try:
#         price = product.find_element(By.CLASS_NAME, "money").text
#     except:
#         price = None

#     # Image
#     try:
#         image = product.find_element(By.TAG_NAME, "img").get_attribute("src")
#     except:
#         image = None

#     data.append({"Title": title, "Price": price, "Image": image})

# driver.quit()

# # ------------------------------
# # Save to pandas DataFrame
# # ------------------------------
# df = pd.DataFrame(data)
# print(df)

# # ------------------------------
# # Push to Google Sheets
# # ------------------------------
# scope = [
#     "https://spreadsheets.google.com/feeds",
#     "https://www.googleapis.com/auth/spreadsheets",
#     "https://www.googleapis.com/auth/drive.file",
#     "https://www.googleapis.com/auth/drive"
# ]

# # Replace with your JSON file path
# creds = ServiceAccountCredentials.from_json_keyfile_name(
#     r"C:\Users\Sara Razeen\Desktop\ML-DL\datacollection-470220-5f31625f6b01.json",
#     scope
# )
# client = gspread.authorize(creds)

# # Replace with your Google Sheet URL
# sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1Ve04OMh2IssDDiBBRWVGP82dvHrJOlGIM-XI5XdgoKc/edit?gid=0#gid=0")
# worksheet = sheet.sheet1

# worksheet.clear()  # Clear old data
# worksheet.update([df.columns.values.tolist()] + df.values.tolist())

# print("✅ Data uploaded to Google Sheet successfully!")






# Saya Multi-Collection Scraper 


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ------------------------------
# Selenium setup
# ------------------------------
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')  # Run in background
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), 
    options=chrome_options
)

# ------------------------------
# Collection URLs
# ------------------------------
urls = [
    "https://saya.pk/collections/saya-lawn-collection-printed-emrboirdered-stitched-ready-to-wear-418208121064",
    "https://saya.pk/collections/unstitched-shirt-dupatta-collection-412870082792",
    "https://saya.pk/collections/summer-lawn-25-printed-427798364392",
    "https://saya.pk/collections/us-3-pcs-jacquard-dupatta-1-437033500904",
    "https://saya.pk/collections/ready-to-wear-stitched-shirt-trouser-coords-collection-436240777448"
]

all_data = []

# ------------------------------
# Scrape all collections
# ------------------------------
for url in urls:
    driver.get(url)
    time.sleep(5)  # Wait for page to load

    # Scroll to bottom to load all products (if lazy-loaded)
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for new products to load
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    products = driver.find_elements(By.CLASS_NAME, "t4s-product-wrapper")

    for product in products:
        # Title
        try:
            title = product.find_element(By.CLASS_NAME, "t4s-product-title").text
        except:
            title = None

        # Price
        try:
            price = product.find_element(By.CLASS_NAME, "money").text
        except:
            price = None

        # Image
        try:
            image = product.find_element(By.TAG_NAME, "img").get_attribute("src")
        except:
            image = None

        all_data.append({"Title": title, "Price": price, "Image": image})

driver.quit()

# ------------------------------
# Save to pandas DataFrame
# ------------------------------
df = pd.DataFrame(all_data)
print(df)

# ------------------------------
# Push to Google Sheets
# ------------------------------
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    r"C:\Users\Sara Razeen\Desktop\ML-DL\datacollection-470220-5f31625f6b01.json",
    scope
)
client = gspread.authorize(creds)

sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1Ve04OMh2IssDDiBBRWVGP82dvHrJOlGIM-XI5XdgoKc/edit#gid=0")
worksheet = sheet.sheet1

worksheet.clear()  # Clear old data
worksheet.update([df.columns.values.tolist()] + df.values.tolist())

print("✅ Data from all collections uploaded successfully!")
