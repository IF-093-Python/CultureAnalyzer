from ddt import ddt, data
from django.test import TestCase

from CultureAnalyzer.exceptions import PValidationError
from users.tests_data.test_validations_error import (
    INVALID_VALIDATION_GREATER_THAN_HUNDRED,
    INVALID_VALIDATION_LESS_THAN_ZERO_DATA,
    INVALID_VALIDATION_NOT_INT)
from users.validators import ProfileValidator


@ddt
class TestValidators(TestCase):
    @data(*INVALID_VALIDATION_LESS_THAN_ZERO_DATA)
    def test_raises_pvalidatior_error_when_less_than_zero(self, value):
        with self.assertRaises(PValidationError):
            ProfileValidator.validate(value)

    @data(*INVALID_VALIDATION_GREATER_THAN_HUNDRED)
    def test_raises_pvalidatior_error_when_grater_than_hundred(self, value):
        with self.assertRaises(PValidationError):
            ProfileValidator.validate(value)

    @data(*INVALID_VALIDATION_NOT_INT)
    def test_raises_pvalidatior_error_when_value_is_not_int(self, value):
        with self.assertRaises(PValidationError):
            ProfileValidator.validate(value)
