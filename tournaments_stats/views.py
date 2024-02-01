from django.shortcuts import render

# Create your views here.
def tournaments_stats(request):
	if request.META.get('HTTP_HX_REQUEST'):
		return render(request, 'tournaments_stats_block.html')
	return render(request, 'tournaments_stats.html')
