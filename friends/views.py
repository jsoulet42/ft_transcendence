import uuid

from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from .models import FriendRequest
from backend.models import CustomUser


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
def accept_friend_request(request, sender_username=None, receiver_username=None):
	if sender_username == None:
		return JsonResponse({'error': 'Invalid sender username'})

	if receiver_username == None:
		return JsonResponse({'error': 'Invalid receiver username'})

	try:
		sender = CustomUser.objects.get(username=sender_username)
		receiver = CustomUser.objects.get(username=receiver_username)
		friend_request = FriendRequest.objects.get(sender=sender, receiver=receiver)

		friend_request.delete()

		sender.friends.add(receiver)
		receiver.friends.add(sender)
	except ObjectDoesNotExist:
		return JsonResponse({'error': 'Couldn\'t accept friend request'})

	return JsonResponse({'success': 'Friend request accepted'})


@login_required
def reject_friend_request(request, sender_username=None, receiver_username=None):
	if sender_username == None:
		return JsonResponse({'error': 'Invalid sender username'})

	if receiver_username == None:
		return JsonResponse({'error': 'Invalid receiver username'})

	try:
		sender = CustomUser.objects.get(username=sender_username)
		receiver = CustomUser.objects.get(username=receiver_username)
		friend_request = FriendRequest.objects.get(sender=sender, receiver=receiver)

		friend_request.delete()
	except ObjectDoesNotExist:
		return JsonResponse({'error': 'Couldn\'t reject friend request'})

	return JsonResponse({'success': 'Friend request rejected'})