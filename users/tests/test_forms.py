from ddt import ddt, data
from django.test import TestCase


from users.tests_data.test_form_data import (
    VALID_UPDATE_USER_DATA,
    INVALID_UPDATE_USER_DATA
)
from users.forms import UserUpdateForm

__all__ = ['UpdateUserFormTest']


@ddt
class UpdateUserFormTest(TestCase):

    @data(*VALID_UPDATE_USER_DATA)
    def test_valid_update_user_data(self, value):
        form = UserUpdateForm(data=value)
        self.assertTrue(form.is_valid())

    @data(*INVALID_UPDATE_USER_DATA)
    def test_invalid_update_user_data(self, value):
        form = UserUpdateForm(data=value)
        self.assertFalse(form.is_valid())
