from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import Group as Profile, Permission
from groups.models import Group
from users.models import CustomUser


class GroupListViewTest(TestCase):
    @classmethod
    def setUp(cls):
        # Create 13 groups for pagination tests
        number_of_groups = 103
        for group_num in range(number_of_groups):
            Group.objects.create(name='Group%s' % group_num)
        user1 = CustomUser.objects.create_user(
            username='temporary1', email='temporary1@gmail.com',
            password='temporary1')
        user2 = CustomUser.objects.create_user(
            username='temporary2', email='temporary2@gmail.com',
            password='temporary2')
        admin = Profile.objects.get(name='Admin')
        mentor = Profile.objects.get(name='Mentor')
        # trainee = Profile.objects.get(name='Trainee')
        permissions = Permission.objects.filter(
            content_type__app_label='groups', codename='view_group')
        for p in permissions:
            admin.permissions.add(p)
        user1.groups.set([admin])
        user2.groups.set([mentor])
        cls.client = Client()

    def test_view_permission(self):
        self.client.login(username='temporary2', password='temporary2')
        resp = self.client.get(reverse('groups:groups-list'))
        self.assertEqual(resp.status_code, 403)

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='temporary1', password='temporary1')
        resp = self.client.get('/groups/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(username='temporary1', password='temporary1')
        resp = self.client.get(reverse('groups:groups-list'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='temporary1', password='temporary1')
        resp = self.client.get(reverse('groups:groups-list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'groups/groups_list.html')

    def test_pagination_is_5(self):
        self.client.login(username='temporary1', password='temporary1')
        resp = self.client.get(reverse('groups:groups-list'), follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(len(resp.context['group_list']) == 50)

    def test_lists_all_groups(self):
        self.client.login(username='temporary1', password='temporary1')
        # Get second page and confirm it has (exactly) remaining 3 items
        resp = self.client.get(reverse('groups:groups-list') + '?page=3')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(len(resp.context['group_list']) == 3)
