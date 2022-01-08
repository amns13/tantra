from django import forms
from django.utils.translation import gettext_lazy as _

from . import models


class PostForm(forms.ModelForm):
    """Form layout for new blog post"""

    class Meta:
        model = models.Post
        fields = (
            'title',
            'body'
        )
