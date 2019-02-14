from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy,reverse
from django.views import generic
from django.db.models import Count
from groups.forms import GroupCreateForm,GroupUpdateForm
from groups.models import Group
from django.contrib.messages.views import SuccessMessageMixin
from users.models import Profile,User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404


PAGINATOR=3


class GroupsList(LoginRequiredMixin, generic.ListView):
    model = Group
    ordering = ('name')
    template_name = 'groups/groups_list.html'
    search=False
    search_label='Search'
    paginate_by = PAGINATOR

    def get_queryset(self):
        result = Group.objects.annotate(total=Count('mentor')).order_by('name')
        if self.request.GET.get('data_search'):
            result = result.filter(
                name__contains=self.request.GET.get('data_search'))
            self.search=True
            self.paginate_by = None
            self.search_label = self.request.GET.get('data_search')
        return result

    def get_context_data(self, **kwargs):
        context = super(GroupsList, self).get_context_data(**kwargs)
        context['search'] = self.search
        context['search_label'] = self.search_label
        return context


class CreateGroupView(LoginRequiredMixin, generic.CreateView,generic.ListView):
    model = Group
    form_class = GroupCreateForm
    template_name = 'groups/group_create.html'
    success_url = reverse_lazy('groups:groups-list')
    search = False
    search_label = ''#''Search Last Name'
    paginate_by = PAGINATOR

    def get_context_data(self, **kwargs):
        context = super(CreateGroupView, self).get_context_data(**kwargs)
        if len(self.search_label)>0:
            context['search_label'] = self.search_label
        context['mentors'] = context['object_list']
        context['search'] = self.search
        print(context)
        return context

    def get_queryset(self):
        result = User.objects.all().filter(is_active=True).order_by(
            'last_name')
        if self.request.GET.get('data_search'):
            result = result.filter(
                last_name__contains=self.request.GET.get('data_search'))
            self.search = True
            self.paginate_by = None
            self.search_label = self.request.GET.get('data_search')
        return result


class UpdateGroupView(SuccessMessageMixin,
                      LoginRequiredMixin, generic.UpdateView,generic.ListView):
    form_class = GroupCreateForm
    template_name = 'groups/group_update.html'
    success_message = "Group was updated successfully"
    search=False
    search_label=''#'Search Last Name'
    paginate_by = PAGINATOR

    def get_success_url(self):
        pk=self.kwargs['pk']
        return reverse('groups:update-group',kwargs={'pk':pk})

    def get_context_data(self, **kwargs):
        context = super(UpdateGroupView, self).get_context_data(**kwargs)
        if len(self.search_label)>0:
            context['search_label'] = self.search_label
        context['checked_mentors']=User.objects.\
            filter(profile__mentor_in_group=context['group']).\
            filter(is_active=True).\
            order_by('last_name')
        context['mentors']=context['object_list']
        context['search']=self.search
        print(context)
        return context

    def get_queryset(self):
        result=User.objects.all().filter(is_active=True).order_by('last_name')
        if self.request.GET.get('data_search'):
            result = result.filter(
                    last_name__contains=self.request.GET.get('data_search'))
            self.search=True
            self.paginate_by=None
            self.search_label=self.request.GET.get('data_search')
        return result

    def get_object(self,context=None):
        context = get_object_or_404(Group, pk=self.kwargs['pk'])
        return context
    # def post(self, request, **kwargs):
    #     print(request.POST)


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
    template_name = 'groups/mentor_group_update.html'
    success_message = "Group was updated successfully"
    #paginate_by = PAGINATOR

    def get_success_url(self):
        pk=self.kwargs['pk']
        return reverse('groups:mentor_group_update',kwargs={'pk':pk})

    def get_context_data(self, **kwargs):
        context = super(MentorGroupUpdate, self).get_context_data(**kwargs)
        context['users']=User.objects.\
            filter(profile__user_in_group=context['group']).\
            filter(is_active=True).\
            order_by('last_name')
        print(context)
        return context

    # def post(self, request, **kwargs):
        # print(request.POST)


class MentorGroupAdd(SuccessMessageMixin,LoginRequiredMixin,
                     generic.UpdateView,generic.ListView):
    model = Group
    form_class = GroupUpdateForm
    template_name = 'groups/mentor_group_add.html'
    success_message = "Group was updated successfully"

    def get_success_url(self):
        pk=self.kwargs['pk']
        return reverse('groups:mentor_group_update',kwargs={'pk':pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users']=User.objects.\
            exclude(profile__user_in_group=context['group']).\
            filter(is_active=True).\
            order_by('last_name')
        context['added_users'] = User.objects.\
            filter(profile__user_in_group=context['group'])
        return context