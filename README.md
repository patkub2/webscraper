information i need :

ceny wynajmu,
ilość pokoi,
metraż,
piętro
umeblowany

- Target Website URL(s):

The specific URLs you intend to scrape.
Structure of the Website:

Is the content static or dynamic? For dynamic content (loaded via JavaScript), you might need tools like Selenium or Puppeteer.
What's the pagination structure? Does it use traditional page numbers, infinite scrolling, or another mechanism?

page numbers

- Specific Data Points You Want to Extract:

For instance, if you're scraping a product page, you might want: product name, price, description, ratings, etc.
Sample HTML snippets or selectors for these data points can be useful.

- Frequency of Scraping:

How often do you intend to scrape the website? Once? Daily? Hourly?

- Handling Edge Cases:

What should the scraper do if it encounters unexpected data or structure? For instance, what if a product lacks a price or a rating?

- Storage Details:

Where do you want to save the scraped data? (e.g., JSON file, database, CSV)
How should the data be structured?

- Error Handling and Logging:

How should the scraper handle errors like timeouts, failed requests, or unexpected website changes?
Do you need logs for monitoring the scraper's performance and issues?

- User-Agent and Headers:

Some sites might block default headers sent by scraping libraries. It might be necessary to set a User-Agent that mimics a real browser or includes other headers.

- Respect robots.txt and Terms of Service (ToS):

Check the website’s robots.txt to determine which parts, if any, can be legally scraped.
Read the website's ToS to ensure you're not violating any rules.

- Avoiding Bans and Rate Limiting:

Techniques such as rotating user agents, using proxies, and introducing delays between requests can help.
Ensure you don't overload the target server, which can be considered a form of a DDoS attack.

plan:

main page

1. chosse city from list that is located in locations.json file and insert it into link https://www.otodom.pl/pl/wyniki/wynajem/mieszkanie/slaskie/katowice/katowice/katowice?ownerTypeSingleSelect=ALL&distanceRadius=0&viewType=listing&limit=72&page=1 in place of katowice

2. search for data-cy="listing-item" find element inside data-cy="listing-item-link" and go to the href link

3. find:
   aria-label="Powierzchnia" > value from the inside of the second div
   aria-label="Czynsz" > value from the inside of the second div
   aria-label="Liczba pokoi" > value from the inside of the second div
   aria-label="Kaucja" > value from the inside of the second div
   aria-label="Piętro" > value from the inside of the second div
   aria-label="Rodzaj zabudowy" > value from the inside of the second div
   aria-label="Stan wykończenia" > value from the inside of the second div
   aria-label="Cena" > inside text
   aria-label="Adres" > inside text

4. save it into a json file where key value is the aria-label and value is the described value so for example the file will look like this:

[
{"Powierzchnia": "22 m3","Czynsz": "600 zł", ...},
{"Powierzchnia": "24 m3","Czynsz": "2300 zł",}, ...
]

5. reapet from second point going throught all links to offerts, stop after 40 reapets

import requests
from bs4 import BeautifulSoup

cities = ["katowice", "gliwice", "sosnowiec", "bytom", "zabrze"]
base_url = "https://www.otodom.pl/pl/wyniki/wynajem/mieszkanie/slaskie/{city}/{city}/{city}?ownerTypeSingleSelect=ALL&distanceRadius=0&viewType=listing&limit=72&page=1"

headers = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def extract_links(url):
response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.content, 'html.parser')
    links = ["https://www.otodom.pl" + anchor.get('href') for anchor in soup.find_all('a', attrs={'data-cy': 'listing-item-link'})]

    return links

all_links = []

for city in cities:
url = base_url.format(city=city)
all_links.extend(extract_links(url))

print(all_links)

now from each link in all_links go inside the link and look for

aria-label="Powierzchnia" > value from the inside of the second div
aria-label="Czynsz" > copy value from the inside of the second div
aria-label="Liczba pokoi" > value from the inside of the second div
aria-label="Kaucja" > value from the inside of the second div
aria-label="Piętro" > value from the inside of the second div
aria-label="Rodzaj zabudowy" > value from the inside of the second div
aria-label="Stan wykończenia" > value from the inside of the second div
aria-label="Cena" > inside text
aria-label="Adres" > inside text

save it into a json file where key value is the aria-label and value is the described value so for example the file will look like this:

[
{"Powierzchnia": "22 m3","Czynsz": "600 zł", ...},
{"Powierzchnia": "24 m3","Czynsz": "2300 zł",}, ...
]

reapet going throught all links
#   w e b s c r a p e r  
 