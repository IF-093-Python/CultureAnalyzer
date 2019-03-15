from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from api.util import PasswordField
from feedbacks.exceptions import FValidationError
from feedbacks.models import Feedback
from feedbacks.validator import FeedbackValidator

__all__ = ['SignUpSerializer', 'FeedbackSerializer']


class SignUpSerializer(serializers.ModelSerializer):
    password = PasswordField()

    class Meta:
        model = get_user_model()
        fields = ("id", "username", "password", 'email',)

    def create(self, validated_data):
        password = make_password(validated_data.get('password'))
        validated_data['password'] = password
        return super(SignUpSerializer, self).create(validated_data)


class FeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feedback
        fields = ('id', 'feedback', 'min_value', 'max_value', 'indicator')

    def validate(self, data):
        try:
            FeedbackValidator.validate_min_value(data)
        except FValidationError as err:
            raise serializers.ValidationError({'min_value': str(err)})
        return data
