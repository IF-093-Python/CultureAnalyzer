from django.test import TestCase

from indicators.models import CountryIndicator
from indicators.forms import CountryIndicatorForm


class CountryIndicatorFormTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.indicator_ukr = CountryIndicator.objects.create(
            iso_code='ukr',
            name='Ukraine',
            pdi=10,
            ind=2,
            mas=30,
            uai=4,
            lto=50,
            ivr=6)

    @classmethod
    def tearDownClass(cls):
        pass

    def test_correct_input(self):
        form = CountryIndicatorForm(data={
            'iso_code': 'deu',
            'name': 'Germany',
            'pdi': 2,
            'ind': 1,
            'mas': 3,
            'uai': 1,
            'lto': 1,
            'ivr': 1,

        })
        self.assertTrue(form.is_valid())

    def test_existing_iso_code_input(self):
        form = CountryIndicatorForm(data={
            'iso_code': 'ukr',
            'name': 'Ukraine',
            'pdi': 2,
            'ind': 1,
            'mas': 3,
            'uai': 1,
            'lto': 1,
            'ivr': 1,
        })
        self.assertFalse(form.is_valid())

    def test_whitespaces_iso_code(self):
        form = CountryIndicatorForm(data={
            'iso_code': 'u ',
            'name': 'some country name',
            'pdi': 2,
            'ind': 1,
            'mas': 3,
            'uai': 1,
            'lto': 1,
            'ivr': 1,
        })
        self.assertFalse(form.is_valid())

    def test_symbols_in_iso_code(self):
        form = CountryIndicatorForm(data={
            'iso_code': 'u3P',
            'name': 'some country name',
            'pdi': 2,
            'ind': 1,
            'mas': 3,
            'uai': 1,
            'lto': 1,
            'ivr': 1,
        })
        self.assertFalse(form.is_valid())

    def test_indicator_negative_input(self):
        form = CountryIndicatorForm(data={
            'iso_code': 'aaa',
            'name': 'some country name',
            'pdi': -2,
            'ind': 1,
            'mas': 3,
            'uai': 1,
            'lto': 1,
            'ivr': 1,
        })
        self.assertFalse(form.is_valid())

    def test_indicator_higher_bound(self):
        form = CountryIndicatorForm(data={
            'iso_code': 'aaa',
            'name': 'some country name',
            'pdi': 2,
            'ind': 1,
            'mas': 3,
            'uai': 101,
            'lto': 1,
            'ivr': 1,
        })
        self.assertFalse(form.is_valid())