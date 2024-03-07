import json

from django.http import JsonResponse, HttpResponse, Http404
from http import HTTPStatus
from django.core.exceptions import ObjectDoesNotExist
from datetime import timedelta
from django.views.decorators.http import require_POST, require_http_methods
from django.utils.translation import gettext as _

from .models import CustomUser, Leaderboard, Game, Tournament


@require_http_methods(["PATCH"])
def set_user_status(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse(
            {'error_code': 'BAD_REQUEST', 'error_message': _('Invalid JSON')},
            status=HTTPStatus.BAD_REQUEST
        )

    username = data.get('username')
    status = data.get('status')

    if not username:
        return JsonResponse(
            {'error_code': 'MISSING_USERNAME', 'error_message': _('Missing username')},
            status=HTTPStatus.BAD_REQUEST
        )

    if not status:
        return JsonResponse(
            {'error_code': 'MISSING_STATUS', 'error_message': _('Missing status')},
            status=HTTPStatus.BAD_REQUEST
        )

    valid_statuses = dict(CustomUser.STATUS_CHOICES).keys()
    if status not in valid_statuses:
        return JsonResponse(
            {'error_code': 'INVALID_STATUS', 'error_message': _('Invalid status. Expected: ') + ', '.join(valid_statuses)},
            status=HTTPStatus.BAD_REQUEST
        )

    try:
        user = CustomUser.objects.get(username=username)
    except CustomUser.DoesNotExist:
        raise Http404(_("User not found"))

    user.status = status
    user.save()
    return HttpResponse(status=HTTPStatus.NO_CONTENT)


@require_POST
def save_game(request):
    game_duration = float(request.POST.get('game_duration', 0))
    host_username = request.POST.get('host_username', None)
    player1 = request.POST.get('player1', None)
    player2 = request.POST.get('player2', None)
    player1_score = request.POST.get('player1_score', None)
    player2_score = request.POST.get('player2_score', None)

    try:
        host = CustomUser.objects.get(username=host_username)
    except ObjectDoesNotExist:
        return JsonResponse(
            {'error_code': 'HOST_NOT_FOUND', 'error_message': _('Could not find game host')},
            status=HTTPStatus.BAD_REQUEST
        )

    game = Game.objects.create(
        game_duration=timedelta(seconds=game_duration),
        host=host,
        player1=player1,
        player2=player2,
        player1_score=player1_score,
        player2_score=player2_score,
        tournament=None,
    )
    host.games.add(game)
    host.stats.games_played += 1

    winner = player1 if player1_score > player2_score else player2

    if host.username == winner:
            host.stats.wins += 1
    else:
        host.stats.losses += 1

    host.stats.save()
    return HttpResponse(status=HTTPStatus.NO_CONTENT)


@require_POST
def save_tournament(request):
    host_username = request.POST.get('host_username', None)
    tournament_name = request.POST.get('tournament_name', None)
    players_count = request.POST.get('players_count', None)
    leaderboard_list = json.loads(request.POST.get('leaderboard', None))
    games_list = json.loads(request.POST.get('games', None))

    try:
        host = CustomUser.objects.get(username=host_username)
    except ObjectDoesNotExist:
        return JsonResponse(
            {'error_code': 'HOST_NOT_FOUND', 'error_message': _('Could not find tournament host')},
            status=HTTPStatus.BAD_REQUEST
        )

    leaderboard = Leaderboard.objects.create(host=host)
    leaderboard.set_usernames(leaderboard_list)

    tournament = Tournament.objects.create(
        name=tournament_name,
        players_count=players_count,
        leaderboard=leaderboard
    )

    for game in games_list:
        game = Game.objects.create(
            game_duration=timedelta(seconds=game.get('game_duration', 0)),
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

            winner = game.player1 if game.player1_score > game.player2_score else game.player2

            if host.username == winner:
                host.stats.wins += 1
            else:
                host.stats.losses += 1

        tournament.games.add(game)

    host.stats.tournaments_played += 1
    host.tournaments.add(tournament)
    leaderboard.save()
    host.stats.save()
    host.save()
    return HttpResponse(status=HTTPStatus.NO_CONTENT)
