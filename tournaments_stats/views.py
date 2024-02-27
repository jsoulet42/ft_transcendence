from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from backend.models import Stats
from django.utils.html import json_script
from django.template.loader import render_to_string

@login_required
def tournaments_stats(request):
	tournaments = request.user.tournaments.all()

	users_stats = Stats.objects.all()

	# Préparer les données dans un format approprié pour l'envoi au template
	data_for_template = []
	for stats in users_stats:
		# try:
		# 	username = stats.user.username
		# except Stats.user.RelatedObjectDoesNotExist:
		# 	username = "N/A"
		data_for_template.append({
			'username' : stats.user.username,
			'victoires': stats.wins,
			'defaites': stats.losses,
		})

	context = {'users_stats': data_for_template}
	context['tournaments'] = tournaments

	if request.META.get('HTTP_HX_REQUEST'):
		return render(request, 'tournaments_stats_block.html', context)
	return render(request, 'tournaments_stats.html', context)

