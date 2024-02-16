import requests

from django.shortcuts import render, redirect
from django.utils.http import urlencode
from django.utils.crypto import get_random_string
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.http import HttpResponse
from backend.models import CustomUser, UsersList
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from transcendence import settings
from .forms import CustomUserCreationForm
from .models import RequestCache
from .decorators import not_authenticated

@not_authenticated
def signin(request):
	if request.method == 'POST':
		form = CustomUserCreationForm(request.POST)
		if form.is_valid():
			# If form is valid, create new user and sign them in
			user = form.save()
			auth_login(request, user)
			# Redirect to a success page or home page
			return redirect('hub')
	else:
		# If request method is GET, render the sign-up form
		form = UserCreationForm()
	
	# Render the sign-up form with validation errors, if any
	return render(request, 'signin.html', {'form': form})

@not_authenticated
def login(request):
	if request.META.get('HTTP_HX_REQUEST'):
		return render(request, 'login_block.html')

	if request.method == 'POST':
		if '42auth' in request.POST != '':
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
		
		if 'login-submit' in request.POST != '':
			user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
			if user is not None:
				auth_login(request, user)
				return redirect('hub')
			return render(request, 'login.html', {'error': 'Invalid username or password'})

		if 'signin' in request.POST != '':
			return signin(request)
	return render(request, 'login.html')

@login_required
def logout(request):
	auth_logout(request)
	request.META['reload'] = 'True'
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
	user_email = json_response.get('email')
	campus_name = json_response.get('campus')[0].get('name')

	photo_medium_url = json_response.get('image').get('versions').get('medium')
	photo_small_url = json_response.get('image').get('versions').get('small')
	
	try:
		user = CustomUser.objects.get(username = user_login)
	except ObjectDoesNotExist:
		return CustomUser.objects.create_user(
			username = user_login,
			userlist_name = '42Users',
			password = None,
			email = user_email,
			campus = campus_name,
			photo_medium_url = photo_medium_url,
			photo_small_url = photo_small_url,
		)

	user.email = user_email
	user.campus = campus_name
	user.photo_medium_url = photo_medium_url
	user.photo_small_url = photo_small_url
	user.save()
	return user
