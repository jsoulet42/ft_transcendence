from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from authentication.views import login_required

@login_required
def pong(request):
	if request.META.get('HTTP_HX_REQUEST'):
		return render(request, 'pong_block.html')
	return render(request, 'pong.html')

def game(request):
	if request.META.get('HTTP_HX_REQUEST'):
		return render(request, 'game_block.html')
	return render(request, 'game.html')

@csrf_exempt
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
