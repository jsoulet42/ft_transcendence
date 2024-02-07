from django.urls import path
from .views import get_user_name

urlpatterns = [
	path('api/user/<int:user_id>/name/', get_user_name),
]
