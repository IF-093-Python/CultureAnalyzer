from django import forms

from feedbacks.models import Feedback, Recommendation
from feedbacks.validator import FeedbackValidator
from feedbacks.exceptions import FValidationError

__all__ = ['FeedbackForm', 'RecommendationForm']


class FeedbackForm(forms.ModelForm):
    def clean(self):
        super().clean()
        try:
            FeedbackValidator.validate_min_value(self.cleaned_data)
        except FValidationError as err:
            self.add_error('min_value', str(err))

    class Meta:
        model = Feedback
        fields = ('feedback', 'min_value', 'max_value', 'indicator')


class RecommendationForm(forms.ModelForm):

    class Meta:
        model = Recommendation
        fields = ['recommendation', ]
