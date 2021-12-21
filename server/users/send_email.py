from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

from .models import EmailActivation, ForgotPasswordKey
from .utils import get_email_activation_key, get_forgot_password_key


def send_activation_email(user):
    activation_key = get_email_activation_key()
    instance = EmailActivation.objects.create(user=user, key=activation_key)
    instance.save()

    recipient_list = [user.email, ]
    link = settings.FRONTEND_URL + 'register/activate?key=' + activation_key
    subject = 'Activate your Curiosity account'
    html_msg = render_to_string('email_activate.html', {'link':link, 'user':user})
    email_from = settings.EMAIL_HOST_USER

    # for debugging purpose
    # response = 1
    response = send_mail(subject, strip_tags(html_msg), email_from, recipient_list, html_message=html_msg)

    if response:
        instance.email_sent = True
        instance.save()


def send_forgot_password_email(user):

    activation_key = get_forgot_password_key()
    instance = ForgotPasswordKey.objects.create(user=user, key=activation_key)
    instance.save()

    recipient_list = [user.email, ]
    link = settings.FRONTEND_URL + 'users/forgot-password?key=' + activation_key
    subject = 'Reset your curiosity account password'
    html_msg = render_to_string('email_forgot_password.html', {'link':link, 'user':user})
    email_from = settings.EMAIL_HOST_USER

    # for debugging purpose
    # response = 1
    response = send_mail(subject, strip_tags(html_msg), email_from, recipient_list, html_message=html_msg)

    if response:
        instance.email_sent = True
        instance.save()
