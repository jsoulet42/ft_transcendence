from django import forms
from backend.models import CustomUser


class ProfilePicForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('upload_image',)
