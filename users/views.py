from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory
from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView, ListView

from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile

__all__ = [
    'LoginView',
    'UserRegisterView',
    'UserUpdateView',
    'PasswordChangeView',
]

ProfileFormSet = inlineformset_factory(User, Profile, form=ProfileUpdateForm,
                                       can_delete=False)


class LoginView(auth_views.LoginView):

    def __init__(self, *args, **kwargs):
        super(LoginView, self).__init__(*args, **kwargs)

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


class AdminListView(ListView):
    model = User
    template_name = 'users/admin_page.html'
    context_object_name = 'users'

    def get_queryset(self):
        result = User.objects.exclude(profile__role__name='Admin')
        if self.request.GET.get('data_search'):
            result = result.filter(
                username__contains=self.request.GET.get('data_search'))
        return result

