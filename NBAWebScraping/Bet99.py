import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3

# DO NOT SCRAPE TOO OFTEN
url = "https://on.bet99.ca/en/sports/basketball/usa/nba/3139"
data = requests.get(url)

with open("bet99.html", "w+", encoding="utf-8") as file:
    file.write(data.text)
    
with open("bet99.html", "r", encoding="utf-8") as f:
    page = f.read()
    
soup = BeautifulSoup(page, "html.parser")

moneyline_odds = "priceblock-fd71515e"

