import requests
import json

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

from .models import CustomUser, Leaderboard, Game, Tournament

def get_user_name(request, user_id):
	user = CustomUser.objects.get(id=user_id)
	return JsonResponse({'name': user.name})

def test_game(request):
	data = {
		'game_duration': '00:10:00',
		'host_username': 'lolefevr',
		'player1': 'lolefevr',
		'player2': 'pos2',
		'player1_score': 2,
		'player2_score': 1,
	}
	headers = {'Content-Type': 'application/json'}
	response = requests.post('http://localhost:8000/backend/game_save/', data=json.dumps(data), headers=headers)

	if response.status_code / 100 != 2:
		return JsonResponse({'error': 'Could not save game'})
	return JsonResponse(response.json())

def test_tournament(request):
	data = {
		'host_username': 'lolefevr',
		'tournament_name': 'test',
		'date': '2020-12-12',
		'players_count': 4,
		'leaderboard': ['lolefevr', 'pos2', 'pos3', 'pos4'],
		'games': [
			{
				'game_duration': '00:10:00',
				'host': 'lolefevr',
				'player1': 'lolefevr',
				'player2': 'pos2',
				'player1_score': 5,
				'player2_score': 1,
			},
			{
				'game_duration': '00:10:00',
				'host': None,
				'player1': 'pos3',
				'player2': 'pos4',
				'player1_score': 2,
				'player2_score': 0,
			},
		]
	}
	headers = {'Content-Type': 'application/json'}
	response = requests.post('http://localhost:8000/backend/tournament_save/', data=json.dumps(data), headers=headers)

	if response.status_code / 100 != 2:
		return JsonResponse({'error': 'Could not save tournament'})
	return JsonResponse(response.json())

@csrf_exempt
def save_game(request):
	if request.method == 'POST':
		game_duration = request.POST.get('game_duration', None)
		host_username = request.POST.get('host_username', None)
		player1 = request.POST.get('player1', None)
		player2 = request.POST.get('player2', None)
		player1_score = request.POST.get('player1_score', None)
		player2_score = request.POST.get('player2_score', None)

		# print(request.POST.get('game_duration', None))
		# data = json.loads(request.body)

		# game_duration = data.get('game_duration', None)
		# host_username = data.get('host_username', None)
		# player1 = data.get('player1', None)
		# player2 = data.get('player2', None)
		# player1_score = data.get('player1_score', None)
		# player2_score = data.get('player2_score', None)

		print(host_username)

		try:
			host = CustomUser.objects.get(username=host_username)
		except ObjectDoesNotExist:
			return JsonResponse({'error': 'Could not find game host'})

		game = Game.objects.create(
			game_duration=game_duration,
			host=host,
			player1=player1,
			player2=player2,
			player1_score=player1_score,
			player2_score=player2_score,
			tournament=None,
		)
		host.games.add(game)
		host.stats.games_played += 1

		if host.username == player1:
			if player1_score > player2_score:
				host.stats.wins += 1
			else:
				host.stats.losses += 1
		else:
			if player2_score > player1_score:
				host.stats.wins += 1
			else:
				host.stats.losses += 1
		host.stats.save()
		return JsonResponse({'success': 'Game saved'})

	return JsonResponse({'error': 'Game not saved'})

@csrf_exempt
def save_tournament(request):
	if request.method == 'POST':
		data = json.loads(request.body)

		host_username = data.get('host_username', None)
		tournament_name = data.get('tournament_name', None)
		date = data.get('date', None)
		players_count = data.get('players_count', None)
		leaderboard_json = data.get('leaderboard', None)
		games_json = data.get('games', None)

		try:
			host = CustomUser.objects.get(username=host_username)
		except ObjectDoesNotExist:
			return JsonResponse({'error': 'Could not find tournament host'})

		leaderboard = Leaderboard.objects.create(host=host)
		leaderboard.set_usernames(leaderboard_json)

		tournament = Tournament.objects.create(
			name=tournament_name,
			players_count=players_count,
			leaderboard=leaderboard
		)

		for game in games_json:
			game = Game.objects.create(
				game_duration=game.get('game_duration'),
				host=host,
				player1=game.get('player1'),
				player2=game.get('player2'),
				player1_score=game.get('player1_score'),
				player2_score=game.get('player2_score'),
			)

			game.tournament = tournament
			game.save()
			if game.host is not None:
				host.games.add(game)
				host.stats.games_played += 1
				if host.username == game.player1:
					if game.player1_score > game.player2_score:
						host.stats.wins += 1
					else:
						host.stats.losses += 1
				else:
					if game.player2_score > game.player1_score:
						host.stats.wins += 1
					else:
						host.stats.losses += 1

			tournament.games.add(game)

		host.stats.tournaments_played += 1
		host.tournaments.add(tournament)
		leaderboard.save()
		host.stats.save()
		host.save()
		return JsonResponse({'success': 'Tournament saved'})

	return JsonResponse({'error': 'Tournament not saved'})
