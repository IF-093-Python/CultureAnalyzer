import random
import uuid

from django.test import TestCase, Client, tag
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import Group as Profile
from django.contrib.auth import get_user_model

from groups.models import Group, Invitation, Shedule
from quiz.models import Quizzes
from users.models import CustomUser
from .utilities import create_user_with_role
from CultureAnalyzer.constants import (ITEMS_ON_PAGE, TRAINEE_ID, MENTOR_ID,
                                       ADMIN_ID)

__all__ = ['GroupListViewTest', 'CreateGroupViewTest', 'UpdateGroupViewTest',
           'DeleteGroupViewTest', 'MentorGroupsViewTest',
           'MentorGroupUpdateTest', 'AddNewUserTest', 'SheduleGroupListTest',
           'SheduleGroupTest', 'AddInvitationTest']


# For correct pagination tests ITEMS_ON_PAGE should be > 3


@tag('slow')
class GroupListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create groups for pagination tests
        for group_num in range(ITEMS_ON_PAGE):
            Group.objects.create(name='Group%s' % group_num)
        for group_num in range(ITEMS_ON_PAGE + 3):
            Group.objects.create(name='Somename%s' % group_num)
        create_user_with_role(ADMIN_ID, 'view_group',
                              username='user_admin', email='1@g.com')
        create_user_with_role(MENTOR_ID)
        cls.client = Client()

    def setUp(self):
        self.client.login(username='user_admin', password='pass')

    def test_group_list_view_permission(self):
        self.client.login(username='Username', password='pass')
        resp = self.client.get(reverse('groups:groups-list'))
        self.assertEqual(resp.status_code, 403)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/groups/')
        self.assertEqual(resp.status_code, 200)

        # test_view_url_accessible_by_name:
        resp = self.client.get(reverse('groups:groups-list'))
        self.assertEqual(resp.status_code, 200)

        # test_view_uses_correct_template(self):
        resp = self.client.get(reverse('groups:groups-list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'groups/groups_list.html')

        # test_pagination_is_ITEMS_ON_PAGE:
        resp = self.client.get(reverse('groups:groups-list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] is True)
        self.assertTrue(len(resp.context['group_list']) == ITEMS_ON_PAGE)

        # test_paginator_lists_all_groups:
        # Get third page and confirm it has (exactly) remaining 3 items
        resp = self.client.get(reverse('groups:groups-list') + '?page=3')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] is True)
        self.assertTrue(len(resp.context['group_list']) == 3)

        # test_GroupListView_search:
        resp = self.client.get(
            reverse('groups:groups-list') + '?data_search=g')
        self.assertEqual(resp.status_code, 200)
        # test search returns ITEMS_ON_PAGE groups (with 'G' or 'g' in name )
        groups = resp.context['group_list']
        self.assertTrue(len(groups) == ITEMS_ON_PAGE)
        self.assertTrue('search' in resp.context)
        self.assertTrue('search_label' in resp.context)
        self.assertTrue(resp.context['search'] is True)
        self.assertTrue(resp.context['search_label'] == 'g')

        # test_GroupListView_without_search:
        resp = self.client.get(reverse('groups:groups-list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('search' in resp.context)
        self.assertTrue('search_label' in resp.context)
        self.assertTrue(resp.context['search'] is False)
        self.assertTrue(resp.context['search_label'] == 'Search')


@tag('slow')
class CreateGroupViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_user_with_role(ADMIN_ID, 'add_group',
                              username='user_admin', email='1@g.com')
        create_user_with_role(MENTOR_ID)
        # Create another ITEMS_ON_PAGE*2+2 mentors  for pagination tests
        for mentor_num in range(ITEMS_ON_PAGE * 2 + 2):
            m = get_user_model().objects. \
                create(username='Mentor%s' % mentor_num,
                       email='Mentor%s@gmail.com' % mentor_num, password='pas')
            # set to mentors that they are 'Mentors'
            m.groups.set([Profile.objects.get(pk=MENTOR_ID)])
            # set then last name for search test
            if mentor_num < ITEMS_ON_PAGE:
                m.last_name = 'Mentor%s' % mentor_num
            else:
                m.last_name = 'Last%s' % mentor_num
            m.save()
        cls.client = Client()

    def setUp(self):
        self.client.login(username='user_admin', password='pass')

    def test_CreateGroupView_permission(self):
        self.client.login(username='Username', password='pass')
        resp = self.client.get(reverse('groups:create-group'))
        self.assertEqual(resp.status_code, 403)

    def test_CreateGroupView_misc(self):
        resp = self.client.get('/groups/create-group/')
        self.assertEqual(resp.status_code, 200)

        # test_CreateGroupView_url_accessible_by_name:
        resp = self.client.get(reverse('groups:create-group'))
        self.assertEqual(resp.status_code, 200)

        # test_CreateGroupView_uses_correct_template:
        resp = self.client.get(reverse('groups:create-group'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'groups/group_create.html')

        # test_CreateGroupView_pagination_is_ITEMS_ON_PAGE:
        resp = self.client.get(reverse('groups:create-group'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] is True)
        self.assertTrue(len(resp.context['object_list']) == ITEMS_ON_PAGE)

        # test_CreateGroupView_paginator_lists_all_mentors:
        # Get third page and confirm it has exactly remaining 3 items
        resp = self.client.get(reverse('groups:create-group') + '?page=3')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(resp.context['object_list']) == 3)

        # test_CreateGroupView_search:
        resp = self.client.get(
            reverse('groups:create-group') + '?data_search=m')
        self.assertEqual(resp.status_code, 200)
        # test search give ITEMS_ON_PAGE mentors (with 'M' or 'm' in last_name)
        mentors = resp.context['object_list']
        self.assertTrue(len(mentors) == ITEMS_ON_PAGE)
        self.assertTrue(resp.context['search'] is True)
        self.assertTrue(resp.context['search_label'] == 'm')

        # test_CreateGroupView_without_search:
        resp = self.client.get(reverse('groups:create-group'))
        self.assertTrue(resp.context['search'] is False)
        self.assertTrue(resp.context['search_label'] == 'Search')

    def test_CreateGroupView_with_data(self):
        # list of random mentors
        mentors_list = ['Mentor%s' % random.randint(0, ITEMS_ON_PAGE * 2 + 2)
                        for i in range(10)]
        mentors = CustomUser.objects.filter(username__in=mentors_list)
        mentors = list(mentors.values_list('id', flat=True))
        group_name = 'somename'
        resp = self.client.post(reverse('groups:create-group'),
                                data={'name': group_name, 'mentor': mentors})
        # Test of redirection after success
        self.assertEqual(resp.get('location'), reverse('groups:groups-list'))
        # Test that group with mentors was created
        # test that group has all randomised mentors:
        group = Group.objects.get(name=group_name)
        mentors_test = group.mentor.all().values_list('id', flat=True)
        self.assertTrue(set(mentors) == set(mentors_test))


@tag('slow')
class UpdateGroupViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_user_with_role(ADMIN_ID, 'change_group',
                              username='user_admin', email='1@g.com')
        create_user_with_role(MENTOR_ID)
        # Create another ITEMS_ON_PAGE*2+2 mentors  for pagination tests
        for mentor_num in range(ITEMS_ON_PAGE * 2 + 2):
            m = get_user_model().objects. \
                create(username='Mentor%s' % mentor_num,
                       email='Mentor%s@gmail.com' % mentor_num, password='pas')
            # set to mentors that they are 'Mentors'
            m.groups.set([Profile.objects.get(name='Mentor')])
            # set then last name for search test
            if mentor_num < ITEMS_ON_PAGE:
                m.last_name = 'Mentor%s' % mentor_num
            else:
                m.last_name = 'Last%s' % mentor_num
            m.save()
        number_of_groups = 3
        for group_num in range(number_of_groups):
            g = Group.objects.create(name='Group%s' % group_num)
            m = CustomUser.objects.get(username='Mentor%s' % group_num)
            g.mentor.set([m])
        cls.client = Client()

    def setUp(self):
        self.client.login(username='user_admin', password='pass')

    def test_UpdateGroupView_permission(self):
        self.client.login(username='Username', password='pass')
        num = random.randint(0, 2)
        group = Group.objects.get(name='Group%s' % num)
        resp = self.client.get(reverse('groups:update-group',
                                       kwargs={'pk': group.pk}))
        self.assertEqual(resp.status_code, 403)

    def test_UpdateGroupView_misc(self):
        num = random.randint(0, 2)
        group = Group.objects.get(name='Group%s' % num)
        resp = self.client.get('/groups/update-group/' + str(group.pk))
        self.assertEqual(resp.status_code, 200)
        # test_UpdateGroupView_url_accessible_by_name:
        resp = self.client.get(reverse('groups:update-group',
                                       kwargs={'pk': group.pk}))
        self.assertEqual(resp.status_code, 200)
        # test_UpdateGroupView_uses_correct_template:
        self.assertTemplateUsed(resp, 'groups/group_update.html')

        # test_UpdateGroupView_pagination_is_ITEMS_ON_PAGE:
        self.assertTrue(resp.context['is_paginated'] is True)
        self.assertTrue(len(resp.context['object_list']) == ITEMS_ON_PAGE)

        # test_UpdateGroupView_paginator_lists_all_mentors:
        # Get third page and confirm it has exactly remaining 3 items
        resp = self.client.get(reverse('groups:update-group',
                                       kwargs={'pk': group.pk}) + '?page=3')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(resp.context['object_list']) == 3)

        # test_UpdateGroupView_search:
        resp = self.client.get(
            reverse('groups:update-group', kwargs={'pk': group.pk}) +
            '?data_search=m')
        self.assertEqual(resp.status_code, 200)
        # test search give ITEMS_ON_PAGE mentors (with 'M' or 'm' in last_name)
        mentors = resp.context['object_list']
        self.assertTrue(len(mentors) == ITEMS_ON_PAGE)
        self.assertTrue(resp.context['search'] is True)
        self.assertTrue(resp.context['search_label'] == 'm')

        # test_UpdateGroupView_without_search:
        resp = self.client.get(reverse('groups:update-group',
                                       kwargs={'pk': group.pk}))
        self.assertTrue(resp.context['search'] is False)
        self.assertTrue(resp.context['search_label'] == 'Search')

    def test_UpdateGroupView_with_data(self):
        num = random.randint(0, 2)
        group = Group.objects.get(name='Group%s' % num)
        pk_old = group.pk
        # list of random mentors
        mentors_list = ['Mentor%s' % random.randint(0, ITEMS_ON_PAGE * 2 + 2)
                        for i in range(10)]
        mentors = CustomUser.objects.filter(username__in=mentors_list)
        mentors = list(mentors.values_list('id', flat=True))
        resp = self.client.post(reverse('groups:update-group',
                                        kwargs={'pk': group.pk}),
                                data={'name': 'somename', 'mentor': mentors})
        # Test of redirection after success
        self.assertEqual(resp.get('location'), reverse('groups:update-group',
                                                       kwargs={
                                                           'pk': group.pk}))
        # Test that group with mentors was updated
        # test that group has all randomised mentors:
        group = Group.objects.get(name='somename')
        self.assertTrue(group.pk == pk_old)
        mentors_test = group.mentor.all().values_list('id', flat=True)
        self.assertTrue(set(mentors) == set(mentors_test))


@tag('slow')
class DeleteGroupViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_user_with_role(ADMIN_ID, 'delete_group',
                              username='user_admin', email='1@g.com')
        create_user_with_role(MENTOR_ID)
        number_of_groups = 3
        for group_num in range(number_of_groups):
            group = Group.objects.create(name='Group%s' % group_num)
            m = CustomUser.objects.get(username='Username')
            group.mentor.set([m])
        cls.client = Client()

    def setUp(self):
        self.client.login(username='user_admin', password='pass')

    def test_DeleteGroupView_permission(self):
        self.client.login(username='Username', password='pass')
        num = random.randint(0, 2)
        group = Group.objects.get(name='Group%s' % num)
        resp = self.client.get(reverse('groups:delete-group',
                                       kwargs={'pk': group.pk}))
        self.assertEqual(resp.status_code, 403)

    def test_DeleteGroupView_misc(self):
        num = random.randint(0, 2)
        group = Group.objects.get(name='Group%s' % num)
        resp = self.client.get('/groups/delete-group/' + str(group.pk))
        self.assertEqual(resp.status_code, 200)
        # test_DeleteGroupView_url_accessible_by_name:
        resp = self.client.get(reverse('groups:delete-group',
                                       kwargs={'pk': group.pk}))
        self.assertEqual(resp.status_code, 200)
        # test_DeleteGroupView_uses_correct_template:
        self.assertTemplateUsed(resp, 'groups/group_delete.html')

    def test_DeleteGroupView_with_data(self):
        # Test that we have 3 groups before deleting
        groups = Group.objects.all()
        self.assertTrue(len(groups) == 3)
        num = random.randint(0, 2)
        group = Group.objects.get(name='Group%s' % num)
        resp = self.client.post(reverse('groups:delete-group',
                                        kwargs={'pk': group.pk}))
        # Test of redirection after success
        self.assertEqual(resp.get('location'), reverse('groups:groups-list'))
        # Test that we deleted group
        groups = Group.objects.all()
        self.assertTrue(len(groups) == 2)
        self.assertFalse(Group.objects.filter(pk=group.pk).exists())


@tag('slow')
class MentorGroupsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_user_with_role(ADMIN_ID)
        user2 = create_user_with_role(MENTOR_ID, 'view_mentor_group',
                                      username='user_mentor', email='1@g.com')
        # Create groups for pagination tests
        number_of_groups = ITEMS_ON_PAGE * 2 + 3
        for group_num in range(number_of_groups):
            if group_num < ITEMS_ON_PAGE:
                g = Group.objects.create(name='Group%s' % group_num)
            else:
                g = Group.objects.create(name='Name%s' % group_num)
            # All groups except last have mentor for test of number of groups
            # of this mentor
            if group_num < number_of_groups - 1:
                g.mentor.set([user2])
        cls.client = Client()

    def setUp(self):
        self.client.login(username='user_mentor', password='pass')

    def test_MentorGroupsView_permission(self):
        self.client.login(username='Username', password='pass')
        resp = self.client.get(reverse('groups:mentor_groups_view'))
        self.assertEqual(resp.status_code, 403)

    def test_MentorGroupsView_misc(self):
        resp = self.client.get('/groups/mentor-groups/')
        self.assertEqual(resp.status_code, 200)
        # test_MentorGroupsView_url_accessible_by_name:
        resp = self.client.get(reverse('groups:mentor_groups_view'))
        self.assertEqual(resp.status_code, 200)
        # test_MentorGroupsView_uses_correct_template:
        self.assertTemplateUsed(resp, 'groups/mentor_groups_list.html')

        # test_MentorGroupsView_pagination_is_ITEMS_ON_PAGE:
        self.assertTrue(resp.context['is_paginated'] is True)
        self.assertTrue(len(resp.context['object_list']) == ITEMS_ON_PAGE)

        # test_MentorGroupsView_paginator_lists_all_mentors:
        # Get third page and confirm it has remaining 3 items
        resp = self.client.get(
            reverse('groups:mentor_groups_view') + '?page=3')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.context['is_paginated'] is True)
        # test that only groups of mentor are in list (should be 2)
        self.assertTrue(len(resp.context['object_list']) == 2)

        # test_MentorGroupsView_search:
        resp = self.client.get(
            reverse('groups:mentor_groups_view') + '?data_search=g')
        self.assertEqual(resp.status_code, 200)
        # test search returns ITEMS_ON_PAGE groups (with 'G'  or 'g' in name)
        groups = resp.context['object_list']
        self.assertTrue(len(groups) == ITEMS_ON_PAGE)
        self.assertTrue(resp.context['search'] is True)
        self.assertTrue(resp.context['search_label'] == 'g')

        # test_MentorGroupsView_without_search:
        resp = self.client.get(reverse('groups:mentor_groups_view'))
        self.assertTrue(resp.context['search'] is False)
        self.assertTrue(resp.context['search_label'] == 'Search')


@tag('slow')
class MentorGroupUpdateTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = create_user_with_role(ADMIN_ID)
        user2 = create_user_with_role(MENTOR_ID, 'change_mentor_group',
                                      username='user_mentor', email='1@g.com')
        # Create ITEMS_ON_PAGE*2+3 users  for pagination tests
        for user_num in range(ITEMS_ON_PAGE * 2 + 3):
            user = get_user_model().objects. \
                create(username='U%s' % user_num,
                       email='U%s@gmail.com' % user_num, password='pas')
            # set then last name for search test
            if user_num < ITEMS_ON_PAGE:
                user.last_name = 'User%s' % user_num
            else:
                user.last_name = 'Last%s' % user_num
            user.save()
        for group_num in range(ITEMS_ON_PAGE):
            group = Group.objects.create(name='Group%s' % group_num)
            if group_num < 3:
                group.mentor.set([user2])
            else:
                group.mentor.set([user1])
            # set users for group without one user for pagination test
            users = CustomUser.objects.filter(groups__pk=TRAINEE_ID). \
                exclude(username='U%s' % 0)
            group.user.set(users)
        cls.client = Client()

    def setUp(self):
        self.client.login(username='user_mentor', password='pass')

    def test_MentorGroupUpdate_permission(self):
        self.client.login(username='Username', password='pass')
        group = Group.objects.get(name='Group0')
        resp = self.client.get(reverse('groups:mentor_group_update',
                                       kwargs={'pk': group.pk}))
        self.assertEqual(resp.status_code, 403)

    def test_MentorGroupUpdate_misc(self):
        group = Group.objects.get(name='Group%s' % random.randint(0, 0))
        resp = self.client.get('/groups/group/' + str(group.pk) + '/')
        self.assertEqual(resp.status_code, 200)
        # test_MentorGroupUpdate_url_accessible_by_name:
        resp = self.client.get(reverse('groups:mentor_group_update',
                                       kwargs={'pk': group.pk}))
        self.assertEqual(resp.status_code, 200)

        # test_MentorGroupUpdate_uses_correct_template:
        self.assertTemplateUsed(resp, 'groups/mentor_group_update.html')

        # test_MentorGroupUpdate_pagination_is_ITEMS_ON_PAGE:
        self.assertTrue(resp.context['is_paginated'] is True)
        self.assertTrue(len(resp.context['object_list']) == ITEMS_ON_PAGE)

        # test_MentorGroupUpdate_paginator_lists_all_users:
        # Get third page and confirm it has remaining 2 items (User0 excluded)
        resp = self.client.get(reverse('groups:mentor_group_update',
                                       kwargs={'pk': group.pk}) + '?page=3')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.context['is_paginated'] is True)
        self.assertTrue(len(resp.context['object_list']) == 2)

        # test_MentorGroupUpdateView_search:
        resp = self.client.get(
            reverse('groups:mentor_group_update',
                    kwargs={'pk': group.pk}) + '?data_search=u')
        self.assertEqual(resp.status_code, 200)
        # test search of ITEMS_ON_PAGE - 1 users (with 'U' or 'u' in last name)
        users = resp.context['object_list']
        self.assertTrue(len(users) == ITEMS_ON_PAGE - 1)
        self.assertTrue(resp.context['search'] is True)
        self.assertTrue(resp.context['search_label'] == 'u')

        # test_MentorGroupUpdateView_without_search:
        resp = self.client.get(reverse('groups:mentor_group_update',
                                       kwargs={'pk': group.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.context['search'] is False)
        self.assertTrue(resp.context['search_label'] == 'Search')

    def test_MentorGroupUpdateView_with_data(self):
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


@tag('slow')
class AddNewUserTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        group = Group.objects.create(name='Group')
        date = timezone.now() + timezone.timedelta(days=1)
        Invitation.objects.create(end=date, group=group, items_left=2,
                                  code=uuid.uuid4())
        create_user_with_role(TRAINEE_ID)
        create_user_with_role(MENTOR_ID, 'change_mentor_group',
                              username='user_mentor', email='1@g.com')
        cls.client = Client()

    def setUp(self):
        self.client.login(username='Username', password='pass')

    def test_AddNewUser_misc(self):
        url = Invitation.objects.get(group__name='Group')
        resp = self.client.get('/groups/join/' + str(url.code))
        self.assertEqual(resp.status_code, 200)
        # test_AddNewUser_url_accessible_by_name:
        resp = self.client.get(reverse('groups:add_new_user',
                                       kwargs={'hash': url.code}))
        self.assertEqual(resp.status_code, 200)

        # test_AddNewUser_uses_correct_template:
        self.assertTemplateUsed(resp, 'groups/add_new_user.html')

    def test_AddNewUser_with_data(self):
        url = Invitation.objects.get(group__name='Group')
        user = self.client.session['_auth_user_id']
        resp = self.client.post(
            reverse('groups:add_new_user', kwargs={'hash': url.code}),
            data={'user': user})
        # Test that we didn't changed name of group
        group = Group.objects.get(user__id=user)
        self.assertTrue(group.name == 'Group')
        # Test of redirection after success
        self.assertEqual(resp.get('location'),
                         reverse('test_player:start_test'))


@tag('slow')
class SheduleGroupListTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        group = Group.objects.create(name='Group')
        quiz = Quizzes.objects.create(title='SomeQuiz', description='ololo',
                                      type_of_quiz='Business')
        start = timezone.now() + timezone.timedelta(days=1)
        end = timezone.now() + timezone.timedelta(days=3)
        Shedule.objects.create(start=start, end=end, group=group, quiz=quiz)
        create_user_with_role(ADMIN_ID)
        user2 = create_user_with_role(MENTOR_ID, 'view_shedule',
                                      username='user_mentor', email='1@g.com')
        group.mentor.set([user2])
        cls.client = Client()

    def setUp(self):
        self.client.login(username='user_mentor', password='pass')

    def test_SheduleGroupList_permission(self):
        self.client.login(username='Username', password='pass')
        group = Group.objects.get(name='Group')
        resp = self.client.get(
            reverse('groups:shedule_group_list', kwargs={'pk': group.pk}))
        self.assertEqual(resp.status_code, 403)

    def test_SheduleGroupList_misc(self):
        group = Group.objects.get(name='Group')
        resp = self.client.get('/groups/group/quiz/' + str(group.pk) + '/')
        self.assertEqual(resp.status_code, 200)
        # test_SheduleGroupList_url_accessible_by_name:
        resp = self.client.get(
            reverse('groups:shedule_group_list', kwargs={'pk': group.pk}))
        self.assertEqual(resp.status_code, 200)
        # test_SheduleGroupList_uses_correct_template:
        self.assertTemplateUsed(resp, 'groups/shedule_group_list.html')


@tag('slow')
class SheduleGroupTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        group = Group.objects.create(name='Group')
        Quizzes.objects.create(title='SomeQuiz', description='ololo',
                               type_of_quiz='Business')
        create_user_with_role(ADMIN_ID)
        user2 = create_user_with_role(MENTOR_ID, 'change_shedule',
                                      username='user_mentor', email='1@g.com')
        group.mentor.set([user2])
        cls.client = Client()

    def setUp(self):
        self.client.login(username='user_mentor', password='pass')

    def test_SheduleGroup_permission(self):
        self.client.login(username='Username', password='pass')
        group = Group.objects.get(name='Group')
        resp = self.client.get(
            reverse('groups:shedule_group', kwargs={'pk': group.pk}))
        self.assertEqual(resp.status_code, 403)

    def test_SheduleGroup_misc(self):
        group = Group.objects.get(name='Group')
        resp = self.client.get('/groups/group/set_quiz/' + str(group.pk) + '/')
        self.assertEqual(resp.status_code, 200)
        # test_SheduleGroup_url_accessible_by_name:
        resp = self.client.get(
            reverse('groups:shedule_group', kwargs={'pk': group.pk}))
        self.assertEqual(resp.status_code, 200)
        # test_SheduleGroup_uses_correct_template:
        self.assertTemplateUsed(resp, 'groups/shedule_group.html')

    def test_SheduleGroup_with_data(self):
        group = Group.objects.get(name='Group')
        Quizzes.objects.get(title='SomeQuiz')
        start = timezone.now() + timezone.timedelta(days=1)
        end = timezone.now() + timezone.timedelta(days=3)
        resp = self.client.post(
            reverse('groups:shedule_group', kwargs={'pk': group.pk}),
            data={'start': start.date(), 'end': end.date(), 'quiz': group.pk})
        self.assertTrue(Shedule.objects.filter(group__name='Group').exists())
        # Test of redirection after success
        self.assertEqual(resp.get('location'),
                         reverse('groups:shedule_group_list',
                                 kwargs={'pk': group.pk}))


@tag('slow')
class AddInvitationTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        group = Group.objects.create(name='Group')
        create_user_with_role(ADMIN_ID)
        user2 = create_user_with_role(MENTOR_ID, 'change_mentor_group',
                                      username='user_mentor', email='1@g.com')
        group.mentor.set([user2])
        cls.client = Client()

    def setUp(self):
        self.client.login(username='user_mentor', password='pass')

    def test_AddInvitation_permission(self):
        self.client.login(username='Username', password='pass')
        group = Group.objects.get(name='Group')
        resp = self.client.get(
            reverse('groups:add_invitation', kwargs={'pk': group.pk}))
        self.assertEqual(resp.status_code, 403)

    def test_AddInvitation_misc(self):
        group = Group.objects.get(name='Group')
        resp = self.client.get('/groups/invite/' + str(group.pk) + '/')
        self.assertEqual(resp.status_code, 200)
        # test_SheduleGroup_url_accessible_by_name:
        resp = self.client.get(
            reverse('groups:add_invitation', kwargs={'pk': group.pk}))
        self.assertEqual(resp.status_code, 200)
        # test_SheduleGroup_uses_correct_template:
        self.assertTemplateUsed(resp, 'groups/add_invitation.html')

    def test_AddInvitation_with_data(self):
        group = Group.objects.get(name='Group')
        end = timezone.now() + timezone.timedelta(days=3)
        resp = self.client.post(
            reverse('groups:add_invitation', kwargs={'pk': group.pk}),
            data={'end': end.date(), 'items_left': 1, 'group': group.pk,
                  'code': uuid.uuid4()})
        self.assertTrue(
            Invitation.objects.filter(group__name='Group').exists())
        # Test of redirection after success
        self.assertEqual(resp.get('location'),
                         reverse('groups:mentor_group_update',
                                 kwargs={'pk': group.pk}))
