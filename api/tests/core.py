from users.models.custom_user import CustomUser
from django.test.testcases import TestCase


class BaseRestTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        CustomUser.objects.create_user(username="john", password="john_qwerty")
        CustomUser.objects.create_user(username="alex", password="alex_qwerty")
        CustomUser.objects.create_user(username="luke", password="luke_qwerty")

    def assert_request(self, response, expected_status_code,
                       expected_response_keys=None,
                       expected_response_data=None):
        self.assertEqual(expected_status_code, response.status_code)
        self.assertIsNotNone(response.data)
        if expected_response_keys:
            self.assertTrue(json_contains_keys(expected_response_keys,
                                               response.data))
        if expected_response_data:
            self.assertEqual(expected_response_data, response.data)


def json_contains_keys(response_json: dict, keys: tuple) -> bool:
    return all(i in response_json for i in keys)
