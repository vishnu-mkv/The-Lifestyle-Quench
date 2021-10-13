from django.urls import path

from .views import profile_pic_upload_view, post_thumbnail_upload_view, post_image_upload_view

app_name = 'images'

urlpatterns = [
    path('profile-pic/', profile_pic_upload_view, name='profile-pic-upload'),
    path('post/thumbnail/', post_thumbnail_upload_view, name='post-thumbnail-upload'),
    path('post/', post_image_upload_view, name='post-image-upload'),
]
