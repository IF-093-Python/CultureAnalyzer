from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy,reverse
from django.views import generic
from django.db.models import Count
from groups.forms import GroupCreateForm,GroupUpdateForm
from groups.models import Group
from django.contrib.messages.views import SuccessMessageMixin
from users.models import Profile,User
from django.http import HttpResponseRedirect


PAGINATOR=20


class GroupsList(LoginRequiredMixin, generic.ListView):
    model = Group
    ordering = ('name')
    template_name = 'groups/groups_list.html'
    search=False
    paginate_by = PAGINATOR

    def get_queryset(self):
        result = Group.objects.annotate(total=Count('mentor')).order_by('name')
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


class UpdateGroupView(SuccessMessageMixin,
                      LoginRequiredMixin, generic.UpdateView):
    model = Group
    form_class = GroupCreateForm
    template_name = 'groups/group_update.html'
    success_message = "Group was updated successfully"

    def get_success_url(self):
        pk=self.kwargs['pk']
        return reverse('groups:update-group',kwargs={'pk':pk})


class DeleteGroupView(LoginRequiredMixin, generic.DeleteView):
    model = Group
    context_object_name = 'group'
    template_name = 'groups/group_delete.html'
    success_url = reverse_lazy('groups:groups-list')


class MentorGroupsView(LoginRequiredMixin,generic.ListView):
    model = Group
    paginate_by = PAGINATOR
    template_name = 'groups/mentor_groups_list.html'
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


class MentorGroupUpdate(SuccessMessageMixin,
                        LoginRequiredMixin,generic.UpdateView):
    model = Group
    form_class = GroupUpdateForm
    template_name = 'groups/mentor_group_update1.html'
    success_message = "Group was updated successfully"

    def get_success_url(self):
        pk=self.kwargs['pk']
        return reverse('groups:mentor_group_update',kwargs={'pk':pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users']=User.objects.filter(profile__user_in_group=context['group'])
        print("lololo", context)
        return context
    # def post(self, request, **kwargs):
    #     group=Group.objects.get(id=self.kwargs['pk'])
    #     print(group.pk,group.name)
    #     a=self.kwargs['pk']
    #     print(a)
    #     users = User.objects.filter(profile__user_in_group=a)
    #     print(users)
    #     for user in users:
    #         print(user.profile.pk,user.username)
    #     print(request.POST)
