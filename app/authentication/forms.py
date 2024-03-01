from django import forms
from django.contrib.auth.forms import UserCreationForm
from backend.models import CustomUser, UsersList
from django.conf import settings


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        list_instance, created = UsersList.objects.get_or_create(name='No42User')
        image_url = settings.MEDIA_URL + 'character2.png'
        user.list = list_instance
        user.profile_image_path = image_url
        if commit:
            user.save()
        return user
