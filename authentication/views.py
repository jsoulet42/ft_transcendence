import requests

from django.shortcuts import render, redirect
from django.utils.http import urlencode
from django.utils.crypto import get_random_string
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from transcendence import settings
from hub.urls import hub
from .models import RequestCache
from backend.models import User, UsersList

def login_required(view_func):
	def wrapper(request, *args, **kwargs):
		if not request.user.is_authenticated:
			return redirect('login')  # Redirige vers la page de connexion si l'utilisateur n'est pas connecté
		return view_func(request, *args, **kwargs)

	return wrapper

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
	response = requests.get(
		settings.EXTERNAL_API_USER_URL,
		headers = {
			'Authorization': 'Bearer ' + access_token,
		})
	if response.status_code // 100 != 2:
		return None
	json_response = response.json()

	user_id = json_response.get('id')
	user_login = json_response.get('login')

	campus_id = json_response.get('campus')[0].get('id')
	campus_name = json_response.get('campus')[0].get('name')

	campus = UsersList.objects.filter(name = campus_name)
	user = User.objects.filter(name = user_login)

	if not campus.exists():
		newlist = UsersList(name = campus_name)
		newlist.save()
		campus = newlist

	if not user.exists():
		newuser = User(
			name = json_response.get('login'),
			list = campus
		)
		newuser.save()
		user = newuser

	user.list = campus
	user.profile_img = json_response.get('image').get('link')
	user.save()
	return response.json()
