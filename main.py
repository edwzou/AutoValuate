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
from groq import Groq
import os
from dotenv import load_dotenv
from sklearn.linear_model import LinearRegression
import numpy as np
from ui import run_ui, show_results

load_dotenv()

def main():
    # Get user parameters from UI
    print("Opening Vehicle Price Predictor UI...")
    settings = run_ui()
    
    if not settings:
        print("No settings provided. Exiting...")
        return
    
    # Extract settings
    city = settings['city']
    make = settings['make']
    model = settings['model']
    model_year = settings['model_year']
    transmission = settings['transmission']
    car_mileage = settings['car_mileage']

    # Set up Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--headless=new')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Set up base url
    base_url = "https://www.facebook.com/marketplace/" + city + "/search?"

    url = base_url + "&transmission=" + transmission + "&query=" + make + "%20" + model

    print(f"Searching for {make} {model} vehicles in {city}...")
    print(f"URL: {url}")

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
    scroll_count = 2
    scroll_delay = 2
    print(f"Scrolling {scroll_count} times with {scroll_delay} second delays...")
    for i in range(scroll_count):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_delay)
        print(f"Scroll {i+1}/{scroll_count} completed")

    # Parse the HTML
    html = driver.page_source

    # Create a BeautifulSoup object from the scraped HTML
    soup_obj = soup(html, 'html.parser')

    # End the automated browsing session
    driver.quit()

    # Extract all the necessary info and intert into lists
    titles_div = soup_obj.find_all('span', class_='x1lliihq x6ikm8r x10wlt62 x1n2onr6')
    titles_list = [title.text.strip() for title in titles_div]
    prices_div = soup_obj.find_all('span', class_='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x676frb x1lkfr7t x1lbecb7 x1s688f xzsf02u')
    prices_list = [price.text.strip() for price in prices_div]
    content_div = soup_obj.find_all('span', class_='x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft x1j85h84')
    content_list = [content.text.strip() for content in content_div]

    location_pattern = re.compile(r'^[A-Za-z\s\-]+, [A-Z]{2}$')
    mileage_pattern = re.compile(r'^\d+K (km|miles)$')

    location_list = []
    mileage_list = []

    i = 0
    while i < len(content_list):
        content = content_list[i]
        if content in ["Log In", "Create new account"]:
            i += 1
            continue
        if location_pattern.match(content):
            location_list.append(content)
            if i + 1 < len(content_list) and mileage_pattern.match(content_list[i + 1]):
                mileage_list.append(content_list[i + 1])
                i += 2
            else:
                mileage_list.append("0K km")
                i += 1
        else:
            i += 1

    mileage_pattern_km = re.compile(r'^\d+K km$')
    mileage_pattern_miles = re.compile(r'^\d+K miles$')

    mileage_list_cleaned = []

    for mileage in mileage_list:
        if mileage_pattern_km.match(mileage):
            mileage_list_cleaned.append(int(mileage.replace('K km', '')) * 1000)
        elif mileage_pattern_miles.match(mileage):
            mileage_list_cleaned.append(int(mileage.replace('K miles', '')) * 1609)

    # Add all the values to a list of dictionaries
    vehicles_list = []

    year_pattern = re.compile(r'\b(19[8-9]\d|20[0-2]\d|2025)\b')
    for i, item in enumerate(titles_list):
        title = titles_list[i]
        title_lower = title.lower()
        # Check for year, make, and model
        year_match = year_pattern.search(title_lower)
        make_match = re.search(make.lower(), title_lower)
        model_match = re.search(model.lower(), title_lower)
        if not (year_match and make_match and model_match):
            continue  # Skip this entry if any are missing
        vehicles_dict = {}
        vehicles_dict['Year'] = int(year_match.group(0))
        vehicles_dict['Make'] = make_match.group(0).capitalize()
        vehicles_dict['Model'] = model_match.group(0).capitalize()
        vehicles_dict['Price'] = int(re.sub(r'[^\d.]', '', prices_list[i]))
        vehicles_dict['Location'] = location_list[i]
        vehicles_dict['Mileage'] = mileage_list_cleaned[i]
        vehicles_list.append(vehicles_dict)

    filtered_vehicles_list = []
    for vehicle in vehicles_list:
        if vehicle['Price'] in [1, 12, 123, 1234, 12345, 123456, 1234567]:
            continue
        if vehicle['Mileage'] == 0:
            continue
        if vehicle['Price'] <= 200:
            continue
        filtered_vehicles_list.append(vehicle)

    print(f"Found {len(filtered_vehicles_list)} matching vehicles")

    # Continue with DataFrame creation and CSV export
    vehicle_df = pd.DataFrame(filtered_vehicles_list)
    # vehicle_df.to_csv('vehicle_data.csv', index=False)

    # Use LLM to get the generation range with enhanced prompt engineering
    def get_generation_prompt(make, model, year, prompt_settings=None):
        client = Groq(api_key=os.getenv("API_KEY"))
        
        # Use enhanced prompt engineering if available
        if prompt_settings and prompt_settings.get('include_context'):
            from ui import PromptEngineering
            prompt_engineer = PromptEngineering()
            prompt_data = prompt_engineer.get_enhanced_generation_prompt(make, model, year, city)
            
            messages = [
                {"role": "system", "content": prompt_data['system']},
                {"role": "user", "content": prompt_data['user']}
            ]
            
            temperature = prompt_settings.get('temperature', 0.3)
            max_tokens = prompt_data.get('max_tokens', 200)
        else:
            # Fallback to original simple prompt
            prompt = (
                f"What generation does a {year} {make} {model} belong to? "
                "Please answer with only the year range of the generation, e.g., '2000-2005'."
            )
            messages = [{"role": "user", "content": prompt}]
            temperature = 0.0
            max_tokens = 100
        
        try:
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error getting generation: {e}")
            return None

    # Extract prompt engineering settings
    prompt_settings = settings.get('prompt_engineering', {})
    
    generation_range = get_generation_prompt(make, model, model_year, prompt_settings)
    if generation_range:
        print(f"The {model_year} {make} {model} belongs to the generation: {generation_range}")
    else:
        print(f"Could not determine generation for {model_year} {make} {model}")
        # Fallback to a reasonable range
        generation_range = f"{model_year-2}-{model_year+2}"
        print(f"Using fallback generation range: {generation_range}")

    # Filter vehicle_df for years within the generation_range
    gen_start, gen_end = [int(x) for x in generation_range.split('-')]
    specific_vehicle_df = vehicle_df[
        (vehicle_df['Year'] >= gen_start) & (vehicle_df['Year'] <= gen_end)
    ]

    # specific_vehicle_df.to_csv('specific_vehicle_data.csv', index=False)

    # Use Linear Regression to predict price based on mileage
    if len(specific_vehicle_df) >= 2:
        mileages = specific_vehicle_df['Mileage'].values.reshape(-1, 1)
        prices = specific_vehicle_df['Price'].values
        lr_model = LinearRegression().fit(mileages, prices)
        lr_predicted_price = lr_model.predict(np.array([[car_mileage]]))[0]
    else:
        lr_predicted_price = 0
    
    # Enhanced AI analysis using prompt engineering
    def get_ai_price_analysis(make, model, year, mileage, city, prompt_settings):
        """Get AI-powered price analysis using enhanced prompts"""
        if not prompt_settings or not prompt_settings.get('include_context'):
            return None
            
        try:
            from ui import PromptEngineering
            prompt_engineer = PromptEngineering()
            prompt_data = prompt_engineer.get_price_analysis_prompt(make, model, year, mileage, city)
            
            client = Groq(api_key=os.getenv("API_KEY"))
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": prompt_data['system']},
                    {"role": "user", "content": prompt_data['user']}
                ],
                max_tokens=prompt_data['max_tokens'],
                temperature=prompt_settings.get('temperature', 0.3),
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error getting AI price analysis: {e}")
            return None
    
    def get_market_insights(make, model, city, prompt_settings):
        """Get market insights using enhanced prompts"""
        if not prompt_settings or not prompt_settings.get('include_context'):
            return None
            
        try:
            from ui import PromptEngineering
            prompt_engineer = PromptEngineering()
            prompt_data = prompt_engineer.get_market_insights_prompt(make, model, city)
            
            client = Groq(api_key=os.getenv("API_KEY"))
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": prompt_data['system']},
                    {"role": "user", "content": prompt_data['user']}
                ],
                max_tokens=prompt_data['max_tokens'],
                temperature=prompt_settings.get('temperature', 0.3),
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error getting market insights: {e}")
            return None
    
    # Get AI analysis if prompt engineering is enabled
    ai_price_analysis = None
    market_insights = None
    
    if prompt_settings and prompt_settings.get('include_context'):
        print("Getting AI-powered price analysis...")
        ai_price_analysis = get_ai_price_analysis(make, model, model_year, car_mileage, city, prompt_settings)
        
        print("Getting market insights...")
        market_insights = get_market_insights(make, model, city, prompt_settings)
        
        if ai_price_analysis:
            print(f"AI Price Analysis: {ai_price_analysis}")
        if market_insights:
            print(f"Market Insights: {market_insights}")

    # Filter for comparable listings with +-20000km of mileage
    subset_vehicle_df = specific_vehicle_df[
        (specific_vehicle_df['Mileage'] >= car_mileage - 20000) & (specific_vehicle_df['Mileage'] <= car_mileage + 20000)]

    #subset_vehicle_df.to_csv('subset_vehicle_data.csv', index=False)

    average_subset_vehicle_price = subset_vehicle_df['Price'].mean()

    predicted_price = (lr_predicted_price + average_subset_vehicle_price) / 2
    
    # Show results in UI popup
    vehicle_info = {
        'model_year': model_year,
        'make': make.capitalize(),
        'model': model.capitalize(),
        'car_mileage': car_mileage,
        'city': city.capitalize()
    }
    
    show_results(vehicle_info, lr_predicted_price, average_subset_vehicle_price, predicted_price, 
                len(filtered_vehicles_list), ai_price_analysis, market_insights)

if __name__ == "__main__":
    main()
