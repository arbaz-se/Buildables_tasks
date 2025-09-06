from bs4 import BeautifulSoup
import os
import pandas as pd


d = {"title": [], "price": []}

for file in os.listdir("data"):
    try:
        with open(f"data/{file}", encoding="utf-8") as f:
            html_doc = f.read()
            soup = BeautifulSoup(html_doc, 'html.parser')

        # Title
        t = soup.find("h2")
        title = t.get_text().strip() if t else None


        # Price
        p = soup.find("span", attrs={"class": "a-price-whole"})
        price = p.get_text().strip() if p else None

        d["title"].append(title)
        d["price"].append(price)

    except Exception as e:
        print(f"Error in file {file}: {e}")

df = pd.DataFrame(d)
df.to_csv("laptop_data.csv", index=False)
