import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import ProcessTeamName as ptn
import ProcessTeamOdds as pto
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

    # CHANGE TO USE SQLAlchemy INSTEAD OF SQLITE
def main():
    # DO NOT SCRAPE TOO OFTEN
    url = "https://sportsbook.draftkings.com/leagues/basketball/nba"
    data = requests.get(url)

    # with open("draftkings.html", "w+", encoding="utf-8") as file:
    #     file.write(data.text)
        
    # with open("draftkings.html", "r", encoding="utf-8") as f:
    #     page = f.read()
        
    # soup = BeautifulSoup(page, "html.parser")
    data.encoding = 'utf-8'
    soup = BeautifulSoup(data.text, "html.parser")

    # odds_table = soup.find_all("tr")
    names_table = soup.find_all(class_="event-cell__name-text")
    odds_table = soup.find_all(class_="sportsbook-odds american no-margin default-color")

    # for name, odds in zip(names_table, odds_table):
    #     # print('\n---NEW TABLE---\n')
    #     # print(name.text.strip())
    #     # print(odds.text.strip())
    #     team = name.text.strip()
    #     odd = odds.text.strip()

    #     data.append({'Team': team, 'Odds': odd})
        
        
    # combined_table = pd.DataFrame(data)

    # # print(combined_table)



    # --- THIS CODE ONLY WORKS IF MONEYLINE IS NOT CLOSED FOR EVERYGAME. DO NOT RUN PROGRAM DURING LIVE ODDS OR WHEN ODDS ARE LOCKED, THE CODE WILL NOT WORK ---

    game_containers = soup.find_all(class_="sportsbook-table")
    data = []
    current_game = {}

    for container in game_containers:
        # Get all odds and teams
        name_elements = container.find_all(class_="event-cell__name-text")
        odds_elements = container.find_all(class_="sportsbook-odds american no-margin default-color")
        
        # To make sure the code only runs if there are odds for every game in the table
        if name_elements and odds_elements and len(name_elements) == len(odds_elements):
            for name_element, odds_element in zip(name_elements, odds_elements):
                team = name_element.text.strip()
                odd = odds_element.text.strip()
                if odd:
                    # CHANGE THE ODDS FROM STR TO INT
                    if len(current_game) == 0:
                        current_game['Team1'] = ptn.process_team_name(team)
                        current_game['away_odds'] = pto.convert_odds_to_int(odd)
                    else:
                        current_game['Team2'] = ptn.process_team_name(team)
                        current_game['home_odds'] = pto.convert_odds_to_int(odd)
                        current_game['bookmaker'] = "DraftKings"
                        data.append(current_game)
                        current_game = {}  # Reset for the next game

    combined_table = pd.DataFrame(data)

    # conn = sqlite3.connect('sports_odds.db')
    # combined_table.to_sql('draftkings_odds', conn, if_exists='replace', index=False)

    # # df = pd.read_sql('SELECT * FROM draftkings_odds', conn)
    # # print(df)

    # conn.close()
    
    load_dotenv()
    
    db_password = os.getenv("DB_PASSWORD")
    engine = create_engine(f"postgresql+psycopg2://postgres:{db_password}@localhost:5432/sports_odds")
    
    combined_table.to_sql(
        name="draft_kings",
        con=engine,          
        if_exists='replace',  
        index=False
    )
    
    

if __name__ == "__main__":
    main()
