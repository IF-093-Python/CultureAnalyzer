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
    feedback = forms.ModelChoiceField(Feedback.objects.none())
    recommendation = forms.Textarea()

    def __init__(self, feedback, *args, **kwargs):
        """
        Set current feedback as selected element
        """
        super(RecommendationForm, self).__init__(*args, **kwargs)
        self.fields['feedback'].queryset = Feedback.objects.filter(pk=feedback)
        self.initial['feedback'] = feedback

    class Meta:
        model = Recommendation
        fields = ('feedback', 'recommendation')
