import csv
import os
import time
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def scrape_sp_sl20():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get("https://www.cse.lk/equity/daily-market-summary")
        time.sleep(5) 
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        for row in soup.find_all('tr'):
            if "S&P SL20" in row.text and "TRI" not in row.text:
                cols = row.find_all('td')
                if len(cols) >= 2:
                    today_value = cols[1].text.strip().replace(',', '')
                    return float(today_value)
    except Exception as e:
        print(f"Scraping failed: {e}")
    finally:
        driver.quit()
    return None

def update_csv():
    price = scrape_sp_sl20()
    if price:
        today = datetime.now().strftime('%Y-%m-%d')
        file_exists = os.path.isfile('sp_sl20_daily.csv')
        
        with open('sp_sl20_daily.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['Date', 'Price']) # Adds headers for the first run
            writer.writerow([today, price])
        print(f"Success: Added {price} for {today}")
    else:
        print("Could not find the S&P SL20 value today.")

if __name__ == "__main__":
    update_csv()
