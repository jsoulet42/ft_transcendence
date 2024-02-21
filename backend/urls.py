from django.urls import path
from .views import get_user_name, test_game, save_game, test_tournament, save_tournament

urlpatterns = [
	path('api/user/<int:user_id>/name/', get_user_name),
	path('game_test/', test_game),
	path('game_save/', save_game),
	path('tournament_test/', test_tournament),
	path('tournament_save/', save_tournament),
]
