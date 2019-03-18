from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from api.util import PasswordField

__all__ = ['SignUpSerializer']


class SignUpSerializer(serializers.ModelSerializer):
    password = PasswordField()

    class Meta:
        model = get_user_model()
        fields = ("id", "username", "password", 'email',)

    def create(self, validated_data):
        password = make_password(validated_data.get('password'))
        validated_data['password'] = password
        return super(SignUpSerializer, self).create(validated_data)
