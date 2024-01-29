from django.shortcuts import render, redirect
from transcendence import settings
from django.utils.http import urlencode
from hub.urls import hub
from django.utils.crypto import get_random_string
from .models import Caches
from django.core.exceptions import PermissionDenied
import requests


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
	code = request.GET.get('code', None)
	state = request.GET.get('state', None)
	error = request.GET.get('error', None)

	if code == None or error != None:
		return redirect('login')
	if state == None or state != Caches.state:
		raise PermissionDenied
	payload={
		'grant_type': 'authorization_code',
		'client_id': settings.EXTERNAL_API_CLIENT_ID,
		'client_secret': settings.EXTERNAL_API_CLIENT_SECRET,
		'code': code,
		'redirect_uri': settings.EXTERNAL_API_REDIRECT_URI,
		'state': state,
	}
	response = requests.post(settings.EXTERNAL_API_TOKEN_URL, data = payload)
	if response.status_code // 100 != 2:
		return HttpResponse(status = 500)
	print(response.json().get('access_token'))
	return redirect('hub')
