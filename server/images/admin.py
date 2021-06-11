from django.contrib import admin
from .models import ProfileImage, PostImage, PostThumbnail

# Register your models here.

admin.site.register(ProfileImage)
admin.site.register(PostImage)
admin.site.register(PostThumbnail)
