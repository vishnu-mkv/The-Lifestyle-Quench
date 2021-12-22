from django.urls import path

from .views import *
from rest_framework.routers import DefaultRouter

app_name = 'posts'

router = DefaultRouter()
router.register('', PostViewSet, basename='post')

urlpatterns = [
    path('<slug>/submit/', postSubmitView, name='submit-delete'),
    path('search/<searchTerm>/', postSearchView, name='post-search'),
    path('writer/<writer_id>/', writerPostListView, name='writer-posts'),
    path('top/', getTopPostsView, name='top-posts'),
    path('subscribe/', subscribeView, name='subscribe')
]

urlpatterns += router.urls
