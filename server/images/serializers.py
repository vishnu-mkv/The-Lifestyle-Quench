from rest_framework import serializers
from .models import ProfileImage, PostThumbnail, PostImage


class ProfilePicSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = ProfileImage
        fields = ['image']


class PostThumbnailSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = PostThumbnail
        fields = ['image']


class PostImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    post = serializers.CharField(source='post.slug', read_only=True)

    class Meta:
        model = PostImage
        fields = ['image']
