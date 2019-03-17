from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from api.util import PasswordField

__all__ = ['SignUpSerializer']


class SignUpSerializer(serializers.ModelSerializer):
    password = PasswordField()

    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'email',
                  'first_name', 'last_name')

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
