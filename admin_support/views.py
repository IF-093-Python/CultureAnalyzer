from django.shortcuts import render,redirect
from users.models import Profile,Role
from groups.models import Group
from django.contrib.auth.models import User
from django.views.generic.list import ListView
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from groups.forms import GroupUpdateForm
from django.urls import reverse_lazy,reverse
from django.http import HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin


PAGINATOR=20


class MentorGroupsView(LoginRequiredMixin,ListView):
    model = Group
    paginate_by = PAGINATOR
    template_name = 'admin_support/mentor_groups_list.html'
    search = False

    def get_queryset(self):
        result = Group.objects.filter(mentor=self.request.user.pk).\
            annotate(total=Count('user')).order_by('name')
        if self.request.GET.get('data_search'):
            result = result.filter(
                name__contains=self.request.GET.get('data_search'))
            self.search=True
        return result

    def get_context_data(self, **kwargs):
        context = super(MentorGroupsView, self).get_context_data(**kwargs)
        context['search'] = self.search
        return context


class MentorGroupUpdate(SuccessMessageMixin,LoginRequiredMixin,UpdateView):
    model = Group
    form_class = GroupUpdateForm
    template_name = 'admin_support/mentor_group_update.html'
    success_message = "Group was updated successfully"

    def get_success_url(self):
        pk=self.kwargs['pk']
        return reverse('admin_support:mentor_group_update',kwargs={'pk':pk})