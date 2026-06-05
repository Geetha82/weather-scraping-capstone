import csv
import os
import ssl
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Bypass local Mac SSL certificate check errors
if not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
    ssl._create_default_https_context = ssl._create_unverified_context

def scrape_to_exact_template():
    # 1. Establish clear absolute folder pathways
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(os.path.join(base_dir, 'data'), exist_ok=True)
    csv_file_path = os.path.join(base_dir, 'data', 'raw_weather.csv')
    
    url = "https://timeanddate.com/weather/"
    print(f"Connecting via Selenium to live endpoint: {url}...")
    
    driver = None
    try:
        # 2. Configure Selenium with browser headers
        options = Options()
        options.add_argument("--headless=new") # Run in the background
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36")
        
        # 3. Boot Selenium and instantly grab the live HTML content
        service = Service()
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)
        
        # time delay to populate on page
        time.sleep(3)
        html_content = driver.page_source
        print("Live page HTML captured successfully. closing browser session...")
        
        # shut down the browser immediately to prevent crashing the window
        driver.quit()
        driver = None

        # 4. scrape elements from the live HTML content
        cities = re.findall(r'<td><a href="/weather/[^"]+">([^<]+)</a></td>', html_content)
        metrics = re.findall(r'<td class="rbi">([^<]+)</td>', html_content)
        
        # 5. Fallback regex layout to handle timeanddate  header modification dynamically
        if not cities:
            cities = re.findall(r'href="/weather/[^>]+>([^<]+)</a>', html_content)
            
        print(f"Extracted {len(cities)} cities and {len(metrics)} weather metrics dynamically!")

        if not cities or not metrics:
            print("Error: Firewalls blocked the text arrays. Please rerun the script.")
            return

        # 6. Stream real scraped elements down to the raw data file
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Country', 'City', 'Temperature', 'Humidity', 'Condition'])
            
            # Loop through the scraped data dynamically
            for i, city_raw in enumerate(cities):
                city_raw = city_raw.strip()
                country = "Global Hub"
                
                if "," in city_raw:
                    city, country = [x.strip() for x in city_raw.split(",", 1)]
                else:
                    city = city_raw
                    
                # TimeAndDate stores data rows sequentially: [Temp 1, Condition 1, Temp 2, Condition 2...]
                temp_idx = i * 2
                cond_idx = (i * 2) + 1
                
                if cond_idx < len(metrics):
                    temperature = metrics[temp_idx].strip()
                    condition = metrics[cond_idx].strip()
                    writer.writerow([country, city, temperature, "N/A", condition])
                
        print(f" Success! Raw storage file created with rows retrieved directly from the URL.")
        
    except Exception as e:
        print(f"Selenium Pipeline Error: {e}")
    finally:
        if driver is not None:
            driver.quit()

if __name__ == "__main__":
    scrape_to_exact_template()
