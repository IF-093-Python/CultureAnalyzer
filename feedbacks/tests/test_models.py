from django.db.utils import IntegrityError
from django.test import TestCase

from feedbacks.models import Feedback, Recommendation

__all__ = ['FeedbackModelTest', ]


class FeedbackModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Feedback.objects.create(feedback='Some useful feedback', min_value=10,
                                max_value=20, indicator='PDI')

    def test_get_absolute_url(self):
        feedback = Feedback.objects.get(pk=1)
        self.assertEquals(feedback.get_absolute_url(), '/feedbacks/1')

    def test_object_name_is_first_30_characters_of_feedback(self):
        feedback = Feedback.objects.get(pk=1)
        expected_object_name = feedback.feedback[:30]
        self.assertEquals(expected_object_name, str(feedback))

    def test_unique_together_min_max_and_indicator(self):
        with self.assertRaises(IntegrityError) as cm:
            Feedback.objects.create(feedback='Some feedback with the same data',
                                    min_value=10, max_value=20, indicator='PDI')
        self.assertTrue(isinstance(cm.exception, IntegrityError))
