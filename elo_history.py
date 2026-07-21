import pandas as pd

from simple_elo import update_elos
from match_data import get_teams


def compute_elo_history(
    match_history,
    start_date,
    end_date,
    default_elo=1400,
    starting_elos=None,
):
    starting_elos = starting_elos or {}

    match_history = match_history[
        (match_history['Date'] >= start_date) &
        (match_history['Date'] < end_date)
    ]

    teams = get_teams(match_history)

    elos = {
        team: starting_elos.get(team, default_elo)
        for team in teams
    }

    history = [
        {'Date': pd.Timestamp(start_date), 'Team': team, 'Elo': elo}
        for team, elo in elos.items()
    ]

    for match in match_history.itertuples(index=False):
        home_elo = elos[match.HomeTeam]
        away_elo = elos[match.AwayTeam]

        new_home_elo, new_away_elo = update_elos(
            home_elo,
            away_elo,
            match.FTR,
        )

        elos[match.HomeTeam] = new_home_elo
        elos[match.AwayTeam] = new_away_elo

        history.extend([
            {
                'Date': match.Date,
                'Team': match.HomeTeam,
                'Elo': new_home_elo,
            },
            {
                'Date': match.Date,
                'Team': match.AwayTeam,
                'Elo': new_away_elo,
            },
        ])

    return pd.DataFrame(history)


def get_final_elos(elo_history):
    return (
        elo_history
        .groupby('Team')['Elo']
        .last()
        .to_dict()
    )
