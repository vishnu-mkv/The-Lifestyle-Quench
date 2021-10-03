from django.conf import settings
from users.models import User
from django.core.exceptions import ValidationError
from django.db import models

from bs4 import BeautifulSoup as bs

from images.models import PostThumbnail, PostImage


def validate_for_writer(user):
    user = User.objects.get(id=user)
    if not user.writer:
        raise ValidationError('User is not a writer')


def validate_for_staff(user):
    user = User.objects.get(id=user)
    if not user.writer:
        raise ValidationError('User is not a staff')


def check_post_status(post):
    post = Post.objects.get(id=post)


POST_STATUS_CHOICES = [
    ('S', 'SUBMITTED'),
    ('D', 'DRAFT'),
    ('P', 'PUBLISHED'),
    ('R', 'REJECTED')
]


class Post(models.Model):
    slug = models.SlugField(max_length=150, unique=True)
    title = models.CharField(max_length=120)
    summary = models.CharField(max_length=1000)
    content = models.TextField()
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, validators=[validate_for_writer],
                               null=True)
    thumbnail = models.ForeignKey(PostThumbnail, on_delete=models.SET_DEFAULT, default=1)
    status = models.CharField(choices=POST_STATUS_CHOICES, default='D', max_length=2)
    last_edited = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.slug}'

    def content_html(self, request):
        soup = bs(self.content, "html.parser")
        images = soup.find_all('img')
        for image in images:
            image_instance = PostImage.objects.get(id=int(image['src']))
            url = request.build_absolute_uri(image_instance.image.url)
            image['src'] = url

        return str(soup)


class Submission(models.Model):
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                    validators=[validate_for_staff],
                                    null=True, related_name='reviewer')
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, validators=[check_post_status], null=True)
    approved = models.BooleanField(default=None, null=True)
    review = models.TextField(null=True, blank=True)
    date_submitted = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'submission - {self.post}'
