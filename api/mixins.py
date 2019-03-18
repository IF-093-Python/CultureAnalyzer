from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from api.fields import PasswordField, UniqueEmailField


class AccountSerializerMixin(serializers.Serializer):
    password = PasswordField()
    email = UniqueEmailField()

    @property
    def validated_data(self):
        validated_data = super().validated_data
        validated_data['password'] = make_password(validated_data['password'])
        return validated_data
