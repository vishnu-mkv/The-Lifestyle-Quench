from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']


class NewPasswordSerializer(serializers.Serializer):

    def __init__(self, **kwargs):
        self.user = None
        super().__init__(**kwargs)

    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, max_length=20)
    new_password = serializers.CharField(required=True, max_length=20, min_length=8)

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

    def save(self, **kwargs):
        self.user.set_password(self.validated_data.get('new_password'))
        return self.user.save()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
