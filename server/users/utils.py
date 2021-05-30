import random
import string

from .models import EmailActivation

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


def key_generator(size=6, chars=string.ascii_uppercase + string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
