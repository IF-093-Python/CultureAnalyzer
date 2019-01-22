from django.contrib.auth import views as auth_views
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from .forms import UserRegisterForm


def index(request):
    return render(request, 'users/index.html')


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


def profile(request):
    return render(request, 'users/profile.html')
