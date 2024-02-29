import json

from backend.models import CustomUser
from django.shortcuts import redirect
from django.utils import timezone

from transcendence import settings


class UserSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Votre logique pour associer l'utilisateur personnalisé à l'objet request
        # Par exemple, si vous stockez l'ID de l'utilisateur dans les sessions
        # et que vous souhaitez charger l'utilisateur à partir de cet ID
        user_id = request.session.get('user_id')
        if user_id and not isinstance(request.user, CustomUser):
            request.user = CustomUser.objects.get(uuid=user_id)
        return self.get_response(request)


class SessionExpiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Vérifie si la session a expiré
        expiry_time_iso = request.session.get('session_expiry')

        if expiry_time_iso is not None:
            if timezone.now() > timezone.datetime.fromisoformat(expiry_time_iso):
                request.META['force_reload'] = 'True'
                print(request.META.get('force_reload'))
                return redirect(settings.SESSION_EXPIRED_REDIRECT_URL)

        response = self.get_response(request)

        return response
