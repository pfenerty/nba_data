from app.models import Season, Game, TeamSeason

from data_getters.requests import NBARequestClient, StatsRequestData
from data_getters.urls.stats import GAME_LOG
from data_getters.util import year_num_to_str


def run():
    c = NBARequestClient()
    log_rd = StatsRequestData(GAME_LOG)
    for season in Season.objects.all().order_by('-year'):
        log_rd.params['Season'] = year_num_to_str(season.year)
        log_rd.params['SeasonType'] = season.season_type.name
        log_data = c.get_stats(log_rd, as_pandas=True)
        game_ids = log_data['GAME_ID'].unique()
        for game_id in game_ids:
            game_data = log_data[log_data['GAME_ID'] == game_id]
            home_game = game_data[game_data['MATCHUP'].str.contains(' @ ')]
            visitor_game = game_data[game_data['MATCHUP'].str.contains(' vs. ')]

            hts = TeamSeason.objects.get(season=season, team_id=home_game['TEAM_ID'])
            vts = TeamSeason.objects.get(season=season, team_id=visitor_game['TEAM_ID'])

            g = Game(
                id=game_id,
                home_team=hts,
                visitor_team=vts,
                season=season,
                date=home_game['GAME_DATE'].iloc[0].split('T')[0]
            )
            g.save()
