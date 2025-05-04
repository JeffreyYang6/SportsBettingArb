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
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv


def main():
    
    # To import odds conversion
    module_path = "C:\\Users\\yangj\\OneDrive - University of Waterloo\\Documents\\GitHub\\SportsBettingArb\\CalculateOdds.py"
    spec = importlib.util.spec_from_file_location("CalculateOdds", module_path)
    CO = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(CO)

    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless") 

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    url = "https://sports.on.betmgm.ca/en/sports/basketball-7/betting/usa-9/nba-6004"
    driver.get(url)

    # TESTING TO SEE THE DOM
    # url = requests.get(url)
    # with open("BetMGM.html", "w+", encoding="utf-8") as file:
    #     file.write(url.text)

    game_class = "grid-event grid-six-pack-event ms-active-highlight two-lined-name ng-star-inserted"

    # Wait for the content to load
    try:
        # MIGHT BE AN ERROR HERE LOOK INTO IT
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "custom-odds-value-style"))
        )
        # This does not work
        # WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.CLASS_NAME, game_class))
        # )
    except Exception as e:
        print(f"Failed to load content: {e}")
        driver.quit()
        return

    # Randomizes sleep time from 4 to 5 sec
    time.sleep(random.uniform(4, 5))

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    data = []
    current_game = {}

    game_containers = soup.find_all(class_="grid-event grid-six-pack-event ms-active-highlight two-lined-name ng-star-inserted")

    # print(game_containers)
    
    for game in game_containers:
        # Extract name and odds
        name_elements = game.find_all(class_="participant ng-star-inserted")
        odds_elements = game.find_all(class_="custom-odds-value-style ng-star-inserted")
        
        # Testing
        # print(name_elements)
        # print(odds_elements)
        # print(len(name_elements))
        # print(len(odds_elements))
        
        # Game exists, and each team has odds (odds are not locked), live odds might break code
        if name_elements and odds_elements and (len(name_elements) == 2 and len(odds_elements) == 7):
            # print("\n")
            # print("---NEW GAME---")
            # Display team with odds
            for i in range(len(name_elements)):
                # print(f"Team: {name_elements[i].text.strip()}")
                # # To target moneyline column
                # print(f"Odds: {CO.decimal_to_american(float(odds_elements[i+5].text.strip()))}")
                
                if i == 0:
                    # Team 1
                    current_game["Team1"] = ptn.process_team_name(name_elements[i].text.strip())
                    current_game["away_odds"] = CO.decimal_to_american(float(odds_elements[i+5].text.strip()))
                else:
                    # Team 2
                    current_game["Team2"] = ptn.process_team_name(name_elements[i].text.strip())
                    current_game["home_odds"] = CO.decimal_to_american(float(odds_elements[i+5].text.strip()))
                    current_game["bookmaker"] = "BetMGM"
                    data.append(current_game)
                    # Clear the game
                    current_game = {}

                
        else:
            continue

    games_df = pd.DataFrame(data)
    # print(games_df)

    # # Close the browser
    # driver.quit()
    
    # conn = sqlite3.connect('sports_odds.db')
    # games_df.to_sql('betMGM_odds', conn, if_exists='replace', index=False)
    
    # # df = pd.read_sql('SELECT * from betMGM_odds', conn)
    # # print(df)
    
    # conn.close()
    
    load_dotenv()
    
    db_password= os.getenv("DB_PASSWORD")
    
    engine = create_engine(f"postgresql+psycopg2://postgres:{db_password}@localhost:5432/sports_odds")
    
    games_df.to_sql(
        name="bet_mgm",
        con=engine,          
        if_exists='replace',  
        index=False
    )
    
if __name__ == "__main__":
    main()