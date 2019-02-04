from django.test import TestCase

from feedbacks.models import Feedback, Recommendation
from feedbacks.forms import FeedbackForm


class FeedbackTestCase(TestCase):
    def setUp(self):
        Feedback.objects.create(feedback='Some useful feedback', min_value=5,
                                max_value=10, indicator='PDI')
        Feedback.objects.create(feedback='Some useless feedback', min_value=0,
                                max_value=15, indicator='IND')

    def test_values(self):
        useful = Feedback.objects.get(feedback='Some useful feedback')
        useless = Feedback.objects.get(feedback='Some useless feedback')
        self.assertEqual(useful.indicator, 'PDI')
        self.assertEqual(useless.max_value, 15)


class FeedbackFormTest(TestCase):
    def test_valid_form(self):
        form = FeedbackForm(data={
            'feedback': 'Some valid feedback',
            'min_value': 0,
            'max_value': 10,
            'indicator': 'PDI',
        })
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = FeedbackForm(data={
            'feedback': 'Some invalid feedback',
            'min_value': 0,
            'max_value': 10,
            'indicator': 'DSA',
        })
        self.assertFalse(form.is_valid())
        form = FeedbackForm(data={
            'feedback': 'Some invalid feedback',
            'min_value': 20,
            'max_value': 10,
            'indicator': 'PDI',
        })
        self.assertFalse(form.is_valid())


class RecommendationTestCase(TestCase):
    def setUp(self):
        Feedback.objects.create(feedback='Some useful feedback', min_value=5,
                                max_value=10, indicator='PDI')
        Recommendation.objects.create(
            recommendation='It is a good advice',
            feedback=Feedback.objects.get(feedback='Some useful feedback'))
        Recommendation.objects.create(
            recommendation='It is a bad advice',
            feedback=Feedback.objects.get(feedback='Some useful feedback'))

    def test_values(self):
        good = Recommendation.objects.get(recommendation='It is a good advice')
        bad = Recommendation.objects.get(recommendation='It is a bad advice')
        feedback = Feedback.objects.get(feedback='Some useful feedback')
        self.assertEqual(good.recommendation, 'It is a good advice')
        self.assertEqual(bad.feedback.feedback, feedback.feedback)
