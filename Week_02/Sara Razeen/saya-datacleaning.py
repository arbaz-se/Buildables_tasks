# tried data cleaning and preprocessing using datatype chacking, encording exctract quantity from embeded words

# import re
# import pandas as pd
# import time
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC


# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')
# chrome_options.add_argument('--disable-gpu')

# driver = webdriver.Chrome(
#     service=Service(ChromeDriverManager().install()), 
#     options=chrome_options
# )
# wait = WebDriverWait(driver, 15)

# def scrape_collection(search_term, collection_type):
#     all_data = []

#     driver.get("https://saya.pk/")
#     wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".mysearch"))).click()

#     search_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.t4s-mini-search__input")))
#     search_input.send_keys(search_term)
#     search_input.send_keys(Keys.ENTER)

#     wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "t4s-product-wrapper")))

#     for _ in range(30):
#         driver.execute_script("window.scrollBy(0, 1200);")
#         time.sleep(1.5)

#     products = driver.find_elements(By.CLASS_NAME, "t4s-product-wrapper")

#     for i, product in enumerate(products, start=1):
#         try:
#             title_elem = product.find_element(By.CSS_SELECTOR, ".t4s-product-title a")
#             title = title_elem.text.strip()
#             link = title_elem.get_attribute("href")
#         except:
#             title, link = None, None

#         try:
#             price = product.find_element(By.CLASS_NAME, "money").text.strip()
#         except:
#             price = None

#         barcode, availability, available_qty = None, None, None
#         if link:
#             driver.execute_script("window.open(arguments[0]);", link)
#             driver.switch_to.window(driver.window_handles[1])
#             time.sleep(2)

#             try:
#                 barcode = driver.find_element(By.CSS_SELECTOR, ".t4s-barcode-value").text.strip()
#             except: pass

#             try:
#                 qty_text = driver.find_element(By.CSS_SELECTOR, ".t4s-available-value").text.strip()
#                 available_qty = qty_text
#             except: pass

#             try:
#                 instock_elem = driver.find_element(By.XPATH, "//p[contains(., 'IN STOCK')]")
#                 if instock_elem and "IN STOCK" in instock_elem.text.upper():
#                     availability = "In Stock"
#                 else:
#                     availability = "Out of Stock"
#             except:
#                 availability = "Out of Stock"

#             driver.close()
#             driver.switch_to.window(driver.window_handles[0])

#         all_data.append({
#             "Collection": collection_type,
#             "Title": title,
#             "Price": price,
#             "Barcode": barcode,
#             "Availability": availability,
#             "Available_Quantity": available_qty,
#             "Link": link
#         })
#         print(f" Scraped {i}/{len(products)} from {collection_type}")

#     return all_data


# stitched_data = scrape_collection("lawn stitched", "Stitched")
# unstitched_data = scrape_collection("lawn unstitched", "Unstitched")
# accessories_data = scrape_collection("accessories", "Accessories")
# men_data = scrape_collection("men", "Men Wear")
# kids_data = scrape_collection("kids", "Kidswear")

# driver.quit()

# all_data = stitched_data + unstitched_data + accessories_data + men_data + kids_data
# raw_df = pd.DataFrame(all_data)

# #pipeline


# def preprocess(df):
#     cleaned_df = df.copy()

#if not avaialable   
#     cleaned_df["Price"] = cleaned_df["Price"].astype(str).str.replace(",", "")
#     cleaned_df["Price"] = cleaned_df["Price"].apply(lambda x: re.sub(r"[^\d.]", "", x) if pd.notna(x) else None)
#     cleaned_df["Price"] = pd.to_numeric(cleaned_df["Price"], errors="coerce")

#Title Cleaning   
#     cleaned_df["Title"] = cleaned_df["Title"].str.strip().str.title()

#in stock=1 out of stock =0  
#     cleaned_df["Availability_Encoded"] = cleaned_df["Availability"].map({"In Stock": 1, "Out of Stock": 0})

#Extract Quantity the integer  
#     cleaned_df["Available_Quantity"] = cleaned_df["Available_Quantity"].str.extract(r"(\d+)").astype(float)

#     return cleaned_df


# cleaned_df = preprocess(raw_df)



# scope = [
#     "https://spreadsheets.google.com/feeds",
#     "https://www.googleapis.com/auth/spreadsheets",
#     "https://www.googleapis.com/auth/drive.file",
#     "https://www.googleapis.com/auth/drive"
# ]

# creds = ServiceAccountCredentials.from_json_keyfile_name(
#     r"C:\Users\Sara Razeen\Desktop\ML-DL\datacollection-470220-5f31625f6b01.json",
#     scope
# )
# client = gspread.authorize(creds)

# sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1z_RPfSl_yMdVw1EojvUi4a_UPWBhnF_IZScwiqZvPgA/edit?gid=0#gid=0")


# try:
#     raw_ws = sheet.worksheet("Uncleaned")
# except:
#     raw_ws = sheet.add_worksheet(title="Uncleaned", rows="1000", cols="20")
# raw_ws.clear()
# raw_ws.update([raw_df.columns.values.tolist()] + raw_df.fillna("").values.tolist())


# try:
#     clean_ws = sheet.worksheet("Cleaned")
# except:
#     clean_ws = sheet.add_worksheet(title="Cleaned", rows="1000", cols="20")
# clean_ws.clear()
# clean_ws.update([cleaned_df.columns.values.tolist()] + cleaned_df.fillna("").values.tolist())

