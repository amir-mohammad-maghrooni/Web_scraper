import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import csv
import time
import logging
import random

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def create_config():
    print("Welcome to the Web Scraper Config Generator!")
    
    base_url = input("Enter the base URL of the website to scrape: ").strip()
    
    output_file = input("Enter the output file name (e.g., data.json or data.csv): ").strip()
    output_format = "json" if output_file.endswith(".json") else "csv"
    
    print("\nDefine the data you want to scrape (e.g., title, price, availability):")
    selectors = {}
    while True:
        field_name = input("Enter the field name (or press Enter to finish): ").strip()
        if not field_name:
            break
        
        css_selector = input(f"Enter the CSS selector for '{field_name}': ").strip()
        selectors[field_name] = css_selector
    
    # Get the pagination selector
    pagination_selector = input("\nEnter the CSS selector for the 'Next' button (or leave blank if no pagination): ").strip()
    
    config = {
        "base_url": base_url,
        "output_file": output_file,
        "output_format": output_format,
        "selectors": selectors,
        "pagination_selector": pagination_selector
    }
    
    # Save the config to a file
    config_file = input("\nEnter the name for the config file (e.g., config.json): ").strip()
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)
    
    print(f"\nConfiguration file '{config_file}' has been created!")
    return config_file



class WebScraper:
    def __init__(self, config_file):
        with open(config_file, "r") as f:
            self.config = json.load(f)

        self.base_url = self.config["base_url"]
        self.output_file = self.config["output_file"]
        self.data = []

    def fetch_page(self, url):
        try:
            response = requests.get(url, headers=self.config.get("headers", {}))
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching {url}: {e}")
            return None

    def parse_page(self, current_url, html):
        soup = BeautifulSoup(html, "html.parser")
        items = []

        for el in soup.select("div.quote"):
            item = {}
            for field, selector in self.config["selectors"].items():
                targets = el.select(selector)
                if targets:
                    if len(targets) > 1:
                        item[field] = [target.text.strip() for target in targets]
                    elif len(targets) == 1:
                        item[field] = targets[0].text.strip()
                else:
                    item[field] = None

            items.append(item)


        # Handle pagination
        next_button = soup.select_one(self.config["pagination_selector"])
        next_url = None
        if next_button and "href" in next_button.attrs:
            relative_next_url = next_button["href"]
            next_url = urljoin(current_url, relative_next_url)

        return items, next_url

    def extract_data(self, element, css_selector):
        target = element.select_one(css_selector)
        return target.text.strip() if target else None

    def save_data(self):
        format = self.config["output_format"]
        if format == "csv":
            self.save_to_csv()
        elif format == "json":
            self.save_to_json()
        else:
            logging.warning(f"Unsupported output format: {format}")

    def save_to_csv(self):
        fieldnames = self.config["selectors"].keys()
        with open(self.output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.data)

    def save_to_json(self):
        with open(self.output_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4)

    def scrape(self):
        url = self.base_url
        previous_url = None
        while url:
            if url == previous_url:
                break
            
            logging.info(f"Scraping {url}...")
            html = self.fetch_page(url)
            if not html:
                break

            items, next_url = self.parse_page(url,html)
            self.data.extend(items)
            logging.info(f"Collected {len(self.data)} items so far.")
            previous_url = url
            url = next_url
            # Random delay to mimic human browsing
            time.sleep(random.uniform(1, 3))

        logging.info("Scraping complete!")
        self.save_data()

if __name__ == "__main__":
    use_existing = input("Do you already have a config file? (y/n): ").strip().lower()
    
    if use_existing == "n":
        config_file = create_config()
    else:
        config_file = input("Enter the path to the existing config file: ").strip()
        
    scraper = WebScraper(config_file)
    scraper.scrape()
