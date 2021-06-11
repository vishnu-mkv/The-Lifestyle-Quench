from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Submission


@receiver(post_save, sender=Submission)
def change_post_status(sender, instance, created, **kwargs):
    if not created:
        print("post", instance, instance.post)
        if instance.approved is True:
            instance.post.status = 'P'
        else:
            instance.post.status = 'D'
    else:
        instance.post.status = 'S'
    instance.post.save()
