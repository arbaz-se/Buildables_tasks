import asyncio
import random
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode, BrowserConfig
from bs4 import BeautifulSoup


async def scrape_collection(crawler, search_term, collection_type):
    all_data = []

   
    search_url = f"https://saya.pk/search?q={search_term}"
    run_cfg = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,  
    )

    result = await crawler.arun(search_url, config=run_cfg)

    if not result.success:
        print(f" Failed to load {collection_type} page")
        return []

    soup = BeautifulSoup(result.html, "html.parser")
    products = soup.select(".t4s-product-wrapper")

    tasks = []
    for i, product in enumerate(products, start=1):
        try:
            title_elem = product.select_one(".t4s-product-title a")
            title = title_elem.text.strip()
            link = title_elem["href"]
            if not link.startswith("http"):
                link = "https://saya.pk" + link
        except:
            title, link = None, None

        try:
            price = product.select_one(".money").text.strip()
        except:
            price = None

    
        if link:
            tasks.append(fetch_product_detail(
                crawler, run_cfg, title, price, link,
                collection_type, i, len(products)
            ))

   
    results = await asyncio.gather(*tasks, return_exceptions=True)

    for r in results:
        if isinstance(r, dict):
            all_data.append(r)

    return all_data


async def fetch_product_detail(crawler, run_cfg, title, price, link, collection_type, idx, total):
    barcode, availability, available_quantity = None, None, None
    detail = await crawler.arun(link, config=run_cfg)
    if detail.success:
        detail_soup = BeautifulSoup(detail.html, "html.parser")
        try:
            barcode = detail_soup.select_one(".t4s-barcode-value").text.strip()
        except:
            pass
        try:
           
            avail_elem = detail_soup.select_one("span[data-instock-status]")
            if avail_elem:
                raw_text = avail_elem.get_text(strip=True).lower()
                if "in stock" in raw_text:
                    availability = "InStock"
                elif "out of stock" in raw_text:
                    availability = "OutOfStock"
                else:
                    availability = avail_elem.get_text(strip=True)
        except:
            pass

        try:
          
            qty_elem = detail_soup.select_one("span[style*='color: rgb(230, 0, 0)']")
            if qty_elem:
                available_quantity = qty_elem.get_text(strip=True)
        except:
            pass

    print(f" Scraped {idx}/{total} from {collection_type}")


    await asyncio.sleep(random.uniform(1, 3))

    return {
        "Collection": collection_type,
        "Title": title,
        "Price": price,
        "Barcode": barcode,
        "Availability": availability,
        "Available_Quantity": available_quantity,
        "Link": link
    }



async def main():
  
    browser_cfg = BrowserConfig(headless=True)
    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        stitched_data = await scrape_collection(crawler, "lawn stitched", "Stitched")
        unstitched_data = await scrape_collection(crawler, "lawn unstitched", "Unstitched")
        accessories_data = await scrape_collection(crawler, "accessories", "Accessories")
        men_data = await scrape_collection(crawler, "men", "Men Wear")
        kids_data = await scrape_collection(crawler, "kids", "Kidswear")

  
    all_data = stitched_data + unstitched_data + accessories_data + men_data + kids_data

    df = pd.DataFrame(all_data)
    print(df)


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

    sheet = client.open_by_url(
        "https://docs.google.com/spreadsheets/d/1-exE8owP3dkH9pMOdf30FwuL7C22E5RUjKBoeetfviw/edit?gid=0#gid=0"
    )
    worksheet = sheet.sheet1

    worksheet.clear()
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())

    print("All scrapped usong crawl4.ai")


if __name__ == "__main__":
    asyncio.run(main())
