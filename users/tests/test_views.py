import datetime

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django import forms

from users.models import Profile, Role


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        Role.objects.create(name='Trainee')
        

    def test_index(self):
        response = self.client.get(reverse('home'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/index.html')

    def test_register_view(self):
        response = self.client.post(reverse('register'), {
            'username': 'Yurii',
            'email':'jura@mail.com',
            'first_name': 'Yurii',
            'last_name': 'Kulyk',
            'password1': 'testview123',
            'password2': 'testview123',
        })

        self.assertEquals(User.objects.get(username='Yurii').email,
                                            'jura@mail.com')
        self.assertEquals(User.objects.get(username='Yurii').profile.role.name,
                                            'Trainee')

    def test_login_view(self):
        response = self.client.post(reverse('login'), {
            'username': 'Test',
            'password': 'testview123'
        })

        self.assertEquals(response.status_code, 200)
        

