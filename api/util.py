from rest_framework import serializers

__all__ = ['PasswordField']


class PasswordField(serializers.CharField):
    def __init__(self, **kwargs):
        kwargs['write_only'] = kwargs.get('help_text', True)
        kwargs['required'] = kwargs.get('required', True)
        kwargs['style'] = kwargs.get('style', {'input_type': 'password',
                                               'placeholder': 'Password'})
        kwargs['help_text'] = kwargs.get('help_text', '')
        super().__init__(**kwargs)
