import datetime

import pytz
from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from .models import User, EmailActivation, validate_key_and_activate_user, ForgotPasswordKey, WriterProfile, \
    WriterApplication
from .send_email import send_activation_email, send_forgot_password_email
from .serializers import RegisterUserSerializer, ChangePasswordSerializer, ForgotPasswordChangeSerializer, \
    UserProfileSerializer, EditProfileSerializer, WriterProfileSerializer, WriterApplicationSerializer, \
    WriterApplicationReviewSerializer, AuthTokenSerializer, ContactUsSerializer


class ObtainExpiringAuthToken(ObtainAuthToken):
    def post(self, request, **kwargs):
        serializer = AuthTokenSerializer(data=request.data)
        if serializer.is_valid():
            token, created = Token.objects.get_or_create(
                user=serializer.validated_data['user'])

            utc_now = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
            if not created and token.created < utc_now - datetime.timedelta(hours=settings.AUTH_TOKEN_VALIDITY):
                token.delete()
                token = Token.objects.create(
                    user=serializer.validated_data['user'])
                token.created = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
                token.save()

            return Response({'token': token.key, 'expiresIn': settings.AUTH_TOKEN_VALIDITY*60*60})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def register_view(request):
    if request.user.is_authenticated:
        return Response({'error': 'You are already logged in', 'name': request.user.get_full_name()},
                        status.HTTP_406_NOT_ACCEPTABLE)

    serializer = RegisterUserSerializer(data=request.data)
    if serializer.is_valid():
        user = User.objects.create_user(**serializer.validated_data)
        return Response({'success': True, 'email': user.email})
    return Response({'success': False, 'email': "", 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


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
        return Response({'email': 'This field is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
        if user.active:
            return Response({'message': 'User is already active'}, status=status.HTTP_400_BAD_REQUEST)

        time_threshold = datetime.datetime.now(
            tz=pytz.utc) - datetime.timedelta(hours=24)
        qs = EmailActivation.objects.filter(
            user=user, generated_on__gt=time_threshold, activated=False)

        # Limit number of requests per day
        if qs.count() >= settings.DAILY_ACTIVATION_LIMIT:
            return Response({'message': 'Too many requests today. Try again tomorrow'},
                            status=status.HTTP_400_BAD_REQUEST)
        send_activation_email(user)
        return Response({'message': 'Activation email has been sent'})

    except User.DoesNotExist:
        return Response({'message': 'Invalid email'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def change_password_view(request):
    serializer = ChangePasswordSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'success': True, 'message': "Password has been changed successfully"})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def forgot_password_change_view(request):
    serializer = ForgotPasswordChangeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'success': True, 'user': serializer.user.email})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def forgot_password_user_view(request):
    key = request.data.get('key')
    if key:
        try:
            instance = ForgotPasswordKey.objects.get(key=key)
            if instance.is_valid():
                return Response({'name': instance.user.get_full_name(), 'email': instance.user.email})
            return Response({'message': 'The key was already used or expired'}, status=status.HTTP_400_BAD_REQUEST)
        except ForgotPasswordKey.DoesNotExist:
            return Response({'message': 'Invalid key'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'message': 'Key is required'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def forgot_password_send_email_view(request):
    email = request.data.get('email')
    if not email:
        return Response({'message': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)

        time_threshold = datetime.datetime.now(
            tz=pytz.utc) - datetime.timedelta(hours=24)
        qs = ForgotPasswordKey.objects.filter(
            user=user, generated_on__gt=time_threshold, password_changed=False)

        # Limit number of requests per day
        if qs.count() >= settings.DAILY_FORGOT_PASSWORD_EMAIL_LIMIT:
            return Response({'message': 'too many requests today. Try again tomorrow'},
                            status=status.HTTP_400_BAD_REQUEST)
        send_forgot_password_email(user)
        return Response({'message': "A mail has been sent to your email. Follow the link to change your password.", 'success': True})

    except User.DoesNotExist:
        return Response({'message': 'invalid email'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    if request.method == "GET":
        profile = request.user.userprofile
        serializer = UserProfileSerializer(
            instance=profile, context={'request': request})
        return Response(serializer.data)
    if request.method == "PATCH":
        serializer = EditProfileSerializer(
            instance=request.user, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.validated_data, 'success': True})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_writer_profile_view(request):
    try:
        profile = WriterProfile.objects.get(user = request.user)
        serializer = WriterProfileSerializer(instance=profile)
        return Response(serializer.data)
    except WriterProfile.DoesNotExist:
        return Response({"user": "Not a writer"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'PATCH'])
def writer_profile_view(request, writer_name):
    try:
        profile = WriterProfile.objects.get(writer_name=writer_name)

        if request.method == "GET":
            serializer = WriterProfileSerializer(instance=profile)
            userSerializer = UserProfileSerializer(instance=profile.user.userprofile, context={'request': request})
            data = {'writer' : serializer.data, 'user': userSerializer.data}
            data['user']['user']['email'] = ""
            return Response(data)

        if request.method == "PATCH":
            if not request.user:
                return Response({"message": "Login required"}, status=status.HTTP_407_PROXY_AUTHENTICATION_REQUIRED)
            if request.user.email != profile.user.email:
                return Response({"message": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

            serializer = WriterProfileSerializer(
                instance=profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                res = serializer.validated_data
                return Response(res)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except WriterProfile.DoesNotExist:
        return Response({"writer_name": "Not Found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST', 'PATCH'])
@permission_classes([IsAuthenticated])
def writer_application_view(request):
    if request.method == "POST":
        can_apply, message = request.user.can_apply_for_writer()

        if can_apply:
            serializer = WriterApplicationSerializer(
                data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            res = {'message': message}
            if request.user.writer:
                res['writer_name'] = request.user.writerprofile.writer_name
            return Response(res, status=status.HTTP_403_FORBIDDEN)

    if request.method == "PATCH":
        user = request.user
        qs = WriterApplication.objects.filter(user=user, approved=None)

        if qs.count == 0:
            return Response({'message': "You don't have any applications active."}, status.HTTP_403_FORBIDDEN)
        serializer = WriterApplicationSerializer(
            instance=qs.first(), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "GET":
        application = WriterApplication.objects.filter(user=request.user, approved=None)
        if application.count() == 0:
            return Response({"application": False})
        return Response({"application": True, "data": WriterApplicationSerializer(application.first()).data})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def writer_application_history_view(request):
        user = request.user
        qs = WriterApplication.objects.filter(
            user=user).order_by('-submitted_on')
        serializer = WriterApplicationSerializer(instance=qs, many=True)
        return Response(serializer.data)


@api_view(['GET', 'PATCH'])
@permission_classes([IsAdminUser])
def writer_application_review_view(request, w_id):
    try:
        application = WriterApplication.objects.get(id=w_id)

        # gives history of applications of user
        if request.method == 'GET':
            applications = WriterApplication.objects.filter(
                user=application.user).order_by('-submitted_on')
            serializer = WriterApplicationReviewSerializer(
                instance=applications, many=True)
            return Response(serializer.data)

        if request.method == 'PATCH':
            serializer = WriterApplicationReviewSerializer(instance=application, data=request.data,
                                                           context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    except WriterApplication.DoesNotExist:
        return Response({'id': w_id, "error": "Not found"}, status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def writer_application_list_review_view(request, approved="none"):
    # gives a list of not reviewed applications
    if approved.lower() == 'none':
        applications = WriterApplication.objects.filter(
            approved=None).order_by('-submitted_on')
    elif approved.lower() == 'accepted':
        applications = WriterApplication.objects.filter(
            approved=True).order_by('-submitted_on')
    elif approved.lower() == 'rejected':
        applications = WriterApplication.objects.filter(
            approved=False).order_by('-submitted_on')
    elif approved.lower() == 'all':
        applications = WriterApplication.objects.all().order_by('-submitted_on')
    else:
        return Response({'error': 'url does not exist'}, status.HTTP_404_NOT_FOUND)
    serializer = WriterApplicationReviewSerializer(
        instance=applications, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def email_availability_view(request):
    email = None
    try:
        email = request.data['email']
        validate_email(email)
        User.objects.get(email=email)
        return Response({'email': email, 'availability': False, 'message': 'account already exists'})
    except KeyError:
        return Response({'email': 'This field is required'}, status.HTTP_400_BAD_REQUEST)
    except ValidationError:
        return Response({'email': 'Invalid email'}, status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({'email': email, 'availability': True})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def writer_name_availability_view(request):
    if not request.user.writer and not request.user.staff:
        return Response({'error': 'Unauthorized'}, status.HTTP_401_UNAUTHORIZED)

    try:
        writer_name = request.data['writer_name']
        copy = writer_name.replace('-', 'a')
        err = {'writer_name': None}
        if not copy.isalnum():
            msg = 'Can only contain alphabets, numbers and hyphen(-).'
            err['writer_name'] = err[writer_name] + \
                msg if err['writer_name'] else msg
        if not len(writer_name) > 5:
            msg = 'Minimum length is 5'
            err['writer_name'] = err[writer_name] + \
                msg if err['writer_name'] else msg
        if not writer_name[0].isalpha():
            msg = 'Should start with alphabets'
            err['writer_name'] = err[writer_name] + \
                msg if err['writer_name'] else msg
        if err['writer_name']:
            return Response(err, status.HTTP_400_BAD_REQUEST)
        instance = WriterProfile.objects.get(writer_name=writer_name)
        if instance.user.email == request.user.email:
            return Response({'writer_name': writer_name, 'availability': True})
        return Response({'writer_name': writer_name, 'availability': False})
    except KeyError:
        return Response({'writer_name': 'This field is required'}, status.HTTP_400_BAD_REQUEST)
    except WriterProfile.DoesNotExist:
        return Response({'writer_name': writer_name, 'availability': True})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def has_pending_writer_application(request):
    application = WriterApplication.objects.filter(user=request.user, approved=None)
    if application.count() == 0:
        return Response({"application": False})
    return Response({"application": True, "data": WriterApplicationSerializer(application.first()).data})

@api_view(['POST'])
def contact_us_view(request):
    serializer = ContactUsSerializer(data=request.data)
    if(serializer.is_valid()):
        serializer.save()
        return Response({'success': True})
    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)