from ddt import ddt, data
from django.contrib.auth import get_user_model
from django.test import TestCase as DjangoTestCase
from unittest import TestCase

from feedbacks.forms import FeedbackForm
from feedbacks.models import Feedback
from feedbacks.tests_data.test_form_data import (FEEDBACK_INVALID_DATA,
                                                 FEEDBACK_VALID_DATA)
from feedbacks.tests_data.test_view_data import PAGE_STRING_VALUES

__all__ = ['FeedbackFormTest', ]


@ddt
class FeedbackFormTest(TestCase):
    @data(*FEEDBACK_VALID_DATA)
    def test_valid_form(self, value):
        form = FeedbackForm(data=value)
        self.assertTrue(form.is_valid())

    @data(*FEEDBACK_INVALID_DATA)
    def test_invalid_form(self, value):
        form = FeedbackForm(data=value)
        self.assertFalse(form.is_valid())


@ddt
class FeedbackListViewTest(DjangoTestCase):
    def setUp(self):
        get_user_model().objects.create_user('user', password='test').save()
        for i in range(10):
            Feedback.objects.create(feedback='Some text', min_value=i + 1,
                                    max_value=i + 5, indicator='PDI')

    def test_call_view_denies_anonymous(self):
        response = self.client.get('/feedbacks/', follow=True)
        self.assertRedirects(response, '/login/?next=/feedbacks/')
        response = self.client.post('/feedbacks/', follow=True)
        self.assertRedirects(response, '/login/?next=/feedbacks/')

    def test_call_view_loads(self):
        self.client.login(username='user', password='test')
        response = self.client.get('/feedbacks/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feedbacks/feedback_list.html')

    @data(*range(-10, 10))
    def test_call_view_where_page_number_int(self, page):
        self.client.login(username='user', password='test')
        response = self.client.get(f'/feedbacks/?page={page}')
        self.assertEqual(response.status_code, 200)

    @data(*PAGE_STRING_VALUES)
    def test_call_view_where_page_number_not_int(self, page):
        self.client.login(username='user', password='test')
        response = self.client.get(f'/feedbacks/?page={page}')
        self.assertEqual(response.status_code, 200)
