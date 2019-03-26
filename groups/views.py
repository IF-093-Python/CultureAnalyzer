from itertools import chain
from django.contrib.auth.mixins import (UserPassesTestMixin,
                                        LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Count
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views import generic

from groups.forms import (GroupCreateForm, GroupUpdateForm, SheduleForm,
                          InvitationForm)
from groups.models import Group, Shedule, Invitation
from groups.service import send_email_to_members, send_email_to_mentor

from CultureAnalyzer.constants import ITEMS_ON_PAGE, TRAINEE_ID, MENTOR_ID
from CultureAnalyzer.mixins import SafePaginationMixin

__all__ = ['GroupsList', 'CreateGroupView', 'UpdateGroupView',
           'DeleteGroupView', 'MentorGroupsView', 'MentorGroupUpdate',
           'MentorGroupAdd', 'AddNewUser', 'SheduleGroupListView',
           'SheduleGroupView', 'AddInvitation']


class GroupsList(PermissionRequiredMixin, SafePaginationMixin,
                 generic.ListView):
    """
    Makes list of all groups with number of mentors in each group
    """
    model = Group
    ordering = 'name'
    template_name = 'groups/groups_list.html'
    _search = False
    _search_label = 'Search'
    paginate_by = ITEMS_ON_PAGE
    permission_required = 'groups.view_group'

    def get_context_data(self, **kwargs):
        context = super(GroupsList, self).get_context_data(**kwargs)
        context['search'] = self._search
        context['search_label'] = self._search_label
        return context

    def get_queryset(self):
        """
        Makes table of groups with number of mentors in them.
        Search by name of group is available.
        """
        result = Group.objects.annotate(total=Count('mentor')).order_by('name')
        if self.request.GET.get('data_search'):
            search = self.request.GET.get('data_search')
            result = result.filter(name__icontains=search)
            self._search = True
            self._search_label = search
        return result


class CreateGroupView(PermissionRequiredMixin, SafePaginationMixin,
                      generic.CreateView, generic.ListView):
    """
    Creates new group of students
    Also makes list with checkboxes of all mentors
    that can be added to this group
    """
    form_class = GroupCreateForm
    template_name = 'groups/group_create.html'
    success_url = reverse_lazy('groups:groups-list')
    _search = False
    _search_label = 'Search'
    paginate_by = ITEMS_ON_PAGE
    permission_required = 'groups.add_group'

    def form_invalid(self, form):
        """Overrides parent function to take object_list if form is invalid"""
        self.object_list = self.get_queryset()
        return super().form_invalid(form=form)

    def form_valid(self, form):
        """Updates existing shedule or creates new one if it doest'n exist"""
        group = form.save()
        mentors = group.mentor.all()
        domain = self.request.build_absolute_uri('/')[:-1]
        send_email_to_mentor(domain, mentors, group)
        return super(CreateGroupView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateGroupView, self).get_context_data(**kwargs)
        context['search_label'] = self._search_label
        context['search'] = self._search
        return context

    def get_queryset(self):
        """List of mentors. Search by last_name is available"""
        result = get_user_model().objects. \
            filter(is_active=True, groups__pk=MENTOR_ID).order_by('last_name')
        if self.request.GET.get('data_search'):
            search = self.request.GET.get('data_search')
            result = result.filter(last_name__icontains=search)
            self._search = True
            self._search_label = search
        return result


class UpdateGroupView(PermissionRequiredMixin, SuccessMessageMixin,
                      SafePaginationMixin, generic.UpdateView,
                      generic.ListView):
    """
    Updates group of students.
    Allows to change name of group and to add or remove mentors
    """
    form_class = GroupCreateForm
    template_name = 'groups/group_update.html'
    success_message = "Group was updated successfully"
    _search = False
    _search_label = 'Search'
    _checked_mentors = None
    paginate_by = ITEMS_ON_PAGE
    permission_required = 'groups.change_group'

    def form_invalid(self, form):
        """Overrides parent function to take object_list if form is invalid"""
        self.object_list = self.get_queryset()
        return super().form_invalid(form=form)

    def get_context_data(self, **kwargs):
        context = super(UpdateGroupView, self).get_context_data(**kwargs)
        context['search_label'] = self._search_label
        context['checked_mentors'] = self._checked_mentors
        context['search'] = self._search
        return context

    def get_object(self, context=None):
        """Returns Group that we are working with"""
        context = get_object_or_404(Group, pk=self.kwargs['pk'])
        return context

    def get_queryset(self):
        """
        Remembers all checked_mentors of group and then
        concatenates them with unchecked mentors, so that
        checked mentors are always first in list
        Search by last_name of mentor is available
        """
        checked_mentors = get_user_model().objects.filter(
            is_active=True, mentor_in_group=self.kwargs['pk']). \
            order_by('last_name')
        self._checked_mentors = checked_mentors
        mentors = get_user_model().objects. \
            filter(is_active=True, groups__pk=MENTOR_ID). \
            exclude(mentor_in_group=self.kwargs['pk']). \
            order_by('last_name')
        if self.request.GET.get('data_search'):
            search = self.request.GET.get('data_search')
            mentors = mentors.filter(last_name__icontains=search)
            checked_mentors = checked_mentors. \
                filter(last_name__icontains=search)
            self._search = True
            self._search_label = search
        result = list(chain(checked_mentors, mentors))
        return result

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('groups:update-group', kwargs={'pk': pk})


class DeleteGroupView(PermissionRequiredMixin, generic.DeleteView):
    """Deletes group"""
    model = Group
    context_object_name = 'group'
    template_name = 'groups/group_delete.html'
    success_url = reverse_lazy('groups:groups-list')
    permission_required = 'groups.delete_group'


class MentorGroupsView(PermissionRequiredMixin, SafePaginationMixin,
                       generic.ListView):
    """
    Makes list of all groups of current Mentor
    """
    model = Group
    template_name = 'groups/mentor_groups_list.html'
    _search = False
    _search_label = 'Search'
    _group_has_quiz = None
    paginate_by = ITEMS_ON_PAGE
    permission_required = 'groups.view_mentor_group'

    def get_context_data(self, **kwargs):
        context = super(MentorGroupsView, self).get_context_data(**kwargs)
        context['has_quiz'] = self._group_has_quiz
        context['search'] = self._search
        context['search_label'] = self._search_label
        return context

    def get_queryset(self):
        """
        List of groups with number of students in them
        Lists only groups that are assigned to current mentor
        Search by name of group is available
        """
        result = Group.objects.filter(mentor__id=self.request.user.pk). \
            annotate(total=Count('user')).order_by('name')
        if self.request.GET.get('data_search'):
            search = self.request.GET.get('data_search')
            result = result.filter(name__icontains=search)
            self._search = True
            self._search_label = search
        self._group_has_quiz = result.filter(shedule__end__gt=timezone.now())
        return result


class MentorGroupUpdate(UserPassesTestMixin, PermissionRequiredMixin,
                        SuccessMessageMixin, SafePaginationMixin,
                        generic.UpdateView, generic.ListView):
    """
    Makes list of students to add or remove from group
    Shows also URL for joining to group if it is valid
    """
    model = Group
    form_class = GroupUpdateForm
    template_name = 'groups/mentor_group_update.html'
    success_message = "Group was updated successfully"
    _search = False
    _search_label = 'Search'
    _users_in_group = None
    paginate_by = ITEMS_ON_PAGE
    permission_required = 'groups.change_mentor_group'

    def get_context_data(self, **kwargs):
        context = super(MentorGroupUpdate, self).get_context_data(**kwargs)
        context['search_label'] = self._search_label
        context['users_in_group'] = self._users_in_group
        context['search'] = self._search
        # Looks for valid invitation link and forms URL if exists
        url = Invitation.objects.filter(group_id=self.kwargs['pk'],
                                        end__gte=timezone.now()).first()
        if url:
            my_url = reverse_lazy('groups:add_new_user',
                                  kwargs={'hash': url.code})
            domain = self.request.build_absolute_uri('/')[:-1]
            context['url'] = domain + str(my_url)
            context['time'] = url.end
            context['left'] = ' %s  students can join.' % url.items_left
        return context

    def get_object(self, context=None):
        """
        Takes group that we are working with for
        changing students in it and making invitation URL to join to group
        """
        context = get_object_or_404(Group, pk=self.kwargs['pk'])
        return context

    def get_queryset(self):
        """List of all students of group. Search by last_name is available"""
        result = get_user_model().objects. \
            filter(is_active=True, user_in_group=self.kwargs['pk']). \
            order_by('last_name')
        self._users_in_group = result
        if self.request.GET.get('data_search'):
            search = self.request.GET.get('data_search')
            result = result.filter(last_name__icontains=search)
            self._search = True
            self._search_label = search
        return result

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('groups:mentor_group_update', kwargs={'pk': pk})

    def test_func(self):
        """If user in not mentor of this group rises 403 exception"""
        return Group.objects.filter(
            pk=self.kwargs['pk'], mentor__id=self.request.user.pk).exists()


class MentorGroupAdd(PermissionRequiredMixin, SuccessMessageMixin,
                     SafePaginationMixin, UserPassesTestMixin,
                     generic.UpdateView, generic.ListView):
    """
    Makes list of all students that can be added to group
    """
    model = Group
    form_class = GroupUpdateForm
    template_name = 'groups/mentor_group_add.html'
    success_message = "Group was updated successfully"
    _search = False
    _search_label = 'Search'
    paginate_by = ITEMS_ON_PAGE
    permission_required = 'groups.add_mentor_group'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_label'] = self._search_label
        context['search'] = self._search
        return context

    def get_object(self, context=None):
        context = get_object_or_404(Group, pk=self.kwargs['pk'])
        return context

    def get_queryset(self):
        """
        Gets all Trainee users that are not in group and
        makes search in their last_name if needed
        """
        result = get_user_model().objects. \
            filter(is_active=True, groups__pk=TRAINEE_ID). \
            exclude(user_in_group=self.kwargs['pk']). \
            order_by('last_name')
        if self.request.GET.get('data_search'):
            search = self.request.GET.get('data_search')
            result = result.filter(last_name__icontains=search)
            self._search = True
            self._search_label = search
        return result

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('groups:mentor_group_update', kwargs={'pk': pk})

    def form_valid(self, form):
        """
        Gets users that are already in group and adds to users
        that where checked in form for adding to group
        """
        users_in_group = get_user_model().objects. \
            filter(is_active=True, user_in_group=self.kwargs['pk'])
        # If we don't add any students:
        if not form.cleaned_data['user']:
            return redirect('groups:mentor_group_update',
                            pk=self.kwargs['pk'])
        try:
            schedule = Shedule.objects.get(
                group=self.kwargs['pk'],)
            print(schedule)
        except Shedule.DoesNotExist:
            schedule = None
        if schedule and schedule.end > timezone.now():
            domain = self.request.build_absolute_uri('/')[:-1]
            send_email_to_members(domain, form.cleaned_data['user'], schedule)
        form.cleaned_data['user'] = \
            chain(form.cleaned_data['user'], users_in_group)
        return super(MentorGroupAdd, self).form_valid(form)

    def test_func(self):
        """If user in not mentor of this group rises 403 exception"""
        return Group.objects.filter(
            pk=self.kwargs['pk'], mentor__id=self.request.user.pk).exists()


class AddNewUser(LoginRequiredMixin, generic.CreateView):
    """
    Adds currently logged student to group
    """
    model = Group
    template_name = 'groups/add_new_user.html'
    form_class = GroupUpdateForm
    success_url = reverse_lazy('test_player:start_test')
    _group = None
    _invitation = None

    def dispatch(self, request, *args, **kwargs):
        """Checks if hash exists and is valid"""
        invitation = Invitation.objects.filter(code__exact=self.kwargs['hash'],
                                               end__gte=timezone.now(),
                                               items_left__gt=0).first()
        if invitation:
            self._group = get_object_or_404(Group, pk=invitation.group.pk)
            self._invitation = invitation
        else:
            raise Http404
        return super(AddNewUser, self).dispatch(request, *args, **kwargs)

    @transaction.atomic()
    def form_valid(self, form):
        """Adds user to group"""
        group = self._group
        invitation = self._invitation
        # Check if user is in group
        if Group.objects.filter(id=group.pk, user=self.request.user).exists():
            message = 'You already are in group "' + group.name + '".'
            messages.success(self.request, message=message)
            return redirect(self.success_url)
        # Check if invitation still has items and we can add user to group
        if invitation.items_left > 0:
            group.user.add(self.request.user.pk)
            invitation.items_left -= 1
            invitation.save()
        else:
            raise Http404
        message = 'You successfully joined to group "' + group.name + '".'
        messages.success(self.request, message=message)
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Checks if user is trainee
        context['trainee'] = get_user_model().objects. \
            filter(pk=self.request.user.pk, groups__pk=TRAINEE_ID).exists()
        if context['trainee']:
            context['group'] = self._group
        else:
            # Takes role of not-Trainee user for message display
            context['role'] = get_user_model().objects. \
                get(pk=self.request.user.pk).groups.values()[0]['name']
        return context


class SheduleGroupListView(PermissionRequiredMixin, UserPassesTestMixin,
                           SuccessMessageMixin, SafePaginationMixin,
                           generic.ListView):
    """
    Makes list of shedules that where assigned to this group
    """
    model = Shedule
    template_name = 'groups/shedule_group_list.html'
    paginate_by = ITEMS_ON_PAGE
    context_object_name = 'quizzes'
    permission_required = 'groups.view_shedule'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group'] = get_object_or_404(Group, pk=self.kwargs['pk'])
        context['now'] = timezone.now()
        return context

    def get_queryset(self):
        quizzes = Shedule.objects. \
            filter(group=self.kwargs['pk']).order_by('-end')
        return quizzes

    def test_func(self):
        """If user in not mentor of this group rises 403 exception"""
        return Group.objects.filter(pk=self.kwargs['pk']). \
            filter(mentor__id=self.request.user.pk).exists()


class SheduleGroupView(PermissionRequiredMixin, UserPassesTestMixin,
                       generic.FormView):
    """
    Adds shedule to group
    """
    form_class = SheduleForm
    template_name = 'groups/shedule_group.html'
    permission_required = 'groups.change_shedule'

    def form_valid(self, form):
        """Updates existing shedule or creates new one if it doest'n exist"""
        group = Group.objects.get(pk=self.kwargs['pk'])
        members = group.user.all()
        form.cleaned_data['group'] = group
        try:
            schedule = Shedule.objects.get(group=group,
                                           quiz=form.instance.quiz)
        except Shedule.DoesNotExist:
            schedule = None
        if schedule:
            schedule.quiz = form.cleaned_data['quiz']
            schedule.start = form.cleaned_data['start']
            schedule.end = form.cleaned_data['end']
            schedule.save()
        else:
            schedule = form.save(commit=False)
            schedule.group = group
            schedule.save()
        messages.success(request=self.request,
                         message=f'{form.instance.quiz} set '
                         f'for "{group}" successfully.')
        domain = self.request.build_absolute_uri('/')[:-1]
        send_email_to_members(domain, members, schedule)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group'] = get_object_or_404(Group, pk=self.kwargs['pk'])
        return context

    def get_success_url(self):
        return reverse_lazy('groups:shedule_group_list',
                            kwargs={'pk': self.kwargs['pk']})

    def test_func(self):
        """If user in not mentor of this group rises 403 exception"""
        return Group.objects.filter(pk=self.kwargs['pk']). \
            filter(mentor__id=self.request.user.pk).exists()


class AddInvitation(PermissionRequiredMixin, UserPassesTestMixin,
                    generic.FormView):
    """
    Makes URL by which users can join to group
    """
    template_name = 'groups/add_invitation.html'
    form_class = InvitationForm
    _group = None
    permission_required = 'groups.change_mentor_group'

    def dispatch(self, request, *args, **kwargs):
        """Checks if there are expired invitations and deletes them"""
        expired_urls = Invitation.objects.filter(end__lt=timezone.now())
        if expired_urls:
            expired_urls.delete()
        return super(AddInvitation, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """If there is some URL for this group we change it or create new"""
        invitation = Invitation.objects.filter(group=form.instance.group)
        if invitation:
            invitation.update(**form.cleaned_data)
        else:
            Invitation.objects.create(**form.cleaned_data)
        message = 'New URL generated successfully!'
        messages.success(self.request, message=message)
        return super(AddInvitation, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group'] = self._group
        return context

    def get_form_kwargs(self):
        """
        Initialises form by current group and
        sets number of students that can join by this link to 1
        """
        kwargs = super().get_form_kwargs()
        group = get_object_or_404(Group, pk=self.kwargs['pk'])
        self._group = group
        kwargs.update(initial={'group': self._group, 'items_left': 1})
        return kwargs

    def get_success_url(self):
        return reverse_lazy('groups:mentor_group_update',
                            kwargs={'pk': self.kwargs['pk']})

    def test_func(self):
        """If user in not mentor of this group rises 403 exception"""
        return Group.objects.filter(
            pk=self.kwargs['pk'], mentor__id=self.request.user.pk).exists()
