from django.http import JsonResponse
from django.shortcuts import render

def tournaments_stats(request):
	if request.META.get('HTTP_HX_REQUEST'):
		return render(request, 'tournaments_stats_block.html')
	return render(request, 'tournaments_stats.html')

def tournaments_stats(request):
    string_array= ['win', 'lost', 'equality']
    return render(request, 'tournaments_stats.html', {'string_array': string_array})
