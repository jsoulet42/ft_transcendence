from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from authentication.views import login_required

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
	a = request.POST.get("p1")
	b = request.POST.get("p2")
	if a is None:
		a = 0
	if b is None:
		b = 0
	result = int(a) + int(b)
	return JsonResponse({"operation_result": result})


def function1():
	print("Django sa mere")
	# def compute(request):
	# 	a = request.POST.get("a")
	# 	b = request.POST.get("b")
	# 	result = int(a) + int(b)
	# 	return JsonResponse({"operation_result": result})
	return 1
