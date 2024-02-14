from django.shortcuts import render
from authentication.views import login_required
from django.http import JsonResponse

@login_required
def profile(request):
	if request.META.get('HTTP_HX_REQUEST'):
		return render(request, 'profile_block.html')
	return render(request, 'profile.html')

def get_image_url(request):
	if request.method == 'POST':
		selected_option = request.POST.get('avatarselect')
		# image_url = 'images/character1.png'
		if selected_option == '1':
			image_url =  '/static/images/defaultcharacter.png'
		# elif selected_option == '2':
		# 	image_url = 'static/profile/images/character2.png'
		# elif selected_option == '3':
		# 	image_url = "profile/images/character2.png"
		# elif selected_option == '4':
		# 	image_url = "images/character1.png"
		# else:
		# 	image_url = 'static/images/character1.png'
		return JsonResponse({'image_url': image_url})
	print('ERRRORRRRRRRRRRRRRRRRRRRRR')
	return JsonResponse({'error': 'Méthode non autorisée'})

