from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

@login_required
def pong(request):
	if request.META.get('HTTP_HX_REQUEST'):
		return render(request, 'pong_block.html')
	return render(request, 'pong.html')

@login_required
def game(request, mode=None):
	context = {}
	if request.method == 'POST' and mode == 'tournament':
		context = {
			'player1': request.user.username,
			'player2': request.POST.get('player2'),
			'player3': request.POST.get('player3'),
			'player4': request.POST.get('player4'),
			'player5': request.POST.get('player5'),
			'player6': request.POST.get('player6'),
			'player7': request.POST.get('player7'),
			'player8': request.POST.get('player8'),
		}
	if request.META.get('HTTP_HX_REQUEST'):
		return render(request, 'game_block.html', context)
	return render(request, 'game.html', context)

def tournaments(request):
	if request.META.get('HTTP_HX_REQUEST'):
		return render(request, 'tournaments_choice_block.html')
	return render(request, 'tournaments_choice.html')

def catjoueurs(request):
	if request.META.get('HTTP_HX_REQUEST'):
		return render(request, '4joueurs_block.html')
	return render(request, '4joueurs.html')

def huitjoueurs(request):
	if request.META.get('HTTP_HX_REQUEST'):
		return render(request, '8joueurs_block.html')
	return render(request, '8joueurs.html')


def pongDjango(request):
	for key, value in request.POST.items():
		print(f'{key}: {value}')

	return JsonResponse({ 'message': 'pongDjango' })

def function1():
	print("Django sa mere")
	# def compute(request):
	# 	a = request.POST.get("a")
	# 	b = request.POST.get("b")
	# 	result = int(a) + int(b)
	# 	return JsonResponse({"operation_result": result})
	return 1
