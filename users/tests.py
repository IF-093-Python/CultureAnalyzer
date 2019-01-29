from django.contrib.auth.models import User
from django.test import TestCase


class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="lion")

    def test_user(self):
        lion = User.objects.get(username="lion")
        self.assertEqual(lion.username, 'lion')
