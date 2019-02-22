import datetime

from django.test import TestCase
from django.urls import reverse

from users.models import CustomUser


class TestViews(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username='Test',
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

        self.assertEquals(CustomUser.objects.get(username='Yurii').email,
                          'jura@mail.com')

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
                                             'date_of_birth': datetime.date(
                                                 1999, 5, 21),
                                             'education': 'Secondary',
                                             'gender': 'Male',
                                         })

        self.user.refresh_from_db()
        self.assertEquals(self.user.first_name, 'Yurii')
        self.assertEquals(self.user.education, 'Secondary')
        self.assertEquals(self.user.gender, 'Male')
        self.assertEquals(self.user.date_of_birth,
                          datetime.date(1999, 5, 21))
