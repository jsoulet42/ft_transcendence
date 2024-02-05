from django.shortcuts import render

# Create your views here.
def home(request):
	show_howtoplay = True
	return render(request, 'home.html', {'show_howtoplay': show_howtoplay})

def pong(request):
	if 'HTTP_HX_REQUEST' in request.META:
		return render(request, 'pong_block.html', {'hx_push_url': '/pong'})
	else:
		return render(request, 'pong.html')

