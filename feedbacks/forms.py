from django import forms

from feedbacks.models import Feedback, Recommendation
from feedbacks.validator import FeedbackValidator

__all__ = ['FeedbackForm', 'RecommendationForm']


class FeedbackForm(forms.ModelForm):
    def clean(self):
        super().clean()
        FeedbackValidator.validate_min_value(self)

    class Meta:
        model = Feedback
        fields = ('feedback', 'min_value', 'max_value', 'indicator')


class RecommendationForm(forms.ModelForm):

    class Meta:
        model = Recommendation
        fields = ['recommendation', ]
