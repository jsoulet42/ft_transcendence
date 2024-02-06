from django.shortcuts import render

# Create your views here.
def home(request):
	show_howtoplay = True
	return render(request, 'home.html')
