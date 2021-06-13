import numpy as np


def kelly(book_odds,win_probability,kelly_multiplier):
    # book odds are in DECIMAL format
    edges = book_odds*win_probability - 1

    # optimal kelly bets should be winning on their own, save complexity by throwing out losing bets
    winning_indices = []
    winning_edges = []
    winning_variances = []

    for i, j in np.ndindex(edges.shape):
        if edges[i, j] > 0:
            winning_indices.append([i, j])
            winning_edges.append(edges[i, j])
            variance = win_probability[i, j] * (book_odds[i, j]-1)**2 + 1 - win_probability[i, j]
            winning_variances.append(variance)

    # approximate full Kelly bets can be obtained by using a Taylor series approximation of the objective function
    n = len(winning_edges)
    A = np.zeros((n, n))
    b = np.array(winning_edges).reshape(n, 1)
    for i in range(n):
        edge_i = winning_edges[i]
        for j in range(n):
            if i == j:
                A[i, i] = winning_variances[i]
            else:
                A[i, j] = edge_i*winning_edges[j]

    # compute the recommended bets, fractional Kelly highly recommended
    kelly_bets = kelly_multiplier*(np.linalg.inv(A)@b)

    for i in range(n):
        winning_indices[i].append(kelly_bets[i])
    return winning_indices
