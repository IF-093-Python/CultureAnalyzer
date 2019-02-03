from django.test import TestCase

from indicators.utils import opposite_letter_case


class OppositeLetterCaseTest(TestCase):

    def test_lower_case_input(self):
        self.assertEqual(opposite_letter_case('abc'), 'ABC')

    def test_upper_case_input(self):
        self.assertEqual(opposite_letter_case('DRY'), 'dry')

    def test_upper_with_different_cases(self):
        self.assertEqual(opposite_letter_case('AbC'), 'abc')
