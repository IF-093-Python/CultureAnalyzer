from django.contrib.auth import password_validation
from django.core import exceptions
from rest_framework import serializers

__all__ = ['password_validator']


def catch_password_errors(password):
    errors = []
    try:
        password_validation.validate_password(password)
    except exceptions.ValidationError as e:
        errors = list(e.messages)
    return errors


def password_validator(password):
    errors = catch_password_errors(password)
    if errors:
        raise serializers.ValidationError(errors)
