from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views import generic
from quiz.models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from quiz.forms import QuizCreateForm


# @login_required
class QuizzesList(LoginRequiredMixin, generic.ListView):
    model = Quizzes
    context_object_name = 'quizzes'
    template_name = 'quiz/quizzes_list.html'


class CreateQuizView(LoginRequiredMixin, generic.CreateView):
    model = Quizzes
    template_name = 'quiz/quiz_create.html'
    form_class = QuizCreateForm
    success_url = reverse_lazy('quizzes-list')
