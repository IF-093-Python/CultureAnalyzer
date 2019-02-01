from django.contrib.auth.models import User
from django.test import TestCase

# noinspection PyUnresolvedReferences
from .signals import (
    create_profile,
    save_profile
)


class UserTestCase(TestCase):
    fixtures = 'fixtures',

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        User.objects.create(username="john")
        User.objects.create(username="alex")
        User.objects.create(username="Admin")

    def test_john(self):
        john = User.objects.get(username="john")
        self.assertEqual(john.username, 'john')

    def test_alex(self):
        alex = User.objects.get(username="alex")
        self.assertEqual(alex.username, 'alex')
