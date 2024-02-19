from django import forms
from backend.models import CustomUser


class ProfilePicForm(forms.ModelForm):
    upload_image = forms.ImageField(label="Upload Image", required=False)
    class Meta:
        model = CustomUser
        fields = ('upload_image',)
