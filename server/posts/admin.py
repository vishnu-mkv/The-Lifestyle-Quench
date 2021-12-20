from django.contrib import admin

# Register your models here.
from .models import Post, Submission, Subscription

admin.site.register(Post)
admin.site.register(Submission)
admin.site.register(Subscription)
