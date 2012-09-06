from django import forms
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from userena import settings as userena_settings
from userena.models import UserenaSignup
from userena.utils import get_profile_model


class UserForm(forms.Form):
    """
    Default user creation form. Can be altered with the
    `SOCIALREGISTRATION_SETUP_FORM` setting.
    """
    username = forms.RegexField(r'^\w+$', max_length=32)
    email = forms.EmailField(required=False)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        else:
            raise forms.ValidationError(_('This username is already in use.'))

    def save(self, request, user, profile, client):
        username, email, password = (self.cleaned_data['username'],
                                        self.cleaned_data['email'],
                                        user.set_unusable_password())

        new_user = UserenaSignup.objects.create_user(username,
                                                     email,
                                                     password,
                                                     not userena_settings.USERENA_ACTIVATION_REQUIRED,
                                                     userena_settings.USERENA_ACTIVATION_REQUIRED)

        profile.user = new_user
        profile.save()

        return new_user, profile
