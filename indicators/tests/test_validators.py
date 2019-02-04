import string

from django.test import TestCase
from django.forms import ValidationError

from indicators.validators import validate_english_letters, validate_identity,\
                        validate_whitespaces
from indicators.models import CountryIndicator
from indicators.utils import opposite_letter_case


class EnglishLettersTest(TestCase):

    def test_all_uppercase_latin_letters_input(self):
        self.assertEqual(validate_english_letters('ABF'), 'ABF')
        self.assertEqual(validate_english_letters('HELLO'), 'HELLO')
        self.assertEqual(validate_english_letters('HHHHH'), 'HHHHH')
        self.assertEqual(validate_english_letters(string.ascii_uppercase),
                          string.ascii_uppercase)

    def test_with_different_characters_input(self):
        self.assertRaises(ValidationError,
                          validate_english_letters, 'AF F')
        self.assertRaises(ValidationError,
                          validate_english_letters, 'AAr')
        self.assertRaises(ValidationError,
                          validate_english_letters, '318')
        self.assertRaises(ValidationError,
                          validate_english_letters, 'ukr')
        self.assertRaises(ValidationError,
                          validate_english_letters, 'KDS!D#S')
        self.assertRaises(ValidationError,
                          validate_english_letters, '-+=')


class WhitespacesTest(TestCase):

    def test_input_without_whitespaces(self):
        self.assertEqual(validate_whitespaces('USA'), 'USA')
        self.assertEqual(validate_whitespaces('UKR'), 'UKR')
        self.assertEqual(validate_whitespaces('fdas$32k'), 'fdas$32k')

    def test_input_with_whitespaces(self):
        self.assertRaises(ValidationError, validate_whitespaces, ' UK')
        self.assertRaises(ValidationError, validate_whitespaces, 'zx ')
        self.assertRaises(ValidationError, validate_whitespaces, '\t\tGER')

    def test_raised_message(self):
        visual_whitespace = "\u2423"

        expected_message = (f'You enter contains spaces:'
                            f' "{visual_whitespace}{visual_whitespace}R"')
        with self.assertRaisesMessage(ValidationError, expected_message):
            validate_whitespaces('  R')

        expected_message = (f'You enter contains spaces:'
                            f' "{visual_whitespace}F{visual_whitespace}"')
        with self.assertRaisesMessage(ValidationError, expected_message):
            validate_whitespaces(' F ')

        expected_message = (f'You enter contains spaces:'
                            f' "as{visual_whitespace}"')
        with self.assertRaisesMessage(ValidationError, expected_message):
            validate_whitespaces('as ')


class IdentityIndicatorTest(TestCase):

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

    def test_new_indicator(self):
        self.assertEqual(validate_identity('usa'), 'usa')

    def test_on_existing_indicator(self):
        self.assertRaises(ValidationError, validate_identity,
                          self.indicator_ukr.iso_code)

    def test_on_existing_indicator_with_different_case(self):
        self.assertRaises(ValidationError, validate_identity,
                          opposite_letter_case(self.indicator_ukr.iso_code))
