from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import random

def main():
    # Set up Chrome options
    options = Options()
    options.add_argument("--headless")

    # Create a new Chrome browser instance
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    url = "https://www.on.bet365.ca/#/AC/B18/C20604387/D48/E1453/F10"
    driver.get(url)
    
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "gl-MarketGroupContainer "))
        )
    except Exception as e:
        print(f"Failed to load content: {e}")
        driver.quit()
        return
    
    # Randomizes sleep time from 4 to 5 sec
    time.sleep(random.uniform(4, 5))

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
