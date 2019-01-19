from django.shortcuts import render

# Create your views here.
from django.views import generic
from quiz.models import *
from django.contrib.auth.decorators import login_required


# @login_required
class QuizzesList(generic.ListView):
    model = Quizzes
