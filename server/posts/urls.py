from django.urls import path

from .views import PostViewSet, submissions_view
from rest_framework.routers import DefaultRouter

app_name = 'posts'

router = DefaultRouter()
router.register('', PostViewSet, basename='post')

urlpatterns = [
    path('<slug:slug>/submit/', submissions_view, name="post-submit")
]

urlpatterns += router.urls
