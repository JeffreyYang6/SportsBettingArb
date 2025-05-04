from multiprocessing import Pool
import importlib.util
import sqlite3
import pandas as pd
import time
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# DO NOT RUN WITH LIVE ODDS, IT WILL BREAK THE PROGRAM

def run_main_function(script_path):
    
    # Dynamically load the script
    spec = importlib.util.spec_from_file_location("module", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Run the main function from the script
    if hasattr(module, 'main'):
        module.main()
    else:
        print(f"No main function found in {script_path}")

def main():
    # To import Arb Calculations
    module_path = "C:\\Users\\yangj\\OneDrive - University of Waterloo\\Documents\\GitHub\\SportsBettingArb\\ArbCalculation.py"
    spec = importlib.util.spec_from_file_location("ArbCalculation", module_path)
    AC = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(AC)
    
    # Create Postgres engine
    load_dotenv()
    db_password= os.getenv("DB_PASSWORD")
    engine = create_engine(f"postgresql+psycopg2://postgres:{db_password}@localhost:5432/sports_odds")
    
    # List of Python file paths
    scripts = [
        "C:\\Users\\yangj\\OneDrive - University of Waterloo\\Documents\\GitHub\\SportsBettingArb\\NBAWebScraping\\BetMGM.py",
        "C:\\Users\\yangj\\OneDrive - University of Waterloo\\Documents\\GitHub\\SportsBettingArb\\NBAWebScraping\\DraftKings.py",
        "C:\\Users\\yangj\\OneDrive - University of Waterloo\\Documents\\GitHub\\SportsBettingArb\\NBAWebScraping\\BetRivers.py"
    ]

    # Use multiprocessing to run all main functions in parallel
    with Pool() as pool:
        pool.map(run_main_function, scripts)
        
    # Search for arb opportunities
    
    # conn = sqlite3.connect("sports_odds.db")
    # # Create a cursor object
    # cursor = conn.cursor()

    # # Query to get all table names
    # table_query = "SELECT name FROM sqlite_master WHERE type='table';"
    # cursor.execute(table_query)

    # # Fetch all table names
    # tables = cursor.fetchall()
    
    query = """
    SELECT table_name FROM information_schema.tables 
    WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
    """

    with engine.connect() as conn:
        result = conn.execute(text(query))
        tables = [row[0] for row in result]
    
    all_games_db = pd.DataFrame()
    
    for table in tables:
        try:
            df = pd.read_sql_table(table, engine)
            all_games_db = pd.concat([all_games_db, df], ignore_index=True)
        except Exception as e:
            print(f"Error reading {table}: {e}")
            
    # print('\n Main Dataframe:')
    # print(all_games_db)
    
    total_stake = 50
    
    all_games_db = all_games_db.reset_index(drop=True)
    
    groupby_obj = all_games_db.groupby(["Team1", "Team2"])
    for group_key, group_data in groupby_obj:
        team1, team2 = group_key
        print(f"\nGroup: {team1} vs {team2}")
        print(group_data)
        print("-" * 50)
    
    grouped_df = groupby_obj.apply(lambda x: AC.find_arbitrage(x, total_stake), include_groups=False).dropna()
    
    if not grouped_df.empty:
        print("Arbitrage opportunities found:")
        print(grouped_df)
    else:
        print("No Arbitrage Opportunities")
        
    # conn.close()




if __name__ == "__main__":
    while True:
        main()
        print('\n')
        print("Sleeping for 5 minutes...")
        # 10 minutes
        time.sleep(300)
        
    