from unittest import TestCase
from ddt import ddt, idata

from feedbacks.test_form_data import FEEDBACK_INVALID_DATA, FEEDBACK_VALID_DATA
from feedbacks.forms import FeedbackForm

__all__ = ['FeedbackFormTest', ]


def data_generator(const):
    for x in const:
        yield x


@ddt
class FeedbackFormTest(TestCase):
    @idata(data_generator(FEEDBACK_VALID_DATA))
    def test_valid_form(self, value):
        form = FeedbackForm(data=value)
        self.assertTrue(form.is_valid())

    @idata(data_generator(FEEDBACK_INVALID_DATA))
    def test_invalid_form(self, value):
        form = FeedbackForm(data=value)
        self.assertFalse(form.is_valid())
