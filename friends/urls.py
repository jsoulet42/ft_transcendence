"""
URL configuration for transcendence project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from .views import get_friend_requests, send_friend_request, accept_friend_request, reject_friend_request

urlpatterns = [
	path('requests/get/', get_friend_requests, name='get_friend_requests'),
	path('requests/send/', send_friend_request, name='send_friend_request'),
	path('requests/accept/<str:sender_username>/<str:receiver_username>/', accept_friend_request),
	path('requests/reject/<str:sender_username>/<str:receiver_username>/', reject_friend_request),
]