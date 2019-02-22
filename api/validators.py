import django.contrib.auth.password_validation as validators
from rest_framework import serializers
from django.core import exceptions

from users.models import CustomUser


def validate_sign_up(data):
    password = data.get('password')
    validate_password(password)


def validate_password(password):
    errors = dict()
    try:
        validators.validate_password(password=password, user=CustomUser)
    except exceptions.ValidationError as e:
        errors['password'] = list(e.messages)
    if errors:
        raise serializers.ValidationError(errors)
    return errors
