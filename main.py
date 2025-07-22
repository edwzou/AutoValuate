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
options.add_argument('--start-maximized')  # Optional: start maximized
# You can add more options if needed, e.g., headless mode

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Set up base url
city = "calgary"
base_url = "https://www.facebook.com/marketplace/" + city + "/vehicles?"

# Set up search parameters
min_price = 1000
max_price = 10000
min_milage = 10000
max_milage = 100000
min_year = 2000
max_year = 2025
days_listed = 1
transmission = "automatic"
make = "toyota"
model = "corolla"

url = base_url + "min_price=" + str(min_price) + "&max_price=" + str(max_price) + "&min_milage=" + str(min_milage) + "&max_milage=" + str(max_milage) + "&min_year=" + str(min_year) + "&max_year=" + str(max_year) + "&days_listed=" + str(days_listed) + "&transmission=" + transmission + "&make=" + make + "&model=" + model

# Open the browser and navigate to the url
driver.get(url)

# Close the login popup

try:
    close_button = WebDriverWait(driver, 10).until(
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
titles_div = soup.find_all('span', class_='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x676frb x1lkfr7t x1lbecb7 x1s688f xzsf02u')