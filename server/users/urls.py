from django.urls import path

from .views import *

app_name = 'users'

urlpatterns = [
    path('login/', ObtainExpiringAuthToken.as_view(), name='login'),
    path('register/', register_view, name='register'),
    path('activate/', activate_user_view, name='register'),
    path('change-password/', change_password_view, name='change-password'),
    path('resend-activation/', resend_activation_view, name='resend-activation'),
]
