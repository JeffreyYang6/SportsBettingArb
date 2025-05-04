import pandas as pd
import importlib.util
from plyer import notification

def find_arbitrage(group, total_stake):  # Add total_stake parameter with a default value
    # Load Calculate Odds Script
    module_path = "C:\\Users\\yangj\\OneDrive - University of Waterloo\\Documents\\GitHub\\SportsBettingArb\\CalculateOdds.py"
    spec = importlib.util.spec_from_file_location("ArbCalculation", module_path)
    CO = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(CO)
    
    home_best = group['home_odds'].max()
    away_best = group['away_odds'].max()
    
    home_prob = CO.implied_probability(home_best)
    away_prob = CO.implied_probability(away_best)
    
    total_prob = home_prob + away_prob
    
    if total_prob < 1:
        home_best_bookmaker = group[group['home_odds'] == home_best]['bookmaker'].iloc[0]
        away_best_bookmaker = group[group['away_odds'] == away_best]['bookmaker'].iloc[0]
        
        # Calculate stakes
        home_stake = (home_prob / total_prob) * total_stake
        away_stake = (away_prob / total_prob) * total_stake
        potential_profit = (total_stake / total_prob) - total_stake
        
        print("About to send notification!")
        notification.notify(
            title="Arbitrage Detected!",
            message="Potential profits can be made, check your program",
        )
        
        ("Arbitrage opportunities found:")
        return pd.Series({
            'home_best_odds': home_best,
            'home_best_bookmaker': home_best_bookmaker,
            'away_best_odds': away_best,
            'away_best_bookmaker': away_best_bookmaker,
            'home_stake': round(home_stake, 2),
            'away_stake': round(away_stake, 2),
            'potential_profit': round(potential_profit, 2)
        })
        
    else:
        # print("No arbitrage opportunities found.")
        return None