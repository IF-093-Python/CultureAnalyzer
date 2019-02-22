import datetime

from django.test import TestCase

from users.forms import UserUpdateForm


class ProfileFormTest(TestCase):

    def test_valid_form(self):
        form = UserUpdateForm(data={
            'experience': 10,
            'date_of_birth': datetime.date(1999, 12, 1),
            'education': 'Higher',
            'gender': 'Male',
        })
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = UserUpdateForm(data={
            'experience': -1,
            'date_of_birth': datetime.date(1999, 12, 1),
            'education': 'Higher',
            'gender': 'Male',
        })
        self.assertFalse(form.is_valid())

    def test_invalid_form_with_invalid_choice(self):
        form = UserUpdateForm(data={
            'experience': 12,
            'date_of_birth': datetime.date(2000, 11, 2),
            'education': '',
            'gender': '',
        })
        self.assertFalse(form.is_valid())
