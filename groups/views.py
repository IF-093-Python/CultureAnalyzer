from itertools import chain
from django.contrib.auth.mixins import UserPassesTestMixin,\
                                       PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.db.models import Count
from groups.forms import GroupCreateForm, GroupUpdateForm
from groups.models import Group
from users.models import CustomUser
from CultureAnalyzer.view import SafePaginationListView

PAGINATOR = 10


class GroupsList(PermissionRequiredMixin, SafePaginationListView):
    """Makes list of all groups with number of mentors in each group"""
    model = Group
    ordering = 'name'
    template_name = 'groups/groups_list.html'
    __search = False
    __search_label = 'Search'
    paginate_by = PAGINATOR
    permission_required = 'groups.view_group'

    def get_context_data(self, **kwargs):
        context = super(GroupsList, self).get_context_data(**kwargs)
        context['search'] = self.__search
        context['search_label'] = self.__search_label
        return context

    def get_queryset(self):
        result = Group.objects.annotate(total=Count('mentor')).order_by('name')
        if self.request.GET.get('data_search'):
            result = result.filter(
                name__contains=self.request.GET.get('data_search'))
            self.__search = True
            self.__search_label = self.request.GET.get('data_search')
        return result


class CreateGroupView(generic.CreateView, PermissionRequiredMixin,
                      SafePaginationListView):
    model = Group
    form_class = GroupCreateForm
    template_name = 'groups/group_create.html'
    success_url = reverse_lazy('groups:groups-list')
    __search = False
    __search_label = 'Search'
    paginate_by = PAGINATOR
    permission_required = 'groups.add_group'

    def get_context_data(self, **kwargs):
        context = super(CreateGroupView, self).get_context_data(**kwargs)
        context['search_label'] = self.__search_label
        context['search'] = self.__search
        return context

    def get_queryset(self):
        result = CustomUser.objects.\
            filter(is_active=True, groups__name='Mentor').order_by('last_name')
        if self.request.GET.get('data_search'):
            result = result.filter(
                last_name__contains=self.request.GET.get('data_search'))
            self.__search = True
            self.__search_label = self.request.GET.get('data_search')
        return result


