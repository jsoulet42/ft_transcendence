import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@login_required
def profile(request):
	if request.META.get('HTTP_HX_REQUEST'):
		return render(request, 'profile_block.html')
	return render(request, 'profile.html')

def get_image_url(request):
	if request.method == 'POST':
		data = json.loads(request.body)
		selected_option = data.get('avatarselect')
		# image_url = 'images/character1.png'
		image_url = request.user.photo_medium_url
		if selected_option == '1':
			image_url = request.user.photo_medium_url
		elif selected_option == '2':
			image_url = '/static/profile/images/character1.png'
		elif selected_option == '3':
			image_url = '/static/profile/images/character2.png'
		elif selected_option == '4':
			image_url = '/static/profile/images/character1.png'
		return JsonResponse({'image_url': image_url})
	return JsonResponse({'error': 'Méthode non autorisée'})

