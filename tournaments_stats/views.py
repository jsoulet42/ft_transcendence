from django.shortcuts import render

# Create your views here.
def tournaments_stats(request):
	return render(request, 'tournaments_stats.html')
