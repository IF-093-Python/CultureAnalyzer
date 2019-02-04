import string
from django import forms

from .models import CountryIndicator


LETTERS = set(string.ascii_uppercase)


def validate_identity(iso_code):
    """
    Validate iso_code on identity with case insensitive value.

    Example: can't be codes 'ukr' and 'Ukr' or 'UKR' at same time.
    Pre-requirements: validate on CountryIndicator model
    :param iso_code: string data
    """
    if CountryIndicator.objects.filter(iso_code__iexact=iso_code)\
                               .count() > 0:
        raise forms.ValidationError(f'Iso code: {iso_code} already '
                                    f'exists.')

    return iso_code


def validate_whitespaces(data):
    """
    Validate if string data on containing whitespaces.

    Replace all whitespaces with visual symbol and pass it to validation
    error message.
    :param data: string data, len(data) > 0
    """
    visual_whitespace = "\u2423"
    data_striped = data.strip()
    if data != data_striped:
        visual_whitespaces_list = []
        index = 0
        for symbol in data:
            if symbol == data_striped[index]:
                visual_whitespaces_list.append(symbol)
                if index < len(data_striped) - 1:
                    index += 1
            else:
                visual_whitespaces_list.append(visual_whitespace)

        visual_whitespaces_string = ''.join(visual_whitespaces_list)
        raise forms.ValidationError(f'You enter contains spaces:'
                                    f' "{visual_whitespaces_string}"')
    return data


def validate_english_letters(data):
    """
    Validate if data contains only upper case latin letters

    :param data: string data, len(data) > 0
    """
    data_set = set(data)
    for i in data_set:
        if i not in LETTERS:
            raise forms.ValidationError('Iso code must contains only latin '
                                        'uppercase letters and only letters')
    return data

