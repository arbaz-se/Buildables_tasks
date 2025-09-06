from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
#Keys is a class in Selenium that contains special keyboard keys (like Enter, Tab, Arrow keys, Ctrl, etc.)
# that you can send to elements using .send_keys().

driver = webdriver.Chrome()
query = "laptop"
file = 0
for i in range(0,10):
    driver.get(f"https://www.amazon.com/s?k={query}&page={i}&xpid=bsKKyqJyoPma7&crid=195L624I24R2N&qid=1756242713&sprefix=lapto%2Caps%2C482&ref=sr_pg_2")
    elems= driver.find_elements(By.CLASS_NAME,"puis-card-container")
    print(f"{len(elems)} elements found")
    for elem in elems:
        d=elem.get_attribute("outerHTML")
        with open(f"data/{query}_{file}.html","w",encoding="utf-8") as f:
            f.write(d)
            file+=1

    time.sleep(2)
driver.close()