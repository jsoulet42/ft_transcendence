from django.shortcuts import render, redirect
from transcendence import settings
from django.utils.http import urlencode
from django.utils.crypto import get_random_string
from .models import Request_cache
from hub.urls import hub

def login(request):
    if request.method == 'GET':
        if '42_login' in request.GET != None:
            Request_cache.state = get_random_string(length=32)
            url = '{0}?{1}&{2}&{3}&{4}&{5}'.format(
                settings.EXTERNAL_API_URL_AUTH,
                urlencode({'client_id': settings.EXTERNAL_API_CLIENT_ID}),
                urlencode({'redirect_uri': settings.EXTERNAL_API_REDIRECT_URI}),
                urlencode({'response_type': 'code'}),
                urlencode({'scope': 'public'}),
                urlencode({'state': Request_cache.state}),
            )
            return redirect(url)
    return render(request, 'login.html')

def authenticate(request):
    code = request.GET.get('code', None)
    state = request.GET.get('state', None)
    error = request.GET.get('error', None)
    if code == None or error != None:
        return redirect('login')
    if state != None and state == Request_cache.state:
        Request_cache.state = None
        return redirect('hub')
    return redirect('login')