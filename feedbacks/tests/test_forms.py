from ddt import ddt, data
from django.test import TestCase

from feedbacks.tests_data.test_form_data import (
    FEEDBACK_MIN_VALUE_IS_LESS_MAX_VALUE_DATA,
    FEEDBACK_MIN_VALUE_IS_GREATER_MAX_VALUE_DATA)
from feedbacks.forms import FeedbackForm

__all__ = ['FeedbackFormTest', ]


@ddt
class FeedbackFormTest(TestCase):
    @data(*FEEDBACK_MIN_VALUE_IS_LESS_MAX_VALUE_DATA)
    def test_feedback_form_min_value_is_less_then_max_value(self, value):
        form = FeedbackForm(data=value)
        self.assertTrue(form.is_valid())

    @data(*FEEDBACK_MIN_VALUE_IS_GREATER_MAX_VALUE_DATA)
    def test_feedback_form_min_value_is_greater_then_max_value(self, value):
        form = FeedbackForm(data=value)
        self.assertFalse(form.is_valid())
