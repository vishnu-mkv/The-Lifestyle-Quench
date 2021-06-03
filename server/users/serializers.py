from rest_framework import serializers

from images.models import ProfileImage

from .models import User, ForgotPasswordKey, UserProfile, WriterProfile, WriterApplication


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']


class BasePasswordChangeSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True, max_length=20, min_length=8)

    def __init__(self, **kwargs):
        self.user = None
        super().__init__(**kwargs)

    def save(self, **kwargs):
        if not self.user:
            return False
        self.user.set_password(self.validated_data.get('new_password'))
        self.user.save()
        return True

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class ChangePasswordSerializer(BasePasswordChangeSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, max_length=20)

    def validate_email(self, email):
        try:
            self.user = User.objects.get(email=email)
            return email
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email")

    def validate_password(self, password):
        if not self.user:
            return password
        if not self.user.check_password(password):
            raise serializers.ValidationError("Email and passwords do not match")
        return password

    def validate(self, data):
        if data.get('password') == data.get('new_password'):
            raise serializers.ValidationError("New password is same as password")
        return data


class ForgotPasswordChangeSerializer(BasePasswordChangeSerializer):
    key = serializers.CharField(required=True)

    def __init__(self, **kwargs):
        self.key = None
        super().__init__(**kwargs)

    def validate_key(self, key):
        try:
            instance = ForgotPasswordKey.objects.get(key=key)
            if not instance.is_valid():
                raise serializers.ValidationError("Key expired or was already used")
            self.user = instance.user
            self.key = instance
            return key
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid key")

    def save(self, **kwargs):
        if self.key and super(ForgotPasswordChangeSerializer, self).save():
            return self.key.mark_as_used()
        return False


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['id', 'password', 'admin', 'last_login']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    profile_pic = serializers.ImageField(source='profile_pic.image', use_url=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'profile_pic']


class EditProfileSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=20, required=False)
    last_name = serializers.CharField(max_length=20, required=False)
    profile_pic = serializers.URLField(required=False)

    def __init__(self, **kwargs):
        self.profile_image_instance = None
        super().__init__(**kwargs)

    def update(self, instance, validated_data):

        first_name = validated_data.get('first_name')
        if first_name and first_name is not instance.first_name:
            instance.first_name = first_name.strip().capitalize()

        last_name = validated_data.get('last_name')
        if last_name and last_name is not instance.last_name:
            instance.last_name = last_name.strip().capitalize()

        instance.save()

        if self.profile_image_instance and self.profile_image_instance is not instance.userprofile.profile_pic:
            instance.userprofile.profile_pic = self.profile_image_instance
            instance.userprofile.save()

        return instance

    def create(self, validated_data):
        pass

    def build_image_url(self, image):
        request = self.context['request']
        return request.build_absolute_uri(image.image.url)

    def validate_profile_pic(self, profile_pic):

        if not profile_pic:
            return profile_pic

        directory = ProfileImage._meta.get_field('image').upload_to
        image_name = profile_pic.split('/')[-1]

        if profile_pic == self.build_image_url(ProfileImage.objects.get(image='default.jpg')):
            return profile_pic

        try:
            image = ProfileImage.objects.get(image=f'{directory}/{image_name}')
            if profile_pic != self.build_image_url(image):
                raise serializers.ValidationError("Invalid uri.")
            self.profile_image_instance = image
            return profile_pic
        except ProfileImage.DoesNotExist:
            raise serializers.ValidationError("Invalid url")

    def validate_email(self, email):

        if self.instance.email != email:
            raise serializers.ValidationError('Cannot change email')
        return email


class WriterProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = WriterProfile
        fields = ['writer_name', 'bio']
        extra_kwargs = {
            'writer_name': {
                'required': True
            }
        }


class WriterApplicationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = WriterApplication
        exclude = ['user', 'approved_by']
        extra_kwargs = {
            'user': {
                'read_only': True
            },
            'approved': {
                'read_only': True
            },
            'submitted_on': {
                'read_only': True
            },
            'bio': {
                'required': True
            },
            'writings': {
                'required': True
            }
        }

    def create(self, validated_data):
        obj = WriterApplication.objects.create(**validated_data, user=self.context['request'].user)
        obj.save()
        return obj


class WriterApplicationReviewSerializer(serializers.ModelSerializer):
    approved_by = serializers.CharField(source="approved_by.get_full_name", read_only=True)
    user = serializers.CharField(source="user.get_full_name", read_only=True)

    class Meta:
        model = WriterApplication
        fields = "__all__"
        extra_kwargs = {
            'id': {
                'required': True
            },
            'user': {
                'read_only': True
            },
            'submitted_on': {
                'read_only': True
            },
            'bio': {
                'read_only': True
            },
            'writings': {
                'read_only': True
            }
        }

    def validate_approved(self, approved):
        if (approved is False or approved is None) and self.instance.approved is True:
            raise serializers.ValidationError("Cannot change approval status")
        return approved

    def update(self, instance, validated_data):
        instance.approved = validated_data['approved']
        if validated_data['approved'] is True:
            instance.approved_by = self.context['request'].user
        instance.save()
        return instance
