from django.db import models


# Create your models here.
class SeasonType(models.Model):
    name = models.CharField(max_length=50)


class Season(models.Model):
    year = models.IntegerField()
    season_type = models.ForeignKey(SeasonType, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('year', 'season_type')


class Player(models.Model):
    id = models.BigIntegerField(primary_key=True)
    college = models.CharField(max_length=50, null=True)
    country = models.CharField(max_length=50, null=True)
    draft_pick = models.IntegerField(null=True)
    birth_date = models.DateField(null=True)


class PlayerSeason(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    height = models.IntegerField(null=True)
    weight = models.IntegerField(null=True)

    class Meta:
        unique_together = ('player', 'season')


class Conference(models.Model):
    name = models.CharField(max_length=10)


class ConferenceSeason(models.Model):
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)


class Division(models.Model):
    name = models.CharField(max_length=20)


class DivisionSeason(models.Model):
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    conference = models.ForeignKey(ConferenceSeason, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)


class Team(models.Model):
    id = models.BigIntegerField(primary_key=True)


class TeamSeason(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    abbreviation = models.CharField(max_length=3, null=True)
    division = models.ForeignKey(DivisionSeason, on_delete=models.CASCADE, null=True)
    city = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50)
    players = models.ManyToManyField(Player)

    class Meta:
        unique_together = ('team', 'season')


class EventType(models.Model):
    name = models.CharField(max_length=50)


class CourtLocation(models.Model):
    x = models.FloatField()
    y = models.FloatField()

    class Meta:
        unique_together = ('x', 'y')


class Lineup(models.Model):
    player1 = models.ForeignKey(PlayerSeason, on_delete=models.CASCADE, related_name='lineup_player1')
    player2 = models.ForeignKey(PlayerSeason, on_delete=models.CASCADE, related_name='lineup_player2')
    player3 = models.ForeignKey(PlayerSeason, on_delete=models.CASCADE, related_name='lineup_player3')
    player4 = models.ForeignKey(PlayerSeason, on_delete=models.CASCADE, related_name='lineup_player4')
    player5 = models.ForeignKey(PlayerSeason, on_delete=models.CASCADE, related_name='lineup_player5')

    class Meta:
        unique_together = ('player1', 'player2', 'player3', 'player4', 'player5')


class Play(models.Model):
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE)
    location = models.ForeignKey(CourtLocation, on_delete=models.CASCADE, null=True)
    description1 = models.CharField(max_length=200)
    description2 = models.CharField(max_length=200, null=True)
    description3 = models.CharField(max_length=200, null=True)
    primary_team = models.ForeignKey(TeamSeason, on_delete=models.CASCADE, related_name='primary_team', null=True)
    player1 = models.ForeignKey(PlayerSeason, on_delete=models.CASCADE, related_name='player1', null=True)
    player2 = models.ForeignKey(PlayerSeason, on_delete=models.CASCADE, related_name='player2', null=True)
    player3 = models.ForeignKey(PlayerSeason, on_delete=models.CASCADE, related_name='player3', null=True)
    time = models.FloatField()

    offense_lineup = models.ForeignKey(Lineup, on_delete=models.CASCADE, related_name='offense_lineup', null=True)
    defense_lineup = models.ForeignKey(Lineup, on_delete=models.CASCADE, related_name='defense_lineup', null=True)


class Possession(models.Model):
    offense = models.ForeignKey(TeamSeason, on_delete=models.CASCADE, related_name='offense', null=True)
    defense = models.ForeignKey(TeamSeason, on_delete=models.CASCADE, related_name='defense', null=True)
    plays = models.ManyToManyField(Play)


class PlayByPlay(models.Model):
    possessions = models.ManyToManyField(Possession)


class Game(models.Model):
    id = models.BigIntegerField(primary_key=True)
    home_team = models.ForeignKey(TeamSeason, on_delete=models.CASCADE, related_name='home_team')
    visitor_team = models.ForeignKey(TeamSeason, on_delete=models.CASCADE, related_name='visitor_team')
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    date = models.DateField()
    pbp = models.OneToOneField(PlayByPlay, on_delete=models.CASCADE, null=True)
