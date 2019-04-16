from datetime import datetime
from django.utils.timezone import get_current_timezone

from unittest import mock


def mock_now_from(**datetime_kwargs):
    mock_value = datetime(tzinfo=get_current_timezone(), **datetime_kwargs)
    return mock.Mock(return_value=mock_value)


def mock_datetime_now(**datetime_kwargs):
    def decorator(fun):
        @mock.patch("users.tasks.datetime")
        def wrapper(*args, **kwargs):
            args = list(args)
            datetime_mock = args.pop(1)
            datetime_mock.now = mock_now_from(**datetime_kwargs)
            return fun(*args, **kwargs)

        return wrapper

    return decorator
