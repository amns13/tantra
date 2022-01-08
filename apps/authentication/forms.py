from typing import Any, Dict

from django import forms
from django.contrib.auth import authenticate, login
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from . import models


class RegistrationForm(forms.ModelForm):
    """Form layout for registering new users."""
    password = forms.CharField(
        widget=forms.PasswordInput,
        help_text=_('Choose a strong password.'))
    password2 = forms.CharField(
        label=_('Repeat pasword'),
        widget=forms.PasswordInput,
        help_text=_('Repeat your password.'))

    class Meta:
        model = models.User
        fields = (
            'username',
            'email'
        )

    def clean(self) -> Dict[str, Any]:
        """This method validates the data in the form"""
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('password2'):
            raise forms.ValidationError(_("Passwords don't match."))

        return cleaned_data


class LoginForm(forms.Form):
    """Form layout for login."""

    def __init__(self, *args, **kwargs):
        """
        Overriding __init__ method as request object is needed
        for validating the details entered by user.
        """
        self.request = kwargs.pop('request', None)
        super(LoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(label=_('Username'))
    password = forms.CharField(widget=forms.PasswordInput, label=_('Password'))

    def clean(self) -> Dict[str, Any]:
        """
        After validating the details, this function calls
        the django in-built login method.
        """
        request = self.request
        cleaned_data = super().clean()
        user = authenticate(request,
                            username=cleaned_data.get('username'),
                            password=cleaned_data.get('password'))
        if not user:
            raise forms.ValidationError(_("Incorrect username or password."))
        login(request, user)

        return cleaned_data
