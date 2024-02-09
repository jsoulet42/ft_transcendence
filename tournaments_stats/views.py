from django.http import JsonResponse
from django.shortcuts import render
from authentication.views import login_required

@login_required
def tournaments_stats(request):
	if request.META.get('HTTP_HX_REQUEST'):
		return render(request, 'tournaments_stats_block.html')
	return render(request, 'tournaments_stats.html')
