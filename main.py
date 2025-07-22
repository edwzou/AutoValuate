# Import libraries and dependencies
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as soup
import re
import pandas as pd
import matplotlib.pyplot as plt
import time

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--headless=new')

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Set up base url
city = "calgary"
base_url = "https://www.facebook.com/marketplace/" + city + "/search?"

# Set up search parameters
min_price = 1000
max_price = 10000
min_mileage = 10000
max_mileage = 100000
min_year = 2000
max_year = 2025
days_listed = 1
transmission = "automatic"
make = "toyota"
model = "corolla"

url = base_url + "min_price=" + str(min_price) + "&max_price=" + str(max_price) + "&min_mileage=" + str(min_mileage) + "&max_mileage=" + str(max_mileage) + "&min_year=" + str(min_year) + "&max_year=" + str(max_year) + "&days_listed=" + str(days_listed) + "&transmission=" + transmission + "&query=" + make + "%20" + model

# Open the browser and navigate to the url
driver.get(url)

# Close the login popup

try:
    close_button = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label="Close"]'))
    )
    close_button.click()
except:
    print("Close button not found or not clickable.")


# Scroll down to load more results
scroll_count = 4
scroll_delay = 2
for _ in range(scroll_count):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_delay)

# Parse the HTML
html = driver.page_source

# Create a BeautifulSoup object from the scraped HTML
soup = soup(html, 'html.parser')

# End the automated browsing session
driver.quit()

# Extract all the necessary info and intert into lists
titles_div = soup.find_all('span', class_='x1lliihq x6ikm8r x10wlt62 x1n2onr6')
titles_list = [title.text.strip() for title in titles_div]
prices_div = soup.find_all('span', class_='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x676frb x1lkfr7t x1lbecb7 x1s688f xzsf02u')
prices_list = [price.text.strip() for price in prices_div]
mileage_div = soup.find_all('span', class_='x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft x1j85h84')
mileage_list = [mileage.text.strip() for mileage in mileage_div]

# Create a regular expression pattern to match city and province entries like "City, AB"
pattern = re.compile(r'(\w+(?:-\w+)?, [A-Z]{2})')

# Initialize lists to store the adjusted milage entries
mileage_list_adjusted = []

# Iterate through the milage entries and adjust them
for mileage in mileage_list:
    mileage_list_adjusted.append(mileage)
    if pattern.match(mileage) and len(mileage_list_adjusted) > 1 and pattern.match(mileage_list_adjusted[-2]):
        mileage_list_adjusted.insert(-1, '0K km')

# Remove the km or miles from mileage entries
mileage_pattern_km = r'(\d+)K km'
mileage_pattern_miles = r'(\d+)K miles'

# Create a list to store the adjusted mileage entries
mileage_list_cleaned = []

for mileage in mileage_list_adjusted:
    match_mileage_km = re.search(mileage_pattern_km, mileage)
    match_mileage_miles = re.search(mileage_pattern_miles, mileage)
    if match_mileage_km or match_mileage_miles:
        if match_mileage_km:
            mileage_list_cleaned.append(int(match_mileage_km.group(1)) * 1000)
        else:
            mileage_list_cleaned.append(int(match_mileage_miles.group(1)) * 1609)

# Add all values to a list of dictionaries
vehicle_list = []

for i, item in enumerate(titles_list):
    vehicles_dict = {}
    title_split = titles_list[i].split()
    vehicles_dict['Year'] = int(title_split[0])
    vehicles_dict['Make'] = title_split[1]
    vehicles_dict['Model'] = title_split[2]
    vehicles_dict['Price'] = int(re.sub(r'[^\d.]', '', prices_list[i]))
    vehicles_dict['Mileage'] = mileage_list_cleaned[i]
    vehicle_list.append(vehicles_dict)

# Filter out anomalies
filtered_vehicle_list = []
for v in vehicle_list:
    if v['Make'] != make and v['Model'] != model:
        continue
    if v['Price'] in [1, 12, 123, 1234, 12345, 123456]:
        continue
    if v['Price'] < 1000 and (v['Mileage'] > 100000 or v['Mileage'] < 100000):
        continue
    filtered_vehicle_list.append(v)

# Continue with DataFrame creation and CSV export
vehicle_df = pd.DataFrame(filtered_vehicle_list)
vehicle_df.to_csv('vehicle_data.csv', index=False)