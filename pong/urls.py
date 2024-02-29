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
from . import views

urlpatterns = [
    path('', views.pong, name='pong'),
    path('game/', views.game, name='game'),
    path('game/<str:mode>/', views.game, name='game_with_mode'),
    path('pongDjango/', views.pongDjango, name='pongDjango'),
    path('tournaments/', views.tournaments, name='tournaments'),
    path('tournaments/catjoueurs/', views.catjoueurs, name='catjoueurs'),
    path('tournaments/huitjoueurs/', views.huitjoueurs, name='huitjoueurs'),
]
