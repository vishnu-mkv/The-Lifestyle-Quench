from django.conf import settings
from django.core.mail import send_mail

from .models import EmailActivation, ForgotPasswordKey
from .utils import get_email_activation_key, get_forgot_password_key


def send_activation_email(user):
    activation_key = get_email_activation_key()
    instance = EmailActivation.objects.create(user=user, key=activation_key)
    instance.save()

    # TODO: change subject and use a template and add the link to it
    recipient_list = [user.email, ]
    subject = 'Thank you for registering to our site'
    message = ' it  means a world to us.'
    email_from = settings.EMAIL_HOST_USER
    # for debugging purpose
    response = 1
    # response = send_mail(subject, message, email_from, recipient_list)

    if response:
        print(f'email sent to ${recipient_list}')
        # email sent successfully
        instance.email_sent = True
        instance.save()


def send_forgot_password_email(user):
    activation_key = get_forgot_password_key()
    instance = ForgotPasswordKey.objects.create(user=user, key=activation_key)
    instance.save()

    # TODO: change subject and use a template and add the link to it
    recipient_list = [user.email, ]
    subject = 'Forgot password'
    message = 'reset your password using this link'
    email_from = settings.EMAIL_HOST_USER
    response = send_mail(subject, message, email_from, recipient_list)

    if response:
        print(f'email sent to ${recipient_list}')
        # email sent successfully
        instance.email_sent = True
        instance.save()
