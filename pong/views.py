from django.shortcuts import render

# Create your views here.
def pong(request):
	if request.META.get('HTTP_HX_REQUEST'):
		return render(request, 'pong_block.html')
	return render(request, 'pong.html')

def pong_1v1(request):
	return render(request, 'ping.html')
