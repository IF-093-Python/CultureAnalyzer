from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.test import TestCase


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
