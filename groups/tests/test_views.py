from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import Group as Profile, Permission
from django.contrib.auth import get_user_model
from groups.models import Group
from users.models import CustomUser

PAGINATOR = 50


class GroupListViewTest(TestCase):
    @classmethod
    def setUp(cls):
        # Create groups for pagination tests
        number_of_groups = PAGINATOR * 2 + 3
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

        # test_view_url_accessible_by_name:
        resp = self.client.get(reverse('groups:groups-list'))
        self.assertEqual(resp.status_code, 200)

        # test_view_uses_correct_template(self):
        resp = self.client.get(reverse('groups:groups-list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'groups/groups_list.html')

        # test_pagination_is_PAGINATOR:
        resp = self.client.get(reverse('groups:groups-list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] is True)
        self.assertTrue(len(resp.context['group_list']) == PAGINATOR)

        # test_paginator_lists_all_groups:
        # Get third page and confirm it has (exactly) remaining 3 items
        resp = self.client.get(reverse('groups:groups-list') + '?page=3')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] is True)
        self.assertTrue(len(resp.context['group_list']) == 3)

        # test_GroupListView_search:
        resp = self.client.get(
            reverse('groups:groups-list') + '?data_search=1')
        self.assertEqual(resp.status_code, 200)
        # test that search returns 22 groups (with '1' in name from 0 to 102)
        groups = resp.context['group_list']
        self.assertTrue(len(groups) == 22)
        self.assertTrue('search' in resp.context)
        self.assertTrue('search_label' in resp.context)
        self.assertTrue(resp.context['search'] is True)
        self.assertTrue(resp.context['search_label'] == '1')

        # test_GroupListView_without_search:
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
        # Create another PAGINATOR*2+2 mentors  for pagination tests
        number_of_mentors = PAGINATOR * 2 + 2
        for mentor_num in range(number_of_mentors):
            get_user_model().objects. \
                create(username='Mentor%s' % mentor_num,
                       email='Mentor%s@gmail.com' % mentor_num,
                       password='password')
            # set to mentors that they are 'Mentors'
            m = CustomUser.objects.get(username='Mentor%s' % mentor_num)
            m.groups.set([mentor])
            # set then last name for search test
            m.last_name = 'Mentor%s' % mentor_num
            m.save()
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

        # test_create_group_view_url_accessible_by_name:
        resp = self.client.get(reverse('groups:create-group'))
        self.assertEqual(resp.status_code, 200)

        # test_create_group_view_uses_correct_template:
        resp = self.client.get(reverse('groups:create-group'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'groups/group_create.html')

        # test_create_group_view_pagination_is_PAGINATOR:
        resp = self.client.get(reverse('groups:create-group'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] is True)
        self.assertTrue(len(resp.context['object_list']) == PAGINATOR)

        # test_create_group_view_paginator_lists_all_mentors:
        # Get third page and confirm it has (exactly) remaining 3 items
        resp = self.client.get(reverse('groups:create-group') + '?page=3')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] is True)
        self.assertTrue(len(resp.context['object_list']) == 3)

        # test_CreateGroupView_search:
        resp = self.client.get(
            reverse('groups:create-group') + '?data_search=1')
        self.assertEqual(resp.status_code, 200)
        # test that search returns 21 mentors (with '1' in name from 0 to 101)
        mentors = resp.context['object_list']
        self.assertTrue(len(mentors) == 21)
        self.assertTrue('search' in resp.context)
        self.assertTrue('search_label' in resp.context)
        self.assertTrue(resp.context['search'] is True)
        self.assertTrue(resp.context['search_label'] == '1')

        # test_CreateGroupView_without_search:
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
        resp = self.client.post(reverse('groups:create-group'),
                                data={'name': 'somename', 'mentor': mentors})
        # Test of redirection after success
        self.assertEqual(resp.get('location'), reverse('groups:groups-list'))
        # Test that group with mentors was created
        # test that group has 4 mentors:
        group = Group.objects.filter(mentor__in=mentors)
        self.assertTrue(Group.objects.filter(mentor__in=mentors).exists())
        self.assertTrue(len(group) == 4)
        # test that there is only 1 group created
        self.assertTrue(len(group.distinct()) == 1)
        # and it's name is 'somename'
        self.assertTrue(
            list(group.distinct().values())[0]['name'] == 'somename')


class UpdateGroupViewTest(TestCase):
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
        # Create another PAGINATOR*2+2 mentors  for pagination tests
        number_of_mentors = PAGINATOR * 2 + 2
        for mentor_num in range(number_of_mentors):
            get_user_model(). \
                objects.create(username='Mentor%s' % mentor_num,
                               email='Mentor%s@gmail.com' % mentor_num,
                               password='password')
            # set to mentors that they are 'Mentors'
            m = get_user_model().objects.get(username='Mentor%s' % mentor_num)
            m.groups.set([mentor])
            # set then last name for search test
            m.last_name = 'Mentor%s' % mentor_num
            m.save()

        number_of_groups = 3
        for group_num in range(number_of_groups):
            g = Group.objects.create(name='Group%s' % group_num)
            m = CustomUser.objects.get(username='Mentor%s' % group_num)
            g.mentor.set([m])

        permission = Permission.objects.get(
            content_type__app_label='groups', codename='change_group')
        admin.permissions.add(permission)
        user1.groups.set([admin])
        user2.groups.set([mentor])
        cls.client = Client()

    def test_update_group_view_permission(self):
        self.client.login(username='temporary2', password='temporary2')
        group = Group.objects.get(name='Group0')
        resp = self.client.get(reverse('groups:update-group',
                                       kwargs={'pk': group.pk}))
        self.assertEqual(resp.status_code, 403)

    def test_update_group_view_url_exists_at_desired_location(self):
        self.client.login(username='temporary1', password='temporary1')
        group = Group.objects.get(name='Group0')
        resp = self.client.get('/groups/update_group/' + str(group.pk))
        self.assertEqual(resp.status_code, 200)
        # test_update_group_view_url_accessible_by_name:
        resp = self.client.get(reverse('groups:update-group',
                                       kwargs={'pk': group.pk}))
        self.assertEqual(resp.status_code, 200)
        # test_update_group_view_uses_correct_template:
        self.assertTemplateUsed(resp, 'groups/group_update.html')

        # test_update_group_view_pagination_is_PAGINATOR:
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] is True)
        self.assertTrue(len(resp.context['object_list']) == PAGINATOR)

        # test_update_group_view_paginator_lists_all_mentors:
        # Get third page and confirm it has (exactly) remaining 3 items
        resp = self.client.get(reverse('groups:update-group',
                                       kwargs={'pk': group.pk}) + '?page=3')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] is True)
        self.assertTrue(len(resp.context['object_list']) == 3)

        # test_UpdateGroupView_search:
        resp = self.client.get(
            reverse('groups:update-group',
                    kwargs={'pk': group.pk}) + '?data_search=1')
        self.assertEqual(resp.status_code, 200)
        # test that search returns 21 mentors (with '1' in name from 0 to 101)
        mentors = resp.context['object_list']
        self.assertTrue(len(mentors) == 21)
        self.assertTrue('search' in resp.context)
        self.assertTrue('search_label' in resp.context)
        self.assertTrue(resp.context['search'] is True)
        self.assertTrue(resp.context['search_label'] == '1')

        # test_UpdateGroupView_without_search:
        resp = self.client.get(reverse('groups:update-group',
                                       kwargs={'pk': group.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('search' in resp.context)
        self.assertTrue('search_label' in resp.context)
        self.assertTrue(resp.context['search'] is False)
        self.assertTrue(resp.context['search_label'] == 'Search')

    def test_UpdateGroupView_with_data(self):
        self.client.login(username='temporary1', password='temporary1')
        group = Group.objects.get(name='Group0')
        pk_old = group.pk
        mentors = CustomUser.objects.filter(
            username__in=['Mentor5', 'Mentor27', 'Mentor93', 'Mentor45'])
        mentors = list(mentors.values_list('id', flat=True))
        resp = self.client.post(reverse('groups:update-group',
                                        kwargs={'pk': group.pk}),
                                data={'name': 'somename', 'mentor': mentors})
        group = Group.objects.get(name='somename')
        # Test that we changed name of group
        self.assertTrue(group.pk == pk_old)
        # Test of redirection after success
        self.assertEqual(resp.get('location'), reverse('groups:update-group',
                                                       kwargs={
                                                           'pk': group.pk}))
        # Test that group with mentors was updated
        # test that group has 4 mentors:
        group = Group.objects.filter(mentor__in=mentors)
        self.assertTrue(Group.objects.filter(mentor__in=mentors).exists())
        self.assertTrue(len(group) == 4)
        # test that there is only 1 group created
        self.assertTrue(len(group.distinct()) == 1)
        # and it's name is 'somename'
        self.assertTrue(
            list(group.distinct().values())[0]['name'] == 'somename')
        # Number of groups with mentors should be 3
        groups = Group.objects.filter(mentor__isnull=False).distinct()
        self.assertTrue(len(groups) == 3)


class DeleteGroupViewTest(TestCase):
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

        permission = Permission.objects.get(
            content_type__app_label='groups', codename='delete_group')
        admin.permissions.add(permission)
        user1.groups.set([admin])
        user2.groups.set([mentor])

        number_of_groups = 3
        for group_num in range(number_of_groups):
            group = Group.objects.create(name='Group%s' % group_num)
            m = CustomUser.objects.get(username='temporary2')
            group.mentor.set([m])
        cls.client = Client()

    def test_delete_group_view_permission(self):
        self.client.login(username='temporary2', password='temporary2')
        group = Group.objects.get(name='Group0')
        resp = self.client.get(reverse('groups:delete-group',
                                       kwargs={'pk': group.pk}))
        self.assertEqual(resp.status_code, 403)

    def test_delete_group_view_url_exists_at_desired_location(self):
        self.client.login(username='temporary1', password='temporary1')
        group = Group.objects.get(name='Group0')
        resp = self.client.get('/groups/delete_group/' + str(group.pk))
        self.assertEqual(resp.status_code, 200)
        # test_delete_group_view_url_accessible_by_name:
        resp = self.client.get(reverse('groups:delete-group',
                                       kwargs={'pk': group.pk}))
        self.assertEqual(resp.status_code, 200)
        # test_delete_group_view_uses_correct_template:
        self.assertTemplateUsed(resp, 'groups/group_delete.html')

    def test_DeleteGroupView_with_data(self):
        self.client.login(username='temporary1', password='temporary1')
        # Test that we have 3 groups before deleting
        groups = Group.objects.all()
        self.assertTrue(len(groups) == 3)
        group = Group.objects.get(name='Group0')
        resp = self.client.post(reverse('groups:delete-group',
                                        kwargs={'pk': group.pk}))
        # Test of redirection after success
        self.assertEqual(resp.get('location'), reverse('groups:groups-list'))
        # Test that we deleted group 'Group0'
        groups = Group.objects.all()
        self.assertTrue(len(groups) == 2)
        self.assertFalse(Group.objects.filter(pk=group.pk).exists())


class MentorGroupsViewTest(TestCase):
    @classmethod
    def setUp(cls):
        user1 = CustomUser.objects.create_user(
            username='temporary1', email='temporary1@gmail.com',
            password='temporary1')
        user2 = CustomUser.objects.create_user(
            username='temporary2', email='temporary2@gmail.com',
            password='temporary2')
        admin = Profile.objects.get(name='Admin')
        mentor = Profile.objects.get(name='Mentor')
        permissions = Permission.objects.get(
            content_type__app_label='groups', codename='view_mentor_group')
        mentor.permissions.add(permissions)
        user1.groups.set([admin])
        user2.groups.set([mentor])
        # Create groups for pagination tests
        number_of_groups = PAGINATOR * 2 + 3
        for group_num in range(number_of_groups):
            g = Group.objects.create(name='Group%s' % group_num)
            # All groups except last have mentor for test of number of groups
            # of this mentor
            if group_num < number_of_groups - 1:
                g.mentor.set([user2])
        cls.client = Client()

    def test_mentor_group_view_permission(self):
        self.client.login(username='temporary1', password='temporary1')
        resp = self.client.get(reverse('groups:mentor_groups_view'))
        self.assertEqual(resp.status_code, 403)

    def test_mentor_group_view_url_exists_at_desired_location(self):
        self.client.login(username='temporary2', password='temporary2')
        resp = self.client.get('/groups/mentor_groups/')
        self.assertEqual(resp.status_code, 200)
        # test_mentor_group_view_url_accessible_by_name:
        resp = self.client.get(reverse('groups:mentor_groups_view'))
        self.assertEqual(resp.status_code, 200)
        # test_mentor_group_view_uses_correct_template:
        self.assertTemplateUsed(resp, 'groups/mentor_groups_list.html')

        # test_mentor_group_view_pagination_is_PAGINATOR:
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] is True)
        self.assertTrue(len(resp.context['object_list']) == PAGINATOR)

        # test_mentor_group_view_paginator_lists_all_mentors:
        # Get third page and confirm it has (exactly) remaining 3 items
        resp = self.client.get(
            reverse('groups:mentor_groups_view') + '?page=3')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] is True)
        groups = Group.objects.all()
        # test that only groups of mentor are in list
        self.assertTrue(len(groups) == PAGINATOR * 2 + 3)
        self.assertTrue(len(resp.context['object_list']) == 2)

        # test_MentorGroupsView_search:
        resp = self.client.get(
            reverse('groups:mentor_groups_view') + '?data_search=1')
        self.assertEqual(resp.status_code, 200)
        # test that search returns 21 groups (with '1' in name from 0 to 101)
        groups = resp.context['object_list']
        self.assertTrue(len(groups) == 21)
        self.assertTrue('search' in resp.context)
        self.assertTrue('search_label' in resp.context)
        self.assertTrue(resp.context['search'] is True)
        self.assertTrue(resp.context['search_label'] == '1')

        # test_MentorGroupsView_without_search:
        resp = self.client.get(reverse('groups:mentor_groups_view'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('search' in resp.context)
        self.assertTrue('search_label' in resp.context)
        self.assertTrue(resp.context['search'] is False)
        self.assertTrue(resp.context['search_label'] == 'Search')


class MentorGroupUpdateTest(TestCase):
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
        # Create PAGINATOR*2+3 users  for pagination tests
        number_of_users = PAGINATOR * 2 + 3
        for user_num in range(number_of_users):
            user = get_user_model(). \
                objects.create(username='User%s' % user_num,
                               email='User%s@gmail.com' % user_num,
                               password='password')
            # set user's last name for search test
            user.last_name = 'User%s' % user_num
            user.save()

        permission = Permission.objects.get(
            content_type__app_label='groups', codename='change_mentor_group')
        mentor.permissions.add(permission)
        user1.groups.set([admin])
        user2.groups.set([mentor])
        # create group for testing
        group = Group.objects.create(name='Group0')
        group.mentor.set([user2])
        # set to group all users except one to test paginator and context
        users = CustomUser.objects.filter(groups__name='Trainee'). \
            exclude(username='User102')
        group.user.set(users)
        cls.client = Client()

    def test_mentor_group_update_permission(self):
        self.client.login(username='temporary1', password='temporary1')
        group = Group.objects.get(name='Group0')
        resp = self.client.get(reverse('groups:mentor_group_update',
                                       kwargs={'pk': group.pk}))
        self.assertEqual(resp.status_code, 403)

    def test_mentor_group_update_url_exists_at_desired_location(self):
        self.client.login(username='temporary2', password='temporary2')
        group = Group.objects.get(name='Group0')
        resp = self.client.get('/groups/group/' + str(group.pk) + '/')
        self.assertEqual(resp.status_code, 200)
        # test_mentor_group_update_url_accessible_by_name:
        resp = self.client.get(reverse('groups:mentor_group_update',
                                       kwargs={'pk': group.pk}))
        self.assertEqual(resp.status_code, 200)

        # test_mentor_group_update_uses_correct_template:
        self.assertTemplateUsed(resp, 'groups/mentor_group_update.html')

        # test_mentor_group_update_pagination_is_PAGINATOR:
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] is True)
        self.assertTrue(len(resp.context['object_list']) == PAGINATOR)

        # test_mentor_group_update_paginator_lists_all_mentors:
        # Get third page and confirm it has (exactly) remaining 2 items
        resp = self.client.get(reverse('groups:mentor_group_update',
                                       kwargs={'pk': group.pk}) + '?page=3')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] is True)
        self.assertTrue(len(resp.context['object_list']) == 2)

        # test_MentorGroupUpdateView_search:
        resp = self.client.get(
            reverse('groups:mentor_group_update',
                    kwargs={'pk': group.pk}) + '?data_search=1')
        self.assertEqual(resp.status_code, 200)
        # test that search returns 21 users (with '1' in name from 0 to 101)
        users = resp.context['object_list']
        self.assertTrue(len(users) == 21)
        self.assertTrue('search' in resp.context)
        self.assertTrue('search_label' in resp.context)
        self.assertTrue(resp.context['search'] is True)
        self.assertTrue(resp.context['search_label'] == '1')

        # test_MentorGroupUpdateView_without_search:
        resp = self.client.get(reverse('groups:mentor_group_update',
                                       kwargs={'pk': group.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('search' in resp.context)
        self.assertTrue('search_label' in resp.context)
        self.assertTrue(resp.context['search'] is False)
        self.assertTrue(resp.context['search_label'] == 'Search')

    def test_MentorGroupUpdateView_with_data(self):
        self.client.login(username='temporary2', password='temporary2')
        group = Group.objects.get(name='Group0')
        users = CustomUser.objects.filter(
            username__in=['User5', 'User27', 'User93', 'User45'])
        users = list(users.values_list('id', flat=True))
        resp = self.client.post(reverse('groups:mentor_group_update',
                                        kwargs={'pk': group.pk}),
                                data={'name': 'somename', 'user': users})
        # Test that we didn't changed name of group
        self.assertFalse(Group.objects.filter(name='somename').exists())
        # Test of redirection after success
        self.assertEqual(resp.get('location'),
                         reverse('groups:mentor_group_update',
                                 kwargs={'pk': group.pk}))
        # Test that group with mentors was updated correctly and has 4 users:
        users_test = list(group.user.all().values_list('id', flat=True))
        self.assertTrue(set(users) == set(users_test))
        self.assertTrue(len(users) == 4)
