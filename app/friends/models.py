from django.db import models

from backend.models import CustomUser


class FriendRequest(models.Model):
    """
    Friend request sent between two users. The receiver can either accept or deny.
    If the receiver accepts, both users are added to each other's friends lists.
    If the receiver denies, the request is destroyed.
    """
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('denied', 'Denied'),
    )

    sender = models.ForeignKey(
        CustomUser, related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(
        CustomUser, related_name='received_requests', on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
