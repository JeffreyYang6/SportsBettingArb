def decimal_to_american(decimal_odds):
    if decimal_odds < 2.0:
        # Handle division by zero
        if decimal_odds == 1:
            return 100
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

# Determines the implied probability in terms of the odds
def implied_probability(american_odds):
    if american_odds > 0:
        return 100 / (american_odds + 100)
    else:
        return abs(american_odds) / (abs(american_odds) + 100)