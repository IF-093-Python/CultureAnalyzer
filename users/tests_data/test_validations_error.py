import random

__all__ = ['INVALID_VALIDATION_LESS_THAN_ZERO_DATA',
           'INVALID_VALIDATION_GREATER_THAN_HUNDRED',
           'INVALID_VALIDATION_NOT_INT']

INVALID_VALIDATION_LESS_THAN_ZERO_DATA = [random.randint(-100, -1) for _ in
                                          range(20)]

INVALID_VALIDATION_GREATER_THAN_HUNDRED = [random.randint(101, 300) for _ in
                                           range(20)]

INVALID_VALIDATION_NOT_INT = ['some', None, [], {}, (), 12.2]

