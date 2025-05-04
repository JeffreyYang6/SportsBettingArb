from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import time
import random
import requests
import importlib.util
import ProcessTeamName as ptn
import re
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

def extract_all_teams(text):
    # Match 2+ capitalized word sequences
    pattern = r'[A-Z][a-z]* [A-Z][a-z]*(?: [A-Z][a-z]*)?'  
    matches = re.findall(pattern, text)
    return matches

def find_odds(span_list):
    # Find the first span tag with 'O' followed by a number, then get the previous two spans for ML odds
    for idx, span in enumerate(span_list):
        text = span.text.strip()
          # Matches 'O' followed by space and a number
        if re.match(r'^O\s+\d+.*$', text):
            if idx >= 2:  # Ensure there are at least two previous spans
                return [
                    span_list[idx-2].text.strip(),  # Previous two spans
                    span_list[idx-1].text.strip()
                ]
    return []  # Return empty list if not found

def main():
    
    options = webdriver.ChromeOptions()
    # To not open external browser
    options.add_argument("--headless")

    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    url = "https://on.betrivers.ca/?page=sportsbook&group=1000093652&type=matches#home"
    driver.get(url)

    # with open("BetRivers.html", "w+", encoding="utf-8") as file:
    #     file.write(data.text)
        
    # with open("BetRivers.html", "r", encoding="utf-8") as f:
    #     page = f.read()
    
    # print(driver.page_source)
    
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="listview-group-1000093652-events-container"]'))
        )

    except Exception as e:
        print(f"Failed to load content: {e}")
        driver.quit()
        return
    
    # Randomizes sleep time from 4 to 5 sec
    time.sleep(random.uniform(4, 5))
    
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    
    # There is only one container, so take that container (index 0)
    outer_container = soup.find_all(attrs={"data-testid": "listview-group-1000093652-events-container"})[0]
    
    data = []
    current_game = {}
        
    for game_container in outer_container:
        
        games = game_container.find_all('article', attrs={'data-testid': lambda x: x and x.startswith('listview-group-1000093652-event-')})
        
        for game in games:
            # print("\n")
            # print("---NEW GAME---")
            # print(game)
            
            # Span Tags have the odds
            span_tag = game.find_all("span")
            aria_label = game.find_all('div', attrs={'aria-label': True})
            string = aria_label[0]
            
            odds = find_odds(span_tag)
            
            # There are odds
            if odds:
                # print(odds)
                # Extracts the teams
                teams = extract_all_teams(string.text.strip())[:2]
                # print(teams)
                
                for i in range(len(odds)):
                    # Team 1
                    if i == 0:
                        current_game["Team1"] = teams[i].split(" ")[-1]
                        current_game["away_odds"] = int(odds[i])
                    else:
                    # Team 2
                        current_game["Team2"] = teams[i].split(" ")[-1]
                        current_game["home_odds"] = int(odds[i])
                        current_game["bookmaker"] = "BetRivers"
                        data.append(current_game)
                        # Clear the game
                        current_game = {}
            
            # Dont do it like this, not reliable
            # # Moneyline odds are at index 8 and 9, this occurs on same day games (CHECK THIS)
            # if (len(span_tag) == 17):
            #     print(span_tag[8].text.strip())
            #     print(span_tag[9].text.strip())
            
            # # Moneyline odds are at index 7 and 8, this occurs on future games
            # elif (len(span_tag) == 16):
            #     print(span_tag[7].text.strip())
            #     print(span_tag[8].text.strip())
            
            # # No valid odds
            # else:
            #     continue
            
            # Extract odds by checking if the next span class is O/U. Do not Scrape live odds
            
    games_df = pd.DataFrame(data)
    # print(games_df)

    # # Close the browser
    # driver.quit()
    
    # conn = sqlite3.connect('sports_odds.db')
    # games_df.to_sql('BetRivers_db', conn, if_exists="replace", index=False)
    
    # conn.close()
    
    load_dotenv()
    
    db_password= os.getenv("DB_PASSWORD")
    
    engine = create_engine(f"postgresql+psycopg2://postgres:{db_password}@localhost:5432/sports_odds")
    
    games_df.to_sql(
        name="bet_rivers",
        con=engine,          
        if_exists='replace',  
        index=False
    )
    


if __name__ == "__main__":
    main()