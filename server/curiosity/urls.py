"""curiosity URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include

from users.views import writer_profile_view, writer_application_list_review_view, writer_application_review_view, \
    writer_name_availability_view, email_availability_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('writer/<writer_name>/', writer_profile_view, name='writer-profile'),
    path('users/', include('users.urls', namespace='users')),
    path('posts/', include('posts.urls', namespace='posts')),
    path('upload/images/', include('images.urls', namespace='images')),
    path('check-availability/email/', email_availability_view, name='email-check'),
    path('check-availability/writer-name/',
         writer_name_availability_view, name='writer-name-check'),

    path('staff/applications/review/<approved>/', writer_application_list_review_view,
         name='writer-apply-review'
         '-filters'),
    path('staff/applications/review/', writer_application_list_review_view,
         name='writer-apply-not-reviewed'),
    path('staff/review/<w_id>/', writer_application_review_view,
         name='writer-apply-review'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
