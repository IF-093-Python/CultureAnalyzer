from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views import generic
from quiz.models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from quiz.forms import QuizCreateForm


class QuizzesList(generic.ListView):
    model = Quizzes
    context_object_name = 'quizzes'
    ordering = ('title')
    template_name = 'quiz/quizzes_list.html'


class CreateQuizView(generic.CreateView):
    model = Quizzes
    template_name = 'quiz/quiz_create.html'
    form_class = QuizCreateForm
    success_url = reverse_lazy('quiz:quizzes-list')


class DeleteQuizView(generic.DeleteView):
    model = Quizzes
    context_object_name = 'quiz'
    template_name = 'quiz/quiz_delete.html'
    success_url = reverse_lazy('quiz:quizzes-list')


class UpdateQuizView(generic.UpdateView):
    model = Quizzes
    form_class = QuizCreateForm
    template_name = 'quiz/quiz_update.html'
    success_url = reverse_lazy('quiz:quizzes-list')
