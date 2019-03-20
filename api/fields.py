from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from api.validators import password_validator

__all__ = ['PasswordField', 'UniqueEmailField']


class PasswordField(serializers.CharField):
    def __init__(self, **kwargs):
        kwargs['write_only'] = kwargs.get('help_text', True)
        kwargs['required'] = kwargs.get('required', True)
        kwargs['style'] = kwargs.get('style', {'input_type': 'password',
                                               'placeholder': 'Password'})
        kwargs['help_text'] = kwargs.get('help_text', '')
        kwargs['validators'] = kwargs.get('validators', [password_validator])
        super().__init__(**kwargs)


class UniqueEmailField(serializers.EmailField):
    def __init__(self, **kwargs):
        message = 'A user with that email already exists.'
        emails = get_user_model().objects.values('email')
        email_unique_validator = UniqueValidator(queryset=emails,
                                                 message=message)
        super().__init__(**kwargs, validators=[email_unique_validator])
