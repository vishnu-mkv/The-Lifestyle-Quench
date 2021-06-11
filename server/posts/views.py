from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import ViewSet

from .models import Post, Submission
# Create your views here.
from .serializers import PostSerializer, SubmissionSerializer


class PostViewSet(ViewSet):

    def list(self, request):
        queryset = Post.objects.filter(status='P')
        serializer = PostSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

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
            return Response({"user": "Authentication required"}, status.HTTP_407_PROXY_AUTHENTICATION_REQUIRED)

        if not request.user.writer:
            return Response({request.user.get_full_name(): 'Unauthorized'}, status.HTTP_401_UNAUTHORIZED)

        queryset = Post.objects.all()
        post = get_object_or_404(queryset, slug=pk)

        if not request.user.email == post.writer.email and not request.user.admin:
            return Response({request.user.get_full_name(): "unauthorized"}, status.HTTP_401_UNAUTHORIZED)

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
            return Response({"user": "Authentication required"}, status.HTTP_407_PROXY_AUTHENTICATION_REQUIRED)

        if not request.user.writer and not request.user.admin:
            return Response({request.user.get_full_name(): 'Unauthorized'}, status.HTTP_401_UNAUTHORIZED)

        queryset = Post.objects.all()
        post = get_object_or_404(queryset, slug=pk)

        if not request.user.admin:

            if post.writer.email != request.user.email:
                return Response({request.user.get_full_name(): 'Unauthorized'}, status.HTTP_401_UNAUTHORIZED)
            else:
                if post.status == 'P':
                    return Response({'post': post.slug, 'delete': False,
                                     'message': "Post published. contact admin to delete"},
                                    status.HTTP_406_NOT_ACCEPTABLE)

        slug = post.slug
        post.delete()
        return Response({'post': slug, 'delete': True})


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def submissions_view(request, slug):
    try:
        post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        return Response({slug: "Not found"}, status.HTTP_404_NOT_FOUND)

    if not request.user.email == post.writer.email and not request.user.staff:
        return Response({request.user.get_full_name(): 'Unauthorized'}, status.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':
        qs = Submission.objects.filter(post=post).order_by('-date_submitted')
        serializer = SubmissionSerializer(qs, many=True)
        return Response(serializer.data)

    if request.method == 'POST':

        if not request.user.email == post.writer.email:
            return Response({request.user.get_full_name(): 'Unauthorized'}, status.HTTP_401_UNAUTHORIZED)

        if post.status == 'P':
            return Response({post.slug: 'Post has been already published'})

        if request.data.get('submit') is None:
            return Response({'submit': "This field is required"}, status.HTTP_400_BAD_REQUEST)

        submit = request.data['submit']

        if submit is not False and submit is not True:
            return Response({'submit': "specify 'true' or 'false'"}, status.HTTP_400_BAD_REQUEST)

        if post.status == 'S' and submit is True:
            return Response({post.slug: 'Post has been already submitted'})

        elif post.status == 'S' and submit is False:
            qs = Submission.objects.filter(post=post, approved=None)
            qs.delete()
            post.status = 'D'
            post.save()
            return Response({post.slug: "Post un-submitted"})

        elif post.status == 'D' and submit is True:
            instance = Submission.objects.create(post=post)
            post.status = 'S'
            post.save()
            serializer = SubmissionSerializer(instance)
            return Response(serializer.data)
        return Response({'ok': True})
