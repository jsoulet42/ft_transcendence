from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from backend.models import CustomUser, UsersList
from django.conf import settings
from django.utils.translation import gettext as _


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control form_signup1', 'placeholder': _('Username')})
        self.fields['email'].widget.attrs.update({'class': 'form-control form_signup2', 'placeholder': _('Email (optional)')})
        self.fields['password1'].widget.attrs.update({'class': 'form-control form_signup3', 'placeholder': _('Password')})
        self.fields['password2'].widget.attrs.update({'class': 'form-control form_signup4', 'placeholder': _('Confirm Password')})

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError(_("User already exists."))
        return username

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        list_instance, created = UsersList.objects.get_or_create(name='No42User')
        image_url = settings.MEDIA_URL + 'character2.png'
        user.list = list_instance
        user.profile_image_path = image_url
        user.nickname = user.username
        if commit:
            user.save()
        return user

# from django import forms
# from backend.models import CustomUser
# 
# class CustomUserCreationForm(forms.ModelForm):
	# password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	# password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
# 
	# class Meta:
		# model = CustomUser
		# fields = ['username', 'email']
# 
	# def clean_password2(self):
		# password1 = self.cleaned_data.get("password1")
		# password2 = self.cleaned_data.get("password2")
		# if password1 and password2 and password1 != password2:
			# raise forms.ValidationError("Passwords don't match")
		# return password2
# 
	# def save(self, commit=True):
		# user = super().save(commit=False)
		# user.set_password(self.cleaned_data["password1"])
		# if commit:
			# user.save()
		# return user