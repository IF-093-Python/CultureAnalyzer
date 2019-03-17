from ddt import ddt, data, unpack
from django.contrib.auth import get_user_model
from django.test import TestCase as DjangoTestCase
from rest_framework import status

from api.tests.data.sign_up import (VALID_SIGN_UP_DATA,
                                    INVALID_SIGN_UP_FULL_DATA)

__all__ = ['SignUpTest']


@ddt
class SignUpTest(DjangoTestCase):
    @data(*VALID_SIGN_UP_DATA)
    def test_sign_up_valid(self, json):
        response = self.client.post('/api/sign-up/', json)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(username=json['username'])
        self.assertEqual(user.email, json['email'])
        self.assertEqual(user.first_name, json['first_name'])
        self.assertEqual(user.last_name, json['last_name'])

        is_login_successful = self.client.login(username=json['username'],
                                                password=json['password'])
        self.assertTrue(is_login_successful)

    @data(*INVALID_SIGN_UP_FULL_DATA)
    @unpack
    def test_sign_up_invalid(self, json, expected_error_message):
        response = self.client.post('/api/sign-up/', json)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_error_message)

    def test_already_exist_username(self):
        expected_error_message = {
            'username': ['A user with that username already exists.']
        }
        response = self.sign_up(login='nick', password='nick_qwerty')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.sign_up(login='nick', password='some_other_pass')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_error_message)

    def sign_up(self, login, password):
        return self.client.post('/api/sign-up/', {'username': login,
                                                  'password': password})
