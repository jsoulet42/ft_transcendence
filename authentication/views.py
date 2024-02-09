import requests

from django.shortcuts import render, redirect
from django.utils.http import urlencode
from django.utils.crypto import get_random_string
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.http import HttpResponse
from transcendence import settings
from hub.urls import hub
from .models import RequestCache
from backend.models import CustomUser, UsersList

def login_required(view_func):
	def wrapper(request, *args, **kwargs):
		if not request.user or not request.user.is_authenticated:
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
	user = store_token_user(request, response.json().get('access_token'))
	if not user:
		return HttpResponse(status = 500)
	request.session['user_id'] = str(user.uuid)
	user.is_authenticated = True
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
	#print(json_response)

	user_id = json_response.get('id')
	user_login = json_response.get('login')

	campus_id = json_response.get('campus')[0].get('id')
	campus_name = json_response.get('campus')[0].get('name')

	try:
		campus = UsersList.objects.get(name = campus_name)
	except ObjectDoesNotExist:
		newlist = UsersList(name = campus_name)
		newlist.save()
		campus = newlist

	try:
		user = CustomUser.objects.get(name = user_login)
	except ObjectDoesNotExist:
		newuser = CustomUser(
			name = json_response.get('login'),
			list = campus
		)
		newuser.save()
		user = newuser

	user.list = campus
	user.photo_medium_url = json_response.get('image').get('versions').get('medium')
	user.photo_small_url = json_response.get('image').get('versions').get('small')
	user.save()
	return user
