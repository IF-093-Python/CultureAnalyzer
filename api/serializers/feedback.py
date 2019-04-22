from rest_framework import serializers

from CultureAnalyzer.exceptions import FValidationError
from feedbacks.models import Feedback
from feedbacks.validator import FeedbackValidator

__all__ = ['FeedbackSerializer']


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
