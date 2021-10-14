import math
from typing import List

from app.models import Game, Play, PlayerSeason, Possession, EventType, TeamSeason, CourtLocation, PlayByPlay, Lineup

from data_getters.requests import NBARequestClient, StatsRequestData, DataRequestData
from data_getters.urls.data import PBP as DATA_PBP_URL
from data_getters.urls.stats import PBPV2 as STATS_PBP_URL
from data_getters.urls.stats import SHOT_DETAIL as SHOT_DETAIL_URL
from data_getters.util import format_game_id, year_num_to_str

person_type_map = {
    0: 'None',
    1: '',
    2: 'Home Team',
    3: 'Visitor Team',
    4: 'Home Player',
    5: 'Visitor Player',
    6: 'Home Coach',
    7: 'Visitor Coach'
}


def get_play_description(play):
    if play['HOMEDESCRIPTION']:
        return play['HOMEDESCRIPTION']
    elif play['VISITORDESCRIPTION']:
        return play['VISITORDESCRIPTION']
    else:
        return play['NEUTRALDESCRIPTION']


class PlayObj:
    desc1: str
    desc2: str
    desc3: str
    team: str
    etype: int
    p1: int
    p2: int
    p3: int

    period: int
    time: float

    x: float
    y: float

    offense_lineup: List[int]
    defense_lineup: List[int]

    @staticmethod
    def from_stats(p, home_id, visitor_id):
        play = PlayObj()

        play.etype = int(p['EVENTMSGTYPE'])

        if p['PERSON1TYPE'] in [2, 3]:
            play.team = p['PLAYER1_ID']
        else:
            play.team = None if math.isnan(p['PLAYER1_TEAM_ID']) else int(p['PLAYER1_TEAM_ID'])

        if play.team == int(home_id):
            play.desc1 = p['HOMEDESCRIPTION']
            play.desc2 = p['VISITORDESCRIPTION']
            play.desc3 = p['NEUTRALDESCRIPTION']
        elif play.team == int(visitor_id):
            play.desc1 = p['VISITORDESCRIPTION']
            play.desc2 = p['HOMEDESCRIPTION']
            play.desc3 = p['NEUTRALDESCRIPTION']
        else:
            play.desc1 = p['NEUTRALDESCRIPTION']
            play.desc2 = p['HOMEDESCRIPTION']
            play.desc3 = p['VISITORDESCRIPTION']

        if play.desc1 is None and play.desc2 is not None:
            play.desc1 = play.desc2
            play.desc2 = None

        if p['PERSON1TYPE'] in [4, 5]:
            play.p1 = None if p['PLAYER1_ID'] == 0 else int(p['PLAYER1_ID'])
        if p['PERSON2TYPE'] in [4, 5]:
            if p['PLAYER2_TEAM_ID'] == p['PLAYER1_TEAM_ID']:
                play.p2 = None if p['PLAYER2_ID'] == 0 else int(p['PLAYER2_ID'])
            else:
                play.p3 = None if p['PLAYER2_ID'] == 0 else int(p['PLAYER2_ID'])
        if p['PERSON3TYPE'] in [4, 5]:
            if p['PLAYER3_TEAM_ID'] == p['PLAYER1_TEAM_ID'] and not hasattr(play, 'p2'):
                play.p2 = None if p['PLAYER3_ID'] == 0 else int(p['PLAYER3_ID'])
            else:
                play.p3 = None if p['PLAYER3_ID'] == 0 else int(p['PLAYER3_ID'])

        if not hasattr(play, 'p2'):
            play.p2 = None
        if not hasattr(play, 'p3'):
            play.p3 = None

        play.x = None if math.isnan(p['LOC_X']) else float(p['LOC_X'])
        play.y = None if math.isnan(p['LOC_Y']) else float(p['LOC_Y'])

        period_length = (12 if p['PERIOD'] < 5 else 5) * 60
        pc_time_string_split = p['PCTIMESTRING'].split(':')
        time_left_in_period = int(pc_time_string_split[0]) * 60 + float(pc_time_string_split[1])
        play.time = float(int(period_length) - int(time_left_in_period))
        play.period = int(p['PERIOD'])
        return play

    @staticmethod
    def from_data(data, period):
        play = PlayObj()
        play.team = None if data['tid'] == 0 else int(data['tid'])
        play.etype = int(data['etype'])
        play.desc1 = data['de']
        play.desc2 = None
        play.desc3 = None
        if data['pid'] != data['tid']:
            play.p1 = None if data['pid'] == 0 else int(data['pid'])
        else:
            play.p1 = None
        play.p2 = None if data['epid'] == '' else int(data['epid'])
        play.p3 = None if data['opid'] == '' else int(data['opid'])
        play.x = data['locX']
        play.y = data['locY']

        period_length = (12 if period < 5 else 5) * 60
        pc_time_string_split = data['cl'].split(':')
        time_left_in_period = int(pc_time_string_split[0]) * 60 + float(pc_time_string_split[1])
        play.time = float(int(period_length) - float(time_left_in_period))
        play.period = int(period)
        return play

    def indicates_offense(self):
        if self.etype in [1, 2, 5]:
            return True
        elif self.etype == 3 and 'technical' not in self.desc1.lower():
            return True
        else:
            return False

    def indicates_possession_end(self):
        if self.etype in [1, 5, 13]:
            return True
        elif self.etype == 3 and 'technical' not in self.desc1.lower():
            desc_split = self.desc1.split(' ')
            of_index = desc_split.index('of')
            ft_num = desc_split[of_index - 1]
            num_ft = desc_split[of_index + 1]
            return ft_num == num_ft and 'MISS' not in self.desc1
        else:
            return False

    def is_player_action(self):
        if self.etype in [1, 2, 3, 4, 5, 10]:
            return True
        elif self.etype == 6 and 'technical' not in self.desc1.lower():
            return True
        else:
            return False


