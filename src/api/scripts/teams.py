from data_getters.requests import NBARequestClient, StatsRequestData, DataRequestData
from data_getters.urls.data import TEAMS
from data_getters.urls.stats import TEAM_STATS, GAME_LOG
from data_getters.util import year_num_to_str
from app.models import Season, SeasonType, Team, TeamSeason, Conference, ConferenceSeason, Division, DivisionSeason

SEASON_TYPES = ['Regular Season', 'Playoffs']


def run():
    c = NBARequestClient()
    data_teams_url = TEAMS
    stats_teams_url = TEAM_STATS

    for year in reversed(range(2016, 2021)):
        data_year_url = data_teams_url.format(year=year)
        data_rd = DataRequestData(data_year_url)
        stats_rd = StatsRequestData(stats_teams_url)
        stats_rd.params['Season'] = year_num_to_str(year)

        data_data = c.get_data(data_rd)

        for season_type in SEASON_TYPES:
            try:
                st = SeasonType.objects.get(name=season_type)
            except SeasonType.DoesNotExist:
                st = SeasonType(name=season_type)
                st.save()

            try:
                s = Season.objects.get(year=year, season_type=st)
            except Season.DoesNotExist:
                s = Season(year=year, season_type=st)
                s.save()

            stats_rd.params['SeasonType'] = season_type
            stats_data = c.get_stats(stats_rd, as_pandas=True)

            for ix, team in stats_data.iterrows():
                team_data = next(x for x in data_data['league']['standard'] if int(x['teamId']) == team['TEAM_ID'])

                try:
                    conf = Conference.objects.get(name=team_data['confName'])
                except Conference.DoesNotExist:
                    conf = Conference(name=team_data['confName'])
                    conf.save()

                try:
                    confs = ConferenceSeason.objects.get(conference=conf, season=s)
                except ConferenceSeason.DoesNotExist:
                    confs = ConferenceSeason(conference=conf, season=s)
                    confs.save()

                try:
                    div = Division.objects.get(name=team_data['divName'])
                except Division.DoesNotExist:
                    div = Division(name=team_data['divName'])
                    div.save()

                try:
                    divs = DivisionSeason.objects.get(division=div, conference=confs, season=s)
                except:
                    divs = DivisionSeason(division=div, conference=confs, season=s)
                    divs.save()

                try:
                    t = Team.objects.get(id=int(team_data['teamId']))
                except Team.DoesNotExist:
                    t = Team(id=int(team_data['teamId']))
                    t.save()

                try:
                    ts = TeamSeason.objects.get(team=t, season=s)
                except TeamSeason.DoesNotExist:
                    ts = TeamSeason(
                        team=t,
                        season=s,
                        abbreviation=team_data['tricode'],
                        division=divs,
                        city=team_data['city'],
                        nickname=team_data['nickname']
                    )
                    ts.save()

    for year in reversed(range(1996, 2017)):
        stats_rd = StatsRequestData(GAME_LOG)
        stats_rd.params['Season'] = year_num_to_str(year)

        for season_type in SEASON_TYPES:
            try:
                st = SeasonType.objects.get(name=season_type)
            except SeasonType.DoesNotExist:
                st = SeasonType(name=season_type)
                st.save()

            try:
                s = Season.objects.get(year=year, season_type=st)
            except Season.DoesNotExist:
                s = Season(year=year, season_type=st)
                s.save()

            stats_rd.params['SeasonType'] = season_type
            stats_data = c.get_stats(stats_rd, as_pandas=True)
            stats_data = stats_data.drop_duplicates(subset='TEAM_ID')

            for ix, team in stats_data.iterrows():
                try:
                    t = Team.objects.get(id=int(team['TEAM_ID']))
                except Team.DoesNotExist:
                    t = Team(id=int(team['TEAM_ID']))
                    t.save()

                team_name_split = team['TEAM_NAME'].split()
                city = ' '.join(team_name_split[:-1])
                nickname = team_name_split[-1]

                try:
                    ts = TeamSeason.objects.get(team=t, season=s)
                except TeamSeason.DoesNotExist:
                    ts = TeamSeason(
                        team=t,
                        season=s,
                        abbreviation=team['TEAM_ABBREVIATION'],
                        city=city,
                        nickname=nickname
                    )
                    ts.save()