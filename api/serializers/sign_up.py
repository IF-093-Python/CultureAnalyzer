from rest_framework import serializers

from api.validators import validate_sign_up
from users.models import CustomUser

__all__ = ['SignUpSerializer', 'ProfileSerializer']


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "username", "password", 'email',)
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = self.create_user(username=validated_data['username'],
                                email=validated_data['email'],
                                password=validated_data['password'])
        return user

    def create_user(self, username, email, password):
        user = CustomUser.objects.create(username=username, email=email)
        user.set_password(password)
        user.save()
        return user

    def validate(self, attrs):
        validate_sign_up(attrs)
        return super().validate(attrs)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'date_of_birth', 'experience',
                  'gender', 'education')
