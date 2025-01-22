# Decimal Odds to American Odds
def decimal_to_american(decimal_odds):
    if decimal_odds < 2.0:
        return round(-100 / (decimal_odds - 1))
    else:
        return round((decimal_odds - 1) * 100)

# Returns a dictionary of the teams odds in American Odds
def compare_teams_odds(team1_name, team1_odds, team2_name, team2_odds):
    american_odds_team1 = decimal_to_american(team1_odds)
    american_odds_team2 = decimal_to_american(team2_odds)

    return {
        team1_name: american_odds_team1,
        team2_name: american_odds_team2
    }