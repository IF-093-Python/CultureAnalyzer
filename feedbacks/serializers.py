from rest_framework import serializers

from feedbacks.models import *
from feedbacks.validator import FeedbackValidator
from feedbacks.exceptions import FValidationError

__all__ = ['FeedbackSerializer', 'RecommendationSerializer', ]


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'

    def validate(self, data):
        try:
            FeedbackValidator.validate_min_value(data)
        except FValidationError as err:
            raise serializers.ValidationError({'min_value': str(err)})
        return data


class RecommendationSerializer(serializers.ModelSerializer):
    feedback = serializers.PrimaryKeyRelatedField(
        queryset=Feedback.objects.all())

    class Meta:
        model = Recommendation
        fields = '__all__'
