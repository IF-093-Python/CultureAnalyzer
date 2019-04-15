from django.test import TestCase as DjangoTestCase

from users.tasks import clear_expired_sessions
from users.tests.utils import mock_now


class TaskClearSessionsTest(DjangoTestCase):
    def setUp(self):
        pass

    @mock_now(year=2028, month=1, day=1, hour=12)
    def test_clear_expired_sessions(self):
        clear_expired_sessions()
