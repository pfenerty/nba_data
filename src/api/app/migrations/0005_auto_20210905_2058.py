# Generated by Django 3.2.5 on 2021-09-05 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_play_primary_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='play',
            name='description1',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='play',
            name='description2',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='play',
            name='description3',
            field=models.CharField(max_length=200, null=True),
        ),
    ]