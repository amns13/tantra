from typing import Any, Dict

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from . import models


class RegistrationForm(forms.ModelForm):
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
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('password2'):
            raise ValidationError(_("Passwords don't match."))

        return cleaned_data
