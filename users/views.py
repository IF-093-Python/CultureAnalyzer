from django.shortcuts import render
from .uimodels import *


def index(request):
    anon = UiAnonymousUser()
    petya = UiAuthenticatedUser('Petya', 'Trainee')
    vasya = UiAuthenticatedUser('Vasya', 'Admin')
    return render(request, 'users/index.html', context={'user': petya})
