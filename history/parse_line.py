#!/usr/bin/env python3
import re

TEAM = r"[A-Za-z!&'.]+(?:\s+[A-Za-z!&'.]+)*"

def _summarize_result(h, a):
    h = int(h)
    a = int(a)
    if h > a:
        return 'H'
    if h < a:
        return 'A'
    return 'D'


def _normalize_team_name(team):
    '''
    Some teams appear with different names: Name, Name FC, Name AFC
    Strip any FC or AFC suffix.
    '''
    return re.sub(r'\s+(?:FC|AFC)$', '', team).strip()

def _parse_scoreline(s):
    'Returns pair of strings representing home, away goals'
    m = re.search(r'(\d+)-(\d+)', s)
    return (m.group(1), m.group(2)) if m else None


def _parse_team_v_team(line):
    m = re.search(rf"^({TEAM})\s+v\s+({TEAM})\b(.*)$", line)
    if not m:
        return None

    home, away, rest = m.group(1), m.group(2), m.group(3)
    score = _parse_scoreline(rest)
    if not score:
        return None

    return _normalize_team_name(home.strip()), _normalize_team_name(away.strip()), *score


def _parse_score_between_teams(line):
    # left team
    m1 = re.match(rf'^({TEAM})\b', line)
    if not m1:
        return None

    # right team (scan from end)
    m2 = re.search(rf'({TEAM})\s*$', line)
    if not m2:
        return None

    home = m1.group(1)
    away = m2.group(1)

    middle = line[m1.end():m2.start()].strip()
    score = _parse_scoreline(middle)
    if not score:
        return None

    return _normalize_team_name(home.strip()), _normalize_team_name(away.strip()), *score


def _strip_time(line):
    return re.sub(r'^\s*\d{1,2}:\d{2}\s+', '', line)


def _strip_trailing_comment(line):
    return re.sub(r'\s*\[[^\]]*\]\s*$', '', line)


def parse_line(line):
    '''
    Parse a result from one line of the raw .txt, or None if not the right shape.

    >>> parse_line('Yeovil Town             v Solihull Moors') is None
    True

    There are two general formats. Scoreline between teams:

    >>> parse_line('Bristol City             0-2 (0-1)  Derby County')
    ('Bristol City', 'Derby County', '0', '2', 'A')

    >>> parse_line('   Bristol City             2-2 (0-1)  Derby County')
    ('Bristol City', 'Derby County', '2', '2', 'D')

    >>> parse_line('Bristol City             3-2 (0-1)  Derby County')
    ('Bristol City', 'Derby County', '3', '2', 'H')

    Other format has a literal 'v' between teams, followed by scoreline:
 
    >>> parse_line('Southend United         v Altrincham FC          2-1 (1-0)')
    ('Southend United', 'Altrincham', '2', '1', 'H')

    Sometimes see a comment in square brackets - don't try to interpret it.
    >>> parse_line(' Bolton Wanderers         0-1  Brentford FC             [awarded]')
    ('Bolton Wanderers', 'Brentford', '0', '1', 'A')

    Sometimes see a leading time - ignore it.
    >>> parse_line('19:45  Swansea City             1-1 (0-1)  Derby County')
    ('Swansea City', 'Derby County', '1', '1', 'D')

    Sometimes see some complexity in the final score.  Find first hyphenated pair of numbers; lose rest
    >>> parse_line('  19:45  Nottingham Forest FC     3-2 pen. 1-2 a.e.t. (1-2, 1-0)  Sheffield United FC')
    ('Nottingham Forest', 'Sheffield United', '3', '2', 'H')

    Check that scores are compared numerically, not lexicographically
    >>> parse_line('Useless team 2-10 Decent team')
    ('Useless team', 'Decent team', '2', '10', 'A')


    '''
    line = _strip_time(line)
    line = _strip_trailing_comment(line)
    line = line.strip()
    v_result = _parse_team_v_team(line)
    if v_result:
        home, away, hg, ag = v_result
        return home, away, hg, ag, _summarize_result(hg, ag)

    no_v_result = _parse_score_between_teams(line)
    if no_v_result:
        home, away, hg, ag = no_v_result
        return home, away, hg, ag, _summarize_result(hg, ag)

    return None


if __name__ == '__main__':
    import doctest
    doctest.testmod()
