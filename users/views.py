from django.shortcuts import render
from django.contrib import messages
from .forms import UserRegisterForm
from django.views.generic import CreateView


def index(request):
    return render(request, 'users/index.html')


class UserRegisterView(CreateView):
    template_name = 'users/registration.html'
    form_class = UserRegisterForm
    success_url = '/'
