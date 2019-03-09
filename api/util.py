from rest_framework import serializers

__all__ = ['password_field']


def password_field(help_text: str):
    return serializers.CharField(
        write_only=True,
        required=True,
        help_text=help_text,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
