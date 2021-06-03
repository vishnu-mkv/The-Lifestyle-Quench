from django.core.management.base import BaseCommand
from django.apps import apps


class Command(BaseCommand):
    help = 'Clean unused images'

    def handle(self, *args, **options):
        model = apps.get_model('images', 'ProfileImage')
        try:
            instance = model.objects.get(id=1)
            self.stdout.write(f'- Already default image exists {instance}')
        except model.DoesNotExist:
            self.stdout.write(f'- Created {model.objects.create(id=1)}')
