from django.urls import path
from .views import get_user_name, save_game, save_tournament, test_tournament

urlpatterns = [
	path('api/user/<int:user_id>/name/', get_user_name),
	path('game/save/', save_game, name='save_game'),
	path('tournament/save/', save_tournament, name='save_tournament'),
	path('tournament/test/', test_tournament, name='test_tournament'),
]
