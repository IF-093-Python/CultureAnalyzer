import random
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from faker import Faker
from CultureAnalyzer.constants import *
from users.choices import *

__all__ = ['create_fake_users', 'generate_fake_users', 'generate_fake_user']

EMAIL_DOMAINS = ('gmail.com', 'yahoo.com',
                 'hotmail.com', 'aol.com',
                 'yandex.ru', 'mail.ru')

fake = Faker()


class User:
    def __init__(self, username, password, first_name, last_name, email,
                 gender,
                 education, experience, date_of_birth):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.gender = gender
        self.education = education
        self.experience = experience
        self.date_of_birth = date_of_birth

    def __repr__(self) -> str:
        return f"User(username='{self.username}', " \
               f"first_name='{self.first_name}', " \
               f"last_name='{self.last_name}')"


def person_data():
    gender = random.choice(GENDER_CHOICES)[0]
    if gender == 'Male':
        first_name = fake.first_name_male()
        last_name = fake.last_name_male()
    else:
        first_name = fake.first_name_female()
        last_name = fake.last_name_female()
    date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=55)
    education = random.choice(EDUCATION_CHOICES)[0]
    return first_name, last_name, gender, date_of_birth, education


def generate_fake_user(username_prefix=''):
    first_name, last_name, gender, date_of_birth, education = person_data()
    username = username_prefix + first_name + last_name
    email = f'{first_name.lower()}_{last_name.lower()}' \
            f'@{random.choice(EMAIL_DOMAINS)}'
    password = username + '_qwerty'
    return User(username=username, password=password, first_name=first_name,
                last_name=last_name, email=email, gender=gender,
                education=education, experience=random.randint(1, 10),
                date_of_birth=date_of_birth)


def generate_fake_users(number, username_prefix=''):
    return (generate_fake_user(username_prefix) for _ in range(number))


def create_fake_users(number, username_prefix='', role_id=TRAINEE_ID):
    for u in generate_fake_users(number, username_prefix):
        created = get_user_model().objects.create(
            username=u.username, password=make_password(u.password),
            email=u.email, first_name=u.first_name, last_name=u.last_name,
            gender=u.gender, date_of_birth=u.date_of_birth,
            experience=u.experience, education=u.education
        )
        created.groups.set([Group.objects.get(id=role_id)])
        print(created.__dict__)
        print('*' * 150)
