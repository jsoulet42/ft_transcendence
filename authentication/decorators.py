from django.contrib.auth.models import AnonymousUser
from django.shortcuts import redirect

def not_authenticated(view_func):
	def wrapper(request, *args, **kwargs):
		if not request.user.is_authenticated:
			return view_func(request, *args, **kwargs)
		return redirect('hub')
	return wrapper
