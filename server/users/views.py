import datetime

import pytz
from django.conf import settings
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import User, EmailActivation, validate_key_and_activate_user
from .send_email import send_activation_email
from .serializers import UserSerializer, NewPasswordSerializer


class ObtainExpiringAuthToken(ObtainAuthToken):
    def post(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token, created = Token.objects.get_or_create(user=serializer.validated_data['user'])

            utc_now = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
            if not created and token.created < utc_now - datetime.timedelta(hours=-1):
                token.delete()
                token = Token.objects.create(user=serializer.validated_data['user'])
                token.created = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
                token.save()

            return Response({'token': token.key})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def register_view(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = User.objects.create_user(**serializer.validated_data)
        return Response({'message': 'success', 'user': user.email})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def activate_user_view(request):
    key = request.data.get('key')
    if not key:
        return Response({'key': 'this field is required'}, status=status.HTTP_400_BAD_REQUEST)
    res = validate_key_and_activate_user(key)
    if res['status'] is False:
        return Response(res, status=status.HTTP_400_BAD_REQUEST)
    return Response(res)


@api_view(['POST'])
def resend_activation_view(request):
    email = request.data.get('email')
    if not email:
        return Response({'email': 'this field is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
        if user.active:
            return Response({'email': 'user is already active'}, status=status.HTTP_400_BAD_REQUEST)

        time_threshold = datetime.datetime.now(tz=pytz.utc) - datetime.timedelta(hours=24)
        qs = EmailActivation.objects.filter(user=user, generated_on__gt=time_threshold, activated=False)
        print("qs", qs)

        # Limit number of requests per day
        if qs.count() >= settings.DAILY_ACTIVATION_LIMIT:
            return Response({'email': 'too many requests today. Try again tomorrow'},
                            status=status.HTTP_400_BAD_REQUEST)
        send_activation_email(user)
        return Response({'success': True})

    except User.DoesNotExist:
        return Response({'email': 'invalid email'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def change_password_view(request):
    serializer = NewPasswordSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'status': 'success', 'user': serializer.validated_data.get('email')})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
