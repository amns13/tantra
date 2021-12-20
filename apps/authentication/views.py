from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
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
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password'])
            messages.success(
                request,
                _("Account created sucessfully. You will receive an email with a link to verify your account. Please follow the link."))
            user.send_email_verification_email()
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


def verify_email(request: HttpRequest, token: str) -> HttpResponse:
    user = User.verify_email_verification_token(token)
    if not user:
        messages.error(request, _("Invalid token."))
    else:
        messages.success(request, _("Account verified successfully!!!"))

    return redirect('home')
