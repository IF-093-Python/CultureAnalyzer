import datetime

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from users.tests.mixins import SetUpMixin


class LoginViewTest(SetUpMixin, TestCase):

    def test_redirect_when_user_logged_in(self):
        response = self.client.post(reverse('login'), {
                                    'username': 'TestUser', 'password': 'test_qwerty'})

        self.assertEqual(response.status_code, 302)

    def test_redirect_to_home_page_if_user_logged_in(self):
        self.client.login(username='TestUser', password='test_qwerty')
        response = self.client.get(reverse('login'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))


class RegisterViewTest(SetUpMixin, TestCase):

    def test_register_view(self):
        response = self.client.post(reverse('register'), {
            'username': 'Yurii',
            'email': 'jura@mail.com',
            'first_name': 'Yurii',
            'last_name': 'Kulyk',
            'password1': 'testview123',
            'password2': 'testview123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(get_user_model().objects.get(username='Yurii').email,
                         'jura@mail.com')

    def test_redirect_to_home_page_if_user_logged_in(self):
        self.client.login(username='TestUser', password='test_qwerty')
        response = self.client.get(reverse('register'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))


class UpdateUserViewTest(SetUpMixin, TestCase):

    def test_valid_data_update_view(self):
        self.client.login(username='TestUser', password='test_qwerty')
        current_user = get_user_model().objects.get(username='TestUser')
        response = self.client.post(reverse('profile', args=[current_user.id]), {
                                    'first_name': 'Yurii', 'last_name': 'Kulyk',
                                    'experience': 1,
                                    'date_of_birth': datetime.date(
                                        1999, 5, 21),
                                    'education': 'Secondary',
                                    'gender': 'Male', })

        current_user.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(current_user.first_name, 'Yurii')

    def test_get_403_to_user(self):
        self.client.login(username='TestUser', password='test_qwerty')
        another_user = get_user_model().objects.create_user(username='Another',
                                                            password='another_qwerty',
                                                            email='ano@mail.com')

        response = self.client.get(reverse('profile', args=[another_user.id]))
        self.assertEqual(response.status_code, 403)
