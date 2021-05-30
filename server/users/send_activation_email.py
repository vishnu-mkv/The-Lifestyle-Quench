from django.conf import settings
from django.core.mail import send_mail

from .models import EmailActivation
from .utils import get_email_activation_key


def send_activation_email(user):
    activation_key = get_email_activation_key()
    instance = EmailActivation.objects.create(user=user, key=activation_key)
    instance.save()

    recipient_list = [user.email, ]
    subject = 'Thank you for registering to our site'
    message = ' it  means a world to us.'
    email_from = settings.EMAIL_HOST_USER
    response = send_mail(subject, message, email_from, recipient_list)

    if response:
        print(f'email sent to ${recipient_list}')
        # email sent successfully
        instance.email_sent = True
        instance.save()
