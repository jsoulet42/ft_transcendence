from django.shortcuts import render, redirect

# Create your views here.
def hub(request):
	return render(request, 'hub.html')