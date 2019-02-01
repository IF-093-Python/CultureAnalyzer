from django.contrib.auth.models import User
from django.test import TestCase

# noinspection PyUnresolvedReferences
from users.signals import (
    create_profile,
    save_profile
)


class TutorTestCase(TestCase):
    fixtures = 'fixtures',

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        User.objects.create(username="a")

    def test_temp(self):
        pass


