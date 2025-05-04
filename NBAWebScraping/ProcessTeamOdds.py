def convert_odds_to_int(odd_str):
    # Replace Unicode minus sign with standard minus sign
    odd_str = odd_str.replace('−', '-')
    
    # Remove any non-numeric characters except for the minus sign
    odd_str = odd_str.replace("+", "").replace(" ", "")
    
    try:
        # Convert to integer
        return int(odd_str)
    except ValueError:
        # If conversion fails, return the original string
        print(ValueError)
        return odd_str
