from django.contrib.auth.models import User
from django.test import TestCase


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
