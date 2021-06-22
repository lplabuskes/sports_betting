from requests import get
from datetime import date
import time
from oddsapi import KEY


def mlb_538():
    page_html = get("https://projects.fivethirtyeight.com/2021-mlb-predictions/games/").text
    team_entries = page_html.split("<tr class=\"tr\">")[1:]

    today = "{d.month}/{d.day}".format(d=date.today())
    odds = []
    teams = []

    for i in range(len(team_entries)):
        # games consist of two entries, opt to handle both with one iteration and skip the next line
        if team_entries[i].startswith("<td class=\"td td-team team\">"):
            continue

        # parse date of game and only include today's games
        game_date = team_entries[i].split("<span class=\"day short\">")[1].split("</span>")[0]
        if game_date != today:
            break

        # identify game by teams and time (to support double headers)
        game_time = team_entries[i].split("<span class=\"time\">")[1].split("<span")[0]
        away_team = team_entries[i].split("<span class=\"team-name short\">")[1].split("</span>")[0]
        home_team = team_entries[i+1].split("<span class=\"team-name short\">")[1].split("</span>")[0]

        # Extracting odds, these are messy because of 538's variable color formatting
        away_prob = team_entries[i].split("<td class=\"td number td-number win-prob\" style=\"background: rgba(237,113,58,")[1].split(")\">")[0]
        home_prob = team_entries[i+1].split("<td class=\"td number td-number win-prob\" style=\"background: rgba(237,113,58,")[1].split(")\">")[0]
        away_prob = float(away_prob)
        home_prob = float(home_prob)

        odds.append([home_prob, away_prob])
        teams.append([home_team, away_team, game_time])

    return odds, teams


def mlb_API():
    options = {"apiKey": KEY, "sport": "baseball_mlb", "region": "us"}
    games = get("https://api.the-odds-api.com/v3/odds/", params=options).json()["data"]

    odds = []
    teams = []

    for game in games:
        bovada_idx = -1
        for i in range(len(game["sites"])):
            if game["sites"][i]["site_key"] == "bovada":
                bovada_idx = i
                break
        if bovada_idx == -1:
            continue

        game_odds = game["sites"][bovada_idx]["odds"]["h2h"]
        game_teams = game["teams"]

        if game["home_team"] == game_teams[0]:
            odds.append(game_odds)
            teams.append([game_teams[0], game_teams[1], game["commence_time"]])
        else:
            odds.append([game_odds[1], game_odds[0]])
            teams.append([game_teams[1], game_teams[0], game["commence_time"]])

    return odds, teams


def combined_parsing():
    short_names = {"Arizona Diamondbacks": "ARI", "Atlanta Braves": "ATL", "Baltimore Orioles": "BAL",
                   "Boston Red Sox": "BOS", "Chicago Cubs": "CHC", "Chicago White Sox": "CWS", "Cincinnati Reds": "CIN",
                   "Cleveland Indians": "CLE", "Colorado Rockies": "COL", "Detroit Tigers": "DET", "Houston Astros": "HOU",
                   "Kansas City Royals": "KC", "Los Angeles Angels": "LAA", "Los Angeles Dodgers": "LAD",
                   "Miami Marlins": "MIA", "Milwaukee Brewers": "MIL", "Minnesota Twins": "MIN", "New York Mets": "NYM",
                   "New York Yankees": "NYY", "Oakland Athletics": "OAK", "Philadelphia Phillies": "PHI",
                   "Pittsburgh Pirates": "PIT", "San Diego Padres": "SD", "San Francisco Giants": "SF",
                   "Seattle Mariners": "SEA", "St. Louis Cardinals": "STL", "Tampa Bay Rays": "TB", "Texas Ramgers": "TEX",
                   "Toronto Blue Jays": "TOR", "Washington Nationals": "WAS"}

    odds_538, teams_538 = mlb_538()
    odds_bov, teams_bov = mlb_API()

    bov_lookup = {}

    # reformatting data from odds API so can match games with 538
    for i in range(len(teams_bov)):
        game = teams_bov[i]
        game[0] = short_names[game[0]]
        game[1] = short_names[game[1]]

        game_time = time.localtime(game[2])
        ampm = "a.m." if game_time.tm_hour < 12 else "p.m."
        hour_12 = ((game_time.tm_hour - 1) % 12) + 1
        game[2] = "{}:{:02} {}".format(hour_12, game_time.tm_min, ampm)

        bov_lookup[game] = odds_bov[i]

    final_538 = []
    final_bov = []
    final_teams = []

    # this reorders the odds so they agree with 538 and eliminates any games that bovada might not have odds for
    for i in range(len(teams_538)):
        if teams_538[i] not in bov_lookup:
            continue
        final_538.append(odds_538[i])
        final_bov.append(bov_lookup[teams_538[i]])
        final_teams.append(teams_538[i])

    return final_bov, final_538, final_teams


if __name__ == "__main__":
    mlb_538()
