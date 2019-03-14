from django import forms

from .models import CountryIndicator

__all__ = ['CountryIndicatorForm']


class CountryIndicatorForm(forms.ModelForm):

    class Meta:
        model = CountryIndicator
        fields = '__all__'
        help_texts = {
            'iso_code': ('*Iso code must contains exactly 3 characters<br>'
                         '*Must contains only latin letters<br>'
                         '*Must be only letters'),
            }

    def clean_iso_code(self):
        return self.cleaned_data.get('iso_code').upper()
