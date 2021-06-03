from django.conf import settings
from django.core.exceptions import FieldDoesNotExist
from django.core.management.base import BaseCommand
from django.apps import apps


class Command(BaseCommand):
    help = 'Clean unused images'

    def handle(self, *args, **options):
        rule_dict = settings.CLEANER_CONFIG

        for model_name, rule_dict in rule_dict.items():

            try:
                model = apps.get_model('images', model_name)
            except LookupError:
                self.stderr.write(f"Unknown model {model_name} in app images.")
                continue

            field_error = False
            for field in list(rule_dict.get('include')) + list(rule_dict.get('exclude')):
                try:
                    model._meta.get_field(field)
                except FieldDoesNotExist:
                    self.stderr.write(f"Unknown field {field} in model {model_name}.")
                    field_error = True

            if field_error:
                return

            qs = model.objects.filter(**rule_dict.get('include')).exclude(**rule_dict.get('exclude'))

            for item in qs:
                self.stdout.write("Found: " + item.image.name)

            found = qs.count()
            total, res = qs.delete()

            self.stdout.write("\nSUMMARY")
            for model, value in res.items():
                self.stdout.write("Deleted in " + model + ": " + str(value))
            self.stdout.write("Total Found: " + str(found))
            self.stdout.write("Total deleted: " + str(total))
