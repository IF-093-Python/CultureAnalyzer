from unittest import TestCase
from ddt import ddt, idata
from django.test import TestCase as DjangoTestCase
from django.contrib.auth.models import User

from feedbacks.test_form_data import FEEDBACK_INVALID_DATA, FEEDBACK_VALID_DATA
from feedbacks.forms import FeedbackForm

__all__ = ['FeedbackFormTest', ]


def form_data_generator(data):
    for x in data:
        yield x


@ddt
class FeedbackFormTest(TestCase):
    @idata(form_data_generator(FEEDBACK_VALID_DATA))
    def test_valid_form(self, value):
        form = FeedbackForm(data=value)
        self.assertTrue(form.is_valid())

    @idata(form_data_generator(FEEDBACK_INVALID_DATA))
    def test_invalid_form(self, value):
        form = FeedbackForm(data=value)
        self.assertFalse(form.is_valid())


class FeedbackListViewTest(DjangoTestCase):
    fixtures = ('users/fixtures/fixtures.json',)

    def setUp(self):
        User.objects.create_user('user', password='test').save()

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
