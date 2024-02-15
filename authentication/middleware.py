from backend.models import CustomUser

class UserSessionMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		# Votre logique pour associer l'utilisateur personnalisé à l'objet request
		# Par exemple, si vous stockez l'ID de l'utilisateur dans les sessions
		# et que vous souhaitez charger l'utilisateur à partir de cet ID
		user_id = request.session.get('user_id')
		if user_id and not isinstance(request.user, CustomUser):
			request.user = CustomUser.objects.get(uuid = user_id)
		return self.get_response(request)