from django.urls import path

from . import views


app_name = 'authentication'
urlpatterns = [
    path('register/', views.RegistrationAPIView.as_view()),
    path(
        'verify-email/<str:token>/',
        views.EmailVerificationAPIView.as_view(),
        name='verify-email'),
]
