# Generated by Django 5.0.1 on 2024-02-19 22:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0021_alter_customuser_profile_image_path_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tournament',
            name='host',
        ),
        migrations.AddField(
            model_name='customuser',
            name='tournaments',
            field=models.ManyToManyField(related_name='players', to='backend.tournament'),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='players_count',
            field=models.PositiveSmallIntegerField(choices=[(4, 4), (8, 8)], default=4),
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('game_duration', models.DurationField()),
                ('player1', models.CharField(max_length=50)),
                ('player2', models.CharField(max_length=50)),
                ('player1_score', models.PositiveSmallIntegerField(default=0)),
                ('player2_score', models.PositiveSmallIntegerField(default=0)),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='host', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='tournament',
            name='games',
            field=models.ManyToManyField(related_name='tournament_games', to='backend.game'),
        ),
        migrations.CreateModel(
            name='Leaderboard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usernames', models.JSONField()),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leaderboard_host', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='tournament',
            name='leaderboard',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='leaderboard', to='backend.leaderboard'),
        ),
        migrations.CreateModel(
            name='Stats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('games_played', models.PositiveSmallIntegerField(default=0)),
                ('tournaments_played', models.PositiveSmallIntegerField(default=0)),
                ('wins', models.PositiveSmallIntegerField(default=0)),
                ('losses', models.PositiveSmallIntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='stats', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]