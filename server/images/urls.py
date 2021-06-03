from django.urls import path

from .views import profile_pic_upload_view

app_name = 'images'

urlpatterns = [
    path('profile-pic/', profile_pic_upload_view, name='profile-pic-upload'),
]
