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

def parse_books(html):
    soup = BeautifulSoup(html, "html.parser")
    books = []

    for book in soup.find_all("article", class_="product_pod"):
        title = book.h3.a['title']
        price = book.find("p", class_="price_color").text.strip()
        availability = book.find("p", class_="instock availability").text.strip()
        rating = book.p['class'][1]
        books.append({
            "title": title,
            "price": price,
            "availability": availability,
            "rating": rating
        })
    
    next_button = soup.find("li", class_="next")
    next_url = next_button.find("a")["href"] if next_button else None

    return books, next_url

def save_to_csv(data, filename):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Titles", "Price", "Availability", "Rating"])  # Header row
        for entry in data:
            writer.writerow([entry["title"], entry["price"], entry["availability"], entry["rating"]])


def save_to_json(data, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
        
        
def scrape_books(base_url,file_name):
    url = base_url
    all_books = []

    while url:
        print(f"Scraping {url}...")
        html = fetch_page(url)
        if not html:
            break
        time.sleep(1)  # Delay between requests to avoid hitting the website's rate limit
        
        books, next_url = parse_books(html)
        all_books.extend(books)
        
        if next_url and "catalogue/" not in next_url:
            next_url = "catalogue/" + next_url
        url = base_url + next_url if next_url else None


        save_to_csv(all_books, file_name + "csv")
        save_to_json(all_books, file_name + "json")
    
    
    print(f"Scraping complete! Data saved to {file_name}csv & {file_name}json")

if __name__ == "__main__":
    BASE_URL = "https://books.toscrape.com/"
    FILE_NAME = 'webscraper\Books.'
    # OUTPUT_FORMAT = "json"  # Change to "csv" for CSV output
    scrape_books(base_url= BASE_URL, file_name= FILE_NAME)

