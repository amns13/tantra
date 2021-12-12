from django.http import HttpResponse, HttpRequest
from django.views.decorators.http import require_safe
from django.template.response import TemplateResponse

from .models import Post


@require_safe
def posts_list(request: HttpRequest) -> HttpResponse:
    template = 'index.html'
    posts = Post.objects.published()
    return TemplateResponse(request, template, context={'posts': posts})
