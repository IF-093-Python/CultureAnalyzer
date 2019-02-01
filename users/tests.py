import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from .forms import ProfileUpdateForm

__all__ = ['ProfileFormTest', 'UserTestCase']


class ProfileFormTest(TestCase):

    def test_valid_form(self):
        form = ProfileUpdateForm(data={
            'experience': 10,
            'date_of_birth': datetime.date(1999, 12, 1),
            'education': 'Higher',
            'gender': 'Male',
        })
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = ProfileUpdateForm(data={
            'experience': -1,
            'date_of_birth': datetime.date(1999, 12, 1),
            'education': 'Higher',
            'gender': 'Male',
        })
        self.assertFalse(form.is_valid())


class UserTestCase(TestCase):
    fixtures = ('fixtures.json',)

    def setUp(self):
        User.objects.create(username="john")
        User.objects.create(username="alex")

    def test_user(self):
        lion = User.objects.get(username="john")
        self.assertEqual(lion.username, 'john')

    def test_some(self):
        lion = User.objects.get(username="alex")
        self.assertEqual(lion.username, 'alex')
