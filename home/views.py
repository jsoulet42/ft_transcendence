import uuid

from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from backend.models import CustomUser, FriendRequest

# Create your views here.
def home(request):
	show_howtoplay = True
	return render(request, 'home.html')

@login_required
def get_friend_requests(request):
	friend_requests = FriendRequest.objects.filter(receiver=request.user)
	data = [{'username': request.sender.username} for request in friend_requests]
	return JsonResponse(data, safe=False)

@login_required
def send_friend_request(request):
	receiver = None
	
	try:
		username = request.POST.get('username', None)
		uuid_str = request.POST.get('uuid', None)
		
		if username != None and username != '':
			receiver = CustomUser.objects.get(username=username)
		
		if uuid_str != None and uuid_str != '':
			try:
				uuid_obj = uuid.UUID(uuid_str)
			except ValueError:
				return JsonResponse({'error': 'Invalid UUID format'})
			receiver = CustomUser.objects.get(uuid=uuid)
	except ObjectDoesNotExist:
		return JsonResponse({'error': 'User not found'})

	already_exists = FriendRequest.objects.filter(sender=request.user, receiver=receiver).exists()

	if receiver != None and receiver != request.user and not already_exists:
		FriendRequest.objects.create(sender=request.user, receiver=receiver)
		return JsonResponse({'success': 'Friend request sent'})

	return JsonResponse({'error': 'Couldn\'t send friend request'})

@login_required
def accept_friend_request(request):
	friend_request_id = request.POST.get('id', None)

	if friend_request_id == None or friend_request_id == '':
		return JsonResponse({'error': 'Invalid request data'})

	try:
		friend_request = FriendRequest.objects.get(id=friend_request_id)

		sender_user = friend_request.sender
		receiver_user = friend_request.receiver
		friend_request.delete()

		if sender_user == None or receiver_user == None:
			raise ObjectDoesNotExist

		sender_user.friends.add(receiver_user)
		receiver_user.friends.add(sender_user)
	except ObjectDoesNotExist:
		return JsonResponse({'error': 'Couldn\'t accept friend request'})

	return JsonResponse({'success': 'Friend request accepted'})