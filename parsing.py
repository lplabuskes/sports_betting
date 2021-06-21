from requests import get
from datetime import date

def mlb538():
    page_html = get("https://projects.fivethirtyeight.com/2021-mlb-predictions/games/").text
    team_entries = page_html.split("<tr class=\"tr\">")[1:]

    today = "{d.month}/{d.day}".format(d=date.today())
    odds = []
    teams = []

    for i in range(len(team_entries)):
        #games consist of two entries, opt to handle both with one iteration and skip the next line
        if team_entries[i].startswith("<td class=\"td td-team team\">"):
            continue

        #parse date of game and only include today's games
        game_date = team_entries[i].split("<span class=\"day short\">")[1].split("</span>")[0]
        if game_date != today:
            break

        #identify game by teams and time (to support double headers)
        game_time = team_entries[i].split("<span class=\"time\">")[1].split("<span")[0]
        away_team = team_entries[i].split("<span class=\"team-name short\">")[1].split("</span>")[0]
        home_team = team_entries[i+1].split("<span class=\"team-name short\">")[1].split("</span>")[0]

        #Extracting odds, these are messy because of 538's variable color formatting
        away_prob = team_entries[i].split("<td class=\"td number td-number win-prob\" style=\"background: rgba(237,113,58,")[1].split(")\">")[0]
        home_prob = team_entries[i+1].split("<td class=\"td number td-number win-prob\" style=\"background: rgba(237,113,58,")[1].split(")\">")[0]
        away_prob = float(away_prob)
        home_prob = float(home_prob)

        odds.append([home_prob, away_prob])
        teams.append([home_team, away_team, game_time])

    return odds, teams


if __name__ == "__main__":
    mlb538()