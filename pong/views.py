from django.shortcuts import render
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
	if request.META.get('HTTP_HX_REQUEST'):
		return render(request, 'game_block.html')
	return render(request, 'game.html')

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

@csrf_exempt
@login_required
def pongDjango(request):
	print(request.POST)
	function1()

	return JsonResponse({"operation_result": 1})

def function1():
	print("Django sa mere")
	# def compute(request):
	# 	a = request.POST.get("a")
	# 	b = request.POST.get("b")
	# 	result = int(a) + int(b)
	# 	return JsonResponse({"operation_result": result})
	return 1
