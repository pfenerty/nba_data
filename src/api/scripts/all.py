from .teams import run as run_teams
from .players import run as run_players
from .games import run as run_games
from .play_types import run as run_play_types


def run():
    run_teams()
    run_players()
    run_games()
    run_play_types()
