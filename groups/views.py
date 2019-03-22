from itertools import chain

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic

from groups.forms import GroupCreateForm
from groups.models import Group
from CultureAnalyzer.mixins import SafePaginationMixin

PAGINATOR = 50

__all__ = ['GroupsList', 'CreateGroupView', 'UpdateGroupView',
           'DeleteGroupView']


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
    paginate_by = PAGINATOR
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
    paginate_by = PAGINATOR
    permission_required = 'groups.add_group'

    def form_invalid(self, form):
        """Overrides parent function to take object_list if form is invalid"""
        self.object_list = self.get_queryset()
        return super().form_invalid(form=form)

    def get_context_data(self, **kwargs):
        context = super(CreateGroupView, self).get_context_data(**kwargs)
        context['search_label'] = self._search_label
        context['search'] = self._search
        return context

    def get_queryset(self):
        """List of mentors. Search by last_name is available"""
        result = get_user_model().objects. \
            filter(is_active=True, groups__name='Mentor').order_by('last_name')
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
    paginate_by = PAGINATOR
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
            filter(is_active=True, groups__name='Mentor'). \
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
