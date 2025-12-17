import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_URL = "https://www.shl.com"
CATALOG_URL = "https://www.shl.com/solutions/products/product-catalog/"

def scrape_catalog():
    rows = []
    visited = set()

    print("Fetching catalog page...")
    response = requests.get(CATALOG_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    # find links to individual assessments
    links = soup.select("a[href*='/assessments/']")

    print(f"Found {len(links)} assessment links")

    for link in links:
        url = BASE_URL + link["href"]

        if url in visited:
            continue
        visited.add(url)

        try:
            page = requests.get(url, timeout=10)
            page_soup = BeautifulSoup(page.text, "html.parser")

            name_tag = page_soup.find("h1")
            name = name_tag.text.strip() if name_tag else ""

            desc_tag = page_soup.find("meta", {"name": "description"})
            description = desc_tag["content"] if desc_tag else ""

            rows.append({
                "name": name,
                "url": url,
                "description": description
            })

            print("Scraped:", name)
            time.sleep(0.3)  # be polite to server

        except Exception as e:
            print("Error scraping", url, "->", e)

    df = pd.DataFrame(rows).drop_duplicates()

    output_path = "data/raw/shl_catalog_raw.csv"
    df.to_csv(output_path, index=False)

    print("\nSCRAPING COMPLETED")
    print("Total assessments scraped:", len(df))
    print("Saved to:", output_path)


if __name__ == "__main__":
    scrape_catalog()
