from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.posts_list, name='home'),
]
