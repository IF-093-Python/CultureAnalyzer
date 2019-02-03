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
    feedback = forms.ModelChoiceField(Feedback.objects.all())
    recommendation = forms.Textarea()

    def __init__(self, feedback, *args, **kwargs):
        """
        Set current feedback as selected element and disable select because
        form field attr disable=True doesn't work
        """
        super(RecommendationForm, self).__init__(*args, **kwargs)
        self.initial['feedback'] = feedback
        self.fields['feedback'].widget.attrs['readonly'] = True

    class Meta:
        model = Recommendation
        fields = ('feedback', 'recommendation')
