from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView, ListView

from CultureAnalyzer.constants import SUPER_USER_ID
from .filters import admin_search
from .forms import (
    UserRegisterForm,
    UserUpdateForm,
    ProfileUpdateForm,
    ChangeRoleForm,
    BlockUserForm,
)

__all__ = [
    'LoginView',
    'UserRegisterView',
    'UserUpdateView',
    'PasswordChangeView',
    'AdminListView',
    'ProfileUpdateView',
]


class LoginView(auth_views.LoginView):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super(LoginView, self).get(request, *args, **kwargs)


class UserRegisterView(CreateView):
    template_name = 'users/registration.html'
    form_class = UserRegisterForm
    success_url = '/login'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super(UserRegisterView, self).get(request, *args, **kwargs)


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'users/profile.html'
    model = User
    form_class = UserUpdateForm
    success_url = '/'

    def test_func(self):
        """
        this func check that the user which want
        to delete the post should be author of this post
        """
        current_user = self.get_object()

        if self.request.user == current_user:
            return True
        else:
            return False

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['p_form'] = ProfileUpdateForm(self.request.POST,
                                                  self.request.FILES,
                                                  instance=self.object.profile)
            context['p_form'].full_clean()
        else:
            context['p_form'] = ProfileUpdateForm(instance=self.object.profile)

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['p_form']

        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()

            return redirect('home')
        else:
            return self.render_to_response(self.get_context_data(form=form))


class PasswordChangeView(UpdateView):
    template_name = 'users/password_change.html'
    form_class = PasswordChangeForm
    success_url = '/'

    def get_object(self, queryset=None):
        return self.request.user

    def get_form_kwargs(self):
        kwargs = super(PasswordChangeView, self).get_form_kwargs()
        kwargs['user'] = kwargs.pop('instance')
        return kwargs


class AdminListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = 'users/admin_page.html'
    context_object_name = 'users'

    def get_queryset(self):
        return admin_search(self.request)

    def test_func(self):
        if self.request.user.profile.role.name == 'Admin':
            return True
        else:
            return False


class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'users/user_detail.html'
    form_class = BlockUserForm
    model = User

    def test_func(self):
        """Admin can change role and block users except admins

        Superuser can`t change own role and block itself
        """
        if self.request.user.id == SUPER_USER_ID and \
                self.kwargs['pk'] != SUPER_USER_ID:
            return True
        elif self.request.user.profile.role.name == 'Admin' and User.objects.get(
                pk=self.kwargs['pk']).profile.role.name != 'Admin':
            return True

        return False

    def get_context_data(self, **kwargs):
        """
        Add second form to context
        """
        context = super(ProfileUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['r_form'] = ChangeRoleForm(self.request.POST,
                                               instance=self.object.profile)
            context['r_form'].full_clean()
        else:
            context['r_form'] = ChangeRoleForm(instance=self.object.profile)

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        form1 = context['r_form']

        if form1.is_valid() and form.is_valid():
            form.save()
            form1.save()

            return redirect('admin')
        else:
            return self.render_to_response(self.get_context_data(form=form))
