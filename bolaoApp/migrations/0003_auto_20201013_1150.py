# Generated by Django 2.2.16 on 2020-10-13 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bolaoApp', '0002_auto_20201008_1549'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='round',
            field=models.CharField(default='Semifinal', max_length=24),
        ),
        migrations.AlterField(
            model_name='game',
            name='goals_team_one',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='game',
            name='goals_team_two',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='game',
            name='winner',
            field=models.CharField(default='Partida Ainda Não Finalizada', max_length=24),
        ),
    ]
