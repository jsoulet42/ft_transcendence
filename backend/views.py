from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from .models import User

def get_user_name(request, user_id):
	user = User.objects.get(id=user_id)
	return JsonResponse({'name': user.name})
