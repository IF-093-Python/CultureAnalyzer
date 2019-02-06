from django.test import TestCase
from ddt import ddt, data, unpack

from indicators.models import CountryIndicator
from indicators.forms import CountryIndicatorForm

__all__ = ['CountryIndicatorFormTest']


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
    @data({'iso_code': 'deu', 'name': 'Germany', 'pdi': 2,
          'ind': 4, 'mas': 6, 'uai': 5, 'lto': 2, 'ivr': 3},
          {'iso_code': 'CHN', 'name': 'Chine', 'pdi': 0,
           'ind': 59, 'mas': 99, 'uai': 100, 'lto': 0, 'ivr': 98})
    def test_correct_input(self, iso_code, name, pdi, ind, mas, uai, lto, ivr):
        form = CountryIndicatorForm(data={
            'iso_code': iso_code,
            'name': name,
            'pdi': pdi,
            'ind': ind,
            'mas': mas,
            'uai': uai,
            'lto': lto,
            'ivr': ivr})
        self.assertTrue(form.is_valid())

    @unpack
    @data({'iso_code': 'ukr', 'name': 'Ukraine', 'pdi': 2,
          'ind': 4, 'mas': 6, 'uai': 5, 'lto': 2, 'ivr': 3},
          {'iso_code': 'u  ', 'name': 'some country name', 'pdi': 1,
           'ind': 2, 'mas': 3, 'uai': 4, 'lto': 5, 'ivr': 6},
          {'iso_code': 'u3P', 'name': 'some country name', 'pdi': 1,
           'ind': 2, 'mas': 3, 'uai': 4, 'lto': 5, 'ivr': 6},
          {'iso_code': 'aaa', 'name': 'some country name', 'pdi': 1,
           'ind': 2, 'mas': -3, 'uai': 4, 'lto': 5, 'ivr': 6},
          {'iso_code': 'aaa', 'name': 'some country name', 'pdi': 1,
           'ind': 2, 'mas': 3, 'uai': 101, 'lto': 5, 'ivr': 6
           })
    def test_incorrect_input(self, iso_code, name, pdi, ind, mas, uai, lto,
                             ivr):
        form = CountryIndicatorForm(data={
            'iso_code': iso_code,
            'name': name,
            'pdi': pdi,
            'ind': ind,
            'mas': mas,
            'uai': uai,
            'lto': lto,
            'ivr': ivr})
        self.assertFalse(form.is_valid())
