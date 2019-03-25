from datetime import datetime

__all__ = ['VALID_UPDATE_USER_DATA', 'INVALID_UPDATE_USER_DATA']

VALID_UPDATE_USER_DATA = [
    {'first_name': 'Yurii', 'last_name': 'Kulyk', 'experience': 1,
     'date_of_birth': datetime.now(), 'education': 'Secondary',
     'gender': 'Male'},
    {'first_name': 'SomeOneElse', 'last_name': 'TestLast', 'experience': 68,
     'date_of_birth': datetime.now(), 'education': 'Secondary',
     'gender': 'Female'},
    {'first_name': 'ValidName', 'last_name': 'Valid', 'experience': 99,
     'date_of_birth': datetime.now(), 'education': 'Higher',
     'gender': 'Female'},
    {'first_name': '123', 'last_name': '123', 'experience': 1,
     'date_of_birth': datetime.now(), 'education': 'Special',
     'gender': 'Male'},
    {'first_name': 'Yurii', 'last_name': 'Kulyk', 'experience': 77,
     'date_of_birth': datetime.now(), 'education': 'Secondary',
     'gender': 'Male'},
]

INVALID_UPDATE_USER_DATA = [
    {'first_name': 'Yurii', 'last_name': 'Kulyk', 'experience': '',
     'date_of_birth': datetime.now(), 'education': 'Secondary',
     'gender': 'Male'},
    {'first_name': 'SomeOneElse', 'last_name': '', 'experience': 68,
     'date_of_birth': datetime.now(), 'education': '',
     'gender': 'Female'},
    {'first_name': '', 'last_name': 'Valid', 'experience': 99,
     'date_of_birth': datetime.now(), 'education': 'Higher',
     'gender': ''},
    {'first_name': '123', 'last_name': '123', 'experience': -1,
     'date_of_birth': datetime.now(), 'education': 'Special',
     'gender': 'Male'},
    {'first_name': 'Yurii', 'last_name': 'Kulyk', 'experience': 101,
     'date_of_birth': datetime.now(), 'education': 'Secondary',
     'gender': 'Male'},
    {'first_name': 'Yurii', 'last_name': 'Kulyk', 'experience': 100,
     'date_of_birth': '12-12-2012', 'education': 'Secondary',
     'gender': 'Male'},
]
