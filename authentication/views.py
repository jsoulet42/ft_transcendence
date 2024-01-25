import requests

from django.http import HttpResponse

from django.shortcuts import render, redirect
from transcendence import settings
from django.utils.http import urlencode
from django.utils.crypto import get_random_string
from django.core.exceptions import PermissionDenied

from .models import Request_cache
from hub.urls import hub

def login(request):
    if request.method == 'GET':
        if '42_login' in request.GET != None:
            Request_cache.state = get_random_string(length=32)
            api_uri = '{0}?{1}&{2}&{3}&{4}&{5}'.format(
                settings.EXTERNAL_API_AUTH_URL,
                urlencode({'client_id': settings.EXTERNAL_API_CLIENT_ID}),
                urlencode({'redirect_uri': settings.EXTERNAL_API_REDIRECT_URI}),
                urlencode({'response_type': 'code'}),
                urlencode({'scope': 'public'}),
                urlencode({'state': Request_cache.state}),
            )
            return redirect(api_uri)
    return render(request, 'login.html')

def authenticate(request):
    code = request.GET.get('code', None)
    state = request.GET.get('state', None)
    error = request.GET.get('error', None)
    
    if code == None or error != None:
        return redirect('login')
    if state == None or state != Request_cache.state:
        raise PermissionDenied

    api_uri = settings.EXTERNAL_API_TOKEN_URL
    payload = {
        'grant_type': 'authorization_code',
        'client_id': settings.EXTERNAL_API_CLIENT_ID,
        'client_secret': settings.EXTERNAL_API_CLIENT_SECRET,
        'code': code,
        'redirect_uri': settings.EXTERNAL_API_REDIRECT_URI,
        'state': Request_cache.state,
    }
    response = requests.post(api_uri, data = payload)
    Request_cache.state = None
    
    if response.status_code // 100 != 2:
        return HttpResponse(status=500)
    print(response.json().get('access_token'))
    return redirect('hub')