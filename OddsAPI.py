import requests
import os
import pandas as pd
import json
from dotenv import load_dotenv
import CalculateOdds as CO

# Load the .env file
load_dotenv()

# Base URL for API endpoints
baseURL = "https://api.the-odds-api.com/"

def get_sports_odds(sport, apiKey, regions, markets):
    url = baseURL + "v4/sports/{}/odds/?apiKey={}&regions={}&markets={}".format(sport, apiKey, regions, markets)
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()  # Parse JSON response
        return data
    except requests.exceptions.HTTPError as http_err:
        return "HTTP error occurred: {}".format(http_err)
    except requests.exceptions.ConnectionError as conn_err:
        return "Connection error occurred: {}".format(conn_err)
    except requests.exceptions.Timeout as timeout_err:
        return "Timeout error occurred: {}".format(timeout_err)
    except requests.exceptions.RequestException as req_err:
        return "Request error occurred: {}".format(req_err)
    except ValueError as value_err:
        return "JSON parsing error occurred: {}".format(value_err)
    except Exception as err:
        return "An unexpected error occurred: {}".format(err)
    
data = get_sports_odds('basketball_nba', os.getenv("API_KEY"), 'us', 'h2h')

with open("OddsAPI.json", "w+") as f:
    f.write(json.dumps(data, indent=2))

print(CO.compare_teams_odds("team1", 1.23, "team2", 4.3))

# df = pd.DataFrame(data)
# print(df.head())
