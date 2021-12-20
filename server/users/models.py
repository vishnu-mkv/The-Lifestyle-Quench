import datetime
from pytz import utc

from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .manager import UserManager
from images.models import ProfileImage


# Create your models here.


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, verbose_name='email address', max_length=255)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)  # True on email activation
    writer = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password', 'first_name', 'last_name']

    def get_full_name(self):
        return str(self.first_name + ' ' + self.last_name)

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

    @property
    def is_writer(self):
        return self.writer

    def can_apply_for_writer(self):
        if self.writer:
            return False, "already a writer"
        if self.writerapplication_set.filter(approved=None).count() > 0:
            return False, "already a application is active"
        return True, "Allowed"


class WriterProfile(models.Model):
    writer_name = models.CharField(max_length=20, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.writer_name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ForeignKey(ProfileImage, on_delete=models.DO_NOTHING, null=True, default=1)

    def __str__(self):
        return f'{self.user.get_full_name()} - Profile'


class WriterApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    approved = models.BooleanField(null=True)
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='Approved_by', blank=True)
    bio = models.TextField(max_length=1000, blank=True)
    writings = models.CharField(max_length=200, blank=True)
    submitted_on = models.DateTimeField(auto_now_add=True)

    def save(self, **kwargs):
        # if user is already a writer
        # do nothing with the application
        if self.user.writer:
            return None
        super(WriterApplication, self).save()

    def __str__(self):
        return self.user.get_full_name() + " - Writer Application"


def check_validity(obj):
    now = datetime.datetime.now().replace(tzinfo=utc)
    max_validity = obj.generated_on + datetime.timedelta(days=obj.validity)
    return now <= max_validity


class EmailActivation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(unique=True, max_length=20)
    generated_on = models.DateTimeField(auto_now_add=True)
    validity = models.PositiveBigIntegerField(default=7, validators=[
        MaxValueValidator(100), MinValueValidator(1)
    ])
    activated = models.BooleanField(default=False)
    email_sent = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.email} - {self.key}'

    def is_valid(self):
        return check_validity(self)

    def activate_user(self):
        if self.user.active:
            return
        if not self.is_valid():
            return False
        self.activated = True
        self.save()
        return True

    def save(self, *args, **kwargs):
        # if user is active no email activation is created
        if self.user.active:
            return None
        super(EmailActivation, self).save(*args, **kwargs)


def validate_key_and_activate_user(key):
    response = {'status': False, 'message': 'unknown error', 'user': None}

    try:
        obj = EmailActivation.objects.get(key=key)
        response['user'] = obj.user.email
        if obj.user.active:
            response['message'] = 'User already active'
            return response
        if not obj.is_valid():
            response['message'] = 'Key expired'

        obj.activated = True
        obj.save()
        response['message'] = 'success'
        response['status'] = 'Activated'

    except EmailActivation.DoesNotExist:
        response['message'] = 'Invalid Key'

    return response


class ForgotPasswordKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=20, unique=True)
    generated_on = models.DateTimeField(auto_now_add=True)
    password_changed = models.BooleanField(default=False)
    email_sent = models.BooleanField(default=False)
    validity = models.PositiveIntegerField(default=7, validators=[
        MaxValueValidator(100), MinValueValidator(1)
    ])

    def __str__(self):
        return f'{self.user.get_short_name()} - Forgot password'

    def is_valid(self):
        return check_validity(self) and not self.password_changed

    def mark_as_used(self):
        self.password_changed = True
        return self.save()

class ContactUs(models.Model):
    email = models.EmailField(blank=False)
    message = models.TextField(blank=False)
    name = models.CharField(blank=False, max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} {self.email} --ContactUs'