class UpdateGroupView(generic.UpdateView, SuccessMessageMixin,
                      PermissionRequiredMixin, SafePaginationListView):
    form_class = GroupCreateForm
    template_name = 'groups/group_update.html'
    success_message = "Group was updated successfully"
    __search = False
    __search_label = 'Search'
    __checked_mentors = None
    paginate_by = PAGINATOR
    permission_required = 'groups.add_group'
    permission_required = 'groups.change_group'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('groups:update-group', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        context = super(UpdateGroupView, self).get_context_data(**kwargs)
        context['search_label'] = self.__search_label
        context['checked_mentors'] = self.__checked_mentors
        context['search'] = self.__search
        return context

    def get_queryset(self):
        """Remembers all checked_mentors of group and then
        concatenates them with unchecked mentors, so that
        checked mentors are always first in list"""
        checked_mentors = CustomUser.objects.filter(
            is_active=True, mentor_in_group=self.kwargs['pk']). \
            order_by('last_name')
        self.__checked_mentors = checked_mentors
        mentors = CustomUser.objects.\
            filter(is_active=True, groups__name='Mentor'). \
            exclude(mentor_in_group=self.kwargs['pk']). \
            order_by('last_name')
        if self.request.GET.get('data_search'):
            mentors = mentors.filter(
                last_name__contains=self.request.GET.get('data_search'))
            checked_mentors = checked_mentors.filter(
                last_name__contains=self.request.GET.get('data_search'))
            self.__search = True
            self.__search_label = self.request.GET.get('data_search')
        result = list(chain(checked_mentors, mentors))
        return result

    def get_object(self, context=None):
        """Returns Group that we are working with"""
        context = get_object_or_404(Group, pk=self.kwargs['pk'])
        return context


class DeleteGroupView(PermissionRequiredMixin, generic.DeleteView):
    model = Group
    context_object_name = 'group'
    template_name = 'groups/group_delete.html'
    success_url = reverse_lazy('groups:groups-list')
    permission_required = 'groups.delete_group'


class MentorGroupsView(PermissionRequiredMixin, SafePaginationListView):
    model = Group
    template_name = 'groups/mentor_groups_list.html'
    __search = False
    __search_label = 'Search'
    paginate_by = PAGINATOR
    permission_required = 'groups.change_group'

    def get_context_data(self, **kwargs):
        context = super(MentorGroupsView, self).get_context_data(**kwargs)
        context['search'] = self.__search
        context['search_label'] = self.__search_label
        return context

    def get_queryset(self):
        result = Group.objects.filter(mentor__id=self.request.user.pk). \
            annotate(total=Count('user')).order_by('name')
        if self.request.GET.get('data_search'):
            result = result.filter(
                name__contains=self.request.GET.get('data_search'))
            self.__search = True
            self.__search_label = self.request.GET.get('data_search')
        return result


class MentorGroupUpdate(generic.UpdateView, SuccessMessageMixin,
                        UserPassesTestMixin, SafePaginationListView):
    model = Group
    form_class = GroupUpdateForm
    template_name = 'groups/mentor_group_update.html'
    success_message = "Group was updated successfully"
    __search = False
    __search_label = 'Search'
    __users_in_group = None
    paginate_by = PAGINATOR
    raise_exception = True

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('groups:mentor_group_update', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        context = super(MentorGroupUpdate, self).get_context_data(**kwargs)
        context['search_label'] = self.__search_label
        context['users_in_group'] = self.__users_in_group
        context['search'] = self.__search
        return context

    def test_func(self):
        """If user in not mentor of this group rises 403 exception"""
        return Group.objects.filter(
            pk=self.kwargs['pk'], mentor__id=self.request.user.pk).exists()

    def get_queryset(self):
        result = CustomUser.objects.\
            filter(is_active=True, user_in_group=self.kwargs['pk']). \
            order_by('last_name')
        self.__users_in_group = result
        if self.request.GET.get('data_search'):
            result = result.filter(
                last_name__contains=self.request.GET.get('data_search'))
            self.__search = True
            self.__search_label = self.request.GET.get('data_search')
        return result

    def get_object(self, context=None):
        context = get_object_or_404(Group, pk=self.kwargs['pk'])
        return context


class MentorGroupAdd(generic.UpdateView, SuccessMessageMixin,
                     UserPassesTestMixin, SafePaginationListView):
    model = Group
    form_class = GroupUpdateForm
    template_name = 'groups/mentor_group_add.html'
    success_message = "Group was updated successfully"
    __search = False
    __search_label = 'Search'
    paginate_by = PAGINATOR
    raise_exception = True

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('groups:mentor_group_update', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_label'] = self.__search_label
        context['search'] = self.__search
        return context

    def test_func(self):
        """If user in not mentor of this group rises 403 exception"""
        return Group.objects.filter(
            pk=self.kwargs['pk'], mentor__id=self.request.user.pk).exists()

    def get_queryset(self):
        """Gets all Trainee users that are not in groups and
        makes search in their last_name if needed"""
        result = CustomUser.objects.\
            filter(is_active=True, groups__name='Trainee'). \
            exclude(user_in_group=self.kwargs['pk']). \
            order_by('last_name')
        if self.request.GET.get('data_search'):
            result = result.filter(
                last_name__contains=self.request.GET.get('data_search'))
            self.__search = True
            self.__search_label = self.request.GET.get('data_search')
        return result

    def get_object(self, context=None):
        context = get_object_or_404(Group, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        """Gets users that are already in group and adds to users
        that where checked in form for adding to group"""
        users_in_group = CustomUser.objects.\
            filter(is_active=True, user_in_group=self.kwargs['pk'])
        if not form.cleaned_data['user']:
            return redirect('groups:mentor_group_update',
                            pk=self.kwargs['pk'])
        form.cleaned_data['user'] = \
            chain(form.cleaned_data['user'], users_in_group)
        return super(MentorGroupAdd, self).form_valid(form)
