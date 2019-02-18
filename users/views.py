from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory
from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView

from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile

__all__ = [
    'LoginView',
    'UserRegisterView',
    'UserUpdateView',
    'PasswordChangeView',
    'index',
]

ProfileFormSet = inlineformset_factory(User, Profile, form=ProfileUpdateForm,
                                       can_delete=False)


def index(request):
    return render(request, 'users/index.html')


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

        return self.request.user == current_user

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['p_form'] = ProfileFormSet(self.request.POST,
                                               self.request.FILES,
                                               instance=self.object)
            context['p_form'].full_clean()
        else:
            context['p_form'] = ProfileFormSet(instance=self.object)

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['p_form']

        if formset.is_valid():
            obj = form.save()
            formset.instance = obj
            formset.save()

            return redirect('home')

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
