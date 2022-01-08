import logging

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.template.response import TemplateResponse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_safe
from django.shortcuts import redirect

from ..authentication.decorators import verified_required
from .models import Post
from .forms import PostForm

logger = logging.getLogger(__name__)


@require_safe
def posts_list(request: HttpRequest) -> HttpResponse:
    template = 'index.html'
    posts = Post.objects.published()
    return TemplateResponse(request, template, context={'posts': posts})


@verified_required(message=_("You need a verified account to write a blog post."))
def create_post(request: HttpRequest) -> HttpResponse:
    template = 'create_post.html'

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            data = form.data
            post = Post.objects.create(
                author=request.user,
                title=data['title'],
                body=data['body'])
            messages.success(request, _("Post published successfully."))
            return redirect('home')
    else:
        form = PostForm()

    return TemplateResponse(request, template, context={'form': form})
