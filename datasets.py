# load all the history data as a convenience
from os import listdir
from os.path import isdir, join, dirname, abspath

from match_data import load_match_history


THIS_DIR = dirname(abspath(__file__))
HISTORY_DIR = join(THIS_DIR, 'history', 'csv')

# get the season names from the directories under 'history/csv'
SEASONS = sorted(
    name
    for name in listdir(HISTORY_DIR)
    if isdir(join(HISTORY_DIR, name))
)

COLUMNS = [ 'Date', 'HomeTeam', 'AwayTeam', 'FTR', ]


def load_league_history(league):
    filenames = [
        join(HISTORY_DIR, season, f'{league}.csv')
        for season in SEASONS
    ]
    return load_match_history(filenames, COLUMNS)


premier = load_league_history('premier')
championship = load_league_history('championship')
league1 = load_league_history('league1')
league2 = load_league_history('league2')
national = load_league_history('national')
