#!/usr/bin/env python3

# Turn text dataset from https://github.com/openfootball/england to csv.

import os
import re
import csv
from datetime import datetime
from os.path import dirname, join

from parse_line import parse_line

# Assume working copy is at ../../england.
INPUT_ROOT=join(dirname(__file__), '../../england')
OUTPUT_ROOT=join(dirname(__file__), 'csv')

HEADER_RE = re.compile(r"#\s*(Teams|Matches)\s+(\d+)")

DATE_RE = re.compile(r"^\s*(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s+([A-Z][a-z]{2})\s+(\d{1,2})(?:\s+(\d{4}))?\s*$")

def parse_date(line, start_year):
    m = DATE_RE.match(line)
    if not m:
        return None

    month = datetime.strptime(m.group(1), '%b').month
    day = int(m.group(2))
    year = start_year + 1 if month <= 5 else start_year

    # sanity check against explicity year if given
    if m.group(3) and year != int(m.group(3)):
        raise ValueError(f'mismatched year {m.group(3)} != {year}')

    return f'{day:02d}/{month:02d}/{year}'


def convert(infile, outfile, start_year):
    #print(f'generating {outfile} from {infile}')
    team_names = set()
    match_count = 0
    current_date = None
    expected = {}
    rows = []

    with open(infile) as in_data:

        for line in in_data:
            m = HEADER_RE.match(line)
            if m:
                expected[m.group(1)] = int(m.group(2))
                continue

            date = parse_date(line, start_year)
            if date:
                current_date = date
                continue

            fields = parse_line(line)
            if fields:
                if current_date is None:
                    raise ValueError(f'Result before date in {infile}: {line.rstrip()}')
                team_names.add(fields[0])
                team_names.add(fields[1])
                match_count += 1
                rows.append([current_date, *fields])


    # Files are organised by matchday, not chronological date.
    # Postponed/rearranged fixtures appear out of order.  Fix this.
    rows.sort(key=lambda r: datetime.strptime(r[0], '%d/%m/%Y'))

    with open(outfile, 'w', newline='') as out:
        writer = csv.writer(out)
        writer.writerow(['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR'])
        writer.writerows(rows)

    if expected.get('Teams') != len(team_names):
        print(f'Warning: File header in {infile} claims {expected.get("Teams")} teams, {len(team_names)} found')

    if expected.get('Matches') != match_count:
        print(f'Warning: File header in {infile} claims {expected.get("Matches")} matches, {match_count} found')



def convert_files(infile, outfile, start_year, count):
    for year in range(start_year, start_year + count):
        season = f'{year}-{(year + 1) % 100:02d}'

        src = os.path.join(INPUT_ROOT, season, infile)
        dst = os.path.join(OUTPUT_ROOT, season, outfile)

        os.makedirs(os.path.dirname(dst), exist_ok=True)

        convert(src, dst, year)


if __name__ == '__main__':
    convert_files('1-premierleague.txt', 'premier.csv', 2015, 10)
    convert_files('2-championship.txt', 'championship.csv', 2015, 10)
    convert_files('3-league1.txt', 'league1.csv', 2015, 10)
    convert_files('4-league2.txt', 'league2.csv', 2015, 10)
    convert_files('5-nationalleague.txt', 'national.csv', 2015, 10)
