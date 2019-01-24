from django import forms
from .models import CountryIndicator


class CountryIndicatorForm(forms.ModelForm):

    class Meta:
        model = CountryIndicator
        fields = '__all__'
