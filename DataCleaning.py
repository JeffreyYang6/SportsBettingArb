import pandas as pd
import json
import CalculateOdds as CO
import ArbCalculation as AC

with open("OddsData.json", "r") as data_file:
    odds_data = json.load(data_file)

games_data = []

for game in odds_data:
    for bookmaker in game['bookmakers']:
        for market in bookmaker['markets']:
            # Filters for only moneyline odds
            if market['key'] == 'h2h':
                home_odds = next(outcome['price'] for outcome in market['outcomes'] if outcome['name'] == game['home_team'])
                away_odds = next(outcome['price'] for outcome in market['outcomes'] if outcome['name'] == game['away_team'])
                
                games_data.append({
                    'home_team': game['home_team'],
                    'home_odds': CO.decimal_to_american(home_odds),
                    'away_team': game['away_team'],
                    'away_odds': CO.decimal_to_american(away_odds),
                    'bookmaker': bookmaker['key']
                })

# Create the DataFrame
df = pd.DataFrame(games_data)

# # Testing to see how the dataframe is structured
# df = df.groupby("home_team")
# for home_team, group in df:
#     print(f"Group for home_team: {home_team}")
    
#     # Drop the current index
#     group = group.reset_index(drop=True)
    
#     # Set 'bookmaker' as the new index
#     group = group.set_index('bookmaker')
    
#     print(group.head())
#     print("\n")

# Total stake
total_stake = 50
    
# Group Dataframe based on the game
arbitrage_opportunities = df.groupby(['home_team', 'away_team']).apply(lambda x: AC.find_arbitrage(x, total_stake), include_groups=False).dropna()

# Sort by potential profit in descending order
try:
    arbitrage_opportunities = arbitrage_opportunities.sort_values('potential_profit', ascending=False)
    
    if not arbitrage_opportunities.empty:
        print("Arbitrage opportunities found:")
        print(arbitrage_opportunities)
except Exception as e:
    # KeyError
    print(e)

# else:
#     print("No arbitrage opportunities found.")
    
