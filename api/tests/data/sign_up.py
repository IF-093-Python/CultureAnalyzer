__all__ = ['VALID_SIGN_UP_DATA', 'INVALID_SIGN_UP_FULL_DATA']

VALID_SIGN_UP_DATA = (
    {'username': 'john0',
     'password': 'John_qwerty',
     'email': 'john@example.com',
     'first_name': 'John',
     'last_name': 'Deli'},

    {'username': 'alex1',
     'password': 'alex_qwerty',
     'email': 'alex@example.com',
     'first_name': 'Alex',
     'last_name': 'Lingard'},

    {'username': 'Leyla',
     'password': 'Leyla_qwerty',
     'email': 'leyla123@example.com',
     'first_name': 'Leyla',
     'last_name': 'Watson'},
)

INVALID_SIGN_UP_DATA = (
    {'username': '',
     'password': 'John_qwerty',
     'email': 'john@example.com',
     'first_name': 'John',
     'last_name': 'Vargas'},

    {'username': 'alex1',
     'password': '',
     'email': 'alex@example.com',
     'first_name': 'Alex',
     'last_name': 'Horner'},

    {'username': 'elon003',
     'password': '123',
     'email': 'elon1234@example.com',
     'first_name': 'Elon',
     'last_name': 'Howell'},

    {'username': 'kelvin22',
     'password': 'qwerty',
     'email': 'kln134@example.com',
     'first_name': 'Kelvin',
     'last_name': 'Jameson'},

    {'username': 'Stephan002',
     'password': 'Stephan002_qwerty12356789',
     'email': '',
     'first_name': 'Stephan',
     'last_name': 'Thompson'},

    {'username': 'Jan23323',
     'password': 'Jan0329_qwerty12356789',
     'email': 'jan@com',
     'first_name': 'Jan',
     'last_name': 'Lane'},
)

INVALID_SIGN_UP_EXPECTED_RESULT = (
    {'username': ['This field may not be blank.']},

    {'password': ['This field may not be blank.']},
    {'password': [
        'This password is too short. It must contain at least 8 characters.',
        'This password is too common.',
        'This password is entirely numeric.',
    ]},
    {'password': [
        'This password is too short. It must contain at least 8 characters.',
        'This password is too common.',
    ]},

    {'email': ['This field may not be blank.']},
    {'email': ['Enter a valid email address.']},
)

INVALID_SIGN_UP_FULL_DATA = zip(INVALID_SIGN_UP_DATA,
                                INVALID_SIGN_UP_EXPECTED_RESULT)
