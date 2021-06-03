from rest_framework import serializers
from .models import ProfileImage


class ProfilePicSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = ProfileImage
        fields = ['image']
