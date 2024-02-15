import requests

from django.shortcuts import render, redirect
from django.utils.http import urlencode
from django.utils.crypto import get_random_string
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.http import HttpResponse
from backend.models import CustomUser, UsersList
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from transcendence import settings
from .models import RequestCache
from .decorators import not_authenticated

@not_authenticated
def login(request):
	if request.META.get('HTTP_HX_REQUEST'):
		return render(request, 'login_block.html')

	if request.method == 'GET' and '42auth' in request.GET != '':
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

@login_required
def logout(request):
	auth_logout(request)
	return redirect('hub')

#~recuperation des donnees du formulaire de login
def custom_auth(request):
	code = request.GET.get('code', None)
	state = request.GET.get('state', None)
	error = request.GET.get('error', None)

	if error != None:
		return render(request, 'login.html', {'error': 'Failed 42 authentication'})
	if code == None or state == None or state != RequestCache.state:
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
		return render(request, 'login.html', {'error': 'Failed 42 authentication'})

	user = store_token_user(request, response.json().get('access_token'))
	if user == None:
		return render(request, 'login.html', {'error': 'Failed 42 authentication'})

	auth_login(request, user)

	return redirect('hub')

def store_token_user(request, access_token):
	response = requests.get(
		settings.EXTERNAL_API_USER_URL,
		headers = {
			'Authorization': 'Bearer ' + access_token,
		})

	if response.status_code // 100 != 2:
		return None

	json_response = response.json()
	user_login = json_response.get('login')
	campus_name = json_response.get('campus')[0].get('name')

	campuslist, created = UsersList.objects.get_or_create(name = campus_name)

	try:
		user = CustomUser.objects.get(username = user_login)
	except ObjectDoesNotExist:
		user = CustomUser.objects.create_user(
			username = json_response.get('login'),
			list = campuslist,
			password = None,
		)

	user.photo_medium_url = json_response.get('image').get('versions').get('medium')
	user.photo_small_url = json_response.get('image').get('versions').get('small')
	user.save()
	return user
