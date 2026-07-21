# utilities for handling the dataset
import pandas as pd

def load_match_history(filenames, columns):
    '''Load history from a bunch of csv files as a single dataframe,
       selecting only the named columns'''
    if isinstance(filenames, str):
        filenames = [filenames]

    histories = [
        pd.read_csv(filename, usecols=columns, parse_dates=['Date'],date_format='%d/%m/%Y')
        for filename in filenames
    ]

    return (pd.concat(histories, ignore_index=True)
        .sort_values('Date')
        .reset_index(drop=True))


def get_teams(match_history):
    return set(match_history['HomeTeam']) | set(match_history['AwayTeam'])
