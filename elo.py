#!/usr/bin/env python3
import pandas as pd

from simple_elo import update_elos

START_ELO = 1400 # For teams with no results yet.


def award_points(home_points, away_points, FTR):
    # Compute the new points so far for home and away.
    if FTR == 'H':
        return home_points + 3, away_points
    if FTR == 'A':
        return home_points, away_points + 3
    if FTR == 'D':
        return home_points + 1, away_points + 1
    raise ValueError('Bad result: ' + FTR)


if __name__ == '__main__':

    raw_data = pd.read_csv('nl_25_26.csv')
    full_time_results = raw_data[['HomeTeam', 'AwayTeam', 'FTR']]

    print('Traditional points table')
    print('------------------------')

    # Current points for each team.
    points_table = {}

    # Walk the full time results in the original order.
    for home, away, FTR in full_time_results.itertuples(index=False):

        # Teams start with zero points.
        if home not in points_table:
            points_table[home] = 0
        if away not in points_table:
            points_table[away] = 0

        # Update the two teams' points.
        points_table[home], points_table[away] = award_points(points_table[home], points_table[away], FTR)

    # Report in descending order of final score.
    for team, points in sorted(points_table.items(), key=lambda pair: pair[1], reverse=True):
        print(team, points)


    print() # blank line

    print('Simple ELO')
    print('----------')

    # Current Elo rating for each team.
    elo_table = {}

    # Walk the full time results in the original order.
    for home, away, FTR in full_time_results.itertuples(index=False):

        if home not in elo_table:
            elo_table[home] = START_ELO
        if away not in elo_table:
            elo_table[away] = START_ELO

        # Update the two teams' Elo ratings.
        elo_table[home], elo_table[away] = update_elos(elo_table[home], elo_table[away], FTR)

    # Report in descending order of final Elo rating.
    for team, elo in sorted(elo_table.items(), key=lambda pair: pair[1], reverse=True):
        print(team, round(elo)) # nearest integer for reporting
