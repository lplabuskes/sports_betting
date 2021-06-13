import numpy as np
from kelly import kelly

odds_bov = np.array([[1.417,3.05],[2,1.833],[1.952,1.87],[1.8,2.05],[2.23,1.699],[2.3,1.667],[1.77,2.1],[1.426,3],[1.87,1.952],[1.787,2.07],[1.588,2.45],[2.12,1.758],[2.12,1.758],[1.645,2.35],[1.909,1.909]])
odds_538 = np.array([[.69,.31],[.49,.51],[.47,.53],[.48,.52],[.43,.57],[.35,.65],[.51,.49],[.65,.35],[.49,.51],[.56,.44],[.6,.4],[.43,.57],[.42,.58],[.57,.43],[.52,.48]])
teams = [['NYY','BOS'],['BAL','CLE'],['PIT','MIA'],['PHI','WAS'],['TOR','HOU'],['ATL','LAD'],['TEX','TB'],['MIL','ARI'],['CWS','DET'],['KC','MIN'],['STL','CIN'],['COL','OAK'],['LAA','SEA'],['SF','CHC'],['SD','NYM']]

recommended_bets = kelly(odds_bov,odds_538,.5)
bankroll = 1000

for bet in recommended_bets:
    amount = np.floor(4*bankroll*bet[2][0])/4
    print("{} on {} at {}".format(amount,teams[bet[0]][bet[1]],odds_bov[bet[0],bet[1]]))