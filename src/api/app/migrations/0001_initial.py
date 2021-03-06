# Generated by Django 3.2.5 on 2021-09-05 14:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Conference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='ConferenceSeason',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.conference')),
            ],
        ),
        migrations.CreateModel(
            name='CourtLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x', models.FloatField()),
                ('y', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Division',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='DivisionSeason',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.conferenceseason')),
                ('division', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.division')),
            ],
        ),
        migrations.CreateModel(
            name='EventType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Lineup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Play',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100)),
                ('time', models.FloatField()),
                ('defense_lineup', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='defense_lineup', to='app.lineup')),
                ('event_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.eventtype')),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.courtlocation')),
                ('offense_lineup', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='offense_lineup', to='app.lineup')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('college', models.CharField(max_length=50, null=True)),
                ('country', models.CharField(max_length=50, null=True)),
                ('draft_pick', models.IntegerField(null=True)),
                ('birth_date', models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SeasonType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='TeamSeason',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('abbreviation', models.CharField(max_length=3, null=True)),
                ('city', models.CharField(max_length=50)),
                ('nickname', models.CharField(max_length=50)),
                ('division', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.divisionseason')),
                ('players', models.ManyToManyField(to='app.Player')),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.season')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.team')),
            ],
        ),
        migrations.AddField(
            model_name='season',
            name='season_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.seasontype'),
        ),
        migrations.CreateModel(
            name='Possession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('defense', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='defense', to='app.teamseason')),
                ('offense', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='offense', to='app.teamseason')),
                ('plays', models.ManyToManyField(to='app.Play')),
            ],
        ),
        migrations.CreateModel(
            name='PlayerSeason',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, null=True)),
                ('last_name', models.CharField(max_length=50, null=True)),
                ('height', models.IntegerField(null=True)),
                ('weight', models.IntegerField(null=True)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.player')),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.season')),
            ],
        ),
        migrations.CreateModel(
            name='PlayByPlay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('possessions', models.ManyToManyField(to='app.Possession')),
            ],
        ),
        migrations.AddField(
            model_name='play',
            name='player1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player1', to='app.playerseason'),
        ),
        migrations.AddField(
            model_name='play',
            name='player2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player2', to='app.playerseason'),
        ),
        migrations.AddField(
            model_name='play',
            name='player3',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player3', to='app.playerseason'),
        ),
        migrations.AddField(
            model_name='play',
            name='primary_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='primary_team', to='app.teamseason'),
        ),
        migrations.AddField(
            model_name='lineup',
            name='player1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lineup_player1', to='app.playerseason'),
        ),
        migrations.AddField(
            model_name='lineup',
            name='player2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lineup_player2', to='app.playerseason'),
        ),
        migrations.AddField(
            model_name='lineup',
            name='player3',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lineup_player3', to='app.playerseason'),
        ),
        migrations.AddField(
            model_name='lineup',
            name='player4',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lineup_player4', to='app.playerseason'),
        ),
        migrations.AddField(
            model_name='lineup',
            name='player5',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lineup_player5', to='app.playerseason'),
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('home_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='home_team', to='app.teamseason')),
                ('pbp', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.playbyplay')),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.season')),
                ('visitor_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visitor_team', to='app.teamseason')),
            ],
        ),
        migrations.AddField(
            model_name='divisionseason',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.season'),
        ),
        migrations.AddField(
            model_name='conferenceseason',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.season'),
        ),
    ]
