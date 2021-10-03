from django.urls import path

from .views import *
from rest_framework.routers import DefaultRouter

app_name = 'posts'

router = DefaultRouter()
router.register('', PostViewSet, basename='post')

urlpatterns = [
    path('<slug>/submit/', postSubmitView, name='submit-delete')
]

urlpatterns += router.urls
