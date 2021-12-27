from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import GenericViewSet
from rest_framework.pagination import PageNumberPagination
from django.conf import settings
from django.db.models import Q
from django.contrib.auth.models import User
from users.models import WriterProfile

from .models import Post, Submission, Subscription
from .serializers import PostSerializer, PostSummarySerializer, SubscriptionSerializer
# Create your views here.


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def writer_post_list_view(request):

    if not request.user.writer:
        return Response({"message": "Not a writer"}, status.HTTP_403_FORBIDDEN)

    queryset = Post.objects.filter(writer=request.user).order_by('-last_edited')
    serializer = PostSummarySerializer(queryset, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
def postSearchView(request, searchTerm):
    paginator = PageNumberPagination()
    paginator.page_size = settings.REST_FRAMEWORK['PAGE_SIZE']
    objects = Post.objects.filter(Q(title__icontains=searchTerm) | Q(summary__icontains=searchTerm))
    result_page = paginator.paginate_queryset(objects, request)
    serializer = PostSummarySerializer(result_page, many=True, context={'request': request})
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def writerPostListView(request, writer_id):
    paginator = PageNumberPagination()
    paginator.page_size = settings.REST_FRAMEWORK['PAGE_SIZE']

    try:
        writerProfile = WriterProfile.objects.get(writer_name=writer_id)
        objects = Post.objects.filter(writer=writerProfile.user, status='P').order_by('-last_edited')
        result_page = paginator.paginate_queryset(objects, request)
        serializer = PostSummarySerializer(result_page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)

    except WriterProfile.DoesNotExist:
        return Response({'writer_id': "invalid writer id"}, status.HTTP_404_NOT_FOUND)

class PostViewSet(ListModelMixin, GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def list(self, request):
        queryset = Post.objects.filter(status='P').order_by('-last_edited')
        page = self.paginate_queryset(queryset)
        serializer = PostSerializer(page, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, pk):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, slug=pk)

        if post.status != 'P':
            if request.user.is_anonymous:
                return Response({pk: "Not Found"}, status.HTTP_404_NOT_FOUND)

            if request.user.staff:
                pass

            elif not request.user.writer or post.writer != request.user:
                return Response({pk: "Not Found"}, status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data)

    def create(self, request):

        if request.user.is_anonymous:
            return Response({"user": "Authentication required"}, status.HTTP_407_PROXY_AUTHENTICATION_REQUIRED)

        if not request.user.writer:
            return Response({request.user.get_full_name(): 'Unauthorized'}, status.HTTP_401_UNAUTHORIZED)

        serializer = PostSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            instance = serializer.save()
            url = reverse('posts:post-detail', args=[instance.slug])
            data = serializer.data
            data['url'] = request.build_absolute_uri(url)
            return Response(data)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):

        if request.user.is_anonymous:
            return Response({"message": "User authentication required"}, status.HTTP_407_PROXY_AUTHENTICATION_REQUIRED)

        if not request.user.writer:
            return Response({'message': request.user.get_full_name()+' Unauthorized'}, status.HTTP_401_UNAUTHORIZED)

        queryset = Post.objects.all()
        post = get_object_or_404(queryset, slug=pk)

        if not request.user.email == post.writer.email and not request.user.admin:
            return Response({'message': request.user.get_full_name()+' Unauthorized'}, status.HTTP_401_UNAUTHORIZED)

        if post.status == 'P' and not request.user.admin:
            return Response({"message": "Not allowed. Contact admin"}, status.HTTP_406_NOT_ACCEPTABLE)

        serializer = PostSerializer(data=request.data, instance=post, context={'request': request})
        if serializer.is_valid():
            instance = serializer.save()
            url = reverse('posts:post-detail', args=[instance.slug])
            data = serializer.data
            data['url'] = request.build_absolute_uri(url)
            return Response(data)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):

        if request.user.is_anonymous:
            return Response({"user": "Authentication required"}, status.HTTP_401_UNAUTHORIZED)

        if not request.user.writer and not request.user.admin:
            return Response({request.user.get_full_name(): 'Unauthorized'}, status.HTTP_401_UNAUTHORIZED)

        queryset = Post.objects.all()
        post = get_object_or_404(queryset, slug=pk)

        if not request.user.admin:

            if post.writer.email != request.user.email:
                return Response({request.user.get_full_name(): 'Unauthorized'}, status.HTTP_401_UNAUTHORIZED)
            else:
                if post.status == 'P':
                    return Response({'slug': post.slug, 'delete': False,
                                     'message': "Post published. contact admin to delete"},
                                    status.HTTP_406_NOT_ACCEPTABLE)

        slug = post.slug
        post.delete()
        return Response({'slug': slug, 'delete': True, 'message': 'Post has been deleted.'})



@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def postSubmitView(request, slug):

    post = None
    try:
        post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        return Response({"message": "Post not found"}, status.HTTP_404_NOT_FOUND)

    if post.status == 'P':
        return Response({'status': 'P', "message": "Post has been already published"}, status.HTTP_400_BAD_REQUEST)

    if (not request.user.writer) or (post.writer != request.user):
        print(post.writer.email, request.user.email)
        return Response({"message": "Forbidden"}, status.HTTP_403_FORBIDDEN)

    if request.method == 'POST':
        if not request.data['submit']:
            return Response({'submit' : 'This field is required'}, status.HTTP_400_BAD_REQUEST)

        if Submission.objects.filter(post=post, approved=None):
            return Response({'status': 'S', 'message': 'Post has been already submitted'})

        if Submission.objects.filter(post=post, approved=False).count() >= 2:
            return Response({'status': 'R', 'message': 'Rejected'}, status.HTTP_400_BAD_REQUEST)

        post.status = 'S'
        post.save()
        Submission.objects.create(post=post)
        return Response({'status': 'S', 'message': 'Post has been submitted'})

    if request.method == 'DELETE':
        submissions = Submission.objects.filter(post = post, approved=None)

        post.status = 'D'
        post.save()
        for sub in submissions:
            sub.delete()

        return Response({'status': 'D', 'message': 'Post submission has been deleted.'})

@api_view(['GET'])
def getTopPostsView(request):
    qs = Post.objects.filter(slug__in=settings.TOP_POST_SLUGS)
    serializer = PostSerializer(qs, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['POST'])
def subscribeView(request):
    serializer = SubscriptionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'success': True})

    if request.data.get('email') and Subscription.objects.filter(email=request.data['email']).count() != 0:
        return Response({'success': True})

    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)







