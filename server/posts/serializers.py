from rest_framework import serializers
import re
from bs4 import BeautifulSoup as bs

from .models import Post, Submission, Subscription
from images.models import PostThumbnail, PostImage
from utils.ImageUrlValidator import validate_image_url


def urlify(s):
    # Remove all non-word characters (everything except numbers and letters)
    s = re.sub(r"[^\w\s]", '', s)

    # Replace all runs of whitespace with a single dash
    s = re.sub(r"\s+", '-', s)

    return s


class ReadWriteSerializerMethodField(serializers.SerializerMethodField):
    def __init__(self, method_name=None, **kwargs):
        self.method_name = method_name
        kwargs['source'] = '*'
        super(serializers.SerializerMethodField, self).__init__(**kwargs)

    def to_internal_value(self, data):
        return {self.field_name: data}

class PostSummarySerializer(serializers.ModelSerializer):

    thumbnail = serializers.SerializerMethodField()
    writer = serializers.CharField(source='writer.get_full_name', read_only=True)

    class Meta:
        model = Post
        exclude = ['content']

    def get_thumbnail(self, obj):
            request = self.context['request']
            return request.build_absolute_uri(obj.thumbnail.image.url)


class PostSerializer(serializers.ModelSerializer):
    thumbnail = ReadWriteSerializerMethodField('get_thumbnail', required=True)
    writer = serializers.CharField(source='writer.get_full_name', read_only=True)
    writer_id = serializers.CharField(source='writer.writerprofile.writer_name', read_only=True)
    content = ReadWriteSerializerMethodField('get_content', required=True)
    writer_profile_pic = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'
        extra_kwargs = {
            'slug': {
                'read_only': True
            },
            'last_edited': {
                'read_only': True
            },
            'status': {
                'read_only': True
            }
        }

    def __init__(self, *args, **kwargs):
        self.thumbnail_image_instance = PostThumbnail.objects.get(id=1)
        self.content_image_set_recieved = []
        super().__init__(*args, **kwargs)

    def get_thumbnail(self, obj):
        request = self.context['request']
        return request.build_absolute_uri(obj.thumbnail.image.url)

    def get_content(self, obj):
        request = self.context['request']
        return obj.content_html(request)

    def get_writer_profile_pic(self, obj):
        request = self.context['request']
        return request.build_absolute_uri(obj.writer.userprofile.profile_pic.image.url)

    def create(self, validated_data):
        validated_data.pop('thumbnail', None)
        instance = Post.objects.create(**validated_data, writer=self.context['request'].user,
                                       slug=urlify(validated_data['title']),
                                       thumbnail=self.thumbnail_image_instance)
        instance.save()
        for image in self.content_image_set_recieved:
            image.post = instance
            image.save()

        return instance

    def update(self, instance, validated_data):
        validated_data.pop('thumbnail', None)

        instance.slug = urlify(validated_data['title'])
        instance.title = validated_data['title']
        instance.content = validated_data['content']
        instance.thumbnail = self.thumbnail_image_instance
        instance.summary = validated_data['summary']
        instance.save()

        original_set = PostImage.objects.filter(post=instance)
        recieved = self.content_image_set_recieved

        for image in original_set:
            if image not in recieved:
                image.post = None
                image.save()

        for image in recieved:
            if image not in original_set:
                image.post = instance
                image.save()

        return instance

    def validate_thumbnail(self, field_dict):
        if not field_dict['thumbnail']:
            return field_dict
        response = validate_image_url(url=field_dict['thumbnail'], Model=PostThumbnail,
                                      request=self.context['request'])
        self.thumbnail_image_instance = response
        return field_dict

    def validate_title(self, title):
        if self.instance and urlify(title) == self.instance.slug:
            return title

        try:
            Post.objects.get(slug=urlify(title))
            raise serializers.ValidationError("A post with this title already exists")
        except Post.DoesNotExist:
            return title

    def validate_content(self, field_dict):

        if not field_dict:
            return field_dict

        content = field_dict['content']

        soup = bs(content, features="html.parser")
        if soup.find('script'):
            raise serializers.ValidationError('script tags not allowed.')
        images = soup.find_all('img')
        err = {}
        for img in images:
            try:
                instance = validate_image_url(img['src'], PostImage, self.context['request'], False)
                self.content_image_set_recieved.append(instance)
                img['src'] = instance.id
            except serializers.ValidationError:
                err[img['src']] = "Invalid image url"

        if err:
            raise serializers.ValidationError(err)

        return {'content': str(soup)}


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'