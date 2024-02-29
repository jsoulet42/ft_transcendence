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
from django.views.decorators.http import require_http_methods

from transcendence import settings
from .forms import CustomUserCreationForm
from .models import RequestCache
from .decorators import not_authenticated

@not_authenticated
def signup(request):
	form = CustomUserCreationForm()
	if request.method == 'POST':
		form = CustomUserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('hub')
	if request.META.get('HTTP_HX_REQUEST'):
		return render(request, 'signup_block.html', {'form': form})
	return render(request, 'signup.html', {'form': form})


@not_authenticated
def login(request):
	if request.method == 'POST':
		if '42auth' in request.POST != '':
			RequestCache.state = get_random_string(length=64)
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
			request_username = request.POST.get('username')
			user = authenticate(username=request_username, password=request.POST.get('password'))
			if user is not None:
				auth_login(request, user)
				return redirect('hub')

			context = {'error': 'Invalid username or password', 'username': request_username}
			if request.META.get('HTTP_HX_REQUEST'):
				return render(request, 'login_block.html', context)
			return render(request, 'login.html', context)

	if request.META.get('HTTP_HX_REQUEST'):
		return render(request, 'login_block.html')
	return render(request, 'login.html')

@login_required
def logout(request):
	auth_logout(request)
	request.META['reload'] = 'True'
	return redirect('hub')

#~recuperation des donnees du formulaire de login
@require_http_methods(['GET'])
def auth42(request):
	code = request.GET.get('code', None)
	state = request.GET.get('state', None)
	error = request.GET.get('error', None)

	payload = {
		'grant_type': 'authorization_code',
		'client_id': settings.EXTERNAL_API_CLIENT_ID,
		'client_secret': settings.EXTERNAL_API_CLIENT_SECRET,
		'code': code,
		'redirect_uri': settings.EXTERNAL_API_REDIRECT_URI,
		'state': RequestCache.state,
	}
	response = requests.post(settings.EXTERNAL_API_TOKEN_URL, data=payload)
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
		headers={
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
		user = CustomUser.objects.get(username=user_login)
	except ObjectDoesNotExist:
		return CustomUser.objects.create_user(
			username=user_login,
			userlist_name='42Users',
			password=None,
			email=user_email,
			campus=campus_name,
			photo_medium_url=photo_medium_url,
			photo_small_url=photo_small_url,
			profile_image_path=photo_small_url,
		)
	user.save()
	return user
