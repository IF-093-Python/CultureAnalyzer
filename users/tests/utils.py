from datetime import datetime
from django.utils.timezone import get_current_timezone

from unittest import mock


def tz_datetime(**datetime_kwargs):
    return datetime(tzinfo=get_current_timezone(), **datetime_kwargs)


def mock_datetime_from(**datetime_kwargs):
    return mock.Mock(return_value=tz_datetime(**datetime_kwargs))


def mock_datetime_now(module, **datetime_kwargs):
    def decorator(fun):
        @mock.patch(module)
        def wrapper(*args, **kwargs):
            args = list(args)
            datetime_mock = args.pop(1)
            datetime_mock.now = mock_datetime_from(**datetime_kwargs)
            return fun(*args, **kwargs)

        return wrapper

    return decorator
