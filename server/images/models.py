# from PIL import Image
from django.db import models


# Create your models here.

class ProfileImage(models.Model):
    image = models.ImageField(unique=True, upload_to='profile_pics', default='default.jpg')

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #
    #     # resizing image to 320*320
    #     img = Image.open(self.image.path)
    #     if img.mode != 'RGB':
    #         img = img.convert('RGB')
    #     if img.height > 320 or img.width > 320:
    #         output_size = (320, 320)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)

    def __str__(self):
        return f'{self.image.name}'


class PostImage(models.Model):
    image = models.ImageField(unique=True, upload_to='post-images')
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        postName = "None"
        if self.post:
            postName = self.post.slug
        return f'{self.image} - {postName}'


class PostThumbnail(models.Model):
    image = models.ImageField(unique=True, upload_to='thumbnails', default='default.jpg')

    def __str__(self):
        return f'{self.image.name} - {self.post_set.count()}'
