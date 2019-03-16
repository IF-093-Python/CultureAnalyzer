from django.contrib.auth import views as auth_views, get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView, DetailView

from users.forms import UserRegisterForm, UserUpdateForm

__all__ = [
    'LoginView',
    'UserRegisterView',
    'UserUpdateView',
    'PasswordChangeView',
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


class UserDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    template_name = 'users/profile.html'
    model = get_user_model()

    def test_func(self):
        """
        this func check that the user which want
        to update profile should have permission to only his profile
        """
        current_user = self.get_object()

        return self.request.user == current_user


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'users/update_profile.html'
    model = get_user_model()
    form_class = UserUpdateForm
    success_url = '/'

    def test_func(self):
        """
        this func check that the user which want
        to update profile should have permission to only his profile
        """
        current_user = self.get_object()

        return self.request.user == current_user

    def form_valid(self, form):
        """Try to save form, and check if image was in form,
        and after save image is None, then there is a error and we
        return error to user
        """
        if form.cleaned_data['image']:
            user = form.save()
            if not user.image:
                form.add_error('__all__', 'Image can`t be saved!')
                return super().form_invalid(form)
        else:
            form.save()
        return redirect('profile', pk=self.request.user.id)


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
