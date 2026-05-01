import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Scrape BLS Occupational Outlook Handbook for job outlook ratings
# Supplements AI exposure analysis with forward-looking labour market data

BASE_URL = "https://www.bls.gov"
HEADERS = {"User-Agent": "student-research-bot/1.0 (university project)"}

# Navigation pages to exclude
NAV_SLUGS = {
    "home.htm", "a-z-index.htm", "ooh-site-map.htm",
    "occupation-finder.htm", "ooh-faqs.htm"
}


def scrape_ooh_index():
    """Scrape the OOH A-Z index to get real occupation links only."""
    url = BASE_URL + "/ooh/a-z-index.htm"
    response = requests.get(url, headers=HEADERS, timeout=10)
    time.sleep(2)
    soup = BeautifulSoup(response.content, "html.parser")

    seen = set()
    unique = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        parts = [p for p in href.split("/") if p]
        # Real occupation pages: /ooh/category/occupation.htm
        if (len(parts) == 3 and parts[0] == "ooh"
                and parts[2].endswith(".htm")
                and parts[2] not in NAV_SLUGS
                and "how-to" not in href
                and "print" not in href):
            full_url = BASE_URL + href
            name = a.get_text(strip=True)
            if full_url not in seen and name and not name.isupper():
                seen.add(full_url)
                unique.append({"occupation": name, "url": full_url})
    return unique


def scrape_occupation(url):
    """Scrape a single OOH occupation page for outlook data."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        time.sleep(1)
        soup = BeautifulSoup(response.content, "html.parser")
        outlook = None
        for tag in soup.find_all(["p", "div", "td"]):
            text = tag.get_text(strip=True).lower()
            if "faster than average" in text:
                outlook = "Faster than average"
                break
            elif "slower than average" in text:
                outlook = "Slower than average"
                break
            elif "about as fast as average" in text:
                outlook = "Average"
                break
            elif "little or no change" in text:
                outlook = "Little or no change"
                break
        return outlook
    except Exception as e:
        print(f"Failed: {e}")
        return None


def main():
    print("Scraping BLS Occupational Outlook Handbook...")
    links = scrape_ooh_index()
    print(f"Found {len(links)} occupation pages")

    results = []
    for i, item in enumerate(links[:80]):
        print(f"Scraping {i+1}/{min(80,len(links))}: {item['occupation']}")
        outlook = scrape_occupation(item["url"])
        results.append({
            "occupation_name_bls": item["occupation"],
            "bls_outlook": outlook,
            "bls_url": item["url"]
        })

    df = pd.DataFrame(results)
    df.to_csv("data/raw/bls_outlook_scraped.csv", index=False)
    print(f"\nSaved {len(df)} records to data/raw/bls_outlook_scraped.csv")
    print(df["bls_outlook"].value_counts())


if __name__ == "__main__":
    main()
