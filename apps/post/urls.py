from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.posts_list, name='home'),
    path('post/', views.posts_list, name='home'),
    path('post/create/', views.create_post, name='create_post'),
]
