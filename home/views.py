from django.shortcuts import render

def home(request):
	show_howtoplay = True
	return render(request, 'home.html')