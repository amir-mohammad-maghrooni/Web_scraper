import requests
from bs4 import BeautifulSoup
import time
import csv

url = 'https://quotes.toscrape.com'
# all_quotes = []
# try:
#         while True:
#             response = requests.get(url)
#             if response.status_code == 200:
#                 soup = BeautifulSoup(response.text, 'html.parser')
#                 quotes = soup.find_all('div', class_='quote')
#                 # print(soup)
#                 # print(quotes)
#                 for quote in quotes:
#                     text = quote.find('span' , class_='text').get_text()
#                     author = quote.find('small' , class_='author').get_text()
#                     tags = [tag.get_text() for tag in quote.find("div", class_="tags").find_all("a", class_="tag")]
#                     print(f"{text} - {author}, {tags}")
#                     all_quotes.append((text, author, ", ".join(tags)))
#                     # Wait for 0.5 seconds before making another request to avoid overwhelming the website server
#                     time.sleep(0.2)

#                 next_button = soup.find('li', class_='next')
#                 if next_button:
#                     next_url = next_button.find('a')['href']
#                     url = "https://quotes.toscrape.com" + next_url
#                     print(f"Scraping next page: {url}")
#                 else:
#                     print("No more next button! Scraping Completed!")
#                     break
#             else:
#                 print(f"Failed to fetch the page. status code: {response.status_code}")
#                 break
#         with open("webscraper\quotes.csv", "w", newline="", encoding="utf-8") as file:
#             writer = csv.writer(file)
#             writer.writerow(["Quote", "Author", "Tags"])
#             writer.writerows(all_quotes)
# except(ConnectionError):
#     print("Failed to establish a connection with the website.")
# except(ConnectionRefusedError):
#     print("Connection refused")
# except(ConnectionResetError):
#     print("Connection reset by peer")
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
print(soup)