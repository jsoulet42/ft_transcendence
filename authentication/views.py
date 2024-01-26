from django.shortcuts import render, redirect
from transcendence import settings
from django.utils.http import urlencode
from hub.urls import hub
from django.utils.crypto import get_random_string
from .models import Caches


def login(request):
	if request.method == 'GET':
		if '42auth' in request.GET != '':
			Caches.state = get_random_string(length=32)
			url = '{0}?{1}&{2}&{3}&{4}&{5}'.format(
				settings.EXTERNAL_API_URL,
				urlencode({'client_id': settings.EXTERNAL_API_CLIENT_ID}),
				urlencode({'redirect_uri': settings.EXTERNAL_API_REDIRECT_URI}),
				urlencode({'response_type': 'code'}),
				urlencode({'scope': 'public'}),
				urlencode({'state': Caches.state}),
			)
			return redirect(url)
	return render(request, 'login.html')

#~recuperation des donnees du formulaire de login
def authenticate(request):
	if not request.GET.get('code') or not request.GET.get('state'):
		return redirect('login')
	code = request.GET.get('code')
	state2 = request.GET.get('state')
	if state2 != Caches.state:
		return redirect('pong')
	return redirect('hub')
