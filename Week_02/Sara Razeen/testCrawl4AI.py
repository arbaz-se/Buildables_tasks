# import asyncio
# import gspread
# from google.oauth2.service_account import Credentials
# from crawl4ai import AsyncWebCrawler
# from bs4 import BeautifulSoup
# import re

# # ============ Google Sheet Setup ============
# SERVICE_ACCOUNT_FILE = "datacollection-470220-5f31625f6b01.json"
# SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1DWEDzzo3HkpBOgsgjYMWWh1aF33RQMpZA8DjouaYWQA/edit?gid=0#gid=0"

# # Authenticate with Google Sheets
# creds = Credentials.from_service_account_file(
#     SERVICE_ACCOUNT_FILE,
#     scopes=["https://www.googleapis.com/auth/spreadsheets"]
# )
# client = gspread.authorize(creds)
# sheet = client.open_by_url(SPREADSHEET_URL).sheet1

# # Clear old data & add header
# sheet.clear()
# sheet.append_row(["Title", "Authors", "Abstract (first 5 lines)", "URL"])

# # ============ ArXiv Browser Automation Scraper ============
# async def scrape_arxiv_browser():
#     async with AsyncWebCrawler(verbose=True, headless=False) as crawler:
#         # Use the correct URL format for January 2024
#         result_listing = await crawler.arun(
#             url="https://arxiv.org/list/astro-ph/2401",  # Correct format: YYMM
#             actions=[
#                 {"action": "wait_for", "selector": "body"},
#                 {"action": "wait", "time": 3},
#                 {"action": "get_html", "var": "html"}
#             ]
#         )

#         # Save HTML for debugging
#         with open("debug_listing.html", "w", encoding="utf-8") as f:
#             f.write(result_listing.html)
#         print("Saved listing page HTML to debug_listing.html")

#         soup_listing = BeautifulSoup(result_listing.html, "html.parser")
        
#         # Check if we got a valid page
#         title = soup_listing.find("title")
#         if title and "404" in title.text:
#             print("❌ Got 404 error. Trying alternative URL...")
#             # Try a different approach - go to the main listings page
#             result_listing = await crawler.arun(
#                 url="https://arxiv.org/list/astro-ph/recent",
#                 actions=[
#                     {"action": "wait_for", "selector": "body"},
#                     {"action": "wait", "time": 3},
#                     {"action": "get_html", "var": "html"}
#                 ]
#             )
#             soup_listing = BeautifulSoup(result_listing.html, "html.parser")

#         # ============ Extract paper links using multiple strategies ============
#         paper_links = []
        
#         # Strategy 1: Look for links in dt elements (standard arXiv format)
#         for dt in soup_listing.find_all("dt"):
#             abstract_links = dt.find_all("a", title="Abstract")
#             for link in abstract_links:
#                 href = link.get("href", "")
#                 if href and href.startswith("/abs/"):
#                     paper_url = "https://arxiv.org" + href
#                     if paper_url not in paper_links:
#                         paper_links.append(paper_url)
        
#         # Strategy 2: Look for all /abs/ links on the page
#         if not paper_links:
#             print("No papers found with Strategy 1, trying Strategy 2...")
#             for link in soup_listing.find_all("a", href=True):
#                 href = link["href"]
#                 if href and href.startswith("/abs/") and "v1" in href:
#                     paper_url = "https://arxiv.org" + href
#                     if paper_url not in paper_links:
#                         paper_links.append(paper_url)
        
#         # Strategy 3: Look for arXiv IDs and construct URLs manually
#         if not paper_links:
#             print("No papers found with Strategy 2, trying Strategy 3...")
#             # Look for arXiv IDs in the page text
#             text_content = soup_listing.get_text()
#             arxiv_ids = re.findall(r'\d{4}\.\d{4,5}', text_content)
#             for arxiv_id in arxiv_ids[:10]:  # Limit to first 10
#                 paper_url = f"https://arxiv.org/abs/{arxiv_id}"
#                 if paper_url not in paper_links:
#                     paper_links.append(paper_url)
        
#         print(f"Found {len(paper_links)} papers to scrape")
        
#         # If still no papers, use some fallback test URLs
#         if not paper_links:
#             print("Using fallback test URLs...")
#             paper_links = [
#                 "https://arxiv.org/abs/2401.00001",
#                 "https://arxiv.org/abs/2401.00002",
#                 "https://arxiv.org/abs/2401.00003"
#             ]

#         papers_data = []

#         # Visit each paper and extract details
#         for paper_url in paper_links[:5]:  # Limit to 5 papers for testing
#             try:
#                 print(f"\n🔹 Scraping paper: {paper_url}")
#                 result_paper = await crawler.arun(
#                     url=paper_url,
#                     actions=[
#                         {"action": "wait_for", "selector": "body"},
#                         {"action": "wait", "time": 2},
#                         {"action": "get_html", "var": "html"}
#                     ]
#                 )

#                 # Save paper HTML for debugging
#                 paper_id = paper_url.split("/")[-1]
#                 with open(f"debug_paper_{paper_id}.html", "w", encoding="utf-8") as f:
#                     f.write(result_paper.html)

#                 soup = BeautifulSoup(result_paper.html, "html.parser")

#                 # Title
#                 title_tag = (soup.find("h1", class_="title mathjax") or 
#                              soup.find("h1", class_="title") or
#                              soup.find("h1"))
#                 title = title_tag.get_text(strip=True).replace("Title:", "").strip() if title_tag else "N/A"
#                 print(f"Title: {title[:60]}...")