class PossObj:
    plays: List[PlayObj]

    def __init__(self):
        self.plays = []


def get_players_on_court(period_plays: List[PlayObj], team_id: int):
    plays = [x for x in period_plays if x.team == team_id]
    starters = []
    subs = []
    for play in plays:
        if play.is_player_action():
            if play.p1 is not None and play.p1 not in starters and play.p1 not in subs:
                starters.append(play.p1)
                if len(starters) == 5:
                    break
            if play.p2 is not None and play.p2 not in starters and play.p2 not in subs:
                starters.append(play.p2)
                if len(starters) == 5:
                    break
        if play.etype == 8:
            subs.append(play.p2)
            if play.p1 not in starters and play.p1 not in subs:
                starters.append(play.p1)
                if len(starters) == 5:
                    break
    return starters


def run():
    c: NBARequestClient = NBARequestClient()
    games: List[Game] = Game.objects.filter(pbp=None, season__year__lt=2015)
    for game in games:
        plays = []
        home_team_id = game.home_team.team.id
        visitor_team_id = game.visitor_team.team.id

        if game.season.year < 2016:
            stats_pbp_rd = StatsRequestData(STATS_PBP_URL)
            stats_pbp_rd.params['GameID'] = format_game_id(game.id)
            stats_pbp_data = c.get_stats(stats_pbp_rd, as_pandas=True)

            shot_detail_rd = StatsRequestData(SHOT_DETAIL_URL)
            shot_detail_rd.params['GameID'] = format_game_id(game.id)
            shot_detail_rd.params['Season'] = year_num_to_str(game.season.year)
            shot_detail_rd.params['SeasonType'] = game.season.season_type.name
            shot_detail_data = c.get_stats(shot_detail_rd, as_pandas=True)

            stats_pbp_data = stats_pbp_data.merge(shot_detail_data[['GAME_EVENT_ID', 'LOC_X', 'LOC_Y']],
                                                  left_on='EVENTNUM',
                                                  right_on='GAME_EVENT_ID', how='left')

            for ix, play in stats_pbp_data.iterrows():
                plays.append(PlayObj.from_stats(play, home_team_id, visitor_team_id))
        else:
            data_pbp_url = DataRequestData(DATA_PBP_URL.format(year=game.season.year, game_id=format_game_id(game.id)))
            data_pbp_data = c.get_data(data_pbp_url)
            for period in data_pbp_data['g']['pd']:
                for play in period['pla']:
                    plays.append(PlayObj.from_data(play, period['p']))

        current_possession = None
        current_offense = None
        possession_objs = []

        home_player_ids_on_court = []
        visitor_player_ids_on_court = []

        for play in plays:

            if play.etype == 12:
                plays_in_period = [x for x in plays if x.period == play.period]
                home_player_ids_on_court = get_players_on_court(plays_in_period, home_team_id)
                visitor_player_ids_on_court = get_players_on_court(plays_in_period, visitor_team_id)

            if play.etype == 8:
                if play.team == home_team_id:
                    home_player_ids_on_court.remove(play.p1)
                    home_player_ids_on_court.append(play.p2)
                else:
                    visitor_player_ids_on_court.remove(play.p1)
                    visitor_player_ids_on_court.append(play.p2)

            if current_possession is None:
                current_possession = PossObj()

            if play.indicates_offense():
                current_offense = play.team

            if play.indicates_possession_end() or (play.etype == 'Rebound' and play.team != current_offense):
                possession_objs.append(current_possession)
                current_possession = PossObj()

            if current_offense == home_team_id:
                play.offense_lineup = sorted(home_player_ids_on_court)
                play.defense_lineup = sorted(visitor_player_ids_on_court)
            else:
                play.offense_lineup = sorted(visitor_player_ids_on_court)
                play.defense_lineup = sorted(home_player_ids_on_court)

            current_possession.plays.append(play)

        all_player_ids = []
        for x in possession_objs:
            for y in x.plays:
                for z in y.offense_lineup:
                    if z not in all_player_ids:
                        all_player_ids.append(z)
                for w in y.defense_lineup:
                    if w not in all_player_ids:
                        all_player_ids.append(w)
        all_players = [PlayerSeason.objects.get(season=game.season, player__id=x) for x in all_player_ids]

        possessions = []
        for ix, poss in enumerate(possession_objs):
            possession = Possession(id=f'{game.id}{ix:03}')
            possession.save()
            for jx, play in enumerate(poss.plays):
                possession_play = Play(
                    id=f'{game.id}{ix:03}{jx:02}',
                    description1=play.desc1,
                    description2=play.desc2,
                    description3=play.desc3
                )
                event_type = EventType.objects.get(id=play.etype)
                possession_play.event_type = event_type

                if play.p1 is not None:
                    possession_play.player1 = PlayerSeason.objects.get(player__id=play.p1, season=game.season)
                if play.p2 is not None:
                    possession_play.player2 = PlayerSeason.objects.get(player__id=play.p2, season=game.season)
                if play.p3 is not None:
                    possession_play.player3 = PlayerSeason.objects.get(player__id=play.p3, season=game.season)
                if play.team is not None:
                    possession_play.primary_team = TeamSeason.objects.get(team__id=play.team, season=game.season)

                try:
                    location = CourtLocation.objects.get(x=play.x, y=play.y)
                except CourtLocation.DoesNotExist:
                    location = CourtLocation(x=play.x, y=play.y)
                    location.save()

                possession_play.location = location

                if play.period < 5:
                    period_start_time = (play.period - 1) * 12 * 60
                else:
                    regulation_end_time = 4 * 12 * 60
                    ot_period = play.period - 5
                    ot_elapsed = ot_period * 5 * 60
                    period_start_time = regulation_end_time + ot_elapsed

                possession_play.time = period_start_time + play.time

                possession_play.save()
                possession.plays.add(possession_play)

            possession.save()
            possessions.append(possession)

        pbp = PlayByPlay(id=game.id)
        pbp.save()
        pbp.possessions.set(possessions)
        game.pbp = pbp
        game.save()
