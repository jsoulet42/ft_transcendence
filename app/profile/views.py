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
from django.core.exceptions import ObjectDoesNotExist
from backend.models import CustomUser, Game


@login_required
def profile(request):
    form = ProfilePicForm()
    if request.META.get('HTTP_HX_REQUEST'):
        return render(request, 'profile_block.html', {'form': form})
    return render(request, 'profile.html', {'form': form})

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
            if 'upload_image' in request.FILES:
                image = form.cleaned_data['upload_image']
                if user.upload_image:
                    if os.path.exists(user.upload_image.path):
                        os.remove(user.upload_image.path)
                user.upload_image = image
                if 'media/images' in user.profile_image_path:
                    user.profile_image_path = settings.MEDIA_URL + \
                        'images/' + str(image)
                user.save()
        return HttpResponseRedirect('/profile')


def match_history(request):
    form = ProfilePicForm()
    # user = request.user
    # .order_by('-date')
    latest_matches = Game.objects.filter(
        player1=request.user, tournament__isnull=True)[:30]
    if request.META.get('HTTP_HX_REQUEST'):
        return render(request, 'match_history.html', {'matches': latest_matches})
    return render(request, 'profile.html', {'form': form})


def match_history_search(request):
	form = ProfilePicForm()
	name = request.POST.get('btn-search')
	latest_matches = Game.objects.filter(player1=name, tournament__isnull=True)[:30]
	if request.META.get('HTTP_HX_REQUEST'):
		return render(request, 'match_history_search.html', {'matches': latest_matches})
	return render(request, 'profile.html', {'form':form})

def tournaments_history(request):
    form = ProfilePicForm()
    # .order_by('-date')
    latest_matches = Game.objects.filter(
        player1=request.user, tournament__isnull=False)[:30]
    if latest_matches:
        match = latest_matches[0]
        print(match.player1)
    if request.META.get('HTTP_HX_REQUEST'):
        return render(request, 'tournaments_history.html', {'matches': latest_matches})
    return render(request, 'profile.html', {'form': form})


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
            image_url = settings.MEDIA_URL + 'character1.png'
        elif selected_option == '2':
            image_url = settings.MEDIA_URL + 'character2.png'
        elif selected_option == '3':
            image_url = request.user.photo_medium_url
        elif selected_option == '4':
            image_url = user.upload_image.url
        user.profile_image_path = image_url
        user.save()
        return HttpResponseRedirect('/profile')


def search_profiles(request):
    if request.method == 'POST':
        searched = request.POST.get('searched')
        if searched:
            userprofile = CustomUser.objects.filter(username=searched)
        if userprofile:
            prof = userprofile[0]
            gamep = prof.stats.games_played
            print(gamep)
            return render(request, 'search-profiles.html', {'searched': searched, 'prof': prof})
        else:
            return render(request, 'search-profiles.html')
    return render(request, 'search-profiles.html')