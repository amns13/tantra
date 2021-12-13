from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .forms import LoginForm, RegistrationForm
from .models import User


def register(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect('home')

    template = 'register.html'

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            data = form.data
            User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password'])
            messages.success(request, _("Account created sucessfully."))
            return redirect('home')
    else:
        form = RegistrationForm()

    return TemplateResponse(request, template, context={'form': form})


def login(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect('home')

    template = 'login.html'
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            return redirect('home')
    else:
        form = LoginForm()

    return TemplateResponse(request, template, context={'form': form})


@login_required
def logout(request: HttpRequest) -> HttpResponse:
    auth_logout(request)
    return redirect('home')
