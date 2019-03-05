from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import Group as Profile, Permission
from django.contrib.auth import get_user_model
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
        permissions = Permission.objects.get(
            content_type__app_label='groups', codename='view_group')
        admin.permissions.add(permissions)
        user1.groups.set([admin])
        user2.groups.set([mentor])
        cls.client = Client()

    def test_group_list_view_permission(self):
        self.client.login(username='temporary2', password='temporary2')
        resp = self.client.get(reverse('groups:groups-list'))
        self.assertEqual(resp.status_code, 403)

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='temporary1', password='temporary1')
        resp = self.client.get('/groups/')
        self.assertEqual(resp.status_code, 200)

    # def test_view_url_accessible_by_name(self):
    #     self.client.login(username='temporary1', password='temporary1')
        resp = self.client.get(reverse('groups:groups-list'))
        self.assertEqual(resp.status_code, 200)

    # def test_view_uses_correct_template(self):
    #     self.client.login(username='temporary1', password='temporary1')
        resp = self.client.get(reverse('groups:groups-list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'groups/groups_list.html')

    # def test_pagination_is_50(self):
    #     self.client.login(username='temporary1', password='temporary1')
        resp = self.client.get(reverse('groups:groups-list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] is True)
        self.assertTrue(len(resp.context['group_list']) == 50)

    # def test_paginator_lists_all_groups(self):
    #     self.client.login(username='temporary1', password='temporary1')
        # Get third page and confirm it has (exactly) remaining 3 items
        resp = self.client.get(reverse('groups:groups-list') + '?page=3')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] is True)
        self.assertTrue(len(resp.context['group_list']) == 3)

    # def test_GroupListView_search(self):
    #     self.client.login(username='temporary1', password='temporary1')
        resp = self.client.get(
            reverse('groups:groups-list') + '?data_search=1')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('search' in resp.context)
        self.assertTrue('search_label' in resp.context)
        self.assertTrue(resp.context['search'] is True)
        self.assertTrue(resp.context['search_label'] == '1')

    # def test_GroupListView_without_search(self):
    #     self.client.login(username='temporary1', password='temporary1')
        resp = self.client.get(reverse('groups:groups-list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('search' in resp.context)
        self.assertTrue('search_label' in resp.context)
        self.assertTrue(resp.context['search'] is False)
        self.assertTrue(resp.context['search_label'] == 'Search')


class CreateGroupViewTest(TestCase):
    @classmethod
    def setUp(cls):
        user1 = get_user_model().objects.create_user(
            username='temporary1', email='temporary1@gmail.com',
            password='temporary1')
        user2 = get_user_model().objects.create_user(
            username='temporary2', email='temporary2@gmail.com',
            password='temporary2')
        admin = Profile.objects.get(name='Admin')
        mentor = Profile.objects.get(name='Mentor')
        # Create another 102 mentors  for pagination tests
        number_of_mentors = 102
        for mentor_num in range(number_of_mentors):
            get_user_model().objects.create(username='Mentor%s' % mentor_num,
                email='Mentor%s@gmail.com' % mentor_num, password='password')
            a = get_user_model().objects.get(username='Mentor%s' % mentor_num)
            a.groups.set([mentor])
        permission = Permission.objects.get(
            content_type__app_label='groups', codename='add_group')
        admin.permissions.add(permission)
        user1.groups.set([admin])
        user2.groups.set([mentor])
        cls.client = Client()

    def test_create_group_view_permission(self):
        self.client.login(username='temporary2', password='temporary2')
        resp = self.client.get(reverse('groups:create-group'))
        self.assertEqual(resp.status_code, 403)

    def test_create_group_view_url_exists_at_desired_location(self):
        self.client.login(username='temporary1', password='temporary1')
        resp = self.client.get('/groups/create_group/')
        self.assertEqual(resp.status_code, 200)

    # def test_create_group_view_url_accessible_by_name(self):
    #     self.client.login(username='temporary1', password='temporary1')
        resp = self.client.get(reverse('groups:create-group'))
        self.assertEqual(resp.status_code, 200)

    # def test_create_group_view_uses_correct_template(self):
    #     self.client.login(username='temporary1', password='temporary1')
        resp = self.client.get(reverse('groups:create-group'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'groups/group_create.html')

    # def test_create_group_view_pagination_is_50(self):
    #     self.client.login(username='temporary1', password='temporary1')
        resp = self.client.get(reverse('groups:create-group'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] is True)
        self.assertTrue(len(resp.context['object_list']) == 50)

    # def test_create_group_view_paginator_lists_all_mentors(self):
    #     self.client.login(username='temporary1', password='temporary1')
        # Get third page and confirm it has (exactly) remaining 3 items
        resp = self.client.get(reverse('groups:create-group') + '?page=3')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] is True)
        self.assertTrue(len(resp.context['object_list']) == 3)

    # def test_CreateGroupView_search(self):
    #     self.client.login(username='temporary1', password='temporary1')
        resp = self.client.get(
            reverse('groups:create-group') + '?data_search=1')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('search' in resp.context)
        self.assertTrue('search_label' in resp.context)
        self.assertTrue(resp.context['search'] is True)
        self.assertTrue(resp.context['search_label'] == '1')

    # def test_CreateGroupView_without_search(self):
    #     self.client.login(username='temporary1', password='temporary1')
        resp = self.client.get(reverse('groups:create-group'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('search' in resp.context)
        self.assertTrue('search_label' in resp.context)
        self.assertTrue(resp.context['search'] is False)
        self.assertTrue(resp.context['search_label'] == 'Search')

    def test_CreateGroupView_with_data(self):
        self.client.login(username='temporary1', password='temporary1')
        mentors = CustomUser.objects.filter(
            username__in=['Mentor5', 'Mentor27', 'Mentor93', 'Mentor45'])
        mentors = list(mentors.values_list('id', flat=True))
        self.client.post(reverse('groups:create-group'),
                         data={'name': 'somename', 'mentor': mentors})
        group = Group.objects.filter(mentor__in=mentors)
        self.assertTrue(Group.objects.filter(mentor__in=mentors).exists())
        self.assertTrue(len(group) == 4)
        self.assertTrue(len(group.distinct()) == 1)
