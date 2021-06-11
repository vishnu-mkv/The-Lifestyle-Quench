from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import WriterApplication, WriterProfile, User, UserProfile, EmailActivation
from .send_email import send_activation_email
from .utils import get_unique_writer_name
from images.models import ProfileImage, PostThumbnail


@receiver(post_save, sender=WriterApplication)
def post_save_write_application(sender, instance, created, **kwargs):
    if not instance.approved:
        # if not approved do nothing
        return

    if instance.approved and (not instance.approved_by.admin or not instance.approved_by.staff):
        # for security purposes
        # if approved by not admin or not staff
        # un approve it
        instance.approved_by = None
        instance.approved = None
        instance.save()
        return

    if instance.approved:
        instance.user.writer = True
        instance.user.save()


@receiver(post_save, sender=User)
def post_save_user(sender, instance, created, **kwargs):
    # create user profile
    if created:
        # check for default profile pic important
        try:
            ProfileImage.objects.get(id=1)
        except ProfileImage.DoesNotExist:
            ProfileImage.objects.create(id=1).save()

        # check for default thumbnail important
        try:
            PostThumbnail.objects.get(id=1)
        except PostThumbnail.DoesNotExist:
            PostThumbnail.objects.create(id=1).save()

        UserProfile.objects.create(user=instance).save()

    # email activation
    if created and not instance.active:
        send_activation_email(instance)

    # create writer profile if writer
    if instance.writer:
        try:
            instance.writerprofile
        except WriterProfile.DoesNotExist:

            # implemented here for directly creating writer from admin panel without a form
            WriterProfile.objects.create(user=instance, writer_name=get_unique_writer_name(instance)).save()


@receiver(post_save, sender=EmailActivation)
def post_save_email_activation(sender, instance, created, **kwargs):
    if instance.activated and not instance.user.active:
        instance.user.active = True
        instance.user.save()
