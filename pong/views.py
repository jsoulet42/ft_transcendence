from django.shortcuts import render

def pong(request):
	if request.META.get('HTTP_HX_REQUEST'):
		return render(request, 'pong_block.html')
	return render(request, 'pong/pong.html')

def game(request):
	if request.META.get('HTTP_HX_REQUEST'):
		return render(request, 'game_block.html', {'hx_push_url': '/game'})
	return render(request, 'game.html')
