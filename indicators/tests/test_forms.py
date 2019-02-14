from django.test import TestCase
from ddt import ddt, data, unpack

from indicators.models import CountryIndicator
from indicators.forms import CountryIndicatorForm

__all__ = ['CountryIndicatorFormTest']


_fx_form_data_valid = (
    (
        {'iso_code': 'deu', 'name': 'Germany', 'pdi': 2,
         'ind': 4, 'mas': 6, 'uai': 5, 'lto': 2, 'ivr': 3},
        True,
    ),
    (
        {'iso_code': 'CHN', 'name': 'Chine', 'pdi': 0,
         'ind': 59, 'mas': 99, 'uai': 100, 'lto': 0, 'ivr': 98},
        True,
    ),
)

_fx_form_data_invalid = (
    (
        {'iso_code': 'ukr', 'name': 'Ukraine', 'pdi': 2,
         'ind': 4, 'mas': 6, 'uai': 5, 'lto': 2, 'ivr': 3},
        False,
    ),
    (
        {'iso_code': 'u  ', 'name': 'some country name', 'pdi': 1,
         'ind': 2, 'mas': 3, 'uai': 4, 'lto': 5, 'ivr': 6},
        False,
    ),
    (
        {'iso_code': 'u3P', 'name': 'some country name', 'pdi': 1,
         'ind': 2, 'mas': 3, 'uai': 4, 'lto': 5, 'ivr': 6},
        False,
    ),
    (
        {'iso_code': 'aaa', 'name': 'some country name', 'pdi': 1,
         'ind': 2, 'mas': -3, 'uai': 4, 'lto': 5, 'ivr': 6},
        False,
    ),
    (
        {'iso_code': 'aaa', 'name': 'some country name', 'pdi': 1,
         'ind': 2, 'mas': 3, 'uai': 101, 'lto': 5, 'ivr': 6},
        False
    ),
)


@ddt
class CountryIndicatorFormTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.indicator_ukr = CountryIndicator.objects.create(
            iso_code='ukr',
            name='Ukraine',
            pdi=10,
            ind=2,
            mas=30,
            uai=4,
            lto=50,
            ivr=6)

    @unpack
    @data(*_fx_form_data_valid, *_fx_form_data_invalid)
    def test_input_data_should_be_validated_correctly(self, data_, expected):
        self.assertEqual(CountryIndicatorForm(data=data_).is_valid(), expected)
