from django import forms

from .models import CountryIndicator
from .validators import *


class CountryIndicatorForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CountryIndicatorForm, self).__init__(*args, **kwargs)
        self.fields['iso_code'].strip = False

    class Meta:
        model = CountryIndicator
        fields = '__all__'
        help_texts = {
            'iso_code': ('*Iso code must contains exactly 3 characters<br>'
                         '*Must contains only latin letters<br>'
                         '*Must be only letters'),
            }

    def clean_iso_code(self):
        iso_code = self.cleaned_data.get('iso_code')
        iso_code = validate_whitespaces(iso_code)
        iso_code = iso_code.upper()
        iso_code = validate_english_letters(iso_code)
        iso_code = validate_identity(iso_code)
        return iso_code
