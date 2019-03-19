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

    def test_already_exists_username(self):
        expected_error_message = {
            'username': ['A user with that username already exists.']
        }
        same_username = 'nick'
        account1 = self.sign_up(login=same_username, password='nick_qwerty',
                                email='nick@example.com')
        account2 = self.sign_up(login=same_username, password='other_pass',
                                email='other@example.com')
        self.assert_user_already_exists(account1, account2,
                                        expected_error_message)

    def test_already_exists_email(self):
        expected_error_message = {
            'email': ['A user with that email already exists.']
        }
        same_email = 'uniq-email@example.com'
        account1 = self.sign_up(login='nick',
                                password='nick_qwerty',
                                email=same_email)
        account2 = self.sign_up(login='alex',
                                password='some_other_pass',
                                email=same_email)
        self.assert_user_already_exists(account1, account2,
                                        expected_error_message)

    def assert_user_already_exists(self, create_account,
                                   create_account_with_same_unique,
                                   expected_error_message):
        response = create_account
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = create_account_with_same_unique
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_error_message)

    def sign_up(self, login, password, email):
        return self.client.post('/api/sign-up/', {'username': login,
                                                  'password': password,
                                                  'email': email})
