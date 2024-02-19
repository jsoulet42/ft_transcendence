from django.shortcuts import render

# Create your views here.
def home(request):
	show_howtoplay = True
	return render(request, 'home.html')

def send_friend_request(request, receiver_username=None, receiver_uuid=None):
	try:
		if receiver_username != None:
			receiver = CustomUser.objects.get(username=receiver_username)
		if receiver_uuid != None:
			receiver = CustomUser.objects.get(uuid=receiver_uuid)
	except ObjectDoesNotExist:
		return JsonResponse({'error': 'User not found'})
	
	if receiver != request.user:
		FriendRequest.objects.create(sender=request.user, receiver=receiver)
		return JsonResponse({'status': 'Friend request sent'})

	return JsonResponse({'error': 'Couldn\'t send friend request'})