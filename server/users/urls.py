from django.urls import path

from posts.views import writerPostListView
from .views import *

app_name = 'users'

urlpatterns = [
    path('login/', ObtainExpiringAuthToken.as_view(), name='login'),
    path('posts/', writerPostListView, name='writer-posts'),
    path('register/', register_view, name='register'),
    path('activate/', activate_user_view, name='register'),
    path('apply/', writer_application_view, name='writer-apply'),
    path('profile/', profile_view, name='profile'),
    path('writer-profile/', get_writer_profile_view, name='writer-profile'),
    path('change-password/', change_password_view, name='change-password'),
    path('forgot-password/send-email/', forgot_password_send_email_view, name='send-forgot-password-email'),
    path('forgot-password/change-password/', forgot_password_change_view, name='forgot-password-change'),
    path('forgot-password/get-user/', forgot_password_user_view, name='forgot-password-key-user'),
    path('resend-activation/', resend_activation_view, name='resend-activation'),
]
