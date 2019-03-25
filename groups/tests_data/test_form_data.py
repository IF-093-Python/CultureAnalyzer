import random, uuid
from django.utils import timezone

__all__ = ['shedule_valid_data', 'shedule_invalid_data',
           'invitation_valid_data', 'invitation_invalid_data', ]


def shedule_valid_data():
    data = [{'start': timezone.now() +
                      timezone.timedelta(minutes=random.randint(1, 3000)),
             'end': timezone.now() +
                    timezone.timedelta(minutes=random.randint(3001, 6000)),
             'quiz': random.randint(1, 100), }
            for _ in range(10)]
    return data


def shedule_invalid_data():
    data = []
    while len(data) < 10:
        random_dict = {
            'start': timezone.now() -
                     timezone.timedelta(minutes=random.randint(0, 3000)) +
                     timezone.timedelta(minutes=random.randint(0, 6000)),
            'end': timezone.now() -
                   timezone.timedelta(minutes=random.randint(0, 3000)) +
                   timezone.timedelta(minutes=random.randint(0, 6000)),
            'quiz': random.randint(1, 100), }
        data.append(random_dict)
    return data


def invitation_valid_data():
    data = [{'end': timezone.now() +
                    timezone.timedelta(minutes=random.randint(6001, 9000)),
             'group': random.randint(1, 100),
             'items_left': random.randint(1, 1000),
             'code': uuid.uuid4()
             }
            for _ in range(10)]
    return data


def invitation_invalid_data():
    data = []
    while len(data) < 10:
        random_dict = {
            'end': timezone.now() -
                   timezone.timedelta(minutes=random.randint(0, 3000)) +
                   timezone.timedelta(minutes=random.randint(0, 6000)),
            'group': random.randint(1, 100),
            'items_left': random.randint(0, 2),
            'code': uuid.uuid4(),
        }
        data.append(random_dict)
    return data