# print("Saved to googlesheet")


import re
import pandas as pd
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), 
    options=chrome_options
)
wait = WebDriverWait(driver, 15)

def scrape_collection(search_term, collection_type):
    all_data = []

    driver.get("https://saya.pk/")
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".mysearch"))).click()

    search_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.t4s-mini-search__input")))
    search_input.send_keys(search_term)
    search_input.send_keys(Keys.ENTER)

    wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "t4s-product-wrapper")))

  
    for _ in range(30):
        driver.execute_script("window.scrollBy(0, 1200);")
        time.sleep(1.5)

    products = driver.find_elements(By.CLASS_NAME, "t4s-product-wrapper")

    for i, product in enumerate(products, start=1):
        try:
            title_elem = product.find_element(By.CSS_SELECTOR, ".t4s-product-title a")
            title = title_elem.text.strip()
            link = title_elem.get_attribute("href")
        except:
            title, link = None, None

        try:
            price = product.find_element(By.CLASS_NAME, "money").text.strip()
        except:
            price = None

        barcode, availability, available_qty = None, None, None
        if link:
            driver.execute_script("window.open(arguments[0]);", link)
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(2)

            try:
                barcode = driver.find_element(By.CSS_SELECTOR, ".t4s-barcode-value").text.strip()
            except: pass

            try:
                qty_text = driver.find_element(By.CSS_SELECTOR, ".t4s-available-value").text.strip()
                available_qty = qty_text
            except: pass

            try:
                instock_elem = driver.find_element(By.XPATH, "//p[contains(., 'IN STOCK')]")
                if instock_elem and "IN STOCK" in instock_elem.text.upper():
                    availability = "In Stock"
                else:
                    availability = "Out of Stock"
            except:
                availability = "Out of Stock"

            driver.close()
            driver.switch_to.window(driver.window_handles[0])

        all_data.append({
            "Collection": collection_type,
            "Title": title,
            "Price": price,
            "Barcode": barcode,
            "Availability": availability,
            "Available_Quantity": available_qty,
            "Link": link
        })
        print(f" Scraped {i}/{len(products)} from {collection_type}")

    return all_data

stitched_data = scrape_collection("lawn stitched", "Stitched")
unstitched_data = scrape_collection("lawn unstitched", "Unstitched")
accessories_data = scrape_collection("accessories", "Accessories")
men_data = scrape_collection("men", "Men Wear")
kids_data = scrape_collection("kids", "Kidswear")

driver.quit()


all_data = stitched_data + unstitched_data + accessories_data + men_data + kids_data
raw_df = pd.DataFrame(all_data)


def preprocess(df):
    cleaned_df = df.copy()

    
    cleaned_df = cleaned_df.fillna({
        "Title": "Not Available",
        "Price": "0",
        "Barcode": "Not Available",
        "Availability": "Out of Stock",
        "Available_Quantity": "0",
        "Link": "Not Available"
    })

  
    cleaned_df["Price"] = cleaned_df["Price"].astype(str).str.replace(",", "")
    cleaned_df["Price"] = cleaned_df["Price"].apply(lambda x: re.sub(r"[^\d.]", "", x) if pd.notna(x) else None)
    cleaned_df["Price"] = pd.to_numeric(cleaned_df["Price"], errors="coerce")
   
    cleaned_df["Title"] = cleaned_df["Title"].str.strip().str.title()

    cleaned_df["Availability"] = cleaned_df["Availability"].str.strip().str.title()
    cleaned_df["Availability"] = cleaned_df["Availability"].replace({"In Stock": "In Stock", "Out Of Stock": "Out of Stock"})

 
    cleaned_df = cleaned_df.drop_duplicates(subset=["Barcode", "Title"], keep="first")

    
    cleaned_df["Availability_Encoded"] = cleaned_df["Availability"].map({"In Stock": 1, "Out of Stock": 0})

   
    cleaned_df["Available_Quantity"] = cleaned_df["Available_Quantity"].astype(str).str.extract(r"(\d+)").astype(float)

    
    cleaned_df["Title_Word_Count"] = cleaned_df["Title"].apply(lambda x: len(str(x).split()))
    cleaned_df["Extracted_Collection"] = cleaned_df["Link"].apply(lambda x: x.split("/")[3] if isinstance(x, str) and "/" in x else "Unknown")

    
    cleaned_df = cleaned_df[cleaned_df["Price"] < 200000]  

    return cleaned_df

cleaned_df = preprocess(raw_df)


scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    r"C:\\Users\\Sara Razeen\\Desktop\\ML-DL\\datacollection-470220-5f31625f6b01.json",
    scope
)
client = gspread.authorize(creds)

sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1z_RPfSl_yMdVw1EojvUi4a_UPWBhnF_IZScwiqZvPgA/edit?gid=0#gid=0")


try:
    raw_ws = sheet.worksheet("Uncleaned")
except:
    raw_ws = sheet.add_worksheet(title="Uncleaned", rows="1000", cols="20")
raw_ws.clear()
raw_ws.update([raw_df.columns.values.tolist()] + raw_df.fillna("").values.tolist())


try:
    clean_ws = sheet.worksheet("Cleaned")
except:
    clean_ws = sheet.add_worksheet(title="Cleaned", rows="1000", cols="20")
clean_ws.clear()
clean_ws.update([cleaned_df.columns.values.tolist()] + cleaned_df.fillna("").values.tolist())

print("saved")
