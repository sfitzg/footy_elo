SCALE = 400
K = 40


def expected_home_score(home_elo, away_elo):
    # Expected home score - between 0.0 (loss) and 1.0 (win)
    return 1 / (1 + 10 ** ((away_elo - home_elo) / SCALE))


def actual_home_score(FTR):
    # Actual home score using the same scale.
    score_for_result = {
        'H' : 1.0,
        'A' : 0.0,
        'D' : 0.5,
    }
    return score_for_result[FTR]


def update_elos(home_elo, away_elo, FTR):

    # Points won by home team from away team (may be negative).
    elo_change = K * (actual_home_score(FTR) - expected_home_score(home_elo, away_elo))

    return home_elo + elo_change, away_elo - elo_change
