from django.contrib.auth import get_user_model
from rest_framework import serializers

from api.mixins import AccountSerializerMixin

__all__ = ['SignUpSerializer', 'ProfileSerializer']


class SignUpSerializer(AccountSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'email',
                  'first_name', 'last_name')


class ProfileSerializer(AccountSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'email',
                  'first_name', 'last_name',
                  'date_of_birth', 'experience', 'gender', 'education',
                  'image')
