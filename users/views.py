from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView

from CultureAnalyzer.settings.default import ITEMS_ON_PAGE
from CultureAnalyzer.view import SafePaginationListView
from .filters import admin_search
from .forms import (
    UserRegisterForm,
    UserUpdateForm,
    BlockUserForm,
)
from .models import CustomUser

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
    model = CustomUser
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


class AdminListView(LoginRequiredMixin, SafePaginationListView):
    model = CustomUser
    template_name = 'users/admin_page.html'
    context_object_name = 'users'
    paginate_by = ITEMS_ON_PAGE

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdminListView, self).get_context_data(**kwargs)
        context['form'] = admin_search(self.request).form
        return context

    def get_queryset(self):
        return admin_search(self.request).qs


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'users/user_detail.html'
    form_class = BlockUserForm
    model = CustomUser
    success_url = '/admin_page'
