from django.urls import path
from .views import set_user_status, save_game, save_tournament

urlpatterns = [
    path('user/set_status/', set_user_status, name='set_user_status'),
    path('game_save/', save_game, name='game_save'),
    path('tournament_save/', save_tournament, name='tournament_save'),
]
