import requests

from django.shortcuts import render, redirect
from django.utils.http import urlencode
from django.utils.crypto import get_random_string
from django.core.exceptions import PermissionDenied

from transcendence import settings
from hub.urls import hub
from .models import RequestCache

def login(request):
	if request.META.get('HTTP_HX_REQUEST'):
		return render(request, 'login_block.html')

	if request.method == 'GET':
		if '42auth' in request.GET != '':
			RequestCache.state = get_random_string(length=32)
			url = '{0}?{1}&{2}&{3}&{4}&{5}'.format(
				settings.EXTERNAL_API_AUTH_URL,
				urlencode({'client_id': settings.EXTERNAL_API_CLIENT_ID}),
				urlencode({'redirect_uri': settings.EXTERNAL_API_REDIRECT_URI}),
				urlencode({'response_type': 'code'}),
				urlencode({'scope': 'public'}),
				urlencode({'state': RequestCache.state}),
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
    if state == None or state != RequestCache.state:
        raise PermissionDenied

    payload = {
        'grant_type': 'authorization_code',
        'client_id': settings.EXTERNAL_API_CLIENT_ID,
        'client_secret': settings.EXTERNAL_API_CLIENT_SECRET,
        'code': code,
        'redirect_uri': settings.EXTERNAL_API_REDIRECT_URI,
        'state': RequestCache.state,
    }
    response = requests.post(settings.EXTERNAL_API_TOKEN_URL, data = payload)
    RequestCache.state = None

    if response.status_code // 100 != 2:
        return HttpResponse(status = 500)
    store_token_user(request, response.json().get('access_token'))
    return redirect('hub')

def store_token_user(request, access_token):

    print(access_token)
