import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import redirect
from .forms import ProfilePicForm
import os
from django.conf import settings

@login_required
def profile(request):
	form = ProfilePicForm()
	if request.META.get('HTTP_HX_REQUEST'):
		return render(request, 'profile_block.html', {'form':form})
	return render(request, 'profile.html', {'form':form})

# def get_image_url(request):
# 	if request.method == 'POST':
# 		data = json.loads(request.body)
# 		selected_option = data.get('avatarselect')
# 		image_url = '/static/profile/images/chacter1.png'
# 		user = request.user
# 		if selected_option == '1':
# 			image_url = '/static/profile/images/charar1.png'
# 		elif selected_option == '2':
# 			image_url = '/static/profile/images/char.png'
# 		elif selected_option == '3':
# 			image_url = request.user.photo_medium_url
# 		elif selected_option == '4':
# 			image_url = '/static/profile/images/charter1.png'
#
# 		# return JsonResponse({'image_url': image_url})
# 	return JsonResponse({'error': 'Méthode non autorisée'})

def update_image(request):
	if request.method == 'POST':
		user = request.user
		form = ProfilePicForm(request.POST, request.FILES)
		if form.is_valid():
			uploaded_image_name = form.cleaned_data['upload_image']
			uploaded_image_url = settings.MEDIA_URL + 'images/' + str(uploaded_image_name)
			user.uploaded_image = uploaded_image_url
			user.profile_image_path = uploaded_image_url
			user.save()
			form.save()
		return HttpResponseRedirect('/profile')


def update_profile(request):
	if request.method == 'POST':
		new_nickname = request.POST.get('new_nickname')
		new_password = request.POST.get('new_password')
		selected_option = request.POST.get('avatarselect')
		user = request.user
		image_url = user.profile_image_path
		if new_nickname:
			user.nickname = new_nickname
		if new_password:
			user.set_password(new_password)
			# Mettre à jour la session pour éviter la déconnexion
			update_session_auth_hash(request, request.user)
		if selected_option == '1':
			image_url = '/static/profile/images/character1.png'
		elif selected_option == '2':
			image_url = '/static/profile/images/character2.png'
		elif selected_option == '3':
			image_url = request.user.photo_medium_url
		elif selected_option == '4':
			image_url = request.user.uploaded_image
		user.profile_image_path = image_url
		user.save()
		return HttpResponseRedirect('/profile')
