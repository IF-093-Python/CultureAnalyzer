from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.test import TestCase
from django.urls import reverse

from feedbacks.tests.mixins import SetUpUserMixin
from users.tests_data.test_view_data import REGISTER_DATA, UPDATE_PROFILE_DATA

__all__ = ['LoginViewTest', 'RegisterViewTest', 'UpdateUserViewTest',
           'PasswordChangeViewTest', 'TestViews']


class LoginViewTest(SetUpUserMixin, TestCase):

    def setUp(self):
        self.client.login(username='test_user', password='12345')

    def test_redirect_when_user_logged_in(self):
        response = self.client.post(reverse('login'), {'username': 'test_user',
                                                       'password': '12345'})

        self.assertEqual(response.status_code, 302)

    def test_redirect_to_home_page_if_user_logged_in(self):
        response = self.client.get(reverse('login'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))


class RegisterViewTest(SetUpUserMixin, TestCase):

    def setUp(self):
        self.client.login(username='test_user', password='12345')

    def test_register_view(self):
        response = self.client.post(reverse('register'), REGISTER_DATA)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(get_user_model().objects.get(username='Yurii').email,
                         'jura@mail.com')

    def test_redirect_to_home_page_if_user_logged_in(self):
        response = self.client.get(reverse('register'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))


class UpdateUserViewTest(SetUpUserMixin, TestCase):

    def setUp(self):
        self.client.login(username='test_user', password='12345')

    def test_valid_data_update_view(self):
        current_user = get_user_model().objects.get(username='test_user')
        response = self.client.post(reverse('profile-update'),
                                    UPDATE_PROFILE_DATA)

        current_user.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('profile'))
        self.assertEqual(current_user.first_name, 'Yurii')


class PasswordChangeViewTest(SetUpUserMixin, TestCase):
    def setUp(self):
        self.client.login(username='test_user', password='12345')

    def test_change_password(self):
        response = self.client.post(
            reverse('password-change'),
            {'old_password': '12345', 'new_password1': 'test_qwerty1',
             'new_password2': 'test_qwerty1'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))


class TestViews(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='Test',
                                                         password='testview123')
        self.response = self.client.login(username='Test',
                                          password='testview123')

    def test_group_and_user_indepenent(self):
        group = Group.objects.get(name="Mentor")
        permission = Permission.objects.get(codename='view_feedback')
        group.permissions.add(permission)
        self.assertFalse(self.user.has_perm('feedbacks.view_feedback'))

    def test_group_provide_permission(self):
        group = Group.objects.get(name="Mentor")
        permission = Permission.objects.get(codename='view_feedback')
        group.permissions.add(permission)
        self.user.groups.add(group)
        self.assertTrue(self.user.has_perm('feedbacks.view_feedback'))

    def test_preserve_user_permissions_when_added_to_a_group_with_privileges(
            self):
        group = Group.objects.get(name="Mentor")
        permission = Permission.objects.get(codename='view_feedback')
        group.permissions.add(permission)
        self.user.groups.add(group)
        self.user.user_permissions.add(permission)
        self.assertTrue(self.user.has_perm('feedbacks.view_feedback'))