#                 # Authors
#                 authors_tag = (soup.find("div", class_="authors") or
#                                soup.find("div", id="authors"))
#                 if authors_tag:
#                     authors = ", ".join([a.get_text(strip=True) for a in authors_tag.find_all("a")])
#                 else:
#                     authors = "N/A"
#                 print(f"Authors: {authors[:60]}...")

#                 # Abstract
#                 abstract_tag = (soup.find("blockquote", class_="abstract mathjax") or
#                                 soup.find("blockquote", class_="abstract"))
#                 if abstract_tag:
#                     abstract_full = abstract_tag.get_text(strip=True).replace("Abstract:", "").strip()
#                     # Get first 5 lines of abstract
#                     lines = [line.strip() for line in abstract_full.split('\n') if line.strip()]
#                     abstract_short = "\n".join(lines[:5])
#                 else:
#                     abstract_short = "N/A"
#                 print(f"Abstract: {abstract_short[:60]}...")

#                 # Append paper data including URL
#                 papers_data.append([title, authors, abstract_short, paper_url])
#                 print(f"✅ Successfully scraped: {title[:50]}...")

#             except Exception as e:
#                 print(f"❌ Error scraping {paper_url}: {str(e)}")
#                 papers_data.append(["Error", "Error", "Error", paper_url])

#         return papers_data

# # ============ Main ============
# async def main():
#     papers = await scrape_arxiv_browser()

#     # Upload to Google Sheets
#     for paper in papers:
#         sheet.append_row(paper)

#     print(f"\n🎉 Successfully uploaded {len(papers)} papers to Google Sheet!")

# if __name__ == "__main__":
#     asyncio.run(main())



import asyncio
import gspread
from google.oauth2.service_account import Credentials
from crawl4ai import AsyncWebCrawler
from bs4 import BeautifulSoup
import re

# ============ Google Sheet Setup ============
SERVICE_ACCOUNT_FILE = "datacollection-470220-5f31625f6b01.json"
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1DWEDzzo3HkpBOgsgjYMWWh1aF33RQMpZA8DjouaYWQA/edit?gid=0#gid=0"

# Authenticate with Google Sheets
creds = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)
client = gspread.authorize(creds)
sheet = client.open_by_url(SPREADSHEET_URL).sheet1

# Clear old data & add header
sheet.clear()
sheet.append_row(["Title", "Authors", "Abstract (first 5 lines)", "URL"])

# ============ ArXiv Browser Automation Scraper ============
async def scrape_arxiv_browser():
    async with AsyncWebCrawler(verbose=True, headless=False) as crawler:
        result_listing = await crawler.arun(
            url="https://arxiv.org/list/astro-ph/2401",  # January 2024 example
            actions=[
                {"action": "wait_for", "selector": "body"},
                {"action": "wait", "time": 3},
                {"action": "get_html", "var": "html"}
            ]
        )

        soup_listing = BeautifulSoup(result_listing.html, "html.parser")

        # ✅ Extract papers in exact webpage order
        paper_links = []
        dl_tag = soup_listing.find("dl")
        if dl_tag:
            for dt in dl_tag.find_all("dt", recursive=False):
                abstract_link = dt.find("a", title="Abstract")
                if abstract_link:
                    href = abstract_link.get("href", "")
                    if href.startswith("/abs/"):
                        paper_links.append("https://arxiv.org" + href)

        print(f"Found {len(paper_links)} papers in webpage order")

        # If no papers found, fallback
        if not paper_links:
            print("⚠️ No papers found, using fallback test URLs...")
            paper_links = [
                "https://arxiv.org/abs/2401.00001",
                "https://arxiv.org/abs/2401.00002",
                "https://arxiv.org/abs/2401.00003"
            ]

        papers_data = []

        for paper_url in paper_links[:10]:  # limit for testing
            try:
                print(f"\n🔹 Scraping paper: {paper_url}")
                result_paper = await crawler.arun(
                    url=paper_url,
                    actions=[
                        {"action": "wait_for", "selector": "body"},
                        {"action": "wait", "time": 2},
                        {"action": "get_html", "var": "html"}
                    ]
                )

                soup = BeautifulSoup(result_paper.html, "html.parser")

                # Title
                title_tag = (soup.find("h1", class_="title mathjax") or
                             soup.find("h1", class_="title") or
                             soup.find("h1"))
                title = title_tag.get_text(strip=True).replace("Title:", "").strip() if title_tag else "N/A"

                # Authors
                authors_tag = (soup.find("div", class_="authors") or
                               soup.find("div", id="authors"))
                if authors_tag:
                    authors = ", ".join([a.get_text(strip=True) for a in authors_tag.find_all("a")])
                else:
                    authors = "N/A"

                # Abstract
                abstract_tag = (soup.find("blockquote", class_="abstract mathjax") or
                                soup.find("blockquote", class_="abstract"))
                if abstract_tag:
                    abstract_full = abstract_tag.get_text(strip=True).replace("Abstract:", "").strip()
                    lines = [line.strip() for line in abstract_full.split('\n') if line.strip()]
                    abstract_short = "\n".join(lines[:5])
                else:
                    abstract_short = "N/A"

                # Save
                papers_data.append([title, authors, abstract_short, paper_url])
                print(f"✅ Scraped: {title[:60]}...")

            except Exception as e:
                print(f"❌ Error scraping {paper_url}: {str(e)}")
                papers_data.append(["Error", "Error", "Error", paper_url])

        return papers_data

# ============ Main ============
async def main():
    papers = await scrape_arxiv_browser()
    for paper in papers:
        sheet.append_row(paper)
    print(f"\n🎉 Uploaded {len(papers)} papers to Google Sheet!")

if __name__ == "__main__":
    asyncio.run(main())
