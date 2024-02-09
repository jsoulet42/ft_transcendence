from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from .models import CustomUser

def get_user_name(request, user_id):
	user = CustomUser.objects.get(id=user_id)
	return JsonResponse({'name': user.name})
