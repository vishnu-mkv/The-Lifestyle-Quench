import random
import string

from .models import EmailActivation, ForgotPasswordKey, WriterProfile

key_min_length = 12
key_max_length = 20


def get_email_activation_key():
    key = key_generator(size=random.randint(key_min_length, key_max_length))
    try:
        # if the key was already used try again
        EmailActivation.objects.get(key=key)
        get_email_activation_key()
    except EmailActivation.DoesNotExist:
        # else return key
        return key


def get_forgot_password_key():
    key = key_generator(size=random.randint(key_min_length, key_max_length))
    try:
        # if the key was already used try again
        ForgotPasswordKey.objects.get(key=key)
        get_email_activation_key()
    except ForgotPasswordKey.DoesNotExist:
        # else return key
        return key


def get_unique_writer_name(user):
    writer_name = f'{user.first_name.lower()}-{user.last_name.lower()}'

    while True:
        try:
            WriterProfile.objects.get(writer_name=writer_name)
            random_str = key_generator(1)
            writer_name += random_str
        except WriterProfile.DoesNotExist:
            return writer_name


def key_generator(size=6, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
