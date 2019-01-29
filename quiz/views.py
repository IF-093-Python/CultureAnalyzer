from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy
from django.views import generic
from quiz.models import *
from users.models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin, \
    PermissionRequiredMixin, PermissionDenied
from quiz.forms import QuizCreateForm


class QuizzesList(LoginRequiredMixin, generic.ListView):
    model = Quizzes
    context_object_name = 'quizzes'
    ordering = ('title')
    template_name = 'quiz/quizzes_list.html'
    search=False

    def get_queryset(self):
        result = super(QuizzesList, self).get_queryset()
        if self.request.GET.get('data_search'):
            result = result.filter(
                title__contains=self.request.GET.get('data_search'))
            self.search=True
        elif self.request.GET.get('clear'):
            self.search=False
            return redirect('quiz:quizzes-list')
        return result

    def get_context_data(self, **kwargs):
        context = super(QuizzesList, self).get_context_data(**kwargs)
        context['search'] = self.search
        #assert False
        return context


class CreateQuizView(LoginRequiredMixin, generic.CreateView):
    model = Quizzes
    template_name = 'quiz/quiz_create.html'
    form_class = QuizCreateForm
    success_url = reverse_lazy('quiz:quizzes-list')


class DeleteQuizView(LoginRequiredMixin, generic.DeleteView):
    model = Quizzes
    context_object_name = 'quiz'
    template_name = 'quiz/quiz_delete.html'
    success_url = reverse_lazy('quiz:quizzes-list')


class UpdateQuizView(LoginRequiredMixin, generic.UpdateView):
    model = Quizzes
    form_class = QuizCreateForm
    template_name = 'quiz/quiz_update.html'
    success_url = reverse_lazy('quiz:quizzes-list')
