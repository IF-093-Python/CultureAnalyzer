import base64
import json
import unittest
from ddt import ddt, data, unpack
from django.contrib.auth.models import User
from rest_framework.exceptions import ErrorDetail

from .core import BaseRestTestCase


def field_error(field_name: str):
    return {field_name: [ErrorDetail(
        string='This field is required.',
        code='required')]}


def incorrect_data_error():
    return {'non_field_errors': [ErrorDetail(
        string='No active account found with the given credentials',
        code='invalid')]}


def incorrect_refresh_error():
    return {'detail': ErrorDetail(string='Token is invalid or expired',
                                  code='token_not_valid'),
            'code': ErrorDetail(string='token_not_valid',
                                code='token_not_valid')}


def credentials(login: str, password: str) -> dict:
    return {"username": login, "password": password}


def valid_john_credentials() -> dict:
    return credentials("john", "john_qwerty")


# ================================ Obtain ====================================
@ddt
class ObtainTokenTestCase(BaseRestTestCase):
    @unpack
    @data(('john', 'john_qwerty'),
          ('alex', 'alex_qwerty'),
          ('luke', 'luke_qwerty'))
    def test_successful_token_obtain(self, login, password):
        response = self.obtain_token(post_data=credentials(login, password))
        self.assert_request(response=response,
                            expected_status_code=200,
                            expected_response_keys=('access', 'refresh'))
        self.assertTrue(is_jwt_valid(response, login))

    @unpack
    @data(('john', 'j2ohn_qwerty'),
          ('alex', 'aalex_qwerty'),
          ('luke1', 'luke_qwerty'))
    def test_token_obtain_with_incorrect_data(self, login, password):
        response = self.obtain_token(post_data=credentials(login, password))
        self.assert_request(response=response,
                            expected_status_code=400,
                            expected_response_data=incorrect_data_error())

    def test_token_obtain_without_login(self):
        response = self.obtain_token(post_data={"password": "john_qwerty"})
        self.assert_request(response=response,
                            expected_status_code=400,
                            expected_response_data=field_error('username'))

    def test_token_obtain_without_password(self):
        response = self.obtain_token(post_data={"username": "john"})
        self.assert_request(response=response,
                            expected_status_code=400,
                            expected_response_data=field_error('password'))

    def obtain_token(self, post_data):
        return self.client.post("/api/token/obtain/",
                                data=post_data,
                                format='json')


# ================================ Refresh ===================================
class RefreshTokenTest(BaseRestTestCase):
    def test_successful_refresh_token(self):
        obtain_tokens = self.obtain_token()
        refresh = obtain_tokens.data['refresh']
        response = self.refresh_token(post_data={'refresh': refresh})
        self.assert_request(response=response,
                            expected_status_code=200,
                            expected_response_keys=('access',))
        old_token, new_token = (obtain_tokens.data['access'],
                                response.data['access'])
        self.assertNotEqual(old_token, new_token)

    def test_unsuccessful_refresh_token(self):
        bad_refresh_token = """
                eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tl
                bl90eXBlIjoicmVmcmVzaCIsImNvbGRfc3R1ZmYiOiLimIMiLCJleHAiOjIzN
                DU2NywianRpIjoiZGUxMmY0ZTY3MDY4NDI3ODg5ZjE1YWMyNzcwZGEwNTEifQ
                .aEoAYkSJjoWH1boshQAaTkf8G3yn0kapko6HFRt7Rh4
        """
        response = self.refresh_token(post_data={'refresh': bad_refresh_token})
        self.assert_request(response=response,
                            expected_status_code=401,
                            expected_response_data=incorrect_refresh_error())

    def obtain_token(self):
        return self.client.post('/api/token/obtain/',
                                data=valid_john_credentials(),
                                format='json')

    def refresh_token(self, post_data):
        return self.client.post("/api/token/refresh/", data=post_data,
                                format='json')


@ddt
class TokenAccessTest(BaseRestTestCase):

    @unittest.skip
    def test_user_has_access_using_token(self, login, password):
        access_token = self.obtain_access_token(login, password)
        response = self.get_protected_page(access_token)
        self.assert_request(response=response,
                            expected_status_code=200,
                            expected_response_data={'username': login})

    def obtain_access_token(self, login, password):
        return self.client.post('/api/token/obtain/',
                                data=credentials(login, password),
                                format='json').data['access']

    def get_protected_page(self, access_token):
        return self.client.get('/api/protected/',
                               HTTP_AUTHORIZATION=f'JWT {access_token}')


def decode_payload(payload_part) -> json:
    return json.loads(base64.b64decode(payload_part).decode('utf-8'))


def is_jwt_valid(response, login) -> bool:
    """
         JWT should looks like xxxx.yyyy.zzzz
         and contains correct user_id in payload after decode
     """
    expected_user_id = User.objects.get(username=login).id
    expected_jwt_parts_number = 3

    access_token, refresh_token = (response.data['access'],
                                   response.data['refresh'])
    split_access_token, split_refresh_token = (access_token.split('.'),
                                               refresh_token.split('.'))
    payload = decode_payload(split_access_token[1])

    return all([
        len(split_access_token) == expected_jwt_parts_number,
        len(split_refresh_token) == expected_jwt_parts_number,
        expected_user_id == payload['user_id']
    ])
