from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import json
cities = ["katowice"]
base_url = "https://www.otodom.pl/pl/wyniki/wynajem/mieszkanie/slaskie/{city}/{city}/{city}?ownerTypeSingleSelect=ALL&distanceRadius=0&viewType=listing&limit=24&page=1"

# Setting up Selenium
options = Options()
# Uncomment to run in headless mode
# options.add_argument('--headless')


driver_path = "./driver/chromedriver.exe"
options.binary_location = driver_path
driver = webdriver.Chrome(options=options)


def close_cookies_popup():
    try:
        # This selector might need to be adapted based on the actual structure of the popup
        close_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "button[id='onetrust-accept-btn-handler']"))
        )
        close_button.click()
    except:
        print("Error closing cookies popup or popup not found")


def extract_links(url):
    driver.get(url)
    close_cookies_popup()  # Call the function to close the cookies popup

    # Scroll the page
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        # Wait for the page to load
        WebDriverWait(driver, 10).until(
            lambda driver: driver.execute_script(
                "return document.readyState") == "complete"
        )
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    try:
        elements = WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "a[data-cy='listing-item-link']"))
        )
        links = [
            element.get_attribute('href') for element in elements]  # "https://www.otodom.pl" +
        return links
    except Exception as e:
        print(f"Error fetching links from {url}: {str(e)}")
        return []


all_links = []

for city in cities:
    url = base_url.format(city=city)
    all_links.extend(extract_links(url))

print(all_links)
print(len(all_links))

test_link = [all_links[1]]
###############################################

# ... [Your previous code here]


def extract_value_from_link(label):

    try:
        # If the label is 'Cena', we need to handle it separately due to its unique structure.
        if label == "Cena":
            element = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, f"strong[aria-label='{label}']"))
            )
            return element.text

        # For all other labels, proceed with the original logic.
        parent_div = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, f"div[aria-label='{label}']"))
        )

        # Adjust the tree structure for the specific label 'Czynsz'.
        if label == "Czynsz":
            value = parent_div.find_element(
                By.CSS_SELECTOR, "div:nth-of-type(3) > div").text
        else:
            value = parent_div.find_element(
                By.CSS_SELECTOR, "div:nth-of-type(2) > div").text

        return value

    except Exception as e:
        print(f"Error fetching {label}: {str(e)}")
        return None


results = []

for link in test_link:
    entry = {"Link": link}
    driver.get(link)

    for label in ["Powierzchnia", "Liczba pokoi", "Stan wykończenia", "Cena"]:
        value = extract_value_from_link(label)
        if value:
            entry[label] = value

    results.append(entry)

with open('output.txt', 'w', encoding='utf-8') as f:
    f.write(str(results))


driver.quit()
