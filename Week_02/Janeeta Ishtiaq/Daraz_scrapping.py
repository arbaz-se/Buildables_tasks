from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.daraz.pk/#?")
wait = WebDriverWait(driver, 10)
search = wait.until(EC.element_to_be_clickable((By.ID, "q")))
search.send_keys("Keyboard", Keys.ENTER)
all_products = []
for page in range(1, 6):
    print(f"\n--- Page {page} ---")
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-qa-locator='product-item']")))

    products = driver.find_elements(By.CSS_SELECTOR, "div[data-qa-locator='product-item']")
    print(f"{len(products)} products found")

    for p in products:
        try:
            title = p.find_element(By.CSS_SELECTOR, "div.RfADt a").get_attribute("title")
        except:
            title = "N/A"

        try:
            price = p.find_element(By.CSS_SELECTOR, "div.aBrP0 span").text
        except:
            price = "N/A"

        all_products.append({"Title": title, "Price": price})
        print(f"{title} | {price}")

    try:
        next_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "li.ant-pagination-next"))
        )
        driver.execute_script("arguments[0].click();", next_btn)
        time.sleep(3)
    except:
        print("No more pages available.")
        break
df = pd.DataFrame(all_products)
df.to_csv("daraz_keyboards.csv", index=False, encoding="utf-8-sig")

print("Data saved to daraz_keyboards.csv")

driver.quit()
