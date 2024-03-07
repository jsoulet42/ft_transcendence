from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from backend.models import CustomUser, UsersList
from django.conf import settings
from django.utils.translation import gettext as _


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control form_signup1',
            'autocomplete': 'username',
            'placeholder': _('Username')})
        self.fields['email'].widget.attrs.update({
            'class': 'form-control form_signup2',
            'autocomplete': 'email',
            'placeholder': _('Email (optional)')})
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control form_signup3',
            'autocomplete': 'current-password',
            'placeholder': _('Password')})
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control form_signup4',
            'autocomplete': 'current-password',
            'placeholder': _('Confirm Password')})

        self.fields['username'].label = _("Username")
        self.fields['email'].label = _("Email")
        self.fields['password1'].label = _("Password")
        self.fields['password2'].label = _("Confirmation Password")

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
        list_instance, created = UsersList.objects.get_or_create(
            name='No42User')
        image_url = settings.MEDIA_URL + 'character2.png'
        user.list = list_instance
        user.profile_image_path = image_url
        user.nickname = user.username
        if commit:
            user.save()
        return user
