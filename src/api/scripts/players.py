import requests
import sys
import os
import django
import datetime
from data_getters.urls.data import PLAYERS
from data_getters.urls.stats import PLAYER_BIOS, PULL_UP_SHOOTING
from data_getters.requests import DataRequestData, NBARequestClient, StatsRequestData
from data_getters.util import year_num_to_str
from app.models import Player, Season, PlayerSeason

SEASON_TYPES = ['Regular Season', 'Playoffs']

def get_players_for_season_with_data(season: Season):
    c = NBARequestClient()

    stats_rd = StatsRequestData(PLAYER_BIOS)
    stats_rd.params['Season'] = year_num_to_str(season.year)
    stats_rd.params['SeasonType'] = season.season_type.name
    stats_data = c.get_stats(stats_rd, as_pandas=True)
    stats_player_ids = stats_data['PLAYER_ID'].unique()

    data_url = PLAYERS.format(year=season.year)
    data_rd = DataRequestData(data_url)
    data_data = c.get_data(data_rd)

    players = [x for x in data_data['league']['standard'] if int(x['personId']) in stats_player_ids]
    for player in players:
        try:
            p = Player.objects.get(id=player['personId'])
        except Player.DoesNotExist:
            p = Player(
                id=player['personId']
            )
            if p.college == None and len(player['collegeName']) > 0:
                p.college = player['collegeName']
            if p.country == None and len(player['country']) > 0:
                p.country = player['country']
            if p.draft_pick == None:
                try:
                    p.draft_pick = (int(player['draft']['roundNum']) - 1) * 30 + int(player['draft']['pickNum'])
                except ValueError:
                    None
            if p.birth_date == None:
                date_format = "%Y-%m-%d"
                try:
                    p.birth_date = datetime.datetime.strptime(player['dateOfBirthUTC'], date_format)
                except ValueError:
                    None
            p.save()

        try:
            ps = PlayerSeason.objects.get(player=p, season=season)
        except PlayerSeason.DoesNotExist:
            ps = PlayerSeason(player=p, season=season, first_name=player['firstName'], last_name=player['lastName'])
            try:
                ps.height = int(player['heightFeet']) * 12 + int(player['heightInches'])
            except ValueError:
                None
            try:
                ps.weight = int(player['weightPounds'])
            except ValueError:
                None
            ps.save()

def get_players_for_season_wo_data(season: Season):
    c = NBARequestClient()

    stats_rd = StatsRequestData(PLAYER_BIOS)
    stats_rd.params['Season'] = year_num_to_str(season.year)
    stats_rd.params['SeasonType'] = season.season_type.name

    for index, player in c.get_stats(stats_rd, as_pandas=True).iterrows():
        try:
            p = Player.objects.get(id=player['PLAYER_ID'])
        except Player.DoesNotExist:
            p = Player(
                id=player['PLAYER_ID']
            )
            try:
                if p.college == None and len(player['COLLEGE']) > 0:
                    p.college = player['COLLEGE']
            except Exception:
                None

            try:
                if p.country == None and len(player['COUNTRY']) > 0:
                    p.country = player['COUNTRY']
            except Exception:
                None

            if p.draft_pick == None:
                try:
                    p.draft_pick = (int(player['DRAFT_ROUND']) - 1) * 30 + int(player['DRAFT_NUMBER'])
                except (ValueError, TypeError):
                    None
            p.save()

        try:
            ps = PlayerSeason.objects.get(player=p, season=season)
        except PlayerSeason.DoesNotExist:
            ps = PlayerSeason(player=p, season=season)
            if ps.first_name == None and ps.last_name == None:
                try:
                    name = player['PLAYER_NAME'].split(' ')
                    if len(name) == 1:
                        ps.last_name = name[0]
                    else:
                        ps.first_name = name[0]
                        ps.last_name = ' '.join(name[1:])
                except Exception:
                    None

            if ps.height == None:
                try:
                    ps.height = int(player['PLAYER_HEIGHT_INCHES'])
                except (ValueError, TypeError):
                    None
            if ps.weight == None:
                try:
                    ps.weight = int(player['PLAYER_WEIGHT'])
                except (ValueError, TypeError):
                    None
            ps.save()

def get_players_for_season(season: Season):
    if season.year > 2012:
        get_players_for_season_with_data(season)
    else:
        get_players_for_season_wo_data(season)


def run():
    for season in Season.objects.all().order_by('-year'):
        get_players_for_season(season)

