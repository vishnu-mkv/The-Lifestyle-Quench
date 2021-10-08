from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import ProfilePicSerializer, PostThumbnailSerializer, PostImageSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def profile_pic_upload_view(request):

    serializer = ProfilePicSerializer(data=request.data)

    if serializer.is_valid():
        instance = serializer.save()
        return Response({'url': request.build_absolute_uri(instance.image.url), 'success': True})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_thumbnail_upload_view(request):
    if not request.user.writer:
        return Response({request.user.get_full_name: 'Unauthorized'}, status.HTTP_401_UNAUTHORIZED)

    serializer = PostThumbnailSerializer(data=request.FILES)
    if serializer.is_valid():
        instance = serializer.save()
        return Response({'image': request.build_absolute_uri(instance.image.url)})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_image_upload_view(request):
    if not request.user.writer:
        return Response({request.user.get_full_name: 'Unauthorized'}, status.HTTP_401_UNAUTHORIZED)

    serializer = PostImageSerializer(data=request.FILES)
    if serializer.is_valid():
        instance = serializer.save()
        return Response({'image': request.build_absolute_uri(instance.image.url)})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
