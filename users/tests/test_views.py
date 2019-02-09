import datetime

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from users.models import Profile, Role


class TestViews(TestCase):

    def setUp(self):
        Role.objects.create(name='Trainee')
        self.user = User.objects.create_user(username='Test',
                                             password='testview123')
        self.response = self.client.login(username='Test',
                                          password='testview123')

    def test_index(self):
        response = self.client.get(reverse('home'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/index.html')

    def test_register_view(self):
        self.client.post(reverse('register'), {
            'username': 'Yurii',
            'email': 'jura@mail.com',
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

        self.assertEquals(response.status_code, 302)

    def test_update_profile_view(self):

        self.response = self.client.post(reverse('profile',
                                                 args=[self.user.id]), {
            'first_name': 'Yurii',
            'experience': 1,
            'date_of_birth': datetime.date(1999, 5, 21),
            'education': 'Secondary',
            'gender': 'Male',
        })

        self.user.refresh_from_db()
        self.assertEquals(self.user.first_name, 'Yurii')
        self.assertEquals(self.user.profile.education, 'Secondary')
        self.assertEquals(self.user.profile.gender, 'Male')
        self.assertEquals(self.user.profile.date_of_birth,
                          datetime.date(1999, 5, 21))
