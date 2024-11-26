import requests
from bs4 import BeautifulSoup
import csv
import time
import json

def fetch_page(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def parse_quotes(html):
    soup = BeautifulSoup(html, "html.parser")
    quotes = []

    for quote in soup.find_all("div", class_="quote"):
        text = quote.find("span", class_="text").get_text()
        author = quote.find("small", class_="author").get_text()
        tags = [tag.get_text() for tag in quote.find("div", class_="tags").find_all("a", class_="tag")]
        quotes.append({"text": text, "author": author, "tags": tags})
    
    next_button = soup.find("li", class_="next")
    next_url = next_button.find("a")["href"] if next_button else None

    return quotes, next_url

def save_to_csv(data, filename):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Quote", "Author", "Tags"])  # Header row
        for entry in data:
            writer.writerow([entry["text"], entry["author"], ", ".join(entry["tags"])])


def save_to_json(data, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
        
        
def scrape_quotes(base_url,file_name):
    url = base_url
    all_quotes = []

    while url:
        print(f"Scraping {url}...")
        html = fetch_page(url)
        if not html:
            break
        time.sleep(1)  # Delay between requests to avoid hitting the website's rate limit
        quotes, next_url = parse_quotes(html)
        all_quotes.extend(quotes)
        url = base_url + next_url if next_url else None

        save_to_csv(all_quotes, file_name + "csv")
        save_to_json(all_quotes, file_name + "json")
    
    
    print(f"Scraping complete! Data saved to {file_name}csv & {file_name}json")

if __name__ == "__main__":
    BASE_URL = "http://quotes.toscrape.com"
    FILE_NAME = 'SQuotes.'
    # OUTPUT_FORMAT = "json"  # Change to "csv" for CSV output
    scrape_quotes(base_url= BASE_URL, file_name= FILE_NAME)

