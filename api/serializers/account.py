from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from api.fields import PasswordField, UniqueEmailField

__all__ = ['AccountSerializer', 'SignUpSerializer', 'ProfileSerializer']


class AccountSerializer(serializers.ModelSerializer):
    password = PasswordField()
    email = UniqueEmailField()

    @property
    def validated_data(self):
        validated_data = super().validated_data
        password = validated_data.get('password')
        if password:
            validated_data['password'] = make_password(password)
        return validated_data


class SignUpSerializer(AccountSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'email',
                  'first_name', 'last_name')


class ProfileSerializer(AccountSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password',
                  'email', 'first_name',
                  'last_name', 'date_of_birth',
                  'experience', 'gender',
                  'education', 'image')
