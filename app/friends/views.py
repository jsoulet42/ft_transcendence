import uuid

from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.utils.translation import gettext as _

from .models import FriendRequest
from backend.models import CustomUser


@login_required
@require_GET
def get_friend_list(request, username=None):
    if username is not None:
        try:
            user = CustomUser.objects.get(username=username)
        except ObjectDoesNotExist:
            return JsonResponse({'error': _('Could not find user')})
    else:
        user = request.user

    data = [{'username': friend.username, 'status': friend.status} for friend in user.friends.all()]
    return JsonResponse(data, safe=False)


@login_required
@require_GET
def get_friend_requests(request):
    friend_requests = FriendRequest.objects.filter(receiver=request.user)
    data = [{'username': friend_request.sender.username}
            for friend_request in friend_requests]
    return JsonResponse(data, safe=False)


@login_required
@require_POST
def remove_friend(request):
    friend_username = request.POST.get('friend_username')
    if not friend_username:
        return JsonResponse({'error': _('Couldn\'t find friend')})

    try:
        user = request.user
        friend = user.friends.get(username=friend_username)
        user.friends.remove(friend)
        user.save()
        return JsonResponse({'success': _('Friend removed successfully')})
    except ObjectDoesNotExist:
        return JsonResponse({'error': _('Could not remove friend')})


@login_required
@require_POST
def send_friend_request(request):
    username = request.POST.get('username', None)
    uuid_str = request.POST.get('uuid', None)

    try:
        if username:
            receiver = CustomUser.objects.get(username=username)
        elif uuid_str:
            try:
                uuid_obj = uuid.UUID(uuid_str)
            except ValueError:
                return JsonResponse({'error': _('Invalid UUID format')})
            receiver = CustomUser.objects.get(uuid=uuid_obj)
    except ObjectDoesNotExist:
        return JsonResponse({'error': _('User not found')})

    if receiver == request.user:
        return JsonResponse({'error': _('Self requests not allowed')})

    if request.user.friends.filter(username=receiver.username).exists():
        return JsonResponse({'error': _('User is already your friend')})

    if FriendRequest.objects.filter(Q(sender=request.user, receiver=receiver) | Q(sender=receiver, receiver=request.user)).exists():
        return JsonResponse({'error': _('Friend request already sent')})

    FriendRequest.objects.create(sender=request.user, receiver=receiver)
    return JsonResponse({'success': _('Friend request sent')})


@login_required
@require_POST
def accept_friend_request(request):
    sender_username = request.POST.get('sender_username')
    if not sender_username:
        return JsonResponse({'error': _('Invalid sender username')})

    receiver_username = request.POST.get('receiver_username')
    if not receiver_username:
        return JsonResponse({'error': _('Invalid receiver username')})

    try:
        sender = CustomUser.objects.get(username=sender_username)
        receiver = CustomUser.objects.get(username=receiver_username)
        friend_request = FriendRequest.objects.get(
            sender=sender, receiver=receiver)

        friend_request.delete()

        sender.friends.add(receiver)
        receiver.friends.add(sender)
    except ObjectDoesNotExist:
        return JsonResponse({'error': _('Could not accept friend request')})

    return JsonResponse({'success': _('Friend request accepted')})


@login_required
@require_POST
def decline_friend_request(request):
    sender_username = request.POST.get('sender_username')
    if not sender_username:
        return JsonResponse({'error': _('Invalid sender username')})

    receiver_username = request.POST.get('receiver_username')
    if not receiver_username:
        return JsonResponse({'error': _('Invalid receiver username')})

    try:
        sender = CustomUser.objects.get(username=sender_username)
        receiver = CustomUser.objects.get(username=receiver_username)
        friend_request = FriendRequest.objects.get(
            sender=sender, receiver=receiver)

        friend_request.delete()
    except ObjectDoesNotExist:
        return JsonResponse({'error': _('Could not decline friend request')})

    return JsonResponse({'success': _('Friend request rejected')})
