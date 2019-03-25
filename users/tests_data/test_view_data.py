import datetime

__all__ = ['REGISTER_DATA', 'UPDATE_PROFILE_DATA']

REGISTER_DATA = {
    'username': 'Yurii',
    'email': 'jura@mail.com',
    'first_name': 'Yurii',
    'last_name': 'Kulyk',
    'password1': 'testview123',
    'password2': 'testview123',
}

UPDATE_PROFILE_DATA = {
    'first_name': 'Yurii',
    'last_name': 'Kulyk',
    'experience': 1,
    'date_of_birth': datetime.date(1999, 5, 21),
    'education': 'Secondary',
    'gender': 'Male',
}
