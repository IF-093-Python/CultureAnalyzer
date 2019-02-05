from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from django.urls import reverse_lazy
from django.views import generic

from groups.forms import GroupCreateForm
from groups.models import Group

PAGINATOR=20

class GroupsList(LoginRequiredMixin, generic.ListView):
    model = Group
    context_object_name = 'groups'
    ordering = ('name')
    template_name = 'groups/groups_list.html'
    search=False
    paginate_by = PAGINATOR

    def get_queryset(self):
        result = super(GroupsList, self).get_queryset()
        if self.request.GET.get('data_search'):
            result = result.filter(
                name__contains=self.request.GET.get('data_search'))
            self.search=True
        return result

    def get_context_data(self, **kwargs):
        context = super(GroupsList, self).get_context_data(**kwargs)
        context['search'] = self.search
        return context


class CreateGroupView(LoginRequiredMixin, generic.CreateView):
    model = Group
    template_name = 'groups/group_create.html'
    form_class = GroupCreateForm
    success_url = reverse_lazy('groups:groups-list')


class UpdateGroupView(LoginRequiredMixin, generic.UpdateView):
    model = Group
    form_class = GroupCreateForm
    template_name = 'groups/group_update.html'
    success_url = reverse_lazy('groups:groups-list')


class DeleteGroupView(LoginRequiredMixin, generic.DeleteView):
    model = Group
    context_object_name = 'group'
    template_name = 'groups/group_delete.html'
    success_url = reverse_lazy('groups:groups-list')


