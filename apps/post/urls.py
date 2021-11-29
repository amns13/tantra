from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('', views.PostListAPIView.as_view()),
    path('<uuid:uuid>/', views.PostDetailAPIView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
