import uuid
from datetime import timedelta
from django.contrib.sessions.models import Session
from django.test import TestCase as DjangoTestCase

from users.tasks import clear_expired_sessions
from users.tests.utils import mock_datetime_now, tz_datetime


class TaskClearSessionsTest(DjangoTestCase):
    @mock_datetime_now("users.tasks.datetime",
                       year=2018, month=1, day=1)
    def test_clear_expired_sessions(self):
        old_and_expired = tz_datetime(year=2017, month=1, day=1)
        new_and_not_expired = tz_datetime(year=2018, month=2, day=1)
        self.generate_sessions(old_and_expired, limit=10)
        self.generate_sessions(new_and_not_expired, limit=3)
        clear_expired_sessions()
        self.assertIs(Session.objects.count(), 3)

    def generate_sessions(self, initial_datetime,
                          days_interval=1, minutes_interval=0, limit=5):
        expire_date = initial_datetime
        for i in range(0, limit):
            random_key = uuid.uuid4().hex[0:35]
            expire_date += timedelta(days=days_interval,
                                     minutes=minutes_interval)
            Session.objects.create(session_key=random_key,
                                   expire_date=expire_date)
