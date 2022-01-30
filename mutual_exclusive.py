import numpy as np
from scipy.optimize import minimize, LinearConstraint

# Doing manual data entry because parsing is annoying and for now this is a one time calculation
team_order = ["76ers", "Bucks", "Bulls", "Cavaliers", "Celtics", "Clippers", "Grizzlies", "Hawks", "Heat", "Hornets", "Jazz", "Kings", "Knicks", "Lakers", "Magic", "Mavericks", 
              "Nets", "Nuggets", "Pacers", "Pelicans", "Pistons", "Raptors", "Rockets", "Spurs", "Suns", "Thunder", "Timberwolves", "Trail Blazers", "Warriors", "Wizards"]
odds_bov = [21.0, 7.5, 21.0, 101.0, 61.0, 41.0, 29.0, 81.0, 13.0, 101.0, 13.0, 1001.0, 251.0, 19.0, 1001.0, 51.0, 3.6, 51.0, 1001.0, 1001.0, 1001.0, 201.0, 1001.0, 1001.0, 7.0, 1001.0, 201.0, 501.0, 5.75, 301.0]
odds_538 = [.0562, .2413, .0068, .0022, .0292, .0292, .0389, .0063, .0602, .0024, .1199, 0, .0006, .0032, 0, .0274, .0921, .0375, .0007, .0006, 0, .0061, 0, .0002, .1911, 0, .0029, .0039, .0418, .0008]

# Goal is to maximize the expected log of wealth
def objective_function(bets, book_odds=odds_bov, true_odds=odds_538):
    if len(bets)!=len(book_odds) or len(book_odds)!=len(true_odds):
        raise RuntimeError("Input Sizes Do Not Match")
    
    total_bet = sum(bets)
    expectation = 0
    for i, bet in enumerate(bets):
        wealth = 1 - total_bet + bet*book_odds[i]  # 1 + sum(bet*payout)
        # print(f"{i}: {team_order[i]}, {odds_bov[i]}, {odds_538[i]}, {bet}, {wealth}")
        if wealth <= 0:
             wealth = np.finfo(np.float64).eps
        expectation += true_odds[i]*np.log(wealth)
    return -expectation  # Because the optimizer minimizes

# Gradient is easy to compute analytically
def gradient_function(bets, book_odds=odds_bov, true_odds=odds_538):
    if len(bets)!=len(book_odds) or len(book_odds)!=len(true_odds):
        raise RuntimeError("Input Sizes Do Not Match")
    
    total_bet = sum(bets)
    # This portion shows up in each element of the gradient
    persistent_term = 0
    for i, bet in enumerate(bets):
        persistent_term -= true_odds[i]/(1 - total_bet + bet*book_odds[i])
    
    varying_term = lambda i : true_odds[i]*book_odds[i]/(1 - total_bet + bets[i]*book_odds[i])
    gradient = [varying_term(i[0])+persistent_term for i in enumerate(bets)]
    return [-element for element in gradient]  # Because the optimizer minimizes

def optimize():
    book_odds = odds_bov
    true_odds = odds_538

    initial_guess = [0.01] * len(true_odds)
    bounds = [(0, 1) for i in true_odds]  # Can't be the house (<0) or leverage (>1)
    total_constraint = {'type': 'ineq', 'fun': lambda x : 1 - sum(x)}  # Sum of bets <=1

    result = minimize(objective_function, initial_guess, args=(book_odds, true_odds), jac=gradient_function, bounds=bounds, constraints=total_constraint)
    return result

if __name__ == "__main__":
    result = optimize()
    bankroll = 1000.0
    kelly_fraction = 0.5
    if result.success:
        for i, bet_fraction in enumerate(result.x):
            if bet_fraction <= 0:
                continue
            exact_bet = bankroll * kelly_fraction * bet_fraction
            rounded_bet = np.floor(4 * exact_bet) / 4
            print(f"{rounded_bet} on {team_order[i]}")