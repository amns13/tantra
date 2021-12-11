from django.http import HttpResponse, HttpRequest
from django.template.response import TemplateResponse
from django.shortcuts import render

from .forms import RegistrationForm
from .models import User


def register(request: HttpRequest) -> HttpResponse:
    template = 'register.html'

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            data = form.data
            User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password'])
        return TemplateResponse(request, template, context={'form': form})

    else:
        form = RegistrationForm()
        return TemplateResponse(request, template, context={'form': form})
