from ddt import ddt, data
from django.contrib.auth import get_user_model
from django.test import TestCase as DjangoTestCase
from rest_framework import status

from api.tests.data.data_sign_up import VALID_SIGN_UP_DATA


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
