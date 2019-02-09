from rest_framework import serializers

from feedbacks.models import *

__all__ = ['FeedbackSerializer', 'RecommendationSerializer', ]


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'


class RecommendationSerializer(serializers.ModelSerializer):
    feedback = serializers.PrimaryKeyRelatedField(queryset=Feedback.objects.all())

    class Meta:
        model = Recommendation
        fields = '__all__'
