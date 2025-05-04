def process_team_name(team):
    # Split the word into parts
    parts = team.split()
    
    # Return the last part if there are multiple parts, otherwise return the team as is
    if len(parts) > 1:
        return parts[-1].capitalize()
    
    # If the team name has only one part, return it capitalized
    return team.capitalize()