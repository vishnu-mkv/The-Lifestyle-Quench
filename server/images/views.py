from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import ProfilePicSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def profile_pic_upload_view(request):
    serializer = ProfilePicSerializer(data=request.FILES)
    if serializer.is_valid():
        instance = serializer.save()
        return Response({'image': request.build_absolute_uri(instance.image.url)})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
