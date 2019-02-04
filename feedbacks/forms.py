from django import forms
from .models import (
    Feedback,
    Recommendation
)
from .validator import FeedbackValidator


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
