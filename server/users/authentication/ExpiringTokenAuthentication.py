import datetime

import pytz
from django.conf import settings
from rest_framework import exceptions
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication


class ExpiringTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):

        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted')

        utc_now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)

        if token.created < utc_now - datetime.timedelta(hours=settings.AUTH_TOKEN_VALIDITY):
            raise exceptions.AuthenticationFailed('Token has expired')

        return token.user, token
