import requests

# USE API

url = "https://on.sportsbook.fanduel.ca/navigation/nba"
data = requests.get(url)

with open("fanduel.html", "w+", encoding="utf-8") as file:
    file.write(data.text)