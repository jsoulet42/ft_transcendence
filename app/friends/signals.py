from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

from backend.models import CustomUser

@receiver(user_logged_out)
def user_logout(sender, request, **kwargs):
	user = request.user
	if user.is_authenticated:
		user.status = CustomUser.STATUS_OFFLINE
		user.save()

@receiver(user_logged_in)
def user_logout(sender, request, **kwargs):
	user = request.user
	if user.is_authenticated:
		user.status = CustomUser.STATUS_ONLINE
		user.save()